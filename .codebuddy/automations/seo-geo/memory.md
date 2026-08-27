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
- **GEO 资产稳定**：data-methodology / babylovegrowth / best-ai-seo-tools / 40+写作工具 ZH 版 在 llms+llms-full+sitemap 均收录，内容未过时。
- **GSC 近 30 天亮点**：MintShovels 博客 `ai-search-visibility-optimization` 单页 254 展现（环比 81 大幅提升 = GEO 被引起效）；aitool 13/0、makerearn 26/0，仍养权重期。
- **外链渠道**：AlternativeTo/PH/HN 仍 403/429 反爬（非存活证据），Feedspot 根 200 但按手册已排除主动提交。外链仍待用户账号操作（策略项未擅动）。
- **内容时效**：16 篇含 "2025" 均为合法历史/事实表述，无价格/列表明显过时。

## 复用经验（下轮直接套用）
1. **误报陷阱 A**：死链脚本须排除 `href="/"` 与 `data:` 内联 SVG。tool-selector 的 `'+t.aff+'`/`'+t.review+'` 及正则误断的 `ht<a href=`(JS 内嵌 HTML 串) 均为假死链，链路本身有效。
2. **误报陷阱 B**：MintShovels 无扩展名 URL（`.html`→308），本地比对会假报缺失，先 curl 实测。
3. **外链渠道**：AlternativeTo/PH/HN 对脚本 UA 一律 403/429，不能据此判定存活，需浏览器/用户账号确认。Feedspot/TAAFT 已排除主动提交。
4. **验证铁律**：git push 后必须 curl 实证（GitHub Pages 构建 60–90s）。
5. `exclude-me.html` 有意不进 sitemap，非 bug。
6. "2025" 多为合法历史表述，勿盲改。
7. **新增陷阱**：sitemap 的 hreflang 交替常漏 ZH 版——新增文章时 EN 进了、ZH 漏进（或反之）。查 sitemap 缺口须逐文件比对 + 检查 hreflang 对称性。

## 待办（策略项，只报告不擅动）
- 目录提交（AlternativeTo / PH / HN / IndieHackers 等）仍待用户账号操作。
- 客座文与 HARO/Featured 记者连线待用户邮箱参与。
- MintShovels 博客 GEO 文章已起量（254 展现），可复制此打法到另两站博客/内容页。
- 三站 GSC 展现偏低 = 权重瓶颈，外链建设是当前最高杠杆。
