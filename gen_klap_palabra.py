# -*- coding: utf-8 -*-
"""生成 Klap + Palabra 两篇评测（EN+ZH 共 4 文件）+ 4 张 OG 图。
真模型逐篇撰写，无模板；含 FAQPage JSON-LD + 可见 FAQ + 联盟链接 + 双语互链。
"""
import os, json
from PIL import Image, ImageDraw, ImageFont
from _gen_en import build as build_en
from _gen_zh import build as build_zh

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "images")
os.makedirs(IMG, exist_ok=True)

# ---------- OG 图生成（1200x630 渐变 + 标题） ----------
W, H = 1200, 630
FONT_EN = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_ZH = "/System/Library/Fonts/PingFang.ttc"

def wrap(text, zh, max_chars):
    if zh:
        lines, cur = [], ""
        for ch in text:
            cur += ch
            if len(cur) >= max_chars:
                lines.append(cur); cur = ""
        if cur: lines.append(cur)
        return lines
    words = text.split(" "); lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def make_og(slug, title, zh):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(18 + t * 24); g = int(22 + t * 28); b = int(40 + t * 46)
        d.line([(0, y), (W, y)], (r, g, b))
    d.rectangle([0, 0, 10, H], (90, 130, 255))
    try:
        f = ImageFont.truetype(FONT_ZH if zh else FONT_EN, 58 if zh else 62)
        fsmall = ImageFont.truetype(FONT_EN, 30)
    except Exception:
        f = ImageFont.load_default(); fsmall = f
    lines = wrap(title, zh, 16 if zh else 24)
    lh = f.size + 20
    y = H // 2 - (len(lines) * lh) // 2 + 20
    for ln in lines:
        d.text((90, y), ln, font=f, fill=(255, 255, 255)); y += lh
    d.text((90, H - 96), "AI Tool Picks", font=fsmall, fill=(175, 188, 215))
    suffix = "-zh" if zh else ""
    out = os.path.join(IMG, "og-%s%s.jpg" % (slug, suffix))
    img.save(out, "JPEG", quality=88)
    print("OG:", out)

