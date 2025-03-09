import requests

base_url = "http://localhost:8000/api/khan"
endpoints = [
    "/students/daily-mastery-change",
    "/all-students/mastery-progress",
    "/students/mastery-rankings",
    "/students/perseverance-rankings",
    "/overall/perseverance-progress",
    "/students/mastery-progress",
    "/test"
]

print("Testing FastAPI endpoints directly:")
for endpoint in endpoints:
    url = base_url + endpoint
    try:
        response = requests.get(url)
        status = response.status_code
        print(f"GET {url}: {status}")
        if status == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error accessing {url}: {str(e)}")
    print("-" * 50) 