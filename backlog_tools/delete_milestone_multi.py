import requests
import json
import logging
from typing import List

from backlog_tools.settings import Settings

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

MILESTONE = "sprint_51"

TARGET_STATUSES = [ # 指定した"状態"のIssueが更新対象
    "未対応",
    "未対応 (優先順位設定済み)",
    # "処理予定",
    # "処理中",
    # "レビュー中",
    # "処理済み",
]
IGNORE_ISSUE_TYPES = [ # 指定した"種別"のIssueは除外される
    "PBI",
]

STATUS_ID_MAP = {}
MILESTONE_MAP = {}
PATH_TO_STATUS_MAP = "./data/statuses.json"
PATH_TO_MILESTONE_MAP = "./data/milestones.json"

def get_issues(settings: Settings, project_id: int, statuses: List[str]=[], offset: int=0, limit: int=100) -> dict:
    settings = Settings()
    base_url = settings.BASE_URL
    api_key = settings.API_KEY
    project_id = settings.PROJECT_ID
    # issue一覧取得
    url = f"{base_url}/api/v2/issues?apiKey={api_key}"
    response = requests.get(
        url,
        json={
            "projectId": [
                project_id
            ],
            "statusId": [STATUS_ID_MAP[status] for status in TARGET_STATUSES],
            "count": limit,
            "offset": offset,
        }
    )
    response.raise_for_status()
    issues = json.loads(response.text)
    return issues

def main():
    """
    指定したステータスの課題にマイルストーンを追加する
    """
    global STATUS_ID_MAP
    with open(PATH_TO_STATUS_MAP, "r") as fp:
        STATUS_ID_MAP = json.load(fp)
    
    global MILESTONE_MAP
    with open(PATH_TO_MILESTONE_MAP, "r") as fp:
        MILESTONE_MAP = json.load(fp)

    if MILESTONE not in MILESTONE_MAP:
        raise Exception("MILESTONE {} is not found.".format(MILESTONE))
    
    settings = Settings()
    base_url = settings.BASE_URL
    api_key = settings.API_KEY
    project_id = settings.PROJECT_ID

    # issue一覧取得
    issues = []
    limit = 100
    offset = 0
    while True:
        _issues = get_issues(settings=settings, project_id=project_id, statuses=TARGET_STATUSES, offset=offset, limit=limit)
        if len(_issues) == 0:
            break
        logger.info("get issues: offset={}, limit={}, len={}".format(offset, limit, len(_issues)))
        issues.extend(_issues)
        offset += 100

    # validation
    issue_id_map = set()
    for issue in issues:
        if issue["id"] in issue_id_map:
            raise Exception("重複したissue_idが存在します: {}".format(issue["id"]))
        issue_id_map.add(issue["id"])

    # マイルストーンを更新
    for issue in issues:
        issue_id = issue["id"]
        milestones = issue["milestone"]
        issue_type = issue["issueType"]["name"]
        milestone_ids = [m["id"] for m in milestones]

        if issue_type in IGNORE_ISSUE_TYPES:
            continue

        milestone_id = MILESTONE_MAP.get(MILESTONE)
        # 指定したマイルストーンが設定されていない場合はスキップ
        if milestone_id not in milestone_ids:
            continue
        milestone_ids.remove(milestone_id)

        print("update ticket! {}: delete mile_stone ({})".format(issue["summary"], MILESTONE))
        url = f"{base_url}/api/v2/issues/{issue_id}?apiKey={api_key}"
        # HACK
        milestone_ids = milestone_ids + [MILESTONE_MAP['default']]
        response = requests.patch(
            url,
            json={
                "milestoneId": milestone_ids,
                "comment": "updated_by_script"
            }
        )
        response.raise_for_status()
    

if __name__ == "__main__":
    main()
