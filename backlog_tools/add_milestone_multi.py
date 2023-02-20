import requests
import json
import logging
from backlog_tools.settings import Settings

logger = logging.getLogger()

MILESTONE_ID = 635640

TARGET_STATUSES = [ # 指定したステータスのIssueが更新対象
    "処理中",
    "処理予定",
    "レビュー中",
]
IGNORE_ISSUE_TYPES = [ # 指定したタイプのIssueは除外される
    "PBI",
]

STATUS_ID_MAP = {}
PATH_TO_STATUS_MAP = "./data/statuses.json"
PATH_TO_MILESTONE_MAP = "./data/milestones.json"

def main():
    """
    指定したステータスの課題にマイルストーンを追加する
    """
    global STATUS_ID_MAP
    with open(PATH_TO_STATUS_MAP, "r") as fp:
        STATUS_ID_MAP = json.load(fp)
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

        if MILESTONE_ID not in milestone_ids:
            milestone_ids.append(MILESTONE_ID)
        print("update ticket! {}".format(issue["summary"]))
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