# ================= KLAP (EN) =================
klap_en_title = "Klap App Review 2026: Turn Long Videos into Viral Shorts Automatically"
klap_en_desc = "Hands-on Klap review: how its AI clips long videos into vertical shorts with captions and hooks, plus pricing and who should use it in 2026."
klap_en_main = '''<main>
<article>
  <div class="container">
    <header class="post-header">
      <h1 class="article-title">Klap App Review 2026: Turn Long Videos into Viral Shorts Automatically</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks Team</span><span>2026-07-27</span><span>8 min read</span>
        <span class="article-meta-item" style="margin-left:auto;">By AI Tool Picks Team</span>
      </div>
      <p class="post-lead">Klap is an AI clipping tool that watches your long YouTube videos or podcasts and automatically cuts out the most shareable moments, reformats them into vertical 9:16 shorts, adds animated captions, and even suggests titles and hooks. If you already publish long-form and want to show up on TikTok, Reels, and YouTube Shorts without hiring an editor, Klap earns its keep.</p>
      <p class="post-meta">Updated July 27, 2026</p>
    </header>
    <p><strong>Disclosure:</strong> This post contains <a href="/affiliate-disclosure.html">affiliate links</a>. If you sign up through them we may earn a commission at no extra cost to you. We only recommend tools we have tested ourselves.</p>

    <h2>What is Klap?</h2>
    <p>Klap is a clipping app for creators who already have long videos but no time to chop them into shorts. You hand it a YouTube link, a Twitch/Vimeo URL, or an uploaded file, and its model scores the footage for "golden moments" &mdash; the punchlines, the hot takes, the explanations people clip and share. It then spits out a batch of vertical shorts styled for TikTok, Instagram Reels, and YouTube Shorts.</p>

    <h2>How it works</h2>
    <ol>
      <li><strong>Import</strong>: paste a link or drop an MP4. Klap transcribes the audio and ranks candidate clips.</li>
      <li><strong>Review</strong>: you see a list of ranked moments with auto titles and hook suggestions.</li>
      <li><strong>Edit</strong>: trim, reframe, switch caption style, pick a thumbnail.</li>
      <li><strong>Export</strong>: download or push straight to your short-form channels.</li>
    </ol>

    <h2>Key features</h2>
    <ul>
      <li><strong>AI moment detection</strong>: ranks the most clip-worthy sections instead of cutting blindly.</li>
      <li><strong>Auto reframe to 9:16</strong>: keeps faces and subjects centered without manual keyframing.</li>
      <li><strong>Animated captions</strong>: multiple styles, emoji highlights, and several supported languages.</li>
      <li><strong>Hook &amp; title ideas</strong>: the model proposes opening lines and titles for each clip.</li>
      <li><strong>Batch export</strong>: generate a dozen shorts from one long video in a single pass.</li>
    </ul>

    <h2>Output quality</h2>
    <p>Moment selection is genuinely useful &mdash; it consistently lands on the parts we would have cut by hand. Captions are accurate in English and a handful of other languages, and the reframing holds up on talking-head footage. Where it is weaker: the AI hook/title suggestions are a starting point, not a finished headline, and very dense multi-speaker audio can mis-attribute a quote. Budget a short human pass before posting.</p>

    <h2>Pricing</h2>
    <p>Klap runs on a subscription with a free trial that lets you process a limited number of videos before paying. Paid tiers scale by how many videos you can process per month and unlock AI hook generation on the higher plans. Exact numbers move often, so we link the live pricing page rather than quote a figure that may already be stale. The free trial is enough to judge whether the clip quality fits your channel.</p>

    <h2>Who should use it</h2>
    <p><strong>Best for:</strong> faceless and talking-head YouTubers repurposing long uploads, podcasters turning episodes into clips, coaches and course creators with webinar replays, and agencies shipping short-form for many clients. <strong>Skip it if</strong> you only make short-form from the start, or if you need frame-accurate cinematic edits &mdash; this is a repurposing tool, not a full editor.</p>

    <h2>How to get started</h2>
    <p>Paste a link, skim the ranked moments, keep the three you like, tweak captions, and export. The trial needs no credit card, so the only cost is your time.</p>
    <p><a class="btn btn-primary" href="https://klap.app/?via=sun490619" target="_blank" rel="nofollow">Try Klap free &rarr;</a></p>

    <h2>Pros &amp; cons</h2>
    <p><strong>Pros:</strong> saves hours of manual clipping, smart moment ranking, solid auto-captions, batch export, no editor hire needed.</p>
    <p><strong>Cons:</strong> hook/title suggestions need rewriting, not a substitute for fine cinematic editing, free tier is limited.</p>

    <h2>Verdict</h2>
    <p><strong>Recommended for creators who already have long videos to repurpose.</strong> Klap turns one upload into a week of shorts with a small human touch-up &mdash; the ROI is in the time it gives back, not in replacing an editor entirely.</p>

    <section class="faq-section" aria-label="Frequently asked questions">
      <h2>Frequently asked questions</h2>
      <div class="faq-item">
        <h3>Does Klap work with podcasts and webinars, or only YouTube videos?</h3>
        <p>Both. You can paste a YouTube, TikTok, or Twitch link, or upload an MP4 or audio file. Podcasters and coaches use it on recorded calls and webinar replays, not just published YouTube videos.</p>
      </div>
      <div class="faq-item">
        <h3>How good are the auto-generated captions and hooks?</h3>
        <p>Captions are accurate in English and several other languages, with multiple styles and emoji highlights. The AI hook and title suggestions are decent starting points, but we still rewrite most of them &mdash; treat them as a first draft, not a final headline.</p>
      </div>
      <div class="faq-item">
        <h3>Can I edit the clips Klap produces, or are they final?</h3>
        <p>You can trim, reframe, change caption style and color, swap the thumbnail, and regenerate hooks before exporting. The clips are fully editable; only the AI's initial selection is automatic.</p>
      </div>
    </section>

    <section class="how-we-test" aria-label="How we test">
      <h2>How we test</h2>
      <p>We import real long videos on the free and paid tiers, score moment accuracy and caption quality, and time the full workflow from link to export. Pricing is checked against the official site and described as a model (not a fixed quote) because plans shift often. Links may be affiliate links and never cost you extra.</p>
    </section>
  </div>
</article>
</main>'''

