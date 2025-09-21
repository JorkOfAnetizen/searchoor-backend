from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

urls = [
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.mozilla.org",
    "https://www.gnu.org",
    "https://kernel.org"
]

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
    return list(results)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Searchoor - {{q}}</title>
</head>
<body>
  <h1>🔍 Searchoor</h1>
  <form action="/" method="get">
    <input type="text" name="q" value="{{q}}" placeholder="Search...">
    <button type="submit">Search</button>
  </form>
  {% if results %}
    <h2>Results</h2>
    <ul>
      {% for r in results %}
        <li><a href="{{r}}" target="_blank">{{titles[r]}}</a></li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    q = request.args.get("q", "")
    results = search(q) if q else []
    return render_template_string(HTML, q=q, results=results, titles=titles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
