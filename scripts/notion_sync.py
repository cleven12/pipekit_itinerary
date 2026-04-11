import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = os.getenv("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_task(title, status="Backlog", priority="Medium", module="Flask", notes=""):
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Task": {
                "title": [{"text": {"content": title}}]
            },
            "Status": {
                "select": {"name": status}
            },
            "Priority": {
                "select": {"name": priority}
            },
            "Module": {
                "select": {"name": module}
            },
            "Notes": {
                "rich_text": [{"text": {"content": notes}}]
            },
        }
    }
    r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if r.status_code == 200:
        print(f"✅ Task added: {title}")
    else:
        print(f"❌ Failed: {r.status_code} — {r.json()}")

def list_tasks():
    r = requests.post(
        f"https://api.notion.com/v1/databases/{DB_ID}/query",
        headers=HEADERS,
        json={}
    )
    if r.status_code != 200:
        print(f"❌ Error: {r.json()}")
        return
    results = r.json().get("results", [])
    print(f"\n📋 {len(results)} tasks in PipeKit Itinerary:\n")
    for page in results:
        props = page["properties"]
        name = props["Task"]["title"][0]["plain_text"] if props["Task"]["title"] else "Untitled"
        status = props.get("Status", {}).get("status", {}).get("name", "—")
        priority = props.get("Priority", {}).get("select", {}) or {}
        print(f"  [{status}] {name} ({priority.get('name', '—')})")

if __name__ == "__main__":
    # Seed initial MVP tasks
    tasks = [
        ("Set up Flask project structure", "Backlog", "High", "Flask", "App factory, blueprints, config"),
        ("Design itinerary input form", "Backlog", "High", "Frontend", "Destination, interests, duration, group size"),
        ("Integrate Groq API for itinerary generation", "Backlog", "High", "AI", "Prompt returns structured JSON"),
        ("Build itinerary JSON renderer", "Backlog", "Medium", "Frontend", "Day-by-day visual output"),
        ("Add PDF export (reportlab)", "Backlog", "Medium", "Flask", "Download generated itinerary"),
        ("Add share link feature", "Backlog", "Low", "Flask", "Unique URL per itinerary"),
        ("Set up .env and config management", "In Progress", "High", "Infra", "NOTION_TOKEN, GROQ_API_KEY etc"),
        ("Write Notion sync script", "In Progress", "Medium", "Infra", "This script"),
    ]
    for t in tasks:
        add_task(*t)

    print("\n")
    list_tasks()