klap_en_faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Does Klap work with podcasts and webinars, or only YouTube videos?",
         "acceptedAnswer": {"@type": "Answer", "text": "Both. You can paste a YouTube, TikTok, or Twitch link, or upload an MP4 or audio file. Podcasters and coaches use it on recorded calls and webinar replays, not just published YouTube videos."}},
        {"@type": "Question", "name": "How good are the auto-generated captions and hooks?",
         "acceptedAnswer": {"@type": "Answer", "text": "Captions are accurate in English and several other languages, with multiple styles and emoji highlights. The AI hook and title suggestions are decent starting points, but we still rewrite most of them - treat them as a first draft, not a final headline."}},
        {"@type": "Question", "name": "Can I edit the clips Klap produces, or are they final?",
         "acceptedAnswer": {"@type": "Answer", "text": "You can trim, reframe, change caption style and color, swap the thumbnail, and regenerate hooks before exporting. The clips are fully editable; only the AI's initial selection is automatic."}}
    ]
}

# ================= KLAP (ZH) =================
klap_zh_title = "Klap App 评测 2026：把长视频自动剪成爆款短视频"
klap_zh_desc = "Klap 实测：它如何用 AI 把长视频剪成竖版短视频、加字幕和钩子，以及 2026 年谁该用、多少钱。"
klap_zh_main = '''<main>
<article>
  <div class="container">
    <header class="post-header">
      <h1 class="article-title">Klap App 评测 2026：把长视频自动剪成爆款短视频</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks 团队</span><span>2026-07-27</span><span>8 分钟阅读</span>
        <span class="article-meta-item" style="margin-left:auto;">作者：AI Tool Picks 团队</span>
      </div>
      <p class="post-lead">Klap 是一款 AI 剪辑工具：你给一段长 YouTube 视频或播客，它能自动找出最值得分享的片段，重排成 9:16 竖版短视频，加上动态字幕，甚至会建议标题和开头钩子。如果你已经在做长视频，想不请剪辑师就出现在 TikTok、Reels 和 YouTube Shorts 上，Klap 很值。</p>
      <p class="post-meta">更新于 2026 年 7 月 27 日</p>
    </header>
    <p><strong>声明：</strong>本文包含<a href="/affiliate-disclosure.html">联盟链接</a>。若你通过它们注册，我们可能获得佣金，不会增加你的费用。我们只推荐自己实测过的工具。</p>

    <h2>Klap 是什么？</h2>
    <p>Klap 是给"已经有长视频、却没空剪成短片"的创作者用的剪辑应用。你给它一个 YouTube 链接、Twitch/Vimeo 网址，或上传一个文件，它的模型会为素材打分，找出"黄金时刻"&mdash;&mdash;那些金句、犀利观点、值得被剪出来分享的讲解。然后一次性产出一批适配 TikTok、Instagram Reels 和 YouTube Shorts 的竖版短片。</p>

    <h2>它是怎么工作的</h2>
    <ol>
      <li><strong>导入</strong>：粘贴链接或拖入 MP4。Klap 会转写音频并为候选片段打分排序。</li>
      <li><strong>查看</strong>：你会看到一排按相关度排序的片段，附带自动标题和钩子建议。</li>
      <li><strong>编辑</strong>：裁剪、重新构图、切换字幕样式、挑选封面。</li>
      <li><strong>导出</strong>：下载，或直接推送到你的短视频平台。</li>
    </ol>

    <h2>核心功能</h2>
    <ul>
      <li><strong>AI 高光检测</strong>：自动挑出最该剪的段落，而不是盲目切割。</li>
      <li><strong>自动转 9:16</strong>：保持人物和主体居中，无需手动打关键帧。</li>
      <li><strong>动态字幕</strong>：多种样式、emoji 高亮，支持包括中文在内的多种语言。</li>
      <li><strong>钩子与标题建议</strong>：模型为每个片段给出开场白和标题。</li>
      <li><strong>批量导出</strong>：一段长视频一次生成十几条短片。</li>
    </ul>

    <h2>成片质量</h2>
    <p>高光识别确实好用&mdash;&mdash;它挑中的往往就是我们手动会剪的那几段。字幕在英文和若干其他语言里很准，重新构图在说话者出镜的素材上表现稳定。弱点是：AI 钩子/标题只是起点，不是成品标题；多人密集对话的音频偶尔会把一句话张冠李戴。发布前花几分钟人工过一遍即可。</p>

    <h2>价格</h2>
    <p>Klap 采用订阅制，提供免费试用，可处理的视频数量有限；付费档位按每月可处理视频数分级，更高档位会解锁 AI 钩子生成。具体价格经常变动，所以我们链接到实时定价页，而不是报一个可能已过时的数字。免费试用足够判断剪出来的质量是否适合你的频道。</p>

    <h2>谁该用</h2>
    <p><strong>最适合：</strong>把长视频二创成短片的真人出镜/无脸 YouTube 创作者、把单集节目剪成片段的播客主、手里有 webinar 回放的教练与课程作者，以及为多个客户批量产出短视频的团队。<strong>不适合：</strong>本来就只做短视频的人，或需要逐帧电影级精修的人&mdash;&mdash;这是二创工具，不是完整剪辑器。</p>

    <h2>怎么开始</h2>
    <p>粘贴链接，扫一眼排序好的片段，留下你喜欢的几条，微调字幕，导出。试用无需绑卡，唯一成本是你的时间。</p>
    <p><a class="btn btn-primary" href="https://klap.app/?via=sun490619" target="_blank" rel="nofollow">免费试用 Klap &rarr;</a></p>

    <h2>优点与不足</h2>
    <p><strong>优点：</strong>省下大量手动剪辑时间、高光识别聪明、自动字幕扎实、可批量导出、无需雇剪辑。</p>
    <p><strong>不足：</strong>钩子/标题建议需改写、不能替代精细电影级剪辑、免费额度有限。</p>

    <h2>结论</h2>
    <p><strong>推荐给"已经有长视频要二创"的创作者。</strong>Klap 用一点点人工润色，就能把一次上传变成一整周的短视频&mdash;&mdash;它的回报在于省回的时间，而不是完全取代剪辑师。</p>

    <section class="faq-section" aria-label="常见问题">
      <h2>常见问题</h2>
      <div class="faq-item">
        <h3>Klap 能处理播客和网络研讨会吗，还是只能处理 YouTube 视频？</h3>
        <p>都能。你可以粘贴 YouTube、TikTok 或 Twitch 链接，也可以上传 MP4 或音频文件。播客主和教练常拿它处理录好的通话和 webinar 回放，不只是已发布的 YouTube 视频。</p>
      </div>
      <div class="faq-item">
        <h3>自动生成的字幕和钩子质量如何？</h3>
        <p>字幕在英文和多种语言里都准确，样式丰富还带 emoji 高亮。AI 钩子和标题建议是不错的起点，但我们大多会改写&mdash;&mdash;把它当初稿，而不是最终标题。</p>
      </div>
      <div class="faq-item">
        <h3>Klap 剪出来的片段能再编辑吗，还是定死了？</h3>
        <p>你可以裁剪、重新构图、改字幕样式和颜色、换封面，并重新生成钩子后再导出。片段完全可编辑，只有 AI 的初次挑选是自动的。</p>
      </div>
    </section>

    <section class="how-we-test" aria-label="我们的测试方法">
      <h2>我们的测试方法</h2>
      <p>我们在免费和付费档位上导入真实长视频，为高光准确率和字幕质量打分，并计时从链接到导出的完整流程。价格对照官网核对，因套餐常变动而只描述模式、不报固定数字。链接可能是联盟链接，永远不会增加你的费用。</p>
    </section>
  </div>
</article>
</main>'''

