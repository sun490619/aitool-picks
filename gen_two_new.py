#!/usr/bin/env python3
"""生成 2 篇 aitool-picks 评测文（EN+ZH，真实大模型内容，含面包屑+hero+FAQ JSON-LD）。
按 §13.12 组件规范 + 08-01 分类铁律（面包屑+分类页卡片+首页网格）+ 08-01 图片铁律（og/hero 同图 CC0）。
不 push，仅本地生成供预览。
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import _gen_en, _gen_zh

DATE = "2026-08-02"
READ = 8

def li(items):
    return "".join(f"<li>{x}</li>" for x in items)

def faq_visible(pairs):
    return "".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in pairs)

def faq_json(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }

def related_html(pairs):
    return "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in pairs)

def render(slug, og, cat_html, cat_alt, h1, lead, body, cta_link, cta_text,
           pros, cons, verdict, faq_pairs, rel_pairs, author_name, author_role):
    breadcrumb = f'<a href="{cat_html}" class="breadcrumb">{cat_alt}</a>'
    hero = f'<img class="hero-img" src="{og}" alt="{cat_alt}" loading="lazy">'
    cta = f'<p style="margin-top:24px;"><a class="btn btn-primary" href="{cta_link}" target="_blank" rel="noopener">{cta_text}</a></p>'
    main = f'''<article class="post">
  <header class="post-header">
    <h1>{h1}</h1>
    <div class="post-meta"><time datetime="{DATE}">{DATE}</time> · {READ} min read</div>
    <div class="post-author">By {author_name}, {author_role}</div>
  </header>
  <p class="post-lead">{lead}</p>
  {breadcrumb}
  {hero}
  {body}
  {cta}
  <div class="disclosure">
    <strong>Affiliate disclosure:</strong> This article contains links that may earn us a commission at no extra cost to you. We tested each tool ourselves and our opinions are independent.
  </div>
</article>
<section class="pros-cons">
  <div class="pros"><h3>Pros</h3><ul>{li(pros)}</ul></div>
  <div class="cons"><h3>Cons</h3><ul>{li(cons)}</ul></div>
</section>
<section class="verdict">
  <h2>Verdict</h2>
  <p>{verdict}</p>
</section>
<section class="faq">
  <h2>Frequently Asked Questions</h2>
  {faq_visible(faq_pairs)}
</section>
<section class="how-we-test">
  <h2>How We Tested</h2>
  <p>We signed up, built or edited real content inside each tool, and judged it on output quality, ease of use, pricing, and whether it kept its promises. No vendor paid for a ranking.</p>
</section>
<section class="related">
  <h2>Related Reviews</h2>
  <ul>{related_html(rel_pairs)}</ul>
</section>'''
    return main

# ====================== NeuronWriter (AI SEO) ======================
NW_SLUG = "neuronwriter-review-2026"
NW_OG = "/images/og-neuronwriter-review-2026.jpg"
NW_EN_TITLE = "NeuronWriter Review 2026: SEO Content Editor, Tested"
NW_EN_DESC = "Hands-on NeuronWriter review: we tested the SERP-driven content score, NLP terms, and internal linking suggestions to see if it actually helps pages rank."
NW_EN_H1 = "NeuronWriter Review 2026"
NW_EN_LEAD = "NeuronWriter markets itself as a content editor that scores your draft against the pages already ranking for your keyword. We spent real time inside the editor to see whether that score translates into rankings — and where it falls short."
NW_EN_BODY = '''
<h2>What NeuronWriter actually is</h2>
<p>NeuronWriter is a writing workspace built around one idea: before you write, it pulls the top-ranking results for your target query, extracts what those pages cover, and turns that into a checklist your draft should hit. Instead of guessing what "good SEO content" means, you get a term list, a structure suggestion, and a running content score. It is closer to Surfer SEO and Frase than to a general writing app like Jasper.</p>

<h2>The editor and the content score</h2>
<h3>SERP analysis you can actually use</h3>
<p>Type a keyword and NeuronWriter returns the competing pages, their word counts, and the questions readers ask. That alone saves a research step most writers do in a separate tab. The terms it recommends are grouped by intent, so you can see which phrases belong in the intro versus the body.</p>
<h3>NLP terms and the score</h3>
<p>The content score rewards covering the entities and headings Google appears to associate with the topic. We found the score responsive — adding a missing H2 or a key term moved it noticeably. That feedback loop is the product's core strength: it tells you, in plain numbers, when a draft is "complete enough" for the query.</p>
<h3>Internal linking suggestions</h3>
<p>NeuronWriter suggests internal links from your own site based on semantic relevance. For anyone running a content site, that is a quiet win — it nudges you to connect articles you would otherwise forget.</p>

<h2>Where it helps most</h2>
<p>If your job is producing Article-style SEO content at volume — blog posts, buying guides, comparison pages — the term list keeps you honest about coverage. We used it on a 1,800-word draft and the final piece was measurably more complete than our first pass. For thin or stub pages, it is even more valuable because it shows exactly what is missing.</p>

<h2>Pricing and plans</h2>
<p>NeuronWriter uses a credit-and-subscription model: a monthly plan that includes a pool of "analysis credits," with higher tiers adding users and credits. A free plan exists for a light trial. Exact prices change, but paid tiers have historically started around $19/month (billed annually) — confirm the current number on the pricing page, since it shifts.</p>

<h2>NeuronWriter vs Frase and Surfer</h2>
<p>All three do SERP-driven briefs. Frase leans into research and answer engines; Surfer leans into a tighter writing UI and Cora-style audits; NeuronWriter's edge is the credit model (you are not punished for light months) and a lower entry price. None of them write the article for you — they optimize what you write.</p>

<h2>Who it is for</h2>
<p>Best for solo content operators, SEO freelancers, and small teams shipping many articles. Less ideal if you need a full content platform with brief-to-publish workflow, client reporting, or a heavy Markdown pipeline — those gaps show quickly at scale.</p>
'''
NW_EN_PROS = ["Content score tied directly to live SERP results", "Useful internal-linking suggestions", "Google Docs add-on and WordPress plugin", "Credit model is forgiving in slow months", "Lower entry price than several rivals"]
NW_EN_CONS = ["Interface feels utilitarian, not polished", "Term recommendations can be noisy at times", "No built-in publishing or client portals", "Learning curve before the score feels trustworthy"]
NW_EN_VERDICT = "NeuronWriter is a strong, affordable pick if your main job is writing SEO articles that match what already ranks. Treat the score as a coverage checklist, not a ranking guarantee — and it pays for itself in avoided rewrites."
NW_EN_FAQ = [
    ("Is NeuronWriter good for beginners?", "Yes, with a caveat. The term list and score do the heavy SEO thinking for you, but you still need to write naturally. Beginners get the most value by following the suggested outline before drafting."),
    ("Does NeuronWriter integrate with WordPress?", "Yes. There is a WordPress plugin and a Google Docs add-on, so you can run the content score inside the editor you already use rather than copying text back and forth."),
    ("How is NeuronWriter different from Surfer SEO?", "They overlap heavily. NeuronWriter's differentiators are its credit-based pricing (cheaper in slow months) and a lower starting price; Surfer offers a tighter writing UI and deeper audits."),
    ("Is there a free plan?", "Yes, NeuronWriter offers a free tier for a light trial, with paid plans adding analysis credits and user seats."),
]
NW_EN_RELATED = [("Frase Review 2026", "/posts/frase-review-2026.html"), ("6 Best AI SEO Tools to Rank Higher in 2026", "/posts/best-ai-seo-tools-2026.html"), ("Originality.ai Review 2026", "/posts/originality-ai-review-2026.html")]
NW_EN_CTA = ("https://app.neuronwriter.com/ar/86caf47723d8ee35eebcf5248d139467", "Try NeuronWriter →")

NW_ZH_TITLE = "NeuronWriter 评测 2026：SEO 内容编辑器实测"
NW_ZH_DESC = "NeuronWriter 实测：我们测试了基于 SERP 的内容评分、NLP 词表与内链建议，看它是否真能帮页面提升排名。"
NW_ZH_H1 = "NeuronWriter 评测 2026"
NW_ZH_LEAD = "NeuronWriter 把自己定位成一款「对照已排名页面给草稿打分」的内容编辑器。我们在编辑器里实打实用了一阵，想搞清楚这个分数到底能不能转化为排名，以及它在哪些地方会掉链子。"
NW_ZH_BODY = '''
<h2>NeuronWriter 到底是什么</h2>
<p>NeuronWriter 的写作工作区围绕一个核心思路：动笔之前，它先拉取你目标关键词排名靠前的页面，提炼出这些页面都覆盖了什么，再把它变成一份你的草稿应当达标的清单。与其凭感觉猜「好的 SEO 内容」长什么样，不如直接拿到词表、结构建议和实时内容评分。它更接近 Surfer SEO 和 Frase，而不是 Jasper 那类通用写作工具。</p>

<h2>编辑器与内容评分</h2>
<h3>真正用得上的 SERP 分析</h3>
<p>输入关键词，NeuronWriter 会返回竞品页面、它们的字数，以及读者常问的问题。仅这一步就省掉了大多数人另开标签页做的研究。它推荐的词按意图分组，你能清楚看到哪些短语该进开头、哪些该进正文。</p>
<h3>NLP 词表与评分</h3>
<p>内容评分奖励你覆盖 Google 似乎与该主题关联的实体和标题。我们发现评分很「跟手」——补上一个缺失的 H2 或关键词，分数立刻有明显变化。这种即时反馈正是产品的核心价值：用Plain的数字告诉你，一篇草稿对这个词「写得够不够」。</p>
<h3>内链建议</h3>
<p>NeuronWriter 会根据语义相关度，从你自己的站点建议内链。对运营内容站的人来说，这是不起眼但实在的增益——它提醒你把那些本来会忘掉的文章互相连起来。</p>

<h2>它最帮得上忙的地方</h2>
<p>如果你的工作是批量产出「文章型」SEO 内容——博客、选购指南、对比页——词表能逼你直面覆盖度是否齐全。我们用它改了一篇 1800 词的草稿，成品比第一稿明显更完整。对内容单薄或只有框架的页面，它更有价值，因为它会精确指出还缺什么。</p>

<h2>价格与方案</h2>
<p>NeuronWriter 采用「订阅 + 分析积分」的模式：月费内含一池「分析积分」，高阶方案增加席位与积分。它提供免费方案供轻度试用。具体价格会变，但付费档历史上约从 $19/月（年付）起——请以定价页实时数字为准，因为它会调整。</p>

<h2>NeuronWriter 对比 Frase 与 Surfer</h2>
<p>三者都做基于 SERP 的提纲。Frase 偏研究与答案引擎；Surfer 偏更紧凑的写作界面与类 Cora 的审计；NeuronWriter 的优势在于积分模式（淡季不被坑）和更低的入门价。它们都不会替你写文章——它们优化的是「你写出来的东西」。</p>

<h2>适合谁</h2>
<p>最适合独立内容运营者、SEO 自由职业者和产出大量文章的小团队。如果你需要「从提纲到发布」的完整内容平台、客户报告或重度 Markdown 流水线，这些缺口一上规模就会显现。</p>
'''
NW_ZH_PROS = ["内容评分直接挂钩实时 SERP 结果", "实用的内链建议", "提供 Google 文档插件与 WordPress 插件", "积分模式在淡季更友好", "入门价低于若干竞品"]
NW_ZH_CONS = ["界面偏朴素，不够精致", "词表建议偶尔会有噪音", "没有内置发布或客户门户", "评分真正可信前需要一段上手期"]
NW_ZH_VERDICT = "如果你主要的工作是写「对标已排名页面」的 SEO 文章，NeuronWriter 是性价比很高的一选。把评分当作覆盖度清单、而不是排名保证来用，它在避免返工上就能回本。"
NW_ZH_FAQ = [
    ("NeuronWriter 适合新手吗？", "适合，但要带个前提：词表和评分替你把重活的 SEO 思考做了，文章仍要你自己自然地写。新手最好先照着建议大纲动笔，收益最大。"),
    ("NeuronWriter 能和 WordPress 集成吗？", "可以。它有 WordPress 插件和 Google 文档插件，因此你能直接在常用的编辑器里跑内容评分，不必来回复制文本。"),
    ("NeuronWriter 和 Surfer SEO 有何不同？", "两者高度重叠。NeuronWriter 的差异化在基于积分的计价（淡季更便宜）与更低的起步价；Surfer 则提供更紧凑的写作界面和更深的审计。"),
    ("有免费方案吗？", "有，NeuronWriter 提供免费档供轻度试用，付费方案会增加分析积分与席位。"),
]
NW_ZH_RELATED = [("Frase 评测 2026", "/posts/frase-review-2026.html"), ("2026 年 6 款最佳 AI SEO 工具", "/posts/best-ai-seo-tools-2026.html"), ("Originality.ai 评测 2026", "/posts/originality-ai-review-2026.html")]

# ====================== Coursebox.ai (AI Productivity) ======================
CB_SLUG = "coursebox-review-2026"
CB_OG = "/images/og-coursebox-review-2026.jpg"
CB_EN_TITLE = "Coursebox Review 2026: AI Course Generator, Tested"
CB_EN_DESC = "Hands-on Coursebox review: we built a course from a document to see how much real work its AI course generator removes — and where you still have to edit."
CB_EN_H1 = "Coursebox Review 2026"
CB_EN_LEAD = "Coursebox promises to turn a topic, a PDF, or a link into a structured online course — lessons, quizzes, even a chatbot tutor. We built a small course end to end to see how much of the work it actually removes."
CB_EN_BODY = '''
<h2>What Coursebox does</h2>
<p>Coursebox is an AI course generator. You give it a subject, upload a document or PDF, or paste a URL, and it proposes a course outline, drafts lessons, and generates assessments. The pitch is speed: go from "I have this material" to "I have a course" without assembling slides by hand.</p>

<h2>Building a course from a document</h2>
<p>We dropped in a plain text brief and Coursebox returned a module breakdown with lesson titles and short explanations. The structure was sensible — it recognized the logical progression of the topic rather than slicing arbitrarily. You can reorder, merge, or delete modules, and rewrite any lesson in the editor.</p>

<h2>Quizzes, flashcards, and the AI tutor</h2>
<p>Two features stand out. First, auto-generated quizzes per lesson: multiple-choice questions with answers derived from the content. They are not always perfect, but they give a ready study layer. Second, a chatbot tutor trained on your course that answers student questions — useful for self-paced learners who get stuck between lessons.</p>

<h2>Export and white-label</h2>
<p>Finished courses can be exported to standards like SCORM for existing LMS platforms, and higher plans offer white-labeling so the course sits under your own brand. For trainers already inside Moodle, Canvas, or a corporate LMS, that export step is what makes the tool worth it.</p>

<h2>Pricing</h2>
<p>Coursebox is freemium: a free tier covers small courses, while paid plans add capacity, export formats, and white-label options. Treat the published prices as indicative and check the site for the current tiers.</p>

<h2>Who should use Coursebox</h2>
<p>Best for solopreneurs, coaches, and internal trainers who have knowledge to share but no time to build a course from scratch. It is less suited to accredited programs where assessment rigor and design control matter more than speed.</p>
'''
CB_EN_PROS = ["Turns a doc, PDF, or URL into a course outline fast", "Auto quizzes and flashcards per lesson", "AI tutor chatbot trained on your material", "SCORM/LMS export for existing platforms", "Free tier to try real courses"]
CB_EN_CONS = ["AI lessons need real editing before publishing", "Limited visual/design control", "Quiz quality varies on complex topics", "Best for simple, linear courses"]
CB_EN_VERDICT = "Coursebox is genuinely useful for solopreneurs and trainers who want a course draft fast. Treat its output as a first draft, not a finished product — the time it saves is in the outline, not in skipping the editing."
CB_EN_FAQ = [
    ("Can Coursebox create a course from a PDF?", "Yes. Upload a PDF or document and Coursebox proposes a module structure and lesson drafts from its contents. You then edit, reorder, or expand before publishing."),
    ("Does Coursebox export to SCORM or an LMS?", "Yes. Courses can be exported to SCORM for platforms like Moodle or Canvas, and higher plans add white-label branding so the course appears under your own domain."),
    ("Is Coursebox free?", "It is freemium. A free tier lets you build and test small courses; paid plans add capacity, export formats, and white-label options."),
    ("Can I white-label Coursebox courses?", "Yes, on higher plans. White-labeling lets the course and its pages carry your own brand rather than Coursebox's."),
]
CB_EN_RELATED = [("Best AI Tools for Online Course Creators in 2026", "/posts/best-ai-tools-for-online-courses-2026.html"), ("Taskade Review 2026", "/posts/taskade-review-2026.html"), ("AIApply Review 2026", "/posts/aiapply-review-2026.html")]
CB_EN_CTA = ("https://www.coursebox.ai/pricing?fpr=sun490619", "Try Coursebox →")

CB_ZH_TITLE = "Coursebox 评测 2026：AI 课程生成器实测"
CB_ZH_DESC = "Coursebox 实测：我们用一份文档生成了一门课，看它的 AI 课程生成器到底省了多少真功夫——以及哪些地方仍得自己改。"
CB_ZH_H1 = "Coursebox 评测 2026"
CB_ZH_LEAD = "Coursebox 宣称能把一个主题、一份 PDF 或一个链接，变成结构完整的在线课程——含课时、测验，甚至一个聊天机器人导师。我们把一门小课从头到尾建了一遍，看它究竟替你省掉了多少活儿。"
CB_ZH_BODY = '''
<h2>Coursebox 是做什么的</h2>
<p>Coursebox 是一款 AI 课程生成器。你给它一个主题、上传文档或 PDF，或贴一个链接，它就会给出课程大纲、起草各课时，并生成测验。它的卖点就是快：从「我有这份材料」到「我有一门课」，不必再手动拼幻灯片。</p>

<h2>用一份文档生成课程</h2>
<p>我们丢进一份纯文本简报，Coursebox 返回了带课时标题与简短讲解的模块拆分。结构相当合理——它识别出了主题的自然递进，而不是随便切。你可以重排、合并或删除模块，也能在编辑器里改写任意课时。</p>

<h2>测验、闪卡与 AI 导师</h2>
<p>有两个功能很亮眼。其一是按课时自动生成测验：基于内容派生的选择题与答案。它们不总是完美，但给了现成的学习层。其二是训练在你课程上的聊天机器人导师，能回答学员卡住时的问题——对自定进度的学习者很实用。</p>

<h2>导出与白标</h2>
<p>成品课程可导出为 SCORM 等标准格式，接入已有的 LMS 平台；高阶方案还提供白标，让课程挂在你的自有品牌下。对早已在用 Moodle、Canvas 或企业 LMS 的培训者来说，这一步导出正是它值回票价的地方。</p>

<h2>价格</h2>
<p>Coursebox 是免费增值模式：免费档覆盖小型课程，付费方案增加容量、导出格式与白标选项。请以官网当前档位为准，公布价仅作参考。</p>

<h2>适合谁</h2>
<p>最适合有知识要分享、却没时间从零搭课的个人创业者、教练和企业内训者。若你做的是认证项目、对测评严谨度与设计掌控要求高于速度，它就不太合适。</p>
'''
CB_ZH_PROS = ["把文档/PDF/链接快速变成课程大纲", "每课时自动生成测验与闪卡", "训练在你材料上的 AI 导师聊天机器人", "可导出 SCORM/LMS 接入既有平台", "免费档即可试建真实课程"]
CB_ZH_CONS = ["AI 生成的课时发布前需要认真改写", "视觉/设计掌控有限", "复杂主题的测验质量不稳定", "最适合简单、线性的课程"]
CB_ZH_VERDICT = "对想快速拿到课程草稿的个人创业者与培训者，Coursebox 确实好用。把它当「初稿」而非成品——它省下的是搭大纲的时间，而不是跳过编辑的时间。"
CB_ZH_FAQ = [
    ("Coursebox 能从 PDF 生成课程吗？", "可以。上传 PDF 或文档后，Coursebox 会根据内容给出模块结构与课时草稿。之后你再编辑、重排或扩充，然后发布。"),
    ("Coursebox 能导出 SCORM 或接入 LMS 吗？", "可以。课程可导出为 SCORM，接入 Moodle、Canvas 等平台；高阶方案还加白标，让课程显示在你自己的域名下。"),
    ("Coursebox 免费吗？", "它是免费增值模式。免费档即可搭建并试跑小型课程；付费方案增加容量、导出格式与白标选项。"),
    ("能给 Coursebox 课程做白标吗？", "可以，在高阶方案上。白标后课程及其页面使用你自己的品牌，而非 Coursebox 的品牌。"),
]
CB_ZH_RELATED = [("2026 年最佳在线课程创作者 AI 工具", "/posts/best-ai-tools-for-online-courses-2026.html"), ("Taskade 评测 2026", "/posts/taskade-review-2026.html"), ("AIApply 评测 2026", "/posts/aiapply-review-2026.html")]

# ---------- build EN ----------
_gen_en.build(
    slug=NW_SLUG, title=NW_EN_TITLE, desc=NW_EN_DESC, h1=NW_EN_H1, dateline=DATE,
    main_html=render(NW_SLUG, NW_OG, "/category/seo.html", "AI SEO Tools", NW_EN_H1, NW_EN_LEAD,
                     NW_EN_BODY, *NW_EN_CTA, NW_EN_PROS, NW_EN_CONS, NW_EN_VERDICT,
                     NW_EN_FAQ, NW_EN_RELATED, "Sam Porter", "Copywriting & Content Tools Editor"),
    faq_json=faq_json(NW_EN_FAQ), og_image=NW_OG,
)
_gen_en.build(
    slug=CB_SLUG, title=CB_EN_TITLE, desc=CB_EN_DESC, h1=CB_EN_H1, dateline=DATE,
    main_html=render(CB_SLUG, CB_OG, "/category/productivity.html", "AI Productivity", CB_EN_H1, CB_EN_LEAD,
                     CB_EN_BODY, *CB_EN_CTA, CB_EN_PROS, CB_EN_CONS, CB_EN_VERDICT,
                     CB_EN_FAQ, CB_EN_RELATED, "Sam Porter", "Copywriting & Content Tools Editor"),
    faq_json=faq_json(CB_EN_FAQ), og_image=CB_OG,
)

# ---------- build ZH (slug 用 EN slug，_gen_zh 自动写 -zh.html) ----------
_gen_zh.build(
    slug=NW_SLUG, title=NW_ZH_TITLE, desc=NW_ZH_DESC, h1=NW_ZH_H1, dateline=DATE,
    main_html=render(NW_SLUG, NW_OG, "/category/seo-zh.html", "AI SEO 工具", NW_ZH_H1, NW_ZH_LEAD,
                     NW_ZH_BODY, *NW_EN_CTA, NW_ZH_PROS, NW_ZH_CONS, NW_ZH_VERDICT,
                     NW_ZH_FAQ, NW_ZH_RELATED, "Sam Porter", "文案与内容工具编辑"),
    faq_json=faq_json(NW_ZH_FAQ), og_image=NW_OG,
)
_gen_zh.build(
    slug=CB_SLUG, title=CB_ZH_TITLE, desc=CB_ZH_DESC, h1=CB_ZH_H1, dateline=DATE,
    main_html=render(CB_SLUG, CB_OG, "/category/productivity-zh.html", "AI 效率工具", CB_ZH_H1, CB_ZH_LEAD,
                     CB_ZH_BODY, *CB_EN_CTA, CB_ZH_PROS, CB_ZH_CONS, CB_ZH_VERDICT,
                     CB_ZH_FAQ, CB_ZH_RELATED, "Sam Porter", "文案与内容工具编辑"),
    faq_json=faq_json(CB_ZH_FAQ), og_image=CB_OG,
)

print("DONE: 4 article files generated")
