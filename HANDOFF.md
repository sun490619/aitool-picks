# AI Tool Picks — 项目交接文档

> 最后更新：2026-06-25（由 Hermes Agent 整理）
> 仓库地址：https://github.com/sun490619/aitool-picks
> 线上地址：https://sun490619.github.io/aitool-picks/

---

## 1. 项目目标
建立专业 AI 工具评测站，通过 Google SEO 长尾流量 + 专属联盟链接变现。

---

## 2. 技术栈 & 部署
- **类型**：纯静态站点（HTML + CSS + JS）
- **托管**：GitHub Pages（用户站点 `sun490619.github.io/aitool-picks`）
- **双目录部署**：根目录 `/` + `docs/` 目录均部署
- **GA4 追踪**：`G-D53DQ3JKKL`
- **设计标准**：Vercel/Apple 极简风，浅灰背景 #F9FAFB，正文 #1F2937，按钮 #2563EB，12px 圆角，Header 毛玻璃

---

## 3. 当前站点结构（`/Users/dawei/aitool-picks/`）
```
├── index.html                  # 首页
├── styles.css                  # 全局样式
├── scripts.js                  # 全局脚本（抽屉菜单、暗黑模式、阅读进度）
├── privacy.html                # Privacy Policy
├── affiliate-disclosure.html   # Affiliate Disclosure
├── category/
│   ├── writing.html            # AI Writing Tools 分类
│   ├── coding.html             # AI Coding Tools 分类
│   ├── video.html              # AI Video Tools 分类
│   └── seo.html                # AI SEO Tools 分类
├── posts/
│   ├── koalawriter-review-2026.html
│   ├── jasper-vs-writesonic.html
│   └── best-ai-seo-tools-2026.html
├── tools/
│   ├── rytr.html
│   ├── grammarly.html
│   ├── jasper.html
│   ├── writesonic.html
│   ├── notion-ai.html
│   ├── copy-ai.html
│   ├── deepl.html
│   ├── quillbot.html
│   ├── languagetool.html
│   └── hemingway.html
└── docs/                       # GitHub Pages docs/副本（与根目录同步）
```

---

## 4. 已完成任务（2026-06-25）
- [x] Header 统一为 **Brand + Hamburger**，桌面端无重复侧边栏
- [x] Drawer 结构统一：默认隐藏，点击汉堡滑出，包含导航 + Lang/Theme
- [x] 暗黑模式 class 统一为 `dark`（`html.dark`）
- [x] 图片 onerror 占位兜底（`img-failed` 渐变背景）
- [x] Explore by Category 网格：`.category-grid`，手机1列、平板2列、桌面4列
- [x] 订阅表单样式重构（圆角、蓝色按钮、hover 反馈）
- [x] Footer 社交图标使用原生 SVG（X / GitHub / LinkedIn）
- [x] 2 篇评测文章更新为专用 tool page 路径（KoalaWriter、SEO）
- [x] 首页 Latest Reviews 统一为 posts 链接
- [x] 全站 40 个页面 Header/Drawer 结构统一
- [x] GA4 追踪码部署全站

---

## 5. 待完成任务 / 已知缺口
- [ ] **内容补全**：Coding / Video / Writing 分类缺独立评测文章
- [ ] **工具详情页**：Video 分类暂无任何工具页（Rytr 除外，位于 Writing）
- [ ] **对比文章**：仅 1 篇（Jasper vs Writesonic），缺少更多 head-to-head
- [ ] **"Best X" 列表文**：Writing / Coding / Video 分类缺少
- [ ] **视觉细节**：卡片 hover 效果、行高、字体层级可再打磨（Vercel 标准）
- [ ] **docs/ 同步**：每次 push 后需手动确认 `docs/` 已同步（或写脚本自动）

---

## 6. 联盟链接真实状态（按截图确认）
| 工具 | 状态 | 截图证据 |
|------|------|----------|
| KoalaWriter | ❌ 被拒绝 | Connor 邮件："We are not interested. Your articles contain way too much incorrect information." |
| Writesonic | ⏳ 审核中 | FirstPromoter 页面：Pending，未批准 |
| Rytr | ✅ 已获批 | `affiliates.rytr.me`，30% commission，Joined June 20, 2026 |
| Originality.ai | ✅ 已获批 | `originality-ai-1.getrewardful.com`，25% 12个月，Joined June 16, 2026 |
| Frase | ✅ 已获批 | `affiliates.frase.io`，30% for 12 months 截图确认 |
| NeuronWriter | ✅ 已获批 | `app.neuronwriter.com/ucp/affiliate`，30% lifetime，截图确认 |
| Notion AI | ❓ 未验证 | 用户提供链接，无截图证明 |
| DeepL | ❓ 未验证 | 用户提供链接，无截图证明 |

**未申请的常见平台：**
Grammarly、Jasper、Copy.ai、QuillBot、LanguageTool、Hemingway

---

## 7. 下一步建议优先级
1. **内容优先**：给已有联盟链接的工具补专用 tool page + review post
   - 顺序：Notion AI / DeepL / Writesonic / NeuronWriter
2. **SEO 补量**：每个分类补 2-3 篇评测文章（至少写完 Coding、Video）
3. **技术债**：把 `scripts.js` 和 HTML 中的旧类名（`drawerOverlay`、`drawerMenu`）彻底清理
4. **自动化**：写一个脚本，在 `git push` 后自动同步 `docs/`，避免手动操作

---

## 8. 重要约定 & 用户偏好
- **设计**：专业评测站风格（Wirecutter / PCMag），极简、高质感、大留白
- **内容语言**：全站英文
- **用户语言**：中文沟通，技术术语可用英文
- **交付要求**：每步做完必须明确汇报"干完了 / 还没干完 / 卡在哪"
- **不要自动推**：`git push` 必须用户确认后再执行
- **规则**：对已有专属链接的工具补内容，无链接的不动

---

## 9. 关键命令速查
```bash
# 查看 git 状态
cd /Users/dawei/aitool-picks && git status --short

# 同步 docs/（手动，每次修改后执行）
rm -rf docs && mkdir -p docs/category docs/posts docs/tools
cp index.html styles.css scripts.js privacy.html affiliate-disclosure.html docs/
cp category/* docs/category/ && cp posts/* docs/posts/ && cp tools/* docs/tools/

# 提交 & 推送（需用户确认）
cd /Users/dawei/aitool-picks && git add -A && git commit -m "fix: ..." && git push

# 线上预览
https://sun490619.github.io/aitool-picks/
```

---

## 10. Contact / 交接对象
- **当前负责人**：用户 dawei（中文，技术型）
- **Agent 平台**：Hermes Agent (Nous Research)
- **模型**：stepfun/step-3.7-flash:free
- **状态**：站点已上线，5 个核心 Bug 已修复，内容补全阶段

---

*如果接手 Agent 看到此文档后还有疑问，先看第 6 节的联盟链接表和第 1 节的项目目标。*