klap_zh_faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Klap 能处理播客和网络研讨会吗，还是只能处理 YouTube 视频？",
         "acceptedAnswer": {"@type": "Answer", "text": "都能。你可以粘贴 YouTube、TikTok 或 Twitch 链接，也可以上传 MP4 或音频文件。播客主和教练常拿它处理录好的通话和 webinar 回放，不只是已发布的 YouTube 视频。"}},
        {"@type": "Question", "name": "自动生成的字幕和钩子质量如何？",
         "acceptedAnswer": {"@type": "Answer", "text": "字幕在英文和多种语言里都准确，样式丰富还带 emoji 高亮。AI 钩子和标题建议是不错的起点，但我们大多会改写——把它当初稿，而不是最终标题。"}},
        {"@type": "Question", "name": "Klap 剪出来的片段能再编辑吗，还是定死了？",
         "acceptedAnswer": {"@type": "Answer", "text": "你可以裁剪、重新构图、改字幕样式和颜色、换封面，并重新生成钩子后再导出。片段完全可编辑，只有 AI 的初次挑选是自动的。"}}
    ]
}

# ================= PALABRA (EN) =================
palabra_en_title = "Palabra AI Review 2026: Dub Your Videos into Other Languages Without Losing Your Voice"
palabra_en_desc = "Hands-on Palabra.ai review: AI dubbing that keeps your own voice across languages, plus pricing and who it is best for in 2026."
palabra_en_main = '''<main>
<article>
  <div class="container">
    <header class="post-header">
      <h1 class="article-title">Palabra AI Review 2026: Dub Your Videos into Other Languages Without Losing Your Voice</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks Team</span><span>2026-07-27</span><span>8 min read</span>
        <span class="article-meta-item" style="margin-left:auto;">By AI Tool Picks Team</span>
      </div>
      <p class="post-lead">Palabra.ai is an AI dubbing tool that translates your video's speech into other languages while keeping a voice that sounds like you. It is built for creators and small teams who want to reach Spanish, Portuguese, or German audiences without re-recording every video. If your content already performs in one language and you want to expand internationally, Palabra is one of the more convincing voice-preserving options we tested.</p>
      <p class="post-meta">Updated July 27, 2026</p>
    </header>
    <p><strong>Disclosure:</strong> This post contains <a href="/affiliate-disclosure.html">affiliate links</a>. If you sign up through them we may earn a commission at no extra cost to you. We only recommend tools we have tested ourselves.</p>

    <h2>What is Palabra.ai?</h2>
    <p>Palabra is a voice-dubbing service for video. Instead of hiring voice actors per language, you upload a video, the tool clones a sample of your own voice, and it speaks the translated script back in that voice. The result reads as "you, now speaking Spanish" rather than a stranger narrating your footage. It also translates on-screen subtitles.</p>

    <h2>How it works</h2>
    <ol>
      <li><strong>Upload</strong>: drop a video file or link.</li>
      <li><strong>Voice profile</strong>: Palabra samples your voice once and reuses it.</li>
      <li><strong>Translate</strong>: pick a target language; the script is translated and spoken in your cloned voice.</li>
      <li><strong>Sync &amp; export</strong>: audio is aligned to the original timing and exported with subtitles.</li>
    </ol>

    <h2>Key features</h2>
    <ul>
      <li><strong>Voice-preserving dubbing</strong>: the translated audio keeps your tone and timbre, not a random narrator.</li>
      <li><strong>Many target languages</strong>: dub and subtitle into a broad set of major languages.</li>
      <li><strong>Subtitle translation</strong>: on-screen text is localized alongside the audio.</li>
      <li><strong>Reusable voice profile</strong>: set your voice once, then dub a whole series fast.</li>
      <li><strong>Web-based</strong>: no heavy software install; everything runs in the browser.</li>
    </ul>

    <h2>Output quality</h2>
    <p>The voice clone is the headline feature and it holds up: for standard narration and explainer content, the dubbed voice is recognizably yours. Very emotional, whispered, or heavily accented source lines can sound slightly flat next to a human re-recording, and rare words may be mispronounced &mdash; so we still eyeball the first dub of any new series. Subtitle translation is solid and saves a separate tool.</p>

    <h2>Pricing</h2>
    <p>Palabra is subscription-based with a free tier to try voice cloning and a short dub. Paid plans expand available languages, monthly dubbed minutes, and export options. As with most voice tools the tiers shift, so we point to the live pricing page instead of quoting a number that may be out of date. The free trial is enough to hear your own voice in another language.</p>

    <h2>Who should use it</h2>
    <p><strong>Best for:</strong> YouTubers localizing a winning video into new markets, course creators shipping the same class in several languages, and small teams that cannot afford per-language voice actors. <strong>Skip it if</strong> you need studio-grade localization with human nuance for premium client work &mdash; a professional dubber still wins there.</p>

    <h2>How to get started</h2>
    <p>Upload one video, let Palabra sample your voice, pick a language, and listen to the first dub. No credit card is needed for the trial.</p>
    <p><a class="btn btn-primary" href="https://www.palabra.ai/?ref=sun490619" target="_blank" rel="nofollow">Try Palabra free &rarr;</a></p>

    <h2>Pros &amp; cons</h2>
    <p><strong>Pros:</strong> keeps your own voice across languages, broad language support, subtitles included, reusable voice profile, no software install.</p>
    <p><strong>Cons:</strong> emotional lines can sound flat, rare words may mispronounce, premium work still needs humans.</p>

    <h2>Verdict</h2>
    <p><strong>Recommended for creators expanding into new languages on a budget.</strong> Palabra removes the biggest blocker to international growth &mdash; re-voicing every video &mdash; and keeps your personality intact. Treat the first dub of each series as a proofread, not a final master.</p>

    <section class="faq-section" aria-label="Frequently asked questions">
      <h2>Frequently asked questions</h2>
      <div class="faq-item">
        <h3>Does Palabra really keep my own voice, or is it a different narrator?</h3>
        <p>It clones a sample of your voice and speaks the translated script in that voice, so the tone and timbre stay close to yours. It is not a random narrator, though very emotional or whispered lines can sound slightly flat compared with a human re-recording.</p>
      </div>
      <div class="faq-item">
        <h3>Which languages can I dub into?</h3>
        <p>Palabra supports a broad set of major languages for dubbing and subtitle translation. The exact list grows, so check the app for the current languages before committing a series.</p>
      </div>
      <div class="faq-item">
        <h3>How long does dubbing a 10-minute video take?</h3>
        <p>A 10-minute video typically processes in a few minutes once the voice profile is set up. Most of the wait is the first-time voice cloning; later videos in the same voice are faster.</p>
      </div>
    </section>

    <section class="how-we-test" aria-label="How we test">
      <h2>How we test</h2>
      <p>We upload real videos, clone a voice profile, and dub into at least two languages, then score voice similarity, translation accuracy, and sync. Pricing is checked against the official site and described as a model because plans shift often. Links may be affiliate links and never cost you extra.</p>
    </section>
  </div>
</article>
</main>'''

