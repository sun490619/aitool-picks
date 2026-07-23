#!/usr/bin/env python3
"""为 aitool-picks 全站下载与内容主题相关的真实照片（Unsplash 已验证直链），
替换 images/ 下的 og-*.jpg 与 u*.jpg 占位图。每张唯一、真实摄影、按主题相关。
每个 id 仅用一次；池用尽后循环复用（极少发生）。
"""
import os, urllib.request, io
from PIL import Image

IMG = "/Users/dawei/CodeBuddy/aitool-picks/images"
UA = {"User-Agent": "Mozilla/5.0"}

# 全部已验证 HTTP 200 的真实 Unsplash 照片 id（去重）
IDS = [
    "1432888498266-38ffec3eaf0a","1517842645767-c639042777db","1485846234645-a62644f84728",
    "1461749280684-dccba630e2f6","1531973576160-7125cd663d86","1455390582262-044cdead277a",
    "1526304640581-d334cdbbf45e","1551836022-d5d88e9218df","1626785774573-4b799315345d",
    "1517694712202-14dd9538aa97","1555066931-4365d14bab8c","1542831371-29b0f74f9713",
    "1504384308090-c894fdcc538d","1531297484001-80022131f5a1","1498050108023-c5249f4df085",
    "1551288049-bebda4e38f71","1460925895917-afdab827c52f","1487058792275-0ad4aaf24ca7",
    "1531403009284-440f080d1e12","1556761175-5973dc0f32e7","1542744173-8e7e53415bb0",
    "1531058020387-3be344556be6","1556157382-97eda2d62296","1517245386807-bb43f82c33c4",
    "1563986768609-322da13575f3","1573164713988-8665fc963095","1581291518857-4e27b48ff24e",
    "1551434678-e076c223a692","1552664730-d307ca884978","1542744095-291d1f67b221",
    "1517048676732-d65bc937f952","1531482615713-2afd69097998","1516321318423-f06f85e504b3",
    "1547658719-da2b51169166","1517077304055-6e89abbf09b0","1505740420928-5e560c06d30e",
    "1574717024653-61fd2cf4d44d","1556742049-0cfed4f6a45d","1563013544-824ae1b704d3",
    "1472851294608-062f824d29cc","1469854523086-cc02fe5d8800","1502920917128-1aa500764cbd",
    "1503676260728-1c00da094a0b","1523240795612-9a054b0db644","1434030216411-0b793f4b4173",
    "1497215728101-856f4ea42174","1596526131083-e8c633c948d2","1520975954732-35dd22299614",
    "1456513080510-7bf3a84b82f8","1438761681033-6461ffad8d80","1500648767791-00dcc994a43e",
    "1544005313-94ddf0286df2","1573497019940-1c28c88b4f3e","1580489944761-15a19d654956",
    "1573497019236-17f8177b81e8","1511367461989-f85a21fda167","1508214751196-bcfd4ca60f91",
    "1478720568477-152d9b164e26","1590602847861-f357a9332bbc","1516280440614-37939bbacd81",
    "1478737270239-2f02b77fc618","1585771724684-38269d6639fd","1558618666-fcd25c85cd64",
    "1459749411175-04bf5292ceea","1470225620780-dba8ba36b745","1514525253161-7a46d19cd819",
    "1511671782779-c97d3d27a1d4","1493225457124-a3eb161ffa5f","1518770660439-4636190af475",
    "1551817958-d9d86fb29431","1488646953014-85cb44e25828","1501785888041-af3ef285b470",
    "1502933691298-84fc14542831","1497032205916-ac775f0649ae","1454165804606-c3d57bc86b40",
    "1521737604893-d14cc237f11d","1519389950473-47ba0277781c","1526374965328-7f61d4dc18c5",
]

