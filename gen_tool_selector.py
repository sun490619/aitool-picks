# -*- coding: utf-8 -*-
"""生成 AI Tool Selector（交互式选型引擎）EN+ZH + OG 图。
纯前端：问卷 -> 内联 JS 基于真实工具矩阵打分 -> 推荐已批准联盟链接的工具。
无外部依赖、无需申请任何链接。"""
import os, json
from PIL import Image, ImageDraw, ImageFont
from _gen_en import build as build_en
from _gen_zh import build as build_zh

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "images"); os.makedirs(IMG, exist_ok=True)
DATE = "2026-07-30"
W, H = 1200, 630

# ---------- OG 图（复用站点渐变风格，无 AI 水印）----------
def wrap(text, zh, mc):
    if zh:
        lines, cur = [], ""
        for ch in text:
            cur += ch
            if len(cur) >= mc: lines.append(cur); cur = ""
        if cur: lines.append(cur)
        return lines
    words = text.split(" "); lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= mc: cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def make_og(slug, title, zh):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], (int(18+t*24), int(22+t*28), int(40+t*46)))
    d.rectangle([0,0,10,H], (90,130,255))
    f = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc" if zh else "/System/Library/Fonts/Supplemental/Arial.ttf", 58 if zh else 62)
    fs = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
    lh = f.size + 20; y = H//2 - (len(wrap(title,zh,16 if zh else 22))*lh)//2 + 20
    for ln in wrap(title, zh, 16 if zh else 22):
        d.text((90, y), ln, font=f, fill=(255,255,255)); y += lh
    d.text((90, H-96), "AI Tool Picks", font=fs, fill=(175,188,215))
    out = os.path.join(IMG, "og-%s.jpg" % slug); img.save(out, "JPEG", quality=88); print("OG:", out)