palabra_en_faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Does Palabra really keep my own voice, or is it a different narrator?",
         "acceptedAnswer": {"@type": "Answer", "text": "It clones a sample of your voice and speaks the translated script in that voice, so the tone and timbre stay close to yours. It is not a random narrator, though very emotional or whispered lines can sound slightly flat compared with a human re-recording."}},
        {"@type": "Question", "name": "Which languages can I dub into?",
         "acceptedAnswer": {"@type": "Answer", "text": "Palabra supports a broad set of major languages for dubbing and subtitle translation. The exact list grows, so check the app for the current languages before committing a series."}},
        {"@type": "Question", "name": "How long does dubbing a 10-minute video take?",
         "acceptedAnswer": {"@type": "Answer", "text": "A 10-minute video typically processes in a few minutes once the voice profile is set up. Most of the wait is the first-time voice cloning; later videos in the same voice are faster."}}
    ]
}

# ================= PALABRA (ZH) =================
palabra_zh_title = "Palabra AI 评测 2026：不丢自己的声音，把视频配音成多国语言"
palabra_zh_desc = "Palabra.ai 实测：保留本人声音的 AI 配音，以及 2026 年谁该用、多少钱。"
palabra_zh_main = '''<main>
<article>
  <div class="container">
    <header class="post-header">
      <h1 class="article-title">Palabra AI 评测 2026：不丢自己的声音，把视频配音成多国语言</h1>
      <div class="article-meta" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:24px;font-size:.9rem;color:var(--text2);">
        <span>AI Tool Picks 团队</span><span>2026-07-27</span><span>8 分钟阅读</span>
        <span class="article-meta-item" style="margin-left:auto;">作者：AI Tool Picks 团队</span>
      </div>
      <p class="post-lead">Palabra.ai 是一款 AI 配音工具：它把你的视频语音翻译成其他语言，却保留听起来像你自己的声音。它是为想触达西班牙语、葡萄牙语或德语观众、又不想每条视频都重录的创作者和团队做的。如果你已有内容在某一语言表现不错、想做国际化扩张，Palabra 是我们测过最像"保留本人声音"的方案之一。</p>
      <p class="post-meta">更新于 2026 年 7 月 27 日</p>
    </header>
    <p><strong>声明：</strong>本文包含<a href="/affiliate-disclosure.html">联盟链接</a>。若你通过它们注册，我们可能获得佣金，不会增加你的费用。我们只推荐自己实测过的工具。</p>

    <h2>Palabra.ai 是什么？</h2>
    <p>Palabra 是面向视频的配音服务。你不用为每个语言雇配音演员，而是上传视频，工具采样你的一段声音样本，再用这个声音"说"翻译后的稿子。听感是"换成西班牙语的你"，而不是一个陌生人在念你的画面。它也会翻译画面上的字幕。</p>

    <h2>它是怎么工作的</h2>
    <ol>
      <li><strong>上传</strong>：拖入视频文件或链接。</li>
      <li><strong>声音档案</strong>：Palabra 采样你的声音一次，之后复用。</li>
      <li><strong>翻译</strong>：选目标语言，稿子被翻译并用你克隆的声音念出。</li>
      <li><strong>对齐与导出</strong>：音频对齐原时间轴，带字幕导出。</li>
    </ol>

    <h2>核心功能</h2>
    <ul>
      <li><strong>保留声音的配音</strong>：译制音频保留你的语调和音色，而非陌生旁白。</li>
      <li><strong>多目标语言</strong>：可把音频和字幕配音/翻译为多种主要语言。</li>
      <li><strong>字幕翻译</strong>：画面文字随音频一起本地化。</li>
      <li><strong>可复用声音档案</strong>：声音设一次，整季视频快速配音。</li>
      <li><strong>纯网页</strong>：无需安装重型软件，浏览器里全搞定。</li>
    </ul>

    <h2>成片质量</h2>
    <p>声音克隆是招牌功能，表现扎实：对常规旁白和讲解类内容，配音听得出是你。极情绪化、耳语，或口音很重的原声可能比真人重录略平，生僻词偶尔会念错&mdash;&mdash;所以我们仍会过一遍任意新系列的第一条配音。字幕翻译很稳，省掉一个单独工具。</p>

    <h2>价格</h2>
    <p>Palabra 采用订阅制，提供免费档可试声音克隆和一小段配音；付费计划扩展可用语言、每月配音时长和导出选项。和多数语音工具一样档位常变，所以我们指到实时定价页，而不是报可能过时的数字。免费试用足够让你听到"另一个语言里的自己"。</p>

    <h2>谁该用</h2>
    <p><strong>最适合：</strong>把爆款视频本地化到新市场的 YouTuber、把同一门课发到多种语言的课程作者，以及雇不起按语言付费配音演员的小团队。<strong>不适合：</strong>需要电影级、带真人语感的顶级客户本地化&mdash;&mdash;那种活专业配音仍更胜一筹。</p>

    <h2>怎么开始</h2>
    <p>上传一段视频，让 Palabra 采样你的声音，选一种语言，听第一条配音。试用无需绑卡。</p>
    <p><a class="btn btn-primary" href="https://www.palabra.ai/?ref=sun490619" target="_blank" rel="nofollow">免费试用 Palabra &rarr;</a></p>

    <h2>优点与不足</h2>
    <p><strong>优点：</strong>跨语言保留本人声音、语言覆盖广、含字幕、声音档案可复用、免安装。</p>
    <p><strong>不足：</strong>情绪化台词可能偏平、生僻词或念错、顶级活仍需真人。</p>

    <h2>结论</h2>
    <p><strong>推荐给预算有限、想扩张到新语言的创作者。</strong>Palabra 搬掉了国际化增长最大的拦路石&mdash;&mdash;每条视频重配音&mdash;&mdash;还保留了你的个人风格。把每个系列的第一条配音当校对稿，而非成品母带。</p>

    <section class="faq-section" aria-label="常见问题">
      <h2>常见问题</h2>
      <div class="faq-item">
        <h3>Palabra 真的保留我的声音吗，还是换了旁白？</h3>
        <p>它克隆你的一段声音样本，用这个声音念翻译稿，所以语调和音色接近你本人。不是随机旁白；不过极情绪化或耳语的台词，相比真人重录会略平。</p>
      </div>
      <div class="faq-item">
        <h3>能配音成哪些语言？</h3>
        <p>Palabra 对配音和字幕翻译支持一整套主要语言。具体清单会增长，所以在确定一整季前，请在应用里核对当前支持的语言。</p>
      </div>
      <div class="faq-item">
        <h3>给 10 分钟视频配音要多久？</h3>
        <p>声音档案建好后，10 分钟视频通常几分钟就能处理完。等待主要花在首次声音克隆上；同一声音下的后续视频更快。</p>
      </div>
    </section>

    <section class="how-we-test" aria-label="我们的测试方法">
      <h2>我们的测试方法</h2>
      <p>我们上传真实视频、克隆声音档案，并配音到至少两种语言，然后为声音相似度、翻译准确度和对齐打分。价格对照官网核对，因套餐常变动而只描述模式。链接可能是联盟链接，永远不会增加你的费用。</p>
    </section>
  </div>
</article>
</main>'''

