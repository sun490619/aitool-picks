import os, threading, json
import http.server, socketserver
from playwright.sync_api import sync_playwright

ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
PORT = 8166
os.chdir(ROOT)
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}"

probes = [
    "posts/best-ai-coding-assistants-2026.html",
    "index.html",
    "posts/rytr-review-2026.html",
    "category/seo.html",
    "tools/rytr.html",
]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for rel in probes:
        pg = b.new_page(viewport={"width":1024,"height":800})
        errs=[]; warns=[]
        pg.on("console", lambda m: (errs.append(m.text) if m.type=="error" else (warns.append(m.text) if m.type=="warning" else None)))
        pg.on("pageerror", lambda e: errs.append("PAGEERR:"+str(e)))
        pg.goto(f"{BASE}/{rel}", wait_until="load")
        pg.wait_for_timeout(2000)
        scripts=[s.get_attribute("src") for s in pg.query_selector_all("script[src]")]
        res[rel]={
            "errs":errs[:6],
            "warns":warns[:3],
            "scripts":scripts,
            "voteUp":bool(pg.query_selector("#voteUp")),
            "filter_btn":len(pg.query_selector_all(".filter-btn")),
            "search":bool(pg.query_selector("#searchInput")) or bool(pg.query_selector("input[type=search]")),
        }
        pg.close()
    b.close()
httpd.shutdown()
print(json.dumps(res, indent=1, ensure_ascii=False))