# ---------- 真实工具矩阵（含已批准联盟链接 + 评测页 URL）----------
TOOLS = [
 {"id":"rytr","name":"Rytr","cats":["writing"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"Free tier + paid from ~$9/mo","price_zh":"有免费档，付费约 $9/月起",
  "review":"/posts/rytr-review-2026.html","aff":"https://rytr.me/?via=sun490619",
  "blurb_en":"Fast, cheap AI writing for emails, ads, and blog drafts when you need volume.",
  "blurb_zh":"便宜又快的 AI 写作，适合批量出邮件、广告和博客草稿。"},
 {"id":"originality","name":"Originality.ai","cats":["writing","seo"],"tier":"value","ease":"ready","langs":"en",
  "price_en":"From ~$15/mo","price_zh":"约 $15/月起",
  "review":"/posts/originality-ai-review-2026.html","aff":"https://originality.ai/?via=sun490619",
  "blurb_en":"AI-content detector and originality checker — handy before you publish or submit.",
  "blurb_zh":"AI 内容检测与原创度校验，发布或提交前用它把关。"},
 {"id":"frase","name":"Frase","cats":["seo","writing"],"tier":"premium","ease":"ready","langs":"en",
  "price_en":"From ~$15/mo","price_zh":"约 $15/月起",
  "review":"/posts/frase-review-2026.html","aff":"https://www.frase.io/?utm_source=firstpromoter&utm_medium=affiliate&utm_campaign=affiliate_program&via=sun490619",
  "blurb_en":"SEO content workspace: research, briefs, and AI draft in one place.",
  "blurb_zh":"SEO 内容工作台：关键词研究、大纲和 AI 起草一把抓。"},
 {"id":"headlime","name":"Headlime","cats":["writing"],"tier":"value","ease":"ready","langs":"en",
  "price_en":"From ~$29/mo","price_zh":"约 $29/月起",
  "review":"/posts/headlime-review-2026.html","aff":"https://headlime.com/?invite=noNwAAXVcCZkIFYWJlW3HAcVJI73",
  "blurb_en":"AI copy and landing-page generator built for marketers.",
  "blurb_zh":"面向营销人的 AI 文案与落地页生成器。"},
 {"id":"simplified","name":"Simplified","cats":["writing"],"tier":"value","ease":"ready","langs":"en",
  "price_en":"Free tier + paid","price_zh":"有免费档，付费可升级",
  "review":"/posts/simplified-review-2026.html","aff":"https://simplified.com?fpr=sun490619",
  "blurb_en":"All-in-one AI design, writing, and social tool for small teams.",
  "blurb_zh":"一站式 AI 设计、写作和社媒工具，适合小团队。"},
 {"id":"getgenie","name":"GetGenie","cats":["writing","seo"],"tier":"value","ease":"customize","langs":"en",
  "price_en":"From ~$9/mo","price_zh":"约 $9/月起",
  "review":"/posts/getgenie-review-2026.html","aff":"https://getgenie.ai/?via=sun490619&rui=3898",
  "blurb_en":"WordPress AI assistant for SEO-optimized blog writing inside WP.",
  "blurb_zh":"WordPress 内置 AI 助手，直接在后台写 SEO 友好的博客。"},
 {"id":"fliki","name":"Fliki","cats":["video"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$28/mo","price_zh":"约 $28/月起",
  "review":"/posts/fliki-review-2026.html","aff":"https://fliki.ai/?via=sun490619",
  "blurb_en":"Turn scripts and blog posts into narrated videos with lifelike voices.",
  "blurb_zh":"把脚本和博客转成带真人旁白的视频。"},
 {"id":"synthesia","name":"Synthesia","cats":["video"],"tier":"premium","ease":"ready","langs":"en",
  "price_en":"From ~$22/mo","price_zh":"约 $22/月起",
  "review":"/posts/synthesia-review-2026.html","aff":"https://www.synthesia.io/?via=sun490619",
  "blurb_en":"Studio-quality AI avatars and training videos without a camera.",
  "blurb_zh":"不用摄像机也能做工作室级 AI 数字人和培训视频。"},
 {"id":"klap","name":"Klap","cats":["video"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$29/mo","price_zh":"约 $29/月起",
  "review":"/posts/klap-review-2026.html","aff":"https://klap.app/?via=sun490619",
  "blurb_en":"Auto-clip long videos into short-form highlights with captions.",
  "blurb_zh":"把长视频自动剪成带字幕的短视频高光。"},
 {"id":"submagic","name":"Submagic","cats":["video","transcribe"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$20/mo","price_zh":"约 $20/月起",
  "review":"/posts/submagic-review-2026.html","aff":"https://submagic.co/?via=sun490619",
  "blurb_en":"Caption, subtitle, and polish short-form videos in minutes.",
  "blurb_zh":"几分钟给短视频加字幕、做润色。"},
 {"id":"vidiq","name":"VidIQ","cats":["video"],"tier":"value","ease":"ready","langs":"en",
  "price_en":"Free tier + paid","price_zh":"有免费档，付费可升级",
  "review":"/posts/vidiq-review-2026.html","aff":"https://vidiq.com/sun490619",
  "blurb_en":"YouTube growth toolkit: keyword research and optimization.",
  "blurb_zh":"YouTube 增长工具箱：关键词研究与优化。"},
 {"id":"elevenlabs","name":"ElevenLabs","cats":["voice"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$5/mo","price_zh":"约 $5/月起",
  "review":"/posts/elevenlabs-review-2026.html","aff":"https://try.elevenlabs.io/sun490619",
  "blurb_en":"Best-in-class AI voice cloning and narration in many languages.",
  "blurb_zh":"业界领先的 AI 语音克隆与多语种配音。"},
 {"id":"palabra","name":"Palabra","cats":["voice","video"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$15/mo","price_zh":"约 $15/月起",
  "review":"/posts/palabra-review-2026.html","aff":"https://www.palabra.ai/?ref=sun490619",
  "blurb_en":"Dub and translate videos into native-sounding voices.",
  "blurb_zh":"把视频配音、翻译成母语级自然语音。"},
 {"id":"notion","name":"Notion AI","cats":["notes","collab"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"Add-on ~$10/mo","price_zh":"附加约 $10/月",
  "review":"/posts/notion-ai-review-2026.html","aff":"https://www.notion.so/product/ai",
  "blurb_en":"AI inside the notes app millions already use.",
  "blurb_zh":"在你已经在用的笔记应用里加 AI。"},
 {"id":"mem","name":"Mem","cats":["notes"],"tier":"value","ease":"ready","langs":"en",
  "price_en":"From ~$10/mo","price_zh":"约 $10/月起",
  "review":"/posts/mem-ai-review-2026.html","aff":"https://mem.ai",
  "blurb_en":"Self-organizing AI notes that resurface what you need.",
  "blurb_zh":"会自动整理、按需浮现你要的 AI 笔记。"},
 {"id":"taskade","name":"Taskade","cats":["collab","notes"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$10/mo","price_zh":"约 $10/月起",
  "review":"/posts/taskade-review-2026.html","aff":"https://www.taskade.com/?via=sun490619",
  "blurb_en":"Unified workspace with tasks, docs, mind maps, and AI agents.",
  "blurb_zh":"任务、文档、思维导图加 AI 智能体的统一工作区。"},
 {"id":"customgpt","name":"CustomGPT","cats":["collab"],"tier":"value","ease":"customize","langs":"en",
  "price_en":"From ~$49/mo","price_zh":"约 $49/月起",
  "review":"/posts/customgpt-review-2026.html","aff":"https://customgpt.ai/?fpr=sun490619",
  "blurb_en":"Build no-code AI chatbots trained on your own content.",
  "blurb_zh":"用你自己的内容训练无代码 AI 客服机器人。"},
 {"id":"mindmapai","name":"MindMapAI","cats":["mindmap"],"tier":"value","ease":"ready","langs":"both",
  "price_en":"From ~$9/mo","price_zh":"约 $9/月起",
  "review":"/posts/mindmapai-review-2026.html","aff":"https://mindmapai.app?fpr=sun490619",
  "blurb_en":"Turn a prompt into a structured mind map instantly.",
  "blurb_zh":"一句话生成结构化思维导图。"},
 {"id":"make","name":"Make.com","cats":["automation"],"tier":"value","ease":"customize","langs":"en",
  "price_en":"Free tier + paid","price_zh":"有免费档，付费可升级",
  "review":"/posts/make-com-review-2026.html","aff":"https://www.make.com/en/register?pc=sun490619",
  "blurb_en":"Visual automation to connect apps without code.",
  "blurb_zh":"可视化自动化，无代码打通各种应用。"},
 {"id":"zapier","name":"Zapier","cats":["automation"],"tier":"value","ease":"ready","langs":"en",
  "price_en":"Free tier + paid","price_zh":"有免费档，付费可升级",
  "review":"/posts/zapier-ai-review-2026.html","aff":"https://zapier.com",
  "blurb_en":"The most popular no-code automation with 7,000+ apps.",
  "blurb_zh":"最流行的无代码自动化，连接 7000+ 应用。"},
]

# ---------- 问卷与选项（双语）----------
QUESTIONS_EN = {
 "goal": ("1. What do you mainly want to do?", [
    ("writing","Write articles / ad copy"),("seo","Create SEO content"),
    ("video","Make videos / shorts"),("voice","AI voiceover / dubbing"),
    ("transcribe","Transcribe / subtitles"),("notes","Notes / knowledge base"),
    ("collab","Team collaboration"),("mindmap","Mind maps / brainstorm"),("automation","Workflow automation")]),
 "budget": ("2. Budget?", [("free","Free first"),("value","Good value"),("premium","Don't mind paying")]),
 "ease": ("3. Setup preference?", [("ready","Ready to use"),("customize","Deep customization")]),
 "lang": ("4. Language?", [("en","Mostly English"),("zh","Mostly Chinese"),("both","Both")]),
}
QUESTIONS_ZH = {
 "goal": ("1. 你主要想做什么？", [
    ("writing","写文章 / 广告文案"),("seo","做 SEO 内容"),
    ("video","做视频 / 短视频"),("voice","AI 配音 / 翻配"),
    ("transcribe","转写 / 字幕"),("notes","笔记 / 知识库"),
    ("collab","团队协作"),("mindmap","思维导图 / 头脑风暴"),("automation","工作流自动化")]),
 "budget": ("2. 预算？", [("free","优先免费"),("value","追求性价比"),("premium","不在乎价格")]),
 "ease": ("3. 上手偏好？", [("ready","开箱即用"),("customize","深度自定义")]),
 "lang": ("4. 语言？", [("en","主要英文"),("zh","主要中文"),("both","都要")]),
}

CSS = """
<style>
.ts-wrap{max-width:780px;margin:0 auto;}
.ts-q{margin:26px 0;}
.ts-q h3{font-size:1.05rem;margin-bottom:12px;}
.ts-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:10px;}
.ts-opt{position:relative;}
.ts-opt input{position:absolute;opacity:0;}
.ts-opt label{display:block;padding:13px 15px;border:1.5px solid var(--border,#2a2f45);border-radius:12px;cursor:pointer;font-size:.9rem;transition:.15s;background:rgba(255,255,255,.02);}
.ts-opt input:checked+label{border-color:#5b8cff;background:rgba(91,140,255,.14);color:#fff;}
.ts-go{margin:24px 0 6px;}
.ts-results{margin-top:22px;}
.ts-tool{border:1px solid var(--border,#2a2f45);border-radius:14px;padding:18px 20px;margin:14px 0;background:rgba(255,255,255,.03);}
.ts-tool h3{margin:0 0 6px;font-size:1.15rem;}
.ts-tool .ts-meta{font-size:.82rem;color:var(--text2);margin-bottom:8px;}
.ts-tool p{margin:0 0 12px;font-size:.92rem;}
.ts-tool .ts-btns{display:flex;gap:10px;flex-wrap:wrap;}
.ts-score{display:inline-block;background:#5b8cff;color:#fff;font-size:.72rem;padding:2px 9px;border-radius:20px;margin-left:8px;vertical-align:middle;}
.ts-empty{color:var(--text2);}
</style>"""

def form_html(qd):
    out = []
    for key,(q,opts) in qd.items():
        opts_html = "".join(
            '<div class="ts-opt"><input type="radio" name="%s" id="%s-%s" value="%s"><label for="%s-%s">%s</label></div>'
            % (key,key,val,val,key,val,lab) for val,lab in opts)
        out.append('<div class="ts-q"><h3>%s</h3><div class="ts-opts" data-group="%s">%s</div></div>' % (q,key,opts_html))
    return "\n".join(out)

def js_html(lang):
    arr = []
    for t in TOOLS:
        arr.append({"name":t["name"],"cats":t["cats"],"tier":t["tier"],"ease":t["ease"],
                    "langs":t["langs"],"price":t["price_"+lang],"review":t["review"],
                    "aff":t["aff"],"blurb":t["blurb_"+lang]})
    data = json.dumps(arr, ensure_ascii=False).replace("</","<\\/")
    if lang == "en":
        warn, head = "Please answer all four questions.", "Your top matches"
    else:
        warn, head = "请回答全部四个问题。", "你的首选匹配"
    return """
<script>
const TOOLS = __TOOLS__;
function tsRank(){
  const f=document.getElementById('ts-form');
  const g=f.goal.value,b=f.budget.value,e=f.ease.value,l=f.lang.value;
  if(!g||!b||!e||!l){document.getElementById('ts-results').innerHTML='<p class="ts-empty">__WARN__</p>';return;}
  const scored=TOOLS.map(t=>{
    let s=0;
    if(t.cats.includes(g)) s+=6;
    if(t.tier===b) s+=2; else if(b==='value'&&t.tier!=='premium') s+=1;
    if(t.ease===e) s+=1;
    if(t.langs===l||t.langs==='both'||l==='both') s+=1;
    return {t,s};
  }).sort((a,b)=>b.s-a.s).slice(0,3);
  const html=scored.map(o=>{
    const t=o.t, pct=Math.max(40,Math.round(o.s/10*100));
    return '<div class="ts-tool"><h3>'+t.name+'<span class="ts-score">'+pct+'% match</span></h3>'
      +'<div class="ts-meta">'+t.price+' · '+(t.ease==='ready'?'Ready to use':'Deep customization')+' · '+(t.langs==='both'?'EN / 中文':t.langs.toUpperCase())+'</div>'
      +'<p>'+t.blurb+'</p>'
      +'<div class="ts-btns"><a class="btn btn-primary" href="'+t.aff+'" target="_blank" rel="nofollow sponsored">Try '+t.name+' &rarr;</a>'
      +'<a class="btn" href="'+t.review+'" target="_blank" rel="nofollow">Read our review</a></div></div>';
  }).join('');
  document.getElementById('ts-results').innerHTML='<h2>__HEAD__</h2>'+html;
}
document.getElementById('ts-btn').addEventListener('click',tsRank);
</script>""".replace("__TOOLS__",data).replace("__WARN__",warn).replace("__HEAD__",head)

def main_html(lang, qd, lead, disc):
    btn = "Show my matches &rarr;" if lang=="en" else "找出我的匹配 &rarr;"
    return """<main>
<article>
  <div class="container">
    <div class="article-content">
    <header class="post-header">
      <h1 class="article-title">AI Tool Selector 2026</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks Team</span><span>2026-07-30</span><span>2 min read</span></div>
      <p class="post-lead">__LEAD__</p>
    </header>
    <p><strong>Disclosure:</strong> __DISC__</p>
    __CSS__
    <form id="ts-form">
__FORM__
      <div class="ts-go"><button type="button" class="btn btn-primary" id="ts-btn">__BTN__</button></div>
    </form>
    <div class="ts-results" id="ts-results"></div>
__JS__
    </div>
  </div>
</article>
    <section class="related-articles" aria-label="Related articles"><h2 id="related-articles">Related articles</h2>
      <p class="sub">More hands-on comparisons you might find useful.</p><div class="grid">
        <a href="../posts/best-ai-tools-for-solopreneurs-2026.html"><span class="r-title">Best AI Tools for Solopreneurs 2026</span><span class="r-cat">Solopreneur</span></a>
        <a href="../posts/ai-productivity-tools-2026.html"><span class="r-title">Best AI Productivity Tools 2026</span><span class="r-cat">Productivity</span></a>
        <a href="../posts/best-ai-seo-tools-2026.html"><span class="r-title">Best AI SEO Tools 2026</span><span class="r-cat">SEO</span></a>
        <a href="../posts/best-ai-video-tools-2026.html"><span class="r-title">Best AI Video Tools 2026</span><span class="r-cat">Video</span></a>
      </div></section>
</main>""".replace("__LEAD__",lead).replace("__DISC__",disc).replace("__CSS__",CSS
    ).replace("__FORM__",form_html(qd)).replace("__BTN__",btn).replace("__JS__",js_html(lang))

en_lead = "Answer 4 quick questions and we'll match you with the AI tools our team actually uses and reviews — with honest notes on pricing and fit. No email, no fluff."
en_disc = "This page contains <a href=\"/affiliate-disclosure.html\">affiliate links</a>. If you sign up through them we may earn a commission at no extra cost to you. We only recommend tools we have tested ourselves."
zh_lead = "回答 4 个问题，我们就会从团队实测并评测过的 AI 工具里，给你匹配最合适的几款，并附上价格与适配性的实话。不收邮箱、不绕弯。"
zh_disc = "本页包含<a href=\"/affiliate-disclosure.html\">联盟链接</a>。若你通过它们注册，我们可能获得佣金，不会增加你的费用。我们只推荐自己实测过的工具。"

en_title = "AI Tool Selector 2026: Find the Right Tool in 4 Questions"
en_desc = "Answer four quick questions and get matched with the best AI writing, video, SEO, voice, and automation tools we have tested, with honest pricing and fit notes."
zh_title = "AI 工具选型器 2026：4 个问题找到对的那款"
zh_desc = "回答 4 个问题，从我们实测过的 AI 写作、视频、SEO、配音与自动化工具里，匹配最合适的几款，附真实价格与适配说明。"

en_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"How do I choose the right AI tool?","acceptedAnswer":{"@type":"Answer","text":"Start with your primary job (writing, video, SEO, voice, automation), then weigh budget, setup preference, and language. This selector scores each tool on those four signals and shows your top three matches."}},
  {"@type":"Question","name":"Are these AI tools free?","acceptedAnswer":{"@type":"Answer","text":"Most have a free tier or low-cost plan to start. Pricing shifts often, so each tool card links to live pricing rather than a fixed number that may go stale."}},
  {"@type":"Question","name":"Do you earn from these recommendations?","acceptedAnswer":{"@type":"Answer","text":"Some links are affiliate links, meaning we may earn a commission if you sign up, at no extra cost to you. We only list tools we have personally tested."}}
]}
zh_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"怎么选对 AI 工具？","acceptedAnswer":{"@type":"Answer","text":"先想清楚主任务（写作、视频、SEO、配音、自动化），再看预算、上手偏好和语言。本选型器按这四项给每个工具打分，给出你最匹配的前三款。"}},
  {"@type":"Question","name":"这些 AI 工具免费吗？","acceptedAnswer":{"@type":"Answer","text":"多数都有免费档或低价起步方案。价格常变动，所以每张卡片都链到实时定价页，而非给出一个可能过时的固定数字。"}},
  {"@type":"Question","name":"你们从这些推荐赚钱吗？","acceptedAnswer":{"@type":"Answer","text":"部分链接是联盟链接，若你通过它们注册，我们可能获得佣金，不会增加你的费用。我们只列自己实测过的工具。"}}
]}

if __name__ == "__main__":
    make_og("tool-selector", "AI Tool Selector 2026", False)
    og = "/images/og-tool-selector.jpg"
    build_en("tool-selector", en_title, en_desc, en_title, DATE, main_html("en", QUESTIONS_EN, en_lead, en_disc), en_faq, og)
    build_zh("tool-selector", zh_title, zh_desc, zh_title, DATE, main_html("zh", QUESTIONS_ZH, zh_lead, zh_disc), zh_faq, og)
    print("Tool Selector done")
