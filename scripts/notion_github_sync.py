import os
import requests
from datetime import datetime, timezone

TOKEN = os.environ["NOTION_TOKEN"]
DB_ID = os.environ["NOTION_GITHUB_DB_ID"]
EVENT = os.environ.get("EVENT_NAME", "")
ACTION = os.environ.get("EVENT_ACTION", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_record(title, event_type, status, author, branch, url):
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": title[:100]}}]
            },
            "Type": {
                "select": {"name": event_type}
            },
            "Status": {
                "select": {"name": status}
            },
            "Author": {
                "rich_text": [{"text": {"content": author}}]
            },
            "Branch": {
                "rich_text": [{"text": {"content": branch}}]
            },
            "URL": {
                "url": url or None
            },
            "Date": {
                "date": {"start": datetime.now(timezone.utc).isoformat()}
            },
        }
    }
    r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if r.status_code == 200:
        print(f"✅ Synced [{event_type}] {title[:60]}")
    else:
        print(f"❌ Failed: {r.status_code} — {r.json()}")

if EVENT == "push":
    msg = os.environ.get("COMMIT_MSG", "No message")
    url = os.environ.get("COMMIT_URL", "")
    author = os.environ.get("COMMIT_AUTHOR", "unknown")
    branch = os.environ.get("BRANCH", "")
    add_record(msg, "Commit", "Open", author, branch, url)

elif EVENT == "issues":
    title = os.environ.get("ISSUE_TITLE", "Untitled Issue")
    url = os.environ.get("ISSUE_URL", "")
    author = os.environ.get("ISSUE_AUTHOR", "unknown")
    status = "Closed" if ACTION == "closed" else "Open"
    add_record(title, "Issue", status, author, "", url)

elif EVENT == "pull_request":
    title = os.environ.get("PR_TITLE", "Untitled PR")
    url = os.environ.get("PR_URL", "")
    author = os.environ.get("PR_AUTHOR", "unknown")
    branch = os.environ.get("PR_BRANCH", "")
    if ACTION == "closed":
        status = "Merged"
    elif ACTION == "opened":
        status = "Open"
    else:
        status = "Closed"
    add_record(title, "PR", status, author, branch, url)

else:
    print(f"⚠️ Unhandled event: {EVENT}")