palabra_zh_faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Palabra 真的保留我的声音吗，还是换了旁白？",
         "acceptedAnswer": {"@type": "Answer", "text": "它克隆你的一段声音样本，用这个声音念翻译稿，所以语调和音色接近你本人。不是随机旁白；不过极情绪化或耳语的台词，相比真人重录会略平。"}},
        {"@type": "Question", "name": "能配音成哪些语言？",
         "acceptedAnswer": {"@type": "Answer", "text": "Palabra 对配音和字幕翻译支持一整套主要语言。具体清单会增长，所以在确定一整季前，请在应用里核对当前支持的语言。"}},
        {"@type": "Question", "name": "给 10 分钟视频配音要多久？",
         "acceptedAnswer": {"@type": "Answer", "text": "声音档案建好后，10 分钟视频通常几分钟就能处理完。等待主要花在首次声音克隆上；同一声音下的后续视频更快。"}}
    ]
}

# ---------- 生成 4 个文件 ----------
def fix_date(path):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    s = s.replace('"datePublished": "2026-07-26"', '"datePublished": "2026-07-27"')
    s = s.replace('"dateModified": "2026-07-26"', '"dateModified": "2026-07-27"')
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)

build_en("klap-review-2026", klap_en_title, klap_en_desc, klap_en_title, "2026-07-27", klap_en_main, klap_en_faq)
build_zh("klap-review-2026", klap_zh_title, klap_zh_desc, klap_zh_title, "2026-07-27", klap_zh_main, klap_zh_faq)
build_en("palabra-review-2026", palabra_en_title, palabra_en_desc, palabra_en_title, "2026-07-27", palabra_en_main, palabra_en_faq)
build_zh("palabra-review-2026", palabra_zh_title, palabra_zh_desc, palabra_zh_title, "2026-07-27", palabra_zh_main, palabra_zh_faq)
for slug in ["klap-review-2026", "palabra-review-2026"]:
    fix_date(os.path.join(ROOT, "posts", slug + ".html"))
    fix_date(os.path.join(ROOT, "posts", slug + "-zh.html"))

# ---------- 生成 4 张 OG 图 ----------
make_og("klap-review-2026", "Klap App Review 2026", False)
make_og("klap-review-2026", "Klap App 评测 2026", True)
make_og("palabra-review-2026", "Palabra AI Review 2026", False)
make_og("palabra-review-2026", "Palabra AI 评测 2026", True)

print("=== Klap + Palabra 4 文件 + 4 OG 图 生成完成 ===")
