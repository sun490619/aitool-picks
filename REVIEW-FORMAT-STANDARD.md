# aitool-picks 评测文格式标准 v1.0

> **生效日期**：2026-07-31  
> **性质**：全站评测文的唯一格式真值源。每次生成/修改文章前必须对照此文件。  
> **替代**：此前 IMAGES-MANIFEST.md 引用的「评测文上线前检查表 §一（13.1）」**不存在**，本文件为首次正式落盘。

---

## 一、文件级元数据（`<head>` 必须包含）

| 字段 | 规则 |
|---|---|
| `<html lang>` | 英文 `"en"`，中文 `"zh-CN"` |
| `data-zh-url` | 英文页必须指向中文版路径（如 `data-zh-url="xxx-zh.html"`） |
| `<title>` | 格式 `{Tool} Review 2026: {Question?}`（英文）/ `{工具名} 评测 2026：{副标题}`（中文） |
| `<meta description>` | 150–160 字符，含工具名+核心卖点+年份 |
| `og:image` | 指向 `/images/og-{slug}.jpg`（必须与实际文件一致） |
| `og:type` | `"article"` |
| `canonical` | 完整 URL `https://aitool-picks.com/posts/{slug}.html` |
| hreflang alternate | EN/ZH/x-default 三条必须齐全 |
| JSON-LD BlogPosting | headline / description / inLanguage / datePublished / dateModified / author(Sam Porter) / publisher(AI Tool Picks) / mainEntityOfPage |
| JSON-LD FAQPage | 如文章有 FAQ 段落则必须加（数值字段用数字不用字符串，引号用全角弯引号） |
| GA + Clarity | `G-D53DQ3JKKL` + `xavbiwb9dt`，每页必须有 |

---

## 二、正文结构顺序（从上到下，不可乱序）

```
<nav>                          ← 全站导航（scripts.js 注入）
<main class="container">
  <article class="article-content">   ← 或 .article-body（两者等价）

    1. .breadcrumb                 ← 面包屑（可选）
    2. .post-meta                  ← 徽章(Review) · 日期 · 阅读时长
    3. <img class="post-hero">     ← Hero 配图（og 图复用为正文大图）
    4. <h1>                        ← 文章标题（仅一个）
    5. <p class="post-lead">       ← 导读段落（灰字、稍大）
    6. .article-content > *        ← 正文主体：
         - <h2> 各章节（自动带蓝色竖条装饰）
         - <p> / <ul> / <ol> / <blockquote> / <table> / <code>
         - <img class="post-figure"> （如有配图）
    7. <div class="verdict">       ← 结论框（绿底=推荐 / .verdict.bad=不推荐）
    8. <div class="pros-cons-grid">← 优缺点对比
         - <div class="pros-card">
         - <div class="cons-card">
    9. CTA 区                      ← .btn-primary 行动按钮 + .disclosure-banner 联盟披露
   10. <div class="affiliate-note">← 底部联盟备注（小字、虚线分隔）

  </article>

  <!-- ===== 相关推荐区块（⚠️ 类名必须严格匹配 CSS）===== -->
  <section class="related-articles">
    <h2>More AI tools you should know</h2>
    <div class="grid">                        ← ⚠️ 必须是 .grid，不是 .related-grid！
      <a href="...">
        <span class="r-thumb" style="background-image:url(...)"></span>  ← ⚠️ 内联背景图，不是 data-img
        <span class="r-title">标题</span>                              ← ⚠️ .r-title 不是 .related-title
        <span class="r-cat">分类</span>                                 ← ⚠️ .r-cat 不能省
      </a>
      （共 3–4 张卡）
    </div>
    <div class="related-resources">                                    ← 可选
      <h3>Tools & resources we use</h3>
      （Amazon / Gumroad 等资源链接）
    </div>
  </section>

</main>
<footer>                     ← 全站页脚（scripts.js 注入）
```

### ⚠️ 相关推荐区块类名对照表（CSS 已定义 vs 禁止使用的旧类名）

| 正确类名（styles.css 已定义） | ❌ 旧/错误类名（禁止使用） |
|---|---|
| `.grid` | `.related-grid` |
| `.r-thumb`（内联 `style="background-image:url(...)"`） | `.related-thumb`（`data-img` 属性，JS 不处理） |
| `.r-title` | `.related-title` |
| `.r-cat` | （无对应旧类，但不能省略） |

**违反后果**：使用错误类名 → CSS 样式全部失效 → 推荐卡变成整行堆叠裸文本框 + 缩略图永远看不见 = "快溢出屏幕/特别乱"。

---

## 三、图片规范（最高优先级）

### 3.1 图片来源优先级（从高到低）

1. **官方 Brand/Media Kit 授权图**（工具官网 press/media 页面下载，明确授权商用）
2. **CC0 真实照片**（Unsplash / Pexels / Openverse / Flickr cc0 / Wikimedia Commons）
3. **CC BY-SA 署名图**（Wikimedia Commons，需在 IMAGES-MANIFEST 记录作者信息）

### 3.2 绝对禁止

