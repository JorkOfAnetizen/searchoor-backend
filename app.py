from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Sites to index
urls = [
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.mozilla.org"
]

# Build a simple index
index = {}
titles = {}

for url in urls:
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text().lower()
        titles[url] = soup.title.string if soup.title else url
        for word in text.split():
            index.setdefault(word, set()).add(url)
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

def search(query):
    words = query.lower().split()
    results = set()
    for word in words:
        results |= index.get(word, set())
    # Return list of dicts for JSON
    return [{"title": titles[r], "url": r} for r in results]

@app.route("/search")
def search_api():
    q = request.args.get("q", "")
    results = search(q) if q else []
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
