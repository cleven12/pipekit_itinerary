import requests, os
r = requests.get(
    f"https://api.notion.com/v1/databases/{os.environ['NOTION_GITHUB_DB_ID']}",
    headers={
        "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
        "Notion-Version": "2022-06-28"
    }
)
print(r.status_code)
print(r.json())