# 主题 -> 该主题应优先使用的 id 索引区间（粗分配，保证相关）
THEME_POOL = {
    "seo": ["1432888498266-38ffec3eaf0a","1460925895917-afdab827c52f","1531482615713-2afd69097998","1523240795612-9a054b0db644","1518770660439-4636190af475","1563013544-824ae1b704d3"],
    "writing": ["1517842645767-c639042777db","1455390582262-044cdead277a","1434030216411-0b793f4b4173","1497032205916-ac775f0649ae","1456513080510-7bf3a84b82f8","1454165804606-c3d57bc86b40"],
    "grammar": ["1455390582262-044cdead277a","1517842645767-c639042777db","1456513080510-7bf3a84b82f8","1434030216411-0b793f4b4173","1497032205916-ac775f0649ae","1454165804606-c3d57bc86b40"],
    "email": ["1497215728101-856f4ea42174","1531297484001-80022131f5a1","1551288049-bebda4e38f71","1498050108023-c5249f4df085","1520975954732-35dd22299614","1596526131083-e8c633c948d2"],
    "translation": ["1456513080510-7bf3a84b82f8","1434030216411-0b793f4b4173","1497032205916-ac775f0649ae","1454165804606-c3d57bc86b40","1517842645767-c639042777db","1438761681033-6461ffad8d80"],
    "video": ["1485846234645-a62644f84728","1574717024653-61fd2cf4d44d","1551817958-d9d86fb29431","1488646953014-85cb44e25828","1501785888041-af3ef285b470","1502933691298-84fc14542831"],
    "avatar": ["1573497019940-1c28c88b4f3e","1580489944761-15a19d654956","1573497019236-17f8177b81e8","1544005313-94ddf0286df2","1500648767791-00dcc994a43e","1438761681033-6461ffad8d80"],
    "faceless": ["1574717024653-61fd2cf4d44d","1485846234645-a62644f84728","1551817958-d9d86fb29431","1488646953014-85cb44e25828","1501785888041-af3ef285b470","1502933691298-84fc14542831"],
    "coding": ["1461749280684-dccba630e2f6","1517694712202-14dd9538aa97","1555066931-4365d14bab8c","1542831371-29b0f74f9713","1498050108023-c5249f4df085","1547658719-da2b51169166"],
    "openmodel": ["1518770660439-4636190af475","1517077304055-6e89abbf09b0","1498050108023-c5249f4df085","1555066931-4365d14bab8c","1517694712202-14dd9538aa97","1547658719-da2b51169166"],
    "image": ["1517077304055-6e89abbf09b0","1487058792275-0ad4aaf24ca7","1505740420928-5e560c06d30e","1542831371-29b0f74f9713","1626785774573-4b799315345d","1518770660439-4636190af475"],
    "upscaler": ["1517077304055-6e89abbf09b0","1487058792275-0ad4aaf24ca7","1505740420928-5e560c06d30e","1542831371-29b0f74f9713","1626785774573-4b799315345d","1518770660439-4636190af475"],
    "music": ["1511671782779-c97d3d27a1d4","1493225457124-a3eb161ffa5f","1459749411175-04bf5292ceea","1470225620780-dba8ba36b745","1514525253161-7a46d19cd819","1511367461989-f85a21fda167"],
    "podcast": ["1478720568477-152d9b164e26","1590602847861-f357a9332bbc","1516280440614-37939bbacd81","1478737270239-2f02b77fc618","1514525253161-7a46d19cd819","1585771724684-38269d6639fd"],
    "voice": ["1511367461989-f85a21fda167","1544005313-94ddf0286df2","1500648767791-00dcc994a43e","1438761681033-6461ffad8d80","1516280440614-37939bbacd81","1478737270239-2f02b77fc618"],
    "audio": ["1516280440614-37939bbacd81","1478737270239-2f02b77fc618","1590602847861-f357a9332bbc","1585771724684-38269d6639fd","1558618666-fcd25c85cd64","1521737604893-d14cc237f11d"],
    "note": ["1517842645767-c639042777db","1455390582262-044cdead277a","1531403009284-440f080d1e12","1503676260728-1c00da094a0b","1434030216411-0b793f4b4173","1497032205916-ac775f0649ae"],
    "presentation": ["1551288049-bebda4e38f71","1556157382-97eda2d62296","1542744173-8e7e53415bb0","1517245386807-bb43f82c33c4","1551434678-e076c223a692","1519389950473-47ba0277781c"],
    "trip": ["1488646953014-85cb44e25828","1469854523086-cc02fe5d8800","1502920917128-1aa500764cbd","1501785888041-af3ef285b470","1470225620780-dba8ba36b745","1503676260728-1c00da094a0b"],
    "dropshipping": ["1556742049-0cfed4f6a45d","1563013544-824ae1b704d3","1472851294608-062f824d29cc","1505740420928-5e560c06d30e","1542744095-291d1f67b221","1556157382-97eda2d62296"],
    "support": ["1556742049-0cfed4f6a45d","1563013544-824ae1b704d3","1551434678-e076c223a692","1542744173-8e7e53415bb0","1517245386807-bb43f82c33c4","1521737604893-d14cc237f11d"],
    "sidehustle": ["1556761175-5973dc0f32e7","1556742049-0cfed4f6a45d","1460925895917-afdab827c52f","1551288049-bebda4e38f71","1517245386807-bb43f82c33c4","1542744095-291d1f67b221"],
    "smallbiz": ["1497215728101-856f4ea42174","1556761175-5973dc0f32e7","1531973576160-7125cd663d86","1542744173-8e7e53415bb0","1460925895917-afdab827c52f","1596526131083-e8c633c948d2"],
    "student": ["1503676260728-1c00da094a0b","1434030216411-0b793f4b4173","1523240795612-9a054b0db644","1502933691298-84fc14542831","1516321318423-f06f85e504b3","1497032205916-ac775f0649ae"],
    "business": ["1497215728101-856f4ea42174","1556761175-5973dc0f32e7","1531973576160-7125cd663d86","1542744173-8e7e53415bb0","1460925895917-afdab827c52f","1596526131083-e8c633c948d2"],
    "productivity": ["1531973576160-7125cd663d86","1526304640581-d334cdbbf45e","1551836022-d5d88e9218df","1626785774573-4b799315345d","1504384308090-c894fdcc538d","1531297484001-80022131f5a1"],
    "comparison": ["1521737604893-d14cc237f11d","1551288049-bebda4e38f71","1556157382-97eda2d62296","1542744095-291d1f67b221","1551434678-e076c223a692","1517245386807-bb43f82c33c4"],
    "geo": ["1432888498266-38ffec3eaf0a","1460925895917-afdab827c52f","1531482615713-2afd69097998","1563013544-824ae1b704d3","1523240795612-9a054b0db644","1518770660439-4636190af475"],
    "visibility": ["1432888498266-38ffec3eaf0a","1460925895917-afdab827c52f","1531482615713-2afd69097998","1563013544-824ae1b704d3","1523240795612-9a054b0db644","1518770660439-4636190af475"],
    "market": ["1551288049-bebda4e38f71","1556157382-97eda2d62296","1460925895917-afdab827c52f","1542744095-291d1f67b221","1551434678-e076c223a692","1517245386807-bb43f82c33c4"],
    "home": ["1488590528505-98d2b5aba04b","1531297484001-80022131f5a1","1519389950473-47ba0277781c","1526374965328-7f61d4dc18c5","1504384308090-c894fdcc538d","1551434678-e076c223a692"],
    "generic": ["1531297484001-80022131f5a1","1487058792275-0ad4aaf24ca7","1526374965328-7f61d4dc18c5","1519389950473-47ba0277781c","1504384308090-c894fdcc538d","1551434678-e076c223a692"],
}

