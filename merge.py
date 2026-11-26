
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

with open("DB.json", encoding="utf-8") as f:
    database = json.load(f)

repos = database["repos"]

def fetch_repo(repo):
    try:
        request = urllib.request.Request(
            repo["url"],
            headers={"User-Agent": "TroveUnified/1.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            source = json.load(response)

        apps = source.get("apps", [])

        if not isinstance(apps, list):
            raise ValueError("Invalid apps format")

        print(f"[OK] {repo['name']}: {len(apps)} apps")
        return apps

    except Exception as e:
        print(f"[ERROR] {repo['name']}: {e}")
        return []

unique_apps = {}

with ThreadPoolExecutor(max_workers=8) as executor:
    for apps in executor.map(fetch_repo, repos):
        for app in apps:
            identifier = app.get("bundleIdentifier")

            if identifier:
                unique_apps.setdefault(identifier, app)

result = {
    "name": "Trove Unified",
    "identifier": "com.caelus.trove",
    "subtitle": "Unified iOS App Repository",
    "description": "Aggregated iOS application catalog",
    "apps": list(unique_apps.values()),
    "news": []
}

if not unique_apps:
    raise RuntimeError("No applications received")

with open("apps.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Repositories: {len(repos)}")
print(f"Unique applications: {len(unique_apps)}")
print("Successfully generated apps.json")
