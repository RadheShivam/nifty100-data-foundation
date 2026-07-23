import threading
import requests
import time

URL = "http://127.0.0.1:8000/api/v1/screener"

results = []


def make_request():
    try:
        response = requests.get(URL)
        results.append(response.status_code)
    except Exception as e:
        results.append(str(e))


threads = []

start = time.time()

for _ in range(10):
    t = threading.Thread(target=make_request)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()

print("=" * 50)
print("Total Requests :", len(results))
print("Successful :", results.count(200))
print("Time Taken :", round(end - start, 2), "seconds")
print("=" * 50)
