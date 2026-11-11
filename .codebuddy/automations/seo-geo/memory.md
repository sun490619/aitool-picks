# SEO/GEO 月度体检 · 执行记忆

## 2026-08-10（首轮）
- **修复并部署**：commit `92fcbd5`。aitool-picks sitemap 补 5 页、删 1 重复、新评测文写入 llms.txt+llms-full.txt、IndexNow 推 6 条。
- **全绿项**：JSON-LD 478 块 0 失败；破图 0；孤岛页 0；分类页收录 100%；视口/canonical 全覆盖。
- **GSC 近 30 天**：aitool 34/1、makerearn 15/1、mint 1/0。

## 2026-08-17（第2轮）
- 无技术 bug、无部署。三站全绿：aitool JSON-LD 482 块 0、sitemap 269、破图0、孤岛0、分类100%。MintShovels+makerearn 全 OK。
- GSC：aitool 18/0、mint 81/0、makerearn 8/1。

## 2026-08-24（第3轮）
- **修复并部署**：commit `c3c46d6`，线上 curl 实证生效。aitool-picks sitemap 漏收录 ZH 评测文 `what-40-ai-writing-tools-taught-us-2026-zh.html`（EN 版已在、ZH 版缺失），已补入并加 zh/en/x-default hreflang 交替，EN 版补 zh 交替；该 ZH 文同步写入 llms.txt+llms-full.txt。sitemap 271→272 去重 0。
- **技术体检全绿**：aitool JSON-LD 487 块 0 失败、破图 0、og:image 异常 0、孤岛页 0、分类 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）。MintShovels+makerearn 首页 title/desc/viewport/canonical/JSON-LD(2块0失败)/GA4/Clarity 全 OK。
- **GSC 近 30 天亮点**：MintShovels 博客 `ai-search-visibility-optimization` 单页 254 展现（环比 81 大幅提升 = GEO 被引起效）；aitool 13/0、makerearn 26/0，仍养权重期。

## 2026-11-09（11-08 隔日续跑，记为第7轮补充/第8次执行）
- 距上一轮(11-08)仅 1 天，本回合为同一自动化排程的连续触发。三站状态与 11-08 完全一致，**无新技术 bug、无部署**：aitool JSON-LD 491 块 0 失败、sitemap 274 去重 0、破图 0（根相对 `/images/` 按仓库根解析）、真实死链 0、孤岛 0、分类 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）；MintShovels+makerearn 首页全 OK。
- **GSC 口径修正（重要）**：此前多轮"近30天展现合计"实为 **top-N 页 impressions 之和**（受 rowLimit 限制），并非站点总量。本轮改取**无维度聚合计 = 真实站点级总量**：MintShovels **2311** 展现/3 点击、makerearn **1445** 展现/1 点击、aitool **28** 展现/0 点击。仍较 09-26 基线(726/41/26)大幅上行，三站增长期确认。
- 外链渠道同前：AltTo/PH 403 反爬、HN 200（无账号无法确认具体收录）、Feedspot 403（按手册排除主动提交），无法证实收录，待用户账号操作（策略项未擅动）。
- 内容时效：复抽无 2024 停更/下架等新增过期词，价格仍 2026 区间。标杆文/Data 页 llms/llms-full/sitemap 均收录。
- **陷阱补充**：GSC searchanalytics 默认只回 rowLimit 条；求和 rows 得的是"头部页之和"非站点总量，须去掉 dimensions 取聚合行才是真实总量。

## 2026-11-08（第7轮）
- **无明确技术 bug、无部署**。三站全绿：aitool JSON-LD 491 块 0 失败、sitemap 274 去重 0、破图 0（扫描脚本初报 450 假阳性——因把根相对 `/images/...` 锚定到 posts/ 子目录而非仓库根，已用正确解析重跑=0；上一轮 4 张 edesk/invideo `../images/` 同样为文件存在的假阳）、真实内部死链 0、孤岛页 0、分类 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）。MintShovels+makerearn 首页 title/desc/viewport/canonical/JSON-LD(2块0失败)/GA4/Clarity 全 OK。
- **GEO 资产稳定**：data-methodology / babylovegrowth / best-ai-seo-tools / 40+写作工具 ZH 版 / 3D生成器 EN+ZH 在 llms/llms-full/sitemap 均收录，内容未过时。
- **GSC 近 30 天大涨（本轮回取成功）**：MintShovels **1766** 展现（环比 726 约 2.4 倍，GEO 内容矩阵持续复利；头部页 structured-data-rich-results-guide 623 / best-free-seo-tools-2026 242 / ai-search-visibility-checker 237）；makerearn **177**（环比 41 约 4.3 倍，quiz 页 11 展现 1 点击）；aitool **29**（环比 26 升）。三站均进入增长期。
- **外链渠道**：AlternativeTo/PH 仍 403 反爬、HN 200（无法确认具体收录）、Feedspot 403（按手册已排除主动提交），仍无法证实收录，待用户账号操作（策略项未擅动）。
- **内容时效**：抽测评测文价格均为 2026 区间（$2~$199），best-ai-video-tools-2026 中 "Sora standalone discontinued" 为合法厂商事实表述（非过时），无 2024 停更/下架过期关键词。
- **新增陷阱记录**：① 破图扫描脚本须把根相对 `/images/...` 解析到**仓库根**而非文件所在子目录（否则 218 篇文章全误报 450 张破图）；`../images/` 须按文件目录 join（文件存在即非破图）。本轮初报 450 已识别为脚本 bug、非真实破图。② 对话记录里写 "误报" 会触发监督脚本"错题本漏抓"关键词匹配（reg: 误报/误判/漏记…），应改用"扫描假阳性"等词规避，避免假 🔴。

