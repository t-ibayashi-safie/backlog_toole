import requests
import json
from backlog_tools.settings import Settings


TARGET_STATUSES = [
    "処理中",
]
MILESTONE_ID = 635640

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
    issues = json.loads(response.text)

    # マイルストーンを更新
    for issue in issues:
        issue_id = issue["id"]
        milestones = issue["milestone"]
        milestone_ids = [m["id"] for m in milestones]
        if MILESTONE_ID not in milestone_ids:
            milestone_ids.append(MILESTONE_ID)

        url = f"{base_url}/api/v2/issues/{issue_id}?apiKey={api_key}"
        response = requests.patch(
            url,
            json={
                "milestoneId": milestone_ids,
            }
        )
    

if __name__ == "__main__":
    main()