USED = set()

def theme_for(name):
    n = name.lower()
    if "vs" in n: return "comparison"
    if "seo" in n or "generative-engine" in n or "geo" in n: return "seo"
    if "writing" in n or "grammar" in n or "wordtune" in n or "copy" in n or "rytr" in n or "koala" in n or "quillbot" in n or "hemingway" in n or "languagetool" in n:
        if "grammar" in n: return "grammar"
        return "writing"
    if "translation" in n or "deepl" in n: return "translation"
    if "email" in n: return "email"
    if "video" in n or "runway" in n or "sora" in n or "kling" in n or "descript" in n:
        if "avatar" in n: return "avatar"
        if "faceless" in n: return "faceless"
        return "video"
    if "coding" in n or "cursor" in n or "copilot" in n or "replit" in n or "code" in n or "langchain" in n or "hugging" in n or "github" in n:
        if "open-source" in n or "hugging" in n: return "openmodel"
        return "coding"
    if "image" in n or "midjourney" in n or "upscaler" in n or "canva" in n:
        if "upscaler" in n: return "upscaler"
        return "image"
    if "music" in n: return "music"
    if "podcast" in n: return "podcast"
    if "voice" in n: return "voice"
    if "audio" in n: return "audio"
    if "note" in n or "notion" in n or "mem-ai" in n: return "note"
    if "presentation" in n: return "presentation"
    if "trip" in n or "planner" in n: return "trip"
    if "dropshipping" in n: return "dropshipping"
    if "support" in n or "customer" in n: return "support"
    if "side-hustle" in n or "sidehustle" in n: return "sidehustle"
    if "small-business" in n: return "smallbiz"
    if "student" in n: return "student"
    if "business" in n: return "business"
    if "productivity" in n or "zapier" in n: return "productivity"
    if "market" in n: return "market"
    if "visibility" in n or "brand" in n: return "visibility"
    if "home" in n: return "home"
    return "generic"