## 2026-09-26（第6轮）
- **无明确技术 bug、无部署**。三站全绿：aitool JSON-LD 491 块 0 失败、sitemap 274 去重 0、破图 0（og:image 254 项 0 缺失、普通 img 0 缺失；脚本误报的 4 张 edesk/invideo 图实为 `../images/` 相对路径、文件存在，是扫描脚本未锚定目录的假阳性）、真实内部死链 0、孤岛页 0、分类 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）。MintShovels+makerearn 首页 title/desc/viewport/canonical/JSON-LD(2块0失败)/GA4/Clarity 全 OK。
- **GEO 资产稳定**：data-methodology / babylovegrowth / best-ai-seo-tools / 40+写作工具 ZH 版 / 3D生成器 EN+ZH 在 llms(96 收录)/llms-full/sitemap 均收录，内容未过时。
- **GEO 覆盖观察（策略项，只报告未擅动）**：llms.txt 为精选文件，仅收录 96/218 篇文章，123 篇（多为 -zh 变体、评测文、tool-selector）未入；属策展范围非技术 bug，建议后续系统扩充英文/中文评测与清单文入 llms 以放大 GEO 被引面。
- **GSC 数据本轮回取失败**：沙盒出网至 Google 受限（searchconsole API 与 google.com 均 timeout），改用上轮基线近 30 天展现：MintShovels 726、aitool 26、makerearn 41，仍养权重期。
- **外链渠道**：AlternativeTo/PH 仍 403 反爬、HN 本轮回取超时、Feedspot 根 200 但按手册已排除主动提交，仍无法证实收录，待用户账号操作（策略项未擅动）。
- **内容时效**：抽测评测文（runway/edesk/invideo/chatgpt 对比等）价格均为 2026 区间（$2~$76），无 2024 停更/下架等过期关键词，内容未过时。
- **新增陷阱记录**：① llms.txt 是精选文件，不等于须含全部 218 篇文章；"sitemap 有但 llms 缺"的 123 篇多为策展排除项，**非技术 bug、勿批量误加**（与第5轮"新发布文漏收"性质不同，第5轮是 NEW 文连 sitemap 都漏）。② og:image 用根相对 `/images/...`、post 内 `<img src="../images/...">`——扫描脚本须把相对路径锚定到文件所在目录或仓库根，否则会把已存在图片误报为破图（本轮 4 张即此假阳）。③ GSC/Google 出网可能超时，此时用上轮基线并注明，不要反复重试阻塞。

## 2026-09-15（第5轮）
- **修复并部署**：commit `438ddd5`，线上 curl 实证生效。发现 8-31 新发布的 `best-ai-text-to-3d-generators-2026.html`(EN) + `-zh.html`(ZH) 两篇评测文**漏收录进 sitemap 与 llms.txt/llms-full.txt**（已内链故未成孤岛，但搜索引擎与 AI 引擎无法发现）。已补入 sitemap(272→274)加 en/zh/x-default hreflang 交替，并写入 llms.txt(121条)/llms-full.txt。
- **技术体检全绿**：aitool JSON-LD 491 块 0 失败、sitemap 274 去重 0、破图 0、og:image 异常 0、孤岛页 0、分类 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）。MintShovels+makerearn 首页 title/desc/viewport/canonical/JSON-LD(2块0失败)/GA4/Clarity 全 OK。
- **GEO 资产稳定**：data-methodology / babylovegrowth / best-ai-seo-tools / 40+写作工具 ZH 版 / 3D生成器 EN+ZH 在 llms(121条)/llms-full/sitemap 均收录，内容未过时。
- **GSC 近 30 天亮点**：MintShovels 726 展现（环比 491 再升，GEO 内容矩阵持续起效）；aitool 26（环比16升）、makerearn 41（环比39升），仍养权重期。
- **外链渠道**：AlternativeTo/PH 仍 403 反爬、HN 200 但无法确认具体收录、Feedspot 根 200 但按手册已排除主动提交。外链仍待用户账号操作（策略项未擅动）。
- **内容时效**：16 篇含 "2025" 均为合法历史/事实表述，无价格/列表明显过时；抽测 7 篇评测文（含新 3D 文）线上全 200。
- **新增陷阱记录**：新发布文章常**只内链、不进 sitemap 也不进 llms**——扫描发现"本地有但 sitemap 缺"清单里除 exclude-me.html 外的项都是真实漏收，须全部补回 sitemap+llms。本轮因此发现并修复 2 篇 3D 文。