- ❌ PIL/AI 代码自绘（渐变背景+文字卡片、装饰图形等一切非真实照片）
- ❌ 带"AI生成/图片由AI生成"水印或任何标注的图
- ❌ 与文章主题**低相关或不相关**的通用库存照（如：求职工具评测用海滩打电话男）
- ❌ 跨文章重复使用同一张 og 图（每篇独立唯一）

### 3.3 高度相关性标准

选择图片时必须回答："读者看到这张图，能猜到这篇文章讲的是什么工具吗？"

| 文章类型 | 高相关图片示例 | 低相关/禁止示例 |
|---|---|---|
| AI 语音合成评测 | 录音设备/声波/播客场景 | 任何无关人物照 |
| AI 写作评测 | 打字/文档编辑器/写作场景 | 任何无关风景照 |
| AI 求职工具评测 | 简历文档/电脑求职/办公桌工作 | 海滩打电话男 ❌❌❌ |
| Mockup 生成器评测 | 产品 mockup 效果图/电商场景 ✅ | 任何无关场景 |
| SEO 工具评测 | 数据图表/分析仪表盘/搜索引擎 | 任何无关场景 |

**关键步骤**：选图后必须用肉眼确认图片内容与工具主题匹配，不能只看关键词搜索结果就套模板。

### 3.4 品牌模板叠加（og 图统一规格）

所有 og/hero 图必须经过 `_tmp_ogsrc/gen_og_today.py` 处理：

| 参数 | 值 |
|---|---|
| 尺寸 | 1200 × 630 px |
| 底图 | 真实来源照铺满（object-fit cover） |
| 遮罩 | 从上到下渐变 `rgba(15,23,42,0.45)` → `rgba(15,23,42,0.72)` |
| 左侧竖条 | `(96,165,250)` 宽 48px |
| 标题 | 白色 Bebas Neue 52px，左对齐偏移 70px |
| 底标 | `AI Tool Picks` 18px 灰色右下角 |

### 3.5 验收量化指标

运行 `gen_og_today.py` 时 verify() 输出必须满足：

| 指标 | 合格范围 |
|---|---|
| 唯一色数 | 4000 – 6000 |
| 平均亮度 | 60 – 85 |
| 标准差 | 30 – 36 |
| 左竖条色 | ≈ `(99,164,246)`（允许 ±3） |

### 3.6 授权留痕

每张图必须在 `/images/IMAGES-MANIFEST.md` 登记一条记录，包含：文件名、用途、来源 URL、许可类型、作者（如有）。

---

## 四、内容质量规则

1. **零模板生成**——所有正文由真实大模型逐篇生成，禁止 template-fill 套话拼接
2. **国际视角**——面向海外用户，避免美国化硬伤（IRS/W-2 等），除非文章专门针对美国市场
3. **准确性**——价格/功能/评分必须与工具当前版本一致（写于 2026 年 7 月的数据就是 2026 年 7 月数据）
4. **字数**——英文评测 ≥ 1500 词；中文评测 ≥ 2500 字
5. **联盟链接**——只在有已批准追踪 ID 的工具上挂链接（见《aitool-picks联盟链接申请清单》），未批准的不挂

---

## 五、发布前检查清单（每次 push 前逐条打勾）

- [ ] `<head>` 元数据完整（§二全部字段）
- [ ] JSON-LD 可被 `json.loads()` 解析（无语法错误）
- [ ] 正文结构顺序正确（§二 1–10 项）
- [ ] Hero 图存在且 HTTP 可访问（`images/og-{slug}.jpg`）
- [ ] Hero 图高度相关（通过 §3.3 肉眼测试）
- [ ] 相关推荐区使用 `.grid` / `.r-thumb` / `.r-title` / `.r-cat`（不是旧类名）
- [ ] `.r-thumb` 用内联 `style="background-image:url(...)"`（不是 `data-img`）
- [ ] 推荐的文章与当前评测主题**相关**（不是每篇都塞同一套通用链接）
- [ ] 无 `© 2026` 或其他日期残留
- [ ] IMAGES-MANIFEST.md 已登记本图
- [ ] `git add` 只包含本次相关文件（不带无关缓存改动）

---

## 六、历史教训（为什么需要本文件）

| # | 事故 | 根因 | 本文件如何防止 |
|---|---|---|---|
| 1 | AIApply 评测 og 图是海滩打电话男（与求职工具零相关） | 选图只看关键词匹配，没肉眼审核内容相关性 | §3.3 强制肉眼审核 + 相关性标准表 |
| 2 | AIApply/Mockey 底部推荐区"快溢出屏幕/特别乱" | HTML 用了 `.related-grid` 等旧类名，CSS 定义的是 `.grid`，样式全失效 | §二类名对照表 + §五检查清单第 6–7 项 |
| 3 | 全站多套文章格式并存（batch12 中文模板 vs review 英文模板） | 没有成文格式标准，各脚本各自为政 | §二统一定义唯一格式 |
| 4 | IMAGES-MANIFEST 引用「§13.1 检查表」但该文件不存在 | 规则只存在于对话记忆中，假装有流程 | 本文件即为正式落盘的标准 |
