import requests
import json
from backlog_tools.settings import Settings


STATUS_ID_MAP = {
    "未対応": 358662,
    "未対応(整理済み)": 134640,
    "処理予定": 132513,
    "処理中": 2,
    "レビュー中": 132466,
    "処理済み": 3,
    "完了": 4,
}

MILESTONE_ID = 635640

def main():
    """
    マイルストーンの一覧を取得する
    """
    settings = Settings()
    base_url = settings.BASE_URL
    api_key = settings.API_KEY
    project_id = settings.PROJECT_ID

    # issue一覧取得
    url = f"{base_url}/api/v2/projects/{project_id}/versions?apiKey={api_key}"
    response = requests.get(
        url
    )
    milestones = json.loads(response.text)
    milestone_map = {}
    for milestone in milestones:
        id = milestone["id"]
        name = milestone["name"]
        milestone_map[name] = id
    print(json.dumps(milestone_map, ensure_ascii=False))


if __name__ == "__main__":
    main()