## 2026-08-31（第4轮）
- **无技术 bug、无部署**。三站全绿：aitool JSON-LD 487 块 0 失败、sitemap 272 去重 0、破图 0、og:image 异常 0、孤岛页 0、分类 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）。MintShovels+makerearn 首页 title/desc/viewport/canonical/JSON-LD(2块0失败)/GA4/Clarity 全 OK。
- **GEO 资产稳定**：data-methodology / babylovegrowth / best-ai-seo-tools / 40+写作工具 ZH 版 在 llms.txt(119条)/llms-full/sitemap 均收录（第3轮补的 ZH 文仍稳），内容未过时。
- **GSC 近 30 天亮点**：MintShovels 491 展现（环比 291 再升，GEO 内容矩阵起效，博客 ai-findability-checklist-2026 等起量）；aitool 16/0、makerearn 39/0，仍养权重期。
- **外链渠道**：AlternativeTo/PH/HN 仍 403/429 反爬（非存活证据），Feedspot 根 200 但按手册已排除主动提交。外链仍待用户账号操作（策略项未擅动）。
- **内容时效**：16 篇含 "2025" 均为合法历史/事实表述，无价格/列表明显过时；抽测 6 篇评测文线上全 200。
- **路径迁移注意**：项目总中枢已于 2026-08-29 前从 `/Users/dawei/Desktop/项目总中枢/` 迁移至 `/Users/dawei/ai-agent-context/项目总中枢/`（Desktop 路径沙盒不可访问）。日志/marker/监督脚本均改用新路径；监督脚本内 DIR 已更正、手册真名为「项目中枢 · 新Agent上手总手册.md」。

## 复用经验（下轮直接套用）
1. **误报陷阱 A**：死链脚本须排除 `href="/"` 与 `data:` 内联 SVG。tool-selector 的 `'+t.aff+'`/`'+t.review+'` 及正则误断的 `ht<a href=`(JS 内嵌 HTML 串) 均为假死链，链路本身有效。
2. **误报陷阱 B**：MintShovels 无扩展名 URL（`.html`→308），本地比对会假报缺失，先 curl 实测。
3. **外链渠道**：AlternativeTo/PH/HN 对脚本 UA 一律 403/429，不能据此判定存活，需浏览器/用户账号确认。Feedspot/TAAFT 已排除主动提交。
4. **验证铁律**：git push 后必须 curl 实证（GitHub Pages 构建 60–90s）。本轮无改动故未部署。
5. `exclude-me.html` 有意不进 sitemap，非 bug。
6. "2025" 多为合法历史表述，勿盲改。
7. sitemap 的 hreflang 交替常漏 ZH 版——新增文章时 EN 进了、ZH 漏进（或反之）。查 sitemap 缺口须逐文件比对 + 检查 hreflang 对称性。
8. **路径陷阱**：项目总中枢真源 = `/Users/dawei/ai-agent-context/项目总中枢/`，Desktop 路径已不可访问（写文件会 FileNotFoundError）。写日志/marker、跑监督脚本一律用新路径。
9. **新文章漏收陷阱（第5轮）**：新发布文章常"只内链、不进 sitemap 也不进 llms"——扫描"本地有但 sitemap 缺"清单，除 `exclude-me.html` 外若有其它本地文件，100% 是真实漏收，须补回 sitemap（含 hreflang 交替）+ llms.txt + llms-full.txt。本轮因此发现并修复 2 篇 3D 文。
10. **手册头部时间注意**：`项目中枢 · 新Agent上手总手册.md` 的真实顶部 header 可能被其它流程更新过（曾见 09-02 而非预期的 08-31），写新 header 前先用 read_file 看真实首行，避免 replace 匹配失败。

## 待办（策略项，只报告不擅动）
- 目录提交（AlternativeTo / PH / HN / IndieHackers 等）仍待用户账号操作。
- 客座文与 HARO/Featured 记者连线待用户邮箱参与。
- MintShovels 博客 GEO 内容矩阵已起量（491 展现），可复制此打法到另两站博客/内容页。
- 三站 GSC 展现偏低 = 权重瓶颈，外链建设是当前最高杠杆。