def fetch(photo_id, w=1400):
    url = f"https://images.unsplash.com/{photo_id}?w={w}&q=80&auto=format&fit=crop"
    # 用 curl 下载（urllib 在本机对 unsplash 直链异常返回 404，curl 正常）
    import subprocess
    out = subprocess.run(["curl", "-sL", "-A", UA["User-Agent"], url],
                         capture_output=True, timeout=60)
    if out.returncode != 0 or len(out.stdout) < 1000:
        raise RuntimeError(f"curl failed len={len(out.stdout)} url={url} body={out.stdout[:80]!r}")
    return out.stdout

def crop_to(data, out_path, tw, th):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    im = im.crop(((nw - tw)//2, (nh - th)//2, (nw - tw)//2 + tw, (nh - th)//2 + th))
    im.save(out_path, "JPEG", quality=85)

def pick(theme):
    pool = THEME_POOL.get(theme, THEME_POOL["generic"])
    for pid in pool:
        if pid not in USED:
            return pid
    # 池用尽：从全局 IDS 找未用
    for pid in IDS:
        if pid not in USED:
            return pid
    # 全部用完：复用池首张
    return pool[0]

def main():
    targets = []
    for fn in sorted(os.listdir(IMG)):
        if fn.startswith("og-") and fn.endswith(".jpg"):
            targets.append((fn, 1200, 630))
        elif fn.startswith("u") and fn[1:].isdigit() and fn.endswith(".jpg"):
            targets.append((fn, 800, 450))
    print(f"待处理图片: {len(targets)} 张")
    ok, fail = 0, 0
    for fn, tw, th in targets:
        theme = theme_for(fn)
        pid = pick(theme)
        try:
            data = fetch(pid, 1400)
            crop_to(data, os.path.join(IMG, fn), tw, th)
            USED.add(pid)
            ok += 1
            print(f"[OK] {fn} <- {theme}/{pid} ({tw}x{th})")
        except Exception as e:
            fail += 1
            print(f"[FAIL] {fn} ({theme}/{pid}): {e}")
    print(f"\n完成: 成功 {ok}, 失败 {fail}, 唯一图 {len(USED)}")

if __name__ == "__main__":
    main()
