import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_og_today import make_og, verify

OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_review')
os.makedirs(OUT, exist_ok=True)

jobs = [
    ("Chatbase Review 2026",
     "https://live.staticflickr.com/6094/6355836319_bd52002ae7_b.jpg",
     "og-chatbase-review-2026.jpg"),
    ("getimg.ai Review 2026",
     "https://live.staticflickr.com/65535/51917430076_f988efa3bd_b.jpg",
     "og-getimg-ai-review-2026.jpg"),
    ("Getreditus Review 2026",
     "https://live.staticflickr.com/65535/48219379972_2393d80c08_b.jpg",
     "og-getreditus-review-2026.jpg"),
    ("Best AI Resume Builders 2026",
     "https://cdn.stocksnap.io/img-thumbs/960w/42H3JH8QI5.jpg",
     "og-best-ai-resume-builders-2026.jpg"),
    ("Mockey.ai Review 2026",
     "https://live.staticflickr.com/65535/51330631769_0922d85d6e_b.jpg",
     "og-mockey-review-2026.jpg"),
]

for title, url, name in jobs:
    out = os.path.join(OUT, name)
    try:
        make_og(out, url, title)
        print(f"[生成] {name}")
        verify(out)
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
