import os
ROOT = "/Users/dawei/CodeBuddy/aitool-picks"

OLD = "0 4.609-2.807 5.624-5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"
NEW = "0 4.609-2.807 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"

fixed = 0
for dp,_,fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith(".html"):
            continue
        fp = os.path.join(dp,f)
        if "samples" in fp:
            continue
        with open(fp, encoding="utf-8") as fh:
            txt = fh.read()
        if OLD in txt:
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(txt.replace(OLD, NEW))
            fixed += 1
            print(f"fixed: {os.path.relpath(fp, ROOT)}")
print(f"TOTAL fixed: {fixed}")
