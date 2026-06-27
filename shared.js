/**
 * AI Tool Picks — Shared Theme & Language Logic
 * 
 * Handles cross-page state persistence:
 * 1. Dark/Light theme toggle (via html.dark class + localStorage)
 * 2. Language switch EN/中文 (via localStorage + full-page text translation)
 * 
 * Translation approach: maintains a complete en→zh translation map,
 * scans ALL text nodes on the page, and replaces matching English text
 * with Chinese equivalents. This covers article content, tool descriptions,
 * navigation, footer, buttons — everything visible.
 * 
 * Load this BEFORE scripts.js on every page.
 */
(function() {
  'use strict';

  var THEME_KEY = 'aitoolpicks-theme';
  var LANG_KEY = 'aitoolpicks-lang';

  // ========================================
  // THEME: Dark/Light Toggle
  // ========================================

  function getSavedTheme() {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved === 'dark' || saved === 'light') return saved;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
    return 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  function updateThemeUI() {
    var isDark = document.documentElement.classList.contains('dark');
    var label = document.getElementById('themeLabel');
    var icon = document.getElementById('themeIcon');
    if (label) {
      label.textContent = isDark ? 'Light' : 'Dark';
    }
    if (icon) {
      icon.innerHTML = isDark
        ? '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'
        : '<circle cx="12" cy="12" r="5"/><g stroke-linecap="round"><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></g>';
    }
  }

  var currentTheme = getSavedTheme();
  applyTheme(currentTheme);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateThemeUI);
  } else {
    updateThemeUI();
  }

  function toggleTheme() {
    var isDark = document.documentElement.classList.contains('dark');
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem(THEME_KEY, 'light');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem(THEME_KEY, 'dark');
    }
    updateThemeUI();
  }

  document.addEventListener('click', function(e) {
    var toggle = e.target.closest('#themeToggle');
    if (toggle) {
      e.preventDefault();
      e.stopPropagation();
      toggleTheme();
    }
  });

  // ========================================
  // LANGUAGE: Full-Page EN ↔ 中文 Translation
  // ========================================

  // Complete translation map: English text → Chinese text
  // Each entry is matched against text nodes on the page.
  // Longer strings are matched first to avoid partial replacements.
  var enToZh = {
    // === Site-wide Navigation ===
    'Home': '首页',
    'AI Writing': 'AI 写作',
    'AI Coding': 'AI 编程',
    'AI Video': 'AI 视频',
    'AI SEO': 'AI SEO',
    'Language': '语言',
    'Theme': '主题',
    'Light': '亮色',
    'Dark': '暗色',

    // === Hero / Homepage ===
    'Updated for 2026': '2026 年更新',
    'Honest': '真实的',
    'AI Tool Reviews': 'AI 工具评测',
    '& Comparisons': '与对比',
    'We test the top AI writing, coding, video, and SEO tools so you don\'t have to. No marketing fluff — just hands-on testing and honest verdicts.': '我们替你测试顶级的 AI 写作、编程、视频和 SEO 工具。没有营销废话——只有亲手测试和真实结论。',
    'Explore AI Writing Tools': '探索 AI 写作工具',
    'Best AI SEO Tools': '最佳 AI SEO 工具',
    'In-Depth Reviews': '深度评测',
    'Categories': '分类',
    'Independent': '独立测试',
    'Hand-tested comparisons to help you pick the right tool': '亲手测试对比，帮你选对工具',
    'Deep-dive comparisons across every major AI tool category': '覆盖所有主流 AI 工具品类的深度对比',

    // === Disclosure Banner ===
    'Disclosure:': '披露：',
    'Some links on this site are affiliate links. If you click and make a purchase, we may earn a commission at no extra cost to you. We only recommend tools we genuinely believe in after hands-on testing.': '本站部分链接为联盟链接。如你点击并购买，我们可能获得佣金，不会增加你的费用。我们只推荐亲手测试后真正认可的工具。',
    'Some links on this site are affiliate links. If you click and make a purchase, we may earn a commission at no extra cost to you.': '本站部分链接为联盟链接。如你点击并购买，我们可能获得佣金，不会增加你的费用。',

    // === Section Headers ===
    'Latest Reviews': '最新评测',
    'Explore by Category': '按分类浏览',
    'View All Reviews': '查看所有评测',
    'Don\'t Miss the Next Review': '不错过下一篇评测',
    'Top tools': '精选工具',

    // === Newsletter ===
    'Join 1,000+ creators getting hands-on AI tool comparisons straight to their inbox. No spam, unsubscribe anytime.': '加入 1,000+ 创作者，亲手测试的 AI 工具对比直达邮箱。无垃圾邮件，可随时退订。',
    'Join 1,000+ developers and writers getting hands-on AI tool comparisons. No spam, unsubscribe anytime.': '加入 1,000+ 开发者和写作者，亲手测试的 AI 工具对比直达邮箱。无垃圾邮件，可随时退订。',
    'Join 1,000+ SEOs getting hands-on AI SEO tool comparisons. No spam, unsubscribe anytime.': '加入 1,000+ SEO 从业者，亲手测试的 AI SEO 工具对比直达邮箱。无垃圾邮件，可随时退订。',
    'Subscribe': '订阅',
    'By subscribing, you agree to our': '订阅即表示你同意我们的',

    // === Category Page Headers ===
    'Writing & Productivity': '写作与效率',
    'AI Tools': 'AI 工具',
    'The world\'s most advanced AI writing assistants for grammar, style, long-form content, and creative productivity — tested for real writers.': '全球最先进的 AI 写作助手——语法、风格、长文内容和创意效率——为真实写作者测试。',
    'AI SEO Tools': 'AI SEO 工具',
    'Best AI SEO tools compared: Surfer SEO, Frase, NeuronWriter, MarketMuse, Scalenut, Originality.ai. Honest reviews for ranking higher in 2026.': '最佳 AI SEO 工具对比：Surfer SEO、Frase、NeuronWriter、MarketMuse、Scalenut、Originality.ai。2026 年排名提升的真实评测。',

    // === Category Cards ===
    'AI Writing Tools': 'AI 写作工具',
    'Jasper, Writesonic, KoalaWriter, Frase, Notion AI — compared for blog posts, ads, emails & long-form content.': 'Jasper、Writesonic、KoalaWriter、Frase、Notion AI——博客、广告、邮件和长文内容对比评测。',
    'AI Coding Assistants': 'AI 编程助手',
    'GitHub Copilot, Cursor, Windsurf, Codex — real dev workflow testing for speed, accuracy & DX.': 'GitHub Copilot、Cursor、Windsurf、Codex——真实开发工作流速度、准确度和开发体验测试。',
    'AI Video Generators': 'AI 视频生成器',
    'Sora, Runway Gen-3, Pika, HeyGen, Synthesia — tested for quality, control & workflow integration.': 'Sora、Runway Gen-3、Pika、HeyGen、Synthesia——质量、控制和工作流集成测试。',
    'Surfer, Frase, NeuronWriter, MarketMuse, Scalenut, Originality.ai — ranked for rankings.': 'Surfer、Frase、NeuronWriter、MarketMuse、Scalenut、Originality.ai——为排名而排名。',
    'Explore our full range of AI tool comparisons': '探索我们完整的 AI 工具对比系列',

    // === Blog Post Cards (Homepage) ===
    'Read full review': '阅读完整评测',
    'Read full review →': '阅读完整评测 →',
    'AI Writing': 'AI 写作',
    'AI SEO': 'AI SEO',
    '12 min read': '阅读 12 分钟',
    '8 min read': '阅读 8 分钟',
    '6 min read': '阅读 6 分钟',

    // === Post Cards Content (Homepage) ===
    'KoalaWriter Review 2026: Honest Hands-On Test & Verdict': 'KoalaWriter 2026 评测：真实上手测试与结论',
    'KoalaWriter is the best value AI writer for SEO content in 2026. At $9/mo, it produces 80% publish-ready articles with real-time SERP data, auto internal linking, and WordPress publishing.': 'KoalaWriter 是 2026 年 SEO 内容性价比最高的 AI 写手。$9/月，利用实时 SERP 数据、自动内链和 WordPress 发布，产出 80% 可直接发布的文章。',
    'Jasper AI vs Writesonic: Which AI Writer Wins in 2026?': 'Jasper AI vs Writesonic：2026 年哪个 AI 写手胜出？',
    'We tested both tools head-to-head on blog posts, ad copy, and long-form content. Here\'s our honest take on which one deserves your money.': '我们对博客文章、广告文案和长文内容进行了正面交锋测试。以下是哪个值得你花钱的诚实看法。',
    '5 Best AI SEO Tools to Rank Higher in 2026': '2026 年 5 款最佳 AI SEO 工具提升排名',
    'From Surfer SEO to Frase, we break down the top AI-powered SEO tools that actually move the needle on your rankings.': '从 Surfer SEO 到 Frase，我们拆解了真正能提升你排名的顶级 AI SEO 工具。',

    // === Footer ===
    'Honest comparisons & reviews of the best AI tools. Hand-tested, independently written, zero fluff.': '最真实的 AI 工具对比与评测。亲手测试，独立写作，零废话。',
    'Popular Reviews': '热门评测',
    'All Writing Tools': '所有写作工具',
    'All SEO Tools': '所有 SEO 工具',
    'Jasper vs Writesonic': 'Jasper vs Writesonic',
    'KoalaWriter Review': 'KoalaWriter 评测',
    'Resources': '资源',
    'Affiliate Disclosure': '联盟披露',
    'Privacy Policy': '隐私政策',
    'Newsletter': '邮件订阅',
    'Best AI SEO Tools': '最佳 AI SEO 工具',
    '&copy; 2026 AI Tool Picks. All rights reserved.': '© 2026 AI Tool Picks. 保留所有权利。',

    // === Post Pages: Common Elements ===
    'Updated': '更新于',
    'Disclosure': '披露',
    'Pros and Cons': '优缺点',
    'Pricing': '定价',
    'Affiliate tip:': '联盟提示：',
    'Who it\'s for:': '适用人群：',
    'Standout features:': '突出特点：',
    'Where it shines:': '优势所在：',
    'Final Verdict': '最终结论',
    'Final verdict': '最终结论',
    'Who Should Use': '谁该使用',
    'Who should use': '谁该使用',
    'Key Features': '核心功能',
    'Key features': '核心功能',

    // === Post: Best AI SEO Tools 2026 ===
    'SEO in 2026 isn\'t just about keywords anymore. With Google AI Overviews, ChatGPT search, and Perplexity changing how people find information, you need tools that optimize for': '2026 年的 SEO 不再只是关键词。随着 Google AI 概览、ChatGPT 搜索和 Perplexity 改变人们获取信息的方式，你需要同时优化',
    'traditional search engines and AI-generated answers.': '传统搜索引擎和 AI 生成答案的工具。',
    'We tested the top 5 AI SEO tools head-to-head. Here\'s what works — and what\'s just hype.': '我们对 5 款顶级 AI SEO 工具进行了正面交锋测试。以下是真正有效的——以及纯属炒作的。',
    'Surfer pioneered the "Content Score" — a real-time 0-100 score that shows how well your content matches the top-ranking pages for your target keyword. It analyzes 500+ on-page signals including NLP terms, heading structure, word count, and image usage.': 'Surfer 首创"内容评分"——一个实时的 0-100 分，显示你的内容与目标关键词排名前列页面的匹配程度。它分析 500+ 页面信号，包括 NLP 术语、标题结构、词数和图片使用。',
    'AI Tracker monitors your brand\'s visibility in ChatGPT, Perplexity, and Google AI Overviews. The Google Docs integration means you never leave your writing flow.': 'AI Tracker 监控你的品牌在 ChatGPT、Perplexity 和 Google AI 概览中的可见度。Google Docs 集成意味着你无需离开写作流程。',
    'Agencies and teams producing 20+ articles/month. The $99/mo price is steep for solo users, but the data quality justifies it at scale.': '适合每月产出 20+ 篇文章的代理机构和团队。$99/月对个人用户偏贵，但数据质量在规模上物有所值。',
    '30% commission with a 60-day cookie window — one of the longest in the industry. A single referral on the $219/mo Scale plan earns you ~$66.': '30% 佣金，60 天 Cookie 窗口——行业最长之一。$219/月 Scale 套餐单次推荐可获得约 $66。',
    'Frase does 80% of what Surfer does at less than half the price. The automated content briefs save hours — just enter a keyword, and Frase pulls SERP data, competitor outlines, and suggested headings into a ready-to-use brief.': 'Frase 以不到一半的价格实现了 Surfer 80% 的功能。自动内容简报节省数小时——只需输入关键词，Frase 即可抓取 SERP 数据、竞品大纲和建议标题，生成即用简报。',
    'The AI writing assistant generates full drafts from your briefs, with SERP-aware optimization that keeps your content competitive without manual tweaking.': 'AI 写作助手根据简报生成完整草稿，具备 SERP 感知优化，无需手动调整即可保持内容竞争力。',
    'Teams wanting Surfer-level insights at a friendlier price point. The free plan is generous enough for testing.': '适合希望以更友好价格获得 Surfer 级别洞察的团队。免费计划足够用于测试。',
    'NeuronWriter takes a different approach — it builds semantic maps using NLP to show you exactly which related terms, entities, and subtopics the top-ranking pages cover. This helps you build topical authority beyond simple keyword matching.': 'NeuronWriter 采用不同方法——它使用 NLP 构建语义地图，精确展示排名前列页面覆盖的相关术语、实体和子主题。这帮助你超越简单关键词匹配，建立主题权威。',
    'The content editor provides real-time LSI suggestions as you type, with difficulty scores and competitor gap analysis built into the workflow.': '内容编辑器在你输入时提供实时 LSI 建议，工作流内置难度评分和竞品差距分析。',
    'SEO writers who want deeper semantic optimization without the enterprise price tag. One-time payment option is a bonus for budget-conscious creators.': '适合希望在无企业级价格标签下获得更深语义优化的 SEO 写作者。一次性付款选项对预算敏感的创作者是加分项。',
    'MarketMuse is the heavyweight — it maps your entire content inventory against competitors, showing you exactly where you have topical gaps. The content briefs are the most comprehensive in the market, pulling from vast knowledge graphs.': 'MarketMuse 是重量级选手——它将你的整个内容库存与竞品对比，精确展示你的主题差距所在。内容简报是市场中最全面的，源自庞大的知识图谱。',
    'Enterprise teams managing 500+ pages. The price is prohibitive for small teams, but the strategic value for large content operations is unmatched.': '适合管理 500+ 页面的企业团队。价格对小团队来说太高，但对大型内容运营的战略价值无可匹敌。',
    'Scalenut positions itself as the affordable all-in-one — combining AI writing, SEO optimization, and content planning in a single dashboard. The Cruise Mode feature generates a complete 3,000-word article from a single keyword, including SERP analysis and NLP optimization.': 'Scalenut 定位为经济实惠的一体化方案——在单一仪表板中结合 AI 写作、SEO 优化和内容规划。Cruise Mode 功能可从单个关键词生成完整的 3,000 字文章，包括 SERP 分析和 NLP 优化。',
    'Solo bloggers and small teams who want SEO + AI writing in one tool without paying for multiple subscriptions.': '适合希望在一个工具中获得 SEO + AI 写作而无需支付多个订阅的个人博主和小团队。',

    // === Post: Jasper vs Writesonic ===
    'Jasper AI vs Writesonic: Which AI Writer Wins in 2026?': 'Jasper AI vs Writesonic：2026 年哪个 AI 写手胜出？',
    'Quick Comparison': '快速对比',
    'Quick comparison': '快速对比',
    'Best for enterprise marketing teams': '最适合企业营销团队',
    'Best for SEO-first content teams': '最适合 SEO 优先的内容团队',
    'Content Quality': '内容质量',
    'Content quality': '内容质量',
    'SEO Capabilities': 'SEO 能力',
    'SEO capabilities': 'SEO 能力',
    'Ease of Use': '易用性',
    'Ease of use': '易用性',
    'Long-form writing is slightly more polished': '长文写作稍显精炼',
    'SEO mode produces better-optimized drafts': 'SEO 模式产出优化更好的草稿',
    'Brand Voice training is more advanced': '品牌语音训练更先进',
    'SERP-aware outlines save editing time': 'SERP 感知大纲节省编辑时间',
    'Winner: Jasper for pure writing quality': '赢家：Jasper 纯写作质量',
    'Winner: Writesonic for SEO optimization': '赢家：Writesonic SEO 优化',
    'Who Should Choose Jasper': '谁该选 Jasper',
    'Who should choose Jasper': '谁该选 Jasper',
    'Who Should Choose Writesonic': '谁该选 Writesonic',
    'Who should choose Writesonic': '谁该选 Writesonic',

    // === Post: KoalaWriter Review ===
    'KoalaWriter Review 2026: Honest Hands-On Test & Verdict': 'KoalaWriter 2026 评测：真实上手测试与结论',
    'What KoalaWriter Gets Right': 'KoalaWriter 的优势',
    'Where It Needs Human Editing': '需要人工编辑的地方',
    'Amazon Product Roundups (Pro+)': 'Amazon 产品综述 (Pro+)',
    'Enter ASINs or search terms → Koala pulls live prices, ratings, images, specs → generates formatted comparison table + pros/cons + buy buttons. Affiliate-ready in minutes.': '输入 ASIN 或搜索词 → Koala 抓取实时价格、评分、图片、规格 → 生成格式化对比表 + 优缺点 + 购买按钮。几分钟即可联盟营销就绪。',

    // === Post: Originality.ai Review ===
    'Originality.ai Review 2026: Best AI Content Detector & Plagiarism Checker?': 'Originality.ai 2026 评测：最佳 AI 内容检测器与抄袭检查器？',
    'We tested Originality.ai for AI content detection, plagiarism, source reporting, and accuracy across real AI-generated and human-written samples. Here\u2019s what publishers and SEO teams should know.': '我们在真实 AI 生成和人工写作样本上测试了 Originality.ai 的 AI 内容检测、抄袭、来源报告和准确度。以下是发布商和 SEO 团队需要了解的。',
    'What Originality.ai Is Used For': 'Originality.ai 的用途',
    'Originality.ai sits at a strange point in the market: half AI detector, half plagiarism checker, half \u201cproof your writer didn\u2019t just paste through an AI tool.\u201d': 'Originality.ai 在市场定位独特：一半 AI 检测器，一半抄袭检查器，一半"证明你的写作者不是直接粘贴 AI 工具"。',
    'Originality.ai uses a pay-as-you-go credit model plus monthly tiers, with higher tiers unlocking full API support and unlimited scans.': 'Originality.ai 采用按量付费积分模式加月度套餐，更高级别解锁完整 API 支持和无限扫描。',
    '25% recurring for 12 months.': '12 个月 25% 持续佣金。',

    // === Tool Pages: Badge Labels ===
    'Grammar': '语法',
    'Translation': '翻译',
    'Workspace': '工作空间',
    'Marketing': '营销',
    'Copywriting': '文案',
    'Affordable': '实惠',
    'Paraphrasing': '改写',
    'Open Source': '开源',
    'Readability': '可读性',
    'SEO': 'SEO',

    // === Tool Pages: Descriptions (Writing Category) ===
    'The world\'s leading AI grammar checker and writing assistant. Real-time corrections for grammar, spelling, punctuation, and tone. Available as a browser extension, desktop app, and mobile keyboard.': '全球领先的 AI 语法检查和写作助手。实时纠正语法、拼写、标点和语气。提供浏览器扩展、桌面应用和手机键盘。',
    'The world\'s most accurate AI translation engine, supporting 30+ languages with neural-network quality that rivals human translators. Includes document translation and API access.': '全球最精准的 AI 翻译引擎，支持 30+ 语言，神经网络质量媲美人工翻译。包含文档翻译和 API 访问。',
    'An embedded AI writing assistant inside Notion. Supports drafting, summarization, rewriting, translation, and outline generation — seamlessly integrated into knowledge-work workflows.': '内嵌于 Notion 的 AI 写作助手。支持起草、摘要、改写、翻译和大纲生成——无缝融入知识工作流程。',
    'An AI content platform built for marketing teams. Offers 50+ templates, brand-voice training, SEO mode, and team collaboration for large-scale content production.': '为营销团队打造的 AI 内容平台。提供 50+ 模板、品牌语音训练、SEO 模式和大规模内容生产的团队协作。',
    'An SEO-focused AI writing platform with article generation, rewriting, expansion, and Chatsonic conversation mode. Built-in SEO optimization suggestions for higher rankings.': '以 SEO 为核心的 AI 写作平台，具备文章生成、改写、扩展和 Chatsonic 对话模式。内置 SEO 优化建议助你提升排名。',
    'A marketing-copy AI tool with 90+ templates covering ads, email, social media, and product descriptions. Friendly for teams that need fast, on-brand first drafts.': '营销文案 AI 工具，90+ 模板覆盖广告、邮件、社交媒体和产品描述。适合需要快速产出品牌风格初稿的团队。',
    'A budget-friendly AI writing assistant supporting 30+ languages, 40+ use-case templates, and built-in plagiarism checking for solo creators and small teams.': '实惠的 AI 写作助手，支持 30+ 语言、40+ 用例模板和内置抄袭检测，适合个人创作者和小团队。',
    'A specialist AI paraphrasing and polishing tool with 7 rewriting modes, grammar checking, citation generation, and plagiarism detection — ideal for academic and professional writing.': '专业 AI 改写和润色工具，7 种重写模式、语法检查、引用生成和抄袭检测——学术和专业写作的理想之选。',
    'An open-source multilingual grammar checker covering 30+ languages. Browser extension and editor-plugin support with a strong focus on privacy for multilingual writers.': '开源多语言语法检查器，覆盖 30+ 语言。浏览器扩展和编辑器插件支持，专注多语言写作者的隐私保护。',
    'A readability-focused editor that highlights long sentences, passive voice, and adverb overuse, then assigns a grade-level score to help you write clearer, stronger prose.': '以可读性为核心的编辑器，高亮长句、被动语态和副词滥用，并给出年级评分，助你写出更清晰、更有力的文字。',

    // === SEO Category: Tool Cards ===
    'Surfer SEO Review 2026': 'Surfer SEO 2026 评测',
    'Content optimizer with SERP-based grading, keyword clustering, and real-time content scoring. Built for in-house SEO teams that need repeatable briefs.': '基于 SERP 评分的内容优化器，具备关键词聚类和实时内容评分。为需要可重复简报的内部 SEO 团队打造。',
    'Frase.io Review 2026': 'Frase.io 2026 评测',
    'Research-to-draft workflow: competitor analysis, SERP outlines, and AI writing. Strong for content teams that want SEO and long-form in one tool.': '从研究到草稿的工作流：竞品分析、SERP 大纲和 AI 写作。适合希望在单一工具中兼顾 SEO 和长文的内容团队。',
    'NeuronWriter Review 2026': 'NeuronWriter 2026 评测',
    'NLP-driven content optimization with semantic LSI suggestions, content planning, and easy WordPress publishing.': 'NLP 驱动的内容优化，提供语义 LSI 建议、内容规划和便捷的 WordPress 发布。',
    'SEMrush AI Writing Assistant Review 2026': 'SEMrush AI 写作助手 2026 评测',
    'Best for teams already on SEMrush. SEO recommendations flow directly into AI drafting, with schema tips and readability checks.': '最适合已在 SEMrush 上的团队。SEO 建议直接流入 AI 草稿，附带 Schema 提示和可读性检查。',
    'MarketMuse Review 2026': 'MarketMuse 2026 评测',
    'Enterprise-grade content inventory and gap analysis with AI briefs. Strong on topical authority and content strategy at scale.': '企业级内容库存和差距分析，配备 AI 简报。在大规模主题权威和内容策略方面表现强劲。',

    // ========================================
    // POST: best-ai-seo-tools-2026.html
    // ========================================
    'Table of Contents': '目录',
    'The Shortlist': '速览',
    'Our Recommendation': '我们的推荐',
    'Tool': '工具',
    'Starting Price': '起价',
    'Best For': '最适合',
    'Affiliate Commission': '联盟佣金',
    'Agencies, content teams': '代理机构、内容团队',
    'Solo creators, freelancers': '个人创作者、自由职业者',
    'Budget optimization': '预算优化',
    'Enterprise strategy': '企业战略',
    'AI-first writers': 'AI 优先写作者',
    'AI content detection': 'AI 内容检测',
    '1. Surfer SEO — Best Overall for Serious SEOs': '1. Surfer SEO — 专业 SEO 最佳之选',
    '2. Frase — Best Value for Solo Creators': '2. Frase — 个人创作者最佳性价比',
    '3. NeuronWriter — Budget King': '3. NeuronWriter — 预算之王',
    '4. MarketMuse — Enterprise Content Intelligence': '4. MarketMuse — 企业内容智能',
    '5. Scalenut — AI-First Content Creation': '5. Scalenut — AI 优先内容创作',
    '6. Originality.ai — Best for AI Content Detection': '6. Originality.ai — 最佳 AI 内容检测',
    'From $99/mo (Essential)': '起价 $99/月 (Essential)',
    'From $45/mo (Basic)': '起价 $45/月 (Basic)',
    'From $19/mo (Bronze)': '起价 $19/月 (Bronze)',
    'From $149/mo': '起价 $149/月',
    'From $39/mo (Growth)': '起价 $39/月 (Growth)',
    'From $14.95/mo': '起价 $14.95/月',
    'Try Surfer SEO →': '试用 Surfer SEO →',
    'Get Started': '立即开始',
    'Try Frase →': '试用 Frase →',
    'Try NeuronWriter →': '试用 NeuronWriter →',
    'Get Started with NeuronWriter': '开始使用 NeuronWriter',
    'Try MarketMuse →': '试用 MarketMuse →',
    'Try Scalenut →': '试用 Scalenut →',
    'Try Originality.ai →': '试用 Originality.ai →',
    'Try KoalaWriter Free →': '免费试用 KoalaWriter →',
    'Get Started with KoalaWriter': '开始使用 KoalaWriter',
    'Get Started with Jasper': '开始使用 Jasper',
    'Get Started with Writesonic': '开始使用 Writesonic',
    'Get Started with Originality.ai': '开始使用 Originality.ai',
    'If you\'re a solo creator on a budget:': '如果你是有预算的个人创作者：',
    'If you run an agency or content team:': '如果你运营代理机构或内容团队：',
    'If you want the AI to do 90% of the work:': '如果你想让 AI 完成 90% 的工作：',
    'Comparison': '对比',

    // ========================================
    // POST: jasper-vs-writesonic.html
    // ========================================
    'Quick Comparison': '快速对比',
    'Quick Comparison: Jasper vs Writesonic (2026)': '快速对比：Jasper vs Writesonic (2026)',
    'Feature': '功能',
    'Jasper AI': 'Jasper AI',
    'Writesonic': 'Writesonic',
    'What Jasper AI Does Best': 'Jasper AI 的优势',
    'What Writesonic Does Best': 'Writesonic 的优势',
    'Output Quality Test': '输出质量测试',
    'Output Quality: Side-by-Side Test': '输出质量：并排测试',
    'The Bottom Line': '最终结论',
    'The Bottom Line: Which Should You Choose?': '最终结论：你该选哪个？',
    'Jasper (formerly Jarvis) launched in 2021 and was the first major AI writing tool before ChatGPT existed. In 2026,': 'Jasper（前身为 Jarvis）于 2021 年推出，是 ChatGPT 出现之前第一款主流 AI 写作工具。在 2026 年，',
    'Jasper\'s biggest differentiator isn\'t raw writing quality — it\'s brand consistency at scale': 'Jasper 最大的差异化优势不是原始写作质量——而是大规模的品牌一致性',
    'Brand Voice (Killer Feature)': '品牌语音（杀手级功能）',
    'Jasper lets you train its AI on your existing content — blog posts, brand guidelines, tone documents — and then': 'Jasper 允许你用现有内容——博客文章、品牌指南、语调文档——训练其 AI，然后',
    'every piece it generates sounds like you': '它生成的每段内容都像你自己写的',
    '. For agencies managing 5+ client brands, this feature alone justifies the price.': '。对于管理 5+ 客户品牌的代理机构来说，仅这一功能就物有所值。',
    '50+ Marketing Templates': '50+ 营销模板',
    'Not generic templates. Jasper has purpose-built frameworks for Facebook ads, Google ads, product descriptions, blog posts, email sequences, and landing pages. Each is optimized for conversion.': '不是通用模板。Jasper 有专为 Facebook 广告、Google 广告、产品描述、博客文章、邮件序列和落地页打造的框架。每个都针对转化优化。',
    'Team Collaboration': '团队协作',
    'Multiple users, shared brand voices, campaign folders — Jasper is built for teams. The Pro ($69/mo) and Business ($125+/mo) plans add admin controls, usage analytics, and priority support.': '多用户、共享品牌语音、活动文件夹——Jasper 专为团队打造。Pro ($69/月) 和 Business ($125+/月) 套餐增加管理员控制、使用分析和优先支持。',
    'Try Jasper AI free for 7 days →': '免费试用 Jasper AI 7 天 →',
    'Plans start at $49/mo. Cancel anytime. No credit card drama.': '套餐起价 $49/月。随时取消。无需信用卡折腾。',
    'Writesonic has pivoted hard in 2026 —': 'Writesonic 在 2026 年进行了大幅转型——',
    'it\'s now a GEO (Generative Engine Optimization) platform first, AI writer second': '它现在首先是 GEO（生成式引擎优化）平台，其次才是 AI 写作工具',
    '. If you care about how your brand appears in ChatGPT, Gemini, and Google AI Overviews, Writesonic is purpose-built for that.': '。如果你关心品牌在 ChatGPT、Gemini 和 Google AI 概览中的表现，Writesonic 就是为此打造的。',
    'AI Search Visibility Tracker': 'AI 搜索可见度追踪器',
    'This is the feature that justifies Writesonic\'s higher starting price ($79/mo). It monitors what ChatGPT, Gemini, Perplexity, and Google AI Overviews say about your brand — and gives you actionable steps to improve your visibility.': '这就是支撑 Writesonic 较高起价 ($79/月) 的功能。它监控 ChatGPT、Gemini、Perplexity 和 Google AI 概览对你的品牌的评价——并提供改善可见度的可操作步骤。',
    'Action Center': '行动中心',
    'Automated on-page and off-page fixes for AI search rankings. Think of it as an SEO tool, but for AI-generated search results rather than traditional Google rankings.': '自动化的站内和站外 AI 搜索排名修复。把它想成 SEO 工具，但针对 AI 生成的搜索结果而非传统 Google 排名。',
    '30% Lifetime Affiliate Commission': '30% 终身联盟佣金',
    'One of the most generous affiliate programs in the AI space — 30% recurring for the lifetime of the customer. A single referral on a $79/mo plan earns you ~$24/month, potentially for years.': 'AI 领域最慷慨的联盟计划之一——客户终身 30% 持续佣金。$79/月套餐单次推荐每月约赚 $24，可能持续多年。',
    'Try Writesonic today →': '立即试用 Writesonic →',
    'Starts at $79/mo. GEO tracking included on all paid plans.': '起价 $79/月。所有付费套餐包含 GEO 追踪。',
    'We gave both tools the same prompt: "Write a 500-word blog post introduction about AI in healthcare, targeting healthcare executives." Here\'s what happened:': '我们给两个工具相同的提示："写一篇 500 字的关于医疗 AI 的博客引言，面向医疗机构高管。"以下是结果：',
    'Produced a polished, brand-consistent intro with proper tone calibration. Generated 3 variants with different angles (regulatory, patient outcomes, cost savings).': '产出了精炼、品牌一致的引言，语调校准准确。生成了 3 个不同角度的变体（监管、患者结果、成本节省）。',
    'Generated a solid intro plus automatically suggested GEO-optimized headings, keyword clusters, and AI-search-friendly structure. The content itself was slightly more generic, but the optimization layer was impressive.': '生成了扎实的引言，并自动建议 GEO 优化标题、关键词集群和 AI 搜索友好结构。内容本身稍显通用，但优化层令人印象深刻。',
    'Winner:': '赢家：',
    ' Jasper for pure writing quality and tone control. Writesonic for content that\'s optimized to be surfaced by AI search engines.': ' Jasper 纯写作质量和语调控制。Writesonic 针对 AI 搜索引擎展示优化。',
    '🏆 Pick Jasper AI if:': '🏆 选择 Jasper AI 如果：',
    '🏆 Pick Writesonic if:': '🏆 选择 Writesonic 如果：',
    'You\'re a marketing team or agency producing content at scale': '你是大规模生产内容的营销团队或代理机构',
    'Brand voice consistency matters (multiple clients, multiple writers)': '品牌语音一致性很重要（多客户、多写手）',
    'You need campaign-specific templates (ads, emails, landing pages)': '你需要特定活动模板（广告、邮件、落地页）',
    'You have a $49-69/mo budget per seat': '每席位预算 $49-69/月',
    'AI search visibility (GEO) is your top priority': 'AI 搜索可见度 (GEO) 是你的首要任务',
    'You want to track how your brand appears in ChatGPT, Gemini, Perplexity': '你想追踪品牌在 ChatGPT、Gemini、Perplexity 中的表现',
    'You need automated SEO fixes alongside content generation': '你需要内容生成同时自动 SEO 修复',
    'You\'re comfortable with the $79+/mo entry point': '你能接受 $79+/月 的入门价格',
    'Honest take:': '坦诚说：',
    ' If you\'re a solo creator or small business, ChatGPT Plus ($20/mo) + a few custom prompts actually handles 80% of what both tools offer. Jasper and Writesonic shine when you need team workflows, brand controls, and platform-specific optimization that raw ChatGPT can\'t deliver.': ' 如果你是个人创作者或小企业，ChatGPT Plus ($20/月) + 几个自定义提示词实际上能处理两款工具 80% 的功能。Jasper 和 Writesonic 在你需要团队工作流、品牌控制和原生 ChatGPT 无法提供的平台特定优化时才真正发光。',

    // ========================================
    // POST: koalawriter-review-2026.html
    // ========================================
    'Quick Verdict': '快速结论',
    'Quick Verdict: Is KoalaWriter Worth It?': '快速结论：KoalaWriter 值得吗？',
    'Pricing & Plans': '定价与套餐',
    'Pricing & Plans (2026)': '定价与套餐 (2026)',
    'Key Features Tested': '核心功能测试',
    'Key Features': '核心功能',
    'Content Quality Test': '内容质量测试',
    'Content Quality Test: 20 Articles Across 4 Niches': '内容质量测试：4 个领域 20 篇文章',
    'SEO Features': 'SEO 功能',
    'SEO Features Deep Dive': 'SEO 功能深入解析',
    'Pros & Cons': '优缺点',
    'Final Verdict: Should You Buy KoalaWriter?': '最终结论：该买 KoalaWriter 吗？',
    'What KoalaWriter Gets Right': 'KoalaWriter 的优势',
    'Where It Needs Human Editing': '需要人工编辑的地方',
    'Real-Time SERP Analysis (The Differentiator)': '实时 SERP 分析（核心差异化）',
    'Auto Internal Linking': '自动内链',
    'One-Click WordPress Publishing': '一键 WordPress 发布',
    'Amazon Product Roundups (Pro+)': 'Amazon 产品综述 (Pro+)',
    'Internal Linking Engine': '内链引擎',
    'Schema & Technical SEO': 'Schema 与技术 SEO',
    '✅ Pros': '✅ 优点',
    '❌ Cons': '❌ 缺点',
    '🏆 Buy KoalaWriter If:': '🏆 购买 KoalaWriter 如果：',
    '❌ Skip If:': '❌ 跳过如果：',
    'Ready to Rank Higher?': '准备好提升排名？',
    'Start with 5,000 free words. No credit card. Cancel anytime.': '从 5,000 免费字数开始。无需信用卡。随时取消。',
    'Start Free Trial (5,000 words)': '开始免费试用 (5,000 字)',
    'Try KoalaWriter Free (5,000 words)': '免费试用 KoalaWriter (5,000 字)',
    'Start Free Trial →': '开始免费试用 →',
    'Plan': '套餐',
    'Monthly': '月费',
    'Words/Mo': '字数/月',
    'GPT-4o': 'GPT-4o',
    'Key Features': '核心功能',
    'Free trial:': '免费试用：',
    ' 5,000 words, no credit card. Enough to test 2-3 full articles.': ' 5,000 字，无需信用卡。足够测试 2-3 篇完整文章。',
    'KoalaWriter scrapes live SERPs for your target keyword, extracts entities, headings, word counts, and LSI terms from top 10 results, then builds an outline. This is': 'KoalaWriter 抓取目标关键词的实时 SERP，从排名前 10 结果中提取实体、标题、字数和 LSI 术语，然后构建大纲。这',
    'not': '不是',
    ' keyword stuffing—it\'s semantic optimization based on what\'s actually ranking': '关键词堆砌——它是基于实际排名的语义优化',
    'In our tests, KoalaWriter\'s outlines matched 85-90% of top-ranking content structure. Surfer SEO does this too, but at 5x the price.': '在我们的测试中，KoalaWriter 的大纲与排名前列内容结构匹配 85-90%。Surfer SEO 也能做到，但价格是 5 倍。',
    'KoalaWriter crawls your existing WordPress site, maps content clusters, and inserts contextual internal links': 'KoalaWriter 抓取你现有的 WordPress 网站，映射内容集群，并在生成过程中插入上下文内链',
    'during generation': '在生成过程中',
    '. In our test on a 200-post site, it added 8-12 relevant internal links per article with 92% relevance. Manual internal linking takes 15-20 min/article; Koala does it in seconds.': '。在 200 篇文章网站的测试中，每篇文章添加了 8-12 条相关内链，相关性 92%。手动内链每篇需 15-20 分钟；Koala 几秒完成。',
    'Connect via REST API or app password. One click pushes formatted HTML (headings, images, tables, schema) directly to draft or publish. Saved us 5-10 min/article vs copy-paste + formatting.': '通过 REST API 或应用密码连接。一键将格式化 HTML（标题、图片、表格、Schema）直接推送到草稿或发布。相比复制粘贴+格式化，每篇节省 5-10 分钟。',
    'Enter ASINs or search terms → Koala pulls live prices, ratings, images, specs → generates formatted comparison table + pros/cons + buy buttons. Affiliate-ready in minutes.': '输入 ASIN 或搜索词 → Koala 抓取实时价格、评分、图片、规格 → 生成格式化对比表 + 优缺点 + 购买按钮。几分钟即可联盟营销就绪。',
    'Affiliate (Best X for Y)': '联盟营销 (Best X for Y)',
    'Local Service (Plumber/HVAC)': '本地服务 (水管工/暖通)',
    'Informational (How-to/Guide)': '信息型 (教程/指南)',
    'SaaS Comparison': 'SaaS 对比',
    'Niche': '领域',
    'Articles': '文章数',
    'Avg Words': '平均字数',
    'Edit Time': '编辑时间',
    'Publish Ready?': '可发布？',
    'Structure:': '结构：',
    ' H2/H3 hierarchy matches top-ranking content 90%+': ' H2/H3 层级与排名前列内容匹配 90%+',
    'Entities:': '实体：',
    ' Injects relevant entities, LSI terms, NLP phrases naturally': ' 自然注入相关实体、LSI 术语、NLP 短语',
    'Formatting:': '格式化：',
    ' Bullet points, tables, FAQ schema, pros/cons boxes auto-generated': ' 项目符号、表格、FAQ Schema、优缺点框自动生成',
    'Accuracy:': '准确度：',
    ' 95%+ factual accuracy for established topics; hallucinates on cutting-edge/new topics': ' 成熟话题 95%+ 事实准确；前沿/新话题会产生幻觉',
    'Tone/Voice:': '语调/语音：',
    ' Default is "SEO neutral"—needs brand voice injection': ' 默认是"SEO 中性"——需要注入品牌语调',
    'Recent Data:': '近期数据：',
    ' Knowledge cutoff limits real-time stats (supplement manually)': ' 知识截止日期限制实时统计（手动补充）',
    'Nuance:': '细微差别：',
    ' Struggles with contrarian takes, expert nuance, personal experience': ' 在反主流观点、专家细节、个人经验方面有困难',
    'Fact-Checking:': '事实核查：',
    ' Always verify stats, prices, specs—~5% error rate': ' 始终验证数据、价格、规格——约 5% 错误率',
    'Real-Time SERP Analysis': '实时 SERP 分析',
    'KoalaWriter fetches live SERP for your keyword, parses top 10 results, extracts:': 'KoalaWriter 获取关键词实时 SERP，解析前 10 结果，提取：',
    'Heading structures (H2/H3 hierarchy)': '标题结构 (H2/H3 层级)',
    'Word count ranges': '字数范围',
    'Entities & NLP phrases (via NLP API)': '实体与 NLP 短语 (通过 NLP API)',
    'Content gaps vs your outline': '内容差距 vs 你的大纲',
    'PAA (People Also Ask) questions': 'PAA (用户还问) 问题',
    'Then builds an optimized outline. You can edit before generation.': '然后构建优化大纲。你可以在生成前编辑。',
    'Connect WordPress → Koala crawls your site, builds topic clusters, suggests 8-15 contextual internal links per article. Anchor text diversity: 70% exact match, 30% partial/branded.': '连接 WordPress → Koala 抓取你的网站，构建主题集群，每篇文章建议 8-15 条上下文内链。锚文本多样性：70% 精确匹配，30% 部分/品牌匹配。',
    'Article schema auto-generated': '文章 Schema 自动生成',
    'FAQ schema from PAA extraction': '来自 PAA 提取的 FAQ Schema',
    'Table of contents with jump links': '带跳转链接的目录',
    'Image alt text auto-generated': '图片 alt 文本自动生成',
    'Open Graph / Twitter cards ready': 'Open Graph / Twitter 卡片就绪',
    'Best value in SEO AI writing ($9-25/mo vs $99+ Surfer+Jasper)': 'SEO AI 写作最佳性价比 ($9-25/月 vs $99+ Surfer+Jasper)',
    'Real-time SERP data, not cached': '实时 SERP 数据，非缓存',
    'Auto internal linking saves hours': '自动内链节省数小时',
    'One-click WordPress publishing': '一键 WordPress 发布',
    '5,000 word free trial (no CC)': '5,000 字免费试用 (无需信用卡)',
    'Responsive support, active Discord community': '响应及时的支持，活跃的 Discord 社区',
    'Tone is "SEO neutral"—needs brand voice editing': '语调是"SEO 中性"——需要品牌语调编辑',
    'Knowledge cutoff affects recent data': '知识截止日期影响近期数据',
    'Amazon roundups need manual ASIN verification': 'Amazon 综述需要手动 ASIN 验证',
    'No built-in plagiarism checker': '无内置抄袭检测器',
    'Accessible API on all plans': '所有套餐可访问 API',
    'You publish 5+ SEO articles/month': '每月发布 5+ 篇 SEO 文章',
    'You use WordPress': '你使用 WordPress',
    'You want SEO optimization without Surfer SEO\'s price tag': '你想要 SEO 优化但不想付 Surfer SEO 的价格',
    'You need internal linking at scale': '你需要规模化内链',
    'ROI matters: $9/mo → 1 ranked article = 100x+ ROI': 'ROI 很重要：$9/月 → 1 篇排名文章 = 100x+ 回报',
    'You need brand voice / thought leadership content': '你需要品牌语调/思想领袖内容',
    'You write < 2 articles/month (not worth subscription)': '每月写 < 2 篇文章 (不值得订阅)',
    'You need recent data (post-2024) without manual research': '你需要近期数据 (2024年后) 但不做手动研究',
    'You want creative writing, storytelling, opinion pieces': '你想要创意写作、故事叙述、观点文章',
    'KoalaWriter has been making waves in the SEO content space since 2023. The promise is bold: "Publish SEO-optimized articles in minutes, not hours." At $9/mo for the Essential plan, it\'s positioned as the budget-friendly alternative to Surfer SEO + Jasper combos. But does it actually deliver publish-ready content, or just another AI text generator with SEO lipstick?': 'KoalaWriter 自 2023 年以来在 SEO 内容领域掀起波澜。其承诺大胆："几分钟发布 SEO 优化文章，而非几小时。"Essential 套餐 $9/月，定位为 Surfer SEO + Jasper 组合的经济替代方案。但它真的能产出可发布的内容，还是只是另一个披着 SEO 外衣的 AI 文本生成器？',
    'We spent two weeks testing KoalaWriter across 20+ articles across niches—affiliate sites, local service pages, informational blogs. Here\'s the unvarnished truth.': '我们花了两周时间在多个领域测试 KoalaWriter——联盟网站、本地服务页面、信息型博客。以下是不加修饰的真相。',
    'KoalaWriter is the best value AI writer for SEO content in 2026. At $9/mo, it produces 80% publish-ready articles with real-time SERP data, auto internal linking, and WordPress publishing. Not perfect—needs human editing for tone and fact-checking—but ROI is undeniable for content teams.': 'KoalaWriter 是 2026 年 SEO 内容性价比最高的 AI 写手。$9/月，利用实时 SERP 数据、自动内链和 WordPress 发布，产出 80% 可直接发布的文章。不完美——需要人工编辑语调和事实核查——但对内容团队来说，ROI 无可否认。',
    'Yes, if you publish 5+ SEO articles/month.': '是的，如果你每月发布 5+ 篇 SEO 文章。',
    ' At $9/mo (Essential) or $25/mo (Pro), KoalaWriter pays for itself with just one ranked article. The real-time SERP analysis, auto internal linking, and one-click WordPress publishing save 2-3 hours per article vs manual writing + Surfer SEO.': ' $9/月 (Essential) 或 $25/月 (Pro)，KoalaWriter 仅凭一篇排名文章就能回本。实时 SERP 分析、自动内链和一键 WordPress 发布，每篇文章比手动写作 + Surfer SEO 节省 2-3 小时。',
    'Not for:': '不适合：',
    ' Pure creative writing, thought leadership, or brand voice–heavy content. KoalaWriter optimizes for search intent, not brand voice.': ' 纯创意写作、思想领袖或品牌语调重度内容。KoalaWriter 优化搜索意图，而非品牌语调。',
    'Tool Review': '工具评测',

    // ========================================
    // POST: originality-ai-review-2026.html
    // ========================================
    'Originality.ai Review 2026: Best AI Content Detector & Plagiarism Checker?': 'Originality.ai 2026 评测：最佳 AI 内容检测器与抄袭检查器？',
    'We tested Originality.ai for AI content detection, plagiarism, source reporting, and accuracy across real AI-generated and human-written samples. Here\u2019s what publishers and SEO teams should know.': '我们在真实 AI 生成和人工写作样本上测试了 Originality.ai 的 AI 内容检测、抄袭、来源报告和准确度。以下是发布商和 SEO 团队需要了解的。',
    'What Originality.ai Is Used For': 'Originality.ai 的用途',
    'Originality.ai sits at a strange point in the market: half AI detector, half plagiarism checker, half \u201cproof your writer didn\u2019t just paste through an AI tool.\u201d': 'Originality.ai 在市场定位独特：一半 AI 检测器，一半抄袭检查器，一半"证明你的写作者不是直接粘贴 AI 工具"。',
    'Pros and Cons': '优缺点',
    'Pros:': '优点：',
    ' Fast scan-speed, API access, built-in plagiarism check, shareable reports.': ' 扫描速度快，API 访问，内置抄袭检查，可分享报告。',
    'Cons:': '缺点：',
    ' No \u201chumanizer\u201d mode to rewrite AI text, and results still need editorial judgment.': ' 无"人性化"模式重写 AI 文本，结果仍需编辑判断。',
    'Originality.ai uses a pay-as-you-go credit model plus monthly tiers, with higher tiers unlocking full API support and unlimited scans.': 'Originality.ai 采用按量付费积分模式加月度套餐，更高级别解锁完整 API 支持和无限扫描。',
    '25% recurring for 12 months.': '12 个月 25% 持续佣金。',

    // ========================================
    // Category Pages: Additional
    // ========================================
    'AI Video Generators': 'AI 视频生成器',
    'AI Coding Assistants': 'AI 编程助手',
    'Don\'t Miss the Next Review': '不错过下一篇评测',
    'Join 1,000+ creators getting hands-on AI tool comparisons straight to their inbox. No spam, unsubscribe anytime.': '加入 1,000+ 创作者，亲手测试的 AI 工具对比直达邮箱。无垃圾邮件，可随时退订。',

    // ========================================
    // General page elements
    // ========================================
    'min read': '分钟阅读',
    'Updated': '更新于',
    'Disclosure': '披露',
    'Pricing': '定价',
    'Pricing & Plans': '定价与套餐',
    'Get Started': '立即开始',
    'Free Trial': '免费试用',
    'Limited free trial': '有限免费试用',
    'Core Strength': '核心优势',
    'Templates': '模板',
    'Affiliate Commission': '联盟佣金',
    'Cookie Window': 'Cookie 窗口',
    'Brand Voice, marketing templates': '品牌语音、营销模板',
    'GEO tracking, AI search visibility': 'GEO 追踪、AI 搜索可见性',
    '50+ (ads, emails, blogs)': '50+ (广告、邮件、博客)',
    'Broad AI agent workflows': '广泛 AI 代理工作流',
    'Marketing teams, agencies': '营销团队、代理机构',
    'SEO teams, AI search optimization': 'SEO 团队、AI 搜索优化',
    '25-30% recurring (12 months)': '25-30% 持续佣金 (12 个月)',
    '30% lifetime recurring': '30% 终身持续佣金',
    '30 days': '30 天',
    'Jasper and Writesonic are two of the most well-known AI writing tools on the market. Both promise to help you write faster — blog posts, ad copy, emails, landing pages — but they\'ve taken very different paths in 2026.': 'Jasper 和 Writesonic 是市场上最知名的两款 AI 写作工具。两者都承诺帮你更快写作——博客文章、广告文案、邮件、落地页——但在 2026 年走上了截然不同的道路。',
    'We tested both extensively. Here\'s the comparison you actually need.': '我们进行了广泛测试。这是你真正需要的对比。',
  };

  // Build sorted keys: longer strings first to avoid partial matches
  var enKeys = Object.keys(enToZh).sort(function(a, b) {
    return b.length - a.length;
  });

  // Keep track of original texts for toggling back to English
  var originalTexts = new Map();

  // Walk all text nodes and translate
  function translateTextNodes(root, toChinese) {
    var walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: function(node) {
          // Skip script, style, noscript, code, pre, textarea, input
          var parent = node.parentElement;
          if (!parent) return NodeFilter.FILTER_REJECT;
          var tag = parent.tagName;
          if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT' ||
              tag === 'CODE' || tag === 'PRE' || tag === 'TEXTAREA' ||
              tag === 'INPUT' || tag === 'SELECT') {
            return NodeFilter.FILTER_REJECT;
          }
          // Skip empty/whitespace-only nodes
          if (!node.textContent.trim()) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    var node;
    while (node = walker.nextNode()) {
      var text = node.textContent;

      if (toChinese) {
        // Save original text if not already saved
        if (!originalTexts.has(node)) {
          originalTexts.set(node, text);
        }
        // Apply translations
        for (var i = 0; i < enKeys.length; i++) {
          var en = enKeys[i];
          var zh = enToZh[en];
          if (text.indexOf(en) !== -1) {
            text = text.split(en).join(zh);
          }
        }
      } else {
        // Restore original
        var orig = originalTexts.get(node);
        if (orig !== undefined) {
          text = orig;
        }
      }

      if (text !== node.textContent) {
        node.textContent = text;
      }
    }
  }

  // Also handle elements with data-i18n (backward compatible)
  var i18nKeys = {
    'nav_home':        { en: 'Home', zh: '首页' },
    'nav_writing':     { en: 'AI Writing', zh: 'AI 写作' },
    'nav_coding':      { en: 'AI Coding', zh: 'AI 编程' },
    'nav_video':       { en: 'AI Video', zh: 'AI 视频' },
    'nav_seo':         { en: 'AI SEO', zh: 'AI SEO' },
    'hero_title_line1': { en: 'Honest', zh: '真实的' },
    'hero_title_line2': { en: 'AI Tool Reviews', zh: 'AI 工具评测' },
    'hero_title_line3': { en: '& Comparisons', zh: '与对比' },
    'hero_subtitle':   { en: 'We test the top AI writing, coding, video, and SEO tools so you don\'t have to. No marketing fluff — just hands-on testing and honest verdicts.', zh: '我们替你测试顶级的 AI 写作、编程、视频和 SEO 工具。没有营销废话——只有亲手测试和真实结论。' },
    'section_latest':  { en: 'Latest Reviews', zh: '最新评测' },
    'section_categories': { en: 'Explore by Category', zh: '按分类浏览' },
    'lang_label':      { en: 'Language', zh: '语言' },
    'theme_label':     { en: 'Theme', zh: '主题' },
    'cta_explore':     { en: 'Explore Tools', zh: '探索工具' },
    'cta_compare':     { en: 'Compare Tools', zh: '对比工具' },
    'read_more':       { en: 'Read More', zh: '阅读更多' },
    'view_all':        { en: 'View All', zh: '查看全部' }
  };

  function getSavedLang() {
    return localStorage.getItem(LANG_KEY) || 'en';
  }

  function updateLangButtons(activeLang) {
    var container = document.getElementById('langSwitch');
    if (!container) return;
    var buttons = container.querySelectorAll('button');
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var isActive = btn.getAttribute('data-lang') === activeLang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    }
  }

  function applyFullTranslation(lang) {
    var toChinese = lang === 'zh';

    // First: data-i18n elements (backward compatible)
    var elements = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < elements.length; i++) {
      var el = elements[i];
      var key = el.getAttribute('data-i18n');
      if (i18nKeys[key] && i18nKeys[key][lang]) {
        el.textContent = i18nKeys[key][lang];
      }
    }

    // Second: translate all text nodes
    translateTextNodes(document.body, toChinese);

    // Update html lang attribute
    document.documentElement.lang = lang;
  }

  function switchLang(lang) {
    localStorage.setItem(LANG_KEY, lang);
    updateLangButtons(lang);
    applyFullTranslation(lang);
  }

  // Initialize language on page load
  var savedLang = getSavedLang();
  updateLangButtons(savedLang);

  // Apply translation after DOM is ready
  function initLang() {
    if (savedLang === 'zh') {
      applyFullTranslation('zh');
    } else {
      // Even for 'en', update the html lang attribute
      document.documentElement.lang = 'en';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLang);
  } else {
    initLang();
  }

  // Delegated click handler for lang switch buttons
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('#langSwitch button');
    if (btn) {
      e.preventDefault();
      e.stopPropagation();
      var lang = btn.getAttribute('data-lang');
      if (lang) switchLang(lang);
    }
  });

  // ========================================
  // Expose globally
  // ========================================
  window.AIToolPicksTheme = {
    toggleTheme: toggleTheme,
    getTheme: function() { return localStorage.getItem(THEME_KEY) || 'light'; },
    switchLang: switchLang,
    getLang: function() { return getSavedLang(); }
  };

})();
