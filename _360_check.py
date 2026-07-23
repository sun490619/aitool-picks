import os, sys, json, threading
import http.server, socketserver
from playwright.sync_api import sync_playwright

ROOT = "/Users/dawei/CodeBuddy/aitool-picks"
PORT = 8155
os.chdir(ROOT)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}"

all_html = []
for dp,_,fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"):
            rel = os.path.relpath(os.path.join(dp,f), ROOT).replace("\\","/")
            all_html.append(rel)
all_html = sorted(set(all_html))

out = {"pages": len(all_html), "overflow": [], "console_errs": {}, "missing_vote": [], "home": {}}

with sync_playwright() as p:
    b = p.chromium.launch()
    for rel in all_html:
        if "samples" in rel or rel.startswith("images/"):
            continue
        pg = b.new_page(viewport={"width":375,"height":800})
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        try:
            pg.goto(f"{BASE}/{rel}", wait_until="load", timeout=20000)
            pg.wait_for_timeout(1500)
        except Exception as e:
            errs.append(f"GOTO_FAIL:{e}")
        sw = pg.evaluate("document.documentElement.scrollWidth")
        cw = pg.evaluate("document.documentElement.clientWidth")
        if sw > cw + 3:
            out["overflow"].append({"page":rel,"sw":sw,"cw":cw})
        if errs:
            out["console_errs"][rel] = errs[:4]
        pg.close()

    # vote component on ALL posts
    posts = [x for x in all_html if x.startswith("posts/")]
    for rel in posts:
        pg = b.new_page()
        try:
            pg.goto(f"{BASE}/{rel}", wait_until="load", timeout=20000)
            pg.wait_for_timeout(800)
        except Exception as e:
            out["missing_vote"].append(rel+":GOTO_FAIL")
            pg.close(); continue
        if not pg.query_selector("#voteUp"):
            out["missing_vote"].append(rel)
        pg.close()

    # home filter + search
    pg = b.new_page(viewport={"width":1024,"height":800})
    pg.goto(f"{BASE}/index.html", wait_until="load")
    pg.wait_for_timeout(1500)
    out["home"]["filter"] = bool(pg.query_selector(".filter-btn"))
    out["home"]["search"] = bool(pg.query_selector("#searchInput")) or bool(pg.query_selector("input[type=search]"))
    out["home"]["filterBtns"] = len(pg.query_selector_all(".filter-btn"))
    pg.close()
    b.close()

httpd.shutdown()
print(json.dumps(out, indent=1, ensure_ascii=False))
