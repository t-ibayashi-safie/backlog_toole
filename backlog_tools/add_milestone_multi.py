import requests
import json
import logging
from backlog_tools.settings import Settings

logger = logging.getLogger()

MILESTONE = "sprint_44"

TARGET_STATUSES = [ # 指定したステータスのIssueが更新対象
    "処理中",
    "処理予定",
    "レビュー中",
]
IGNORE_ISSUE_TYPES = [ # 指定したタイプのIssueは除外される
    "PBI",
]

STATUS_ID_MAP = {}
MILESTONE_MAP = {}
PATH_TO_STATUS_MAP = "./data/statuses.json"
PATH_TO_MILESTONE_MAP = "./data/milestones.json"

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
    url = f"{base_url}/api/v2/issues?apiKey={api_key}"
    response = requests.get(
        url,
        json={
            "projectId": [
                project_id
            ],
            "statusId": [STATUS_ID_MAP[status] for status in TARGET_STATUSES],
        }
    )
    response.raise_for_status()
    issues = json.loads(response.text)

    # マイルストーンを更新
    for issue in issues:
        issue_id = issue["id"]
        milestones = issue["milestone"]
        issue_type = issue["issueType"]["name"]
        milestone_ids = [m["id"] for m in milestones]

        if issue_type in IGNORE_ISSUE_TYPES:
            continue

        milestone_id = MILESTONE_MAP.get(MILESTONE)
        if milestone_id not in milestone_ids:
            milestone_ids.append(milestone_id)

        print("update ticket! {}: add mile_stone ({})".format(issue["summary"], MILESTONE))
        url = f"{base_url}/api/v2/issues/{issue_id}?apiKey={api_key}"
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
