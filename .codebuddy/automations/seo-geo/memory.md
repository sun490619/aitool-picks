# SEO/GEO 月度体检 · 执行记忆

## 2026-08-10（首轮）
- **修复并部署**：commit `92fcbd5`。aitool-picks sitemap 补 5 页（media-kit-zh / data-methodology-zh / changelog-zh / babylovegrowth EN+ZH）、删 1 条重复（best-ai-presentation-tools）、新评测文写入 llms.txt + llms-full.txt、IndexNow 推 6 条。线上 curl 已实证生效。
- **全绿项**：JSON-LD 478 块 0 失败；破图 0；og:image 异常 0；孤岛页 0；分类页收录 100%；视口/canonical 全覆盖。
- **GSC 近 30 天**：aitool 34 展现/1 点击、makerearn 15/1、mintshovels 1/0。仍为新站养权重期。

## 2026-08-17（第2轮）
- **无技术 bug、无部署**。三站全绿：aitool JSON-LD 482 块 0 失败、sitemap 269 条去重 0、破图 0、og:image 0、孤岛页 0、分类收录 100%、视口/canonical 全覆盖（exclude-me.html 有意排除）。MintShovels + makerearn 首页 title/desc/viewport/canonical/JSON-LD(2块0失败)/GA4/Clarity 全 OK。
- **GEO 资产稳定**：data-methodology / babylovegrowth / best-ai-seo-tools 在 llms.txt(118条) + llms-full + sitemap 均收录，内容未过时。sitemap 269（首轮 267 → +2 新页）。
- **GSC 近 30 天**：aitool 18 展现/0 点击、mint 81/0、makerearn 8/1。仍养权重期。
- **外链渠道**：AlternativeTo/PH/HN 仍 403/429 反爬拦截（非存活证据），Feedspot 根 200 但按手册已排除主动提交。外链仍待用户账号操作（策略项未擅动）。
- **内容时效**：16 篇含 "2025" 均为合法历史/事实表述（如 Topaz 2025末停售永久许可），无价格/列表明显过时。

## 复用经验（下轮直接套用，避免重复踩坑）
1. **误报陷阱 A**：死链脚本须排除 `href="/"`（根路径）与 `data:` 内联 SVG，否则误报。tool-selector.html 里的 `'+t.aff+'` / `'+t.review+'` 是 JS 模板串，非真死链。
2. **误报陷阱 B**：MintShovels 用**无扩展名 URL**（`.html` → 308 重定向），拿本地 `*.html` 比对 sitemap 会假报缺失。判定前先 curl 实测。
3. **外链渠道**：AlternativeTo / ProductHunt / HN 对脚本 UA 一律 403/429，**不能据此判定收录存活**，需浏览器视角或用户账号确认。Feedspot 与 TAAFT 已因付费墙排除（见外链作战手册）。
4. **验证铁律**：git push 后必须 curl 实证线上（GitHub Pages 构建约需 60–90s）。本轮无改动故未部署。
5. `exclude-me.html` 为有意不进 sitemap，非 bug。
6. 文章中出现 "2025" 多为合法历史/事实表述，非过时内容，勿盲改。

## 待办（策略项，只报告不擅动）
- 目录提交（AlternativeTo / PH / HN / IndieHackers 等）仍待用户账号操作。
- 客座文与 HARO/Featured 记者连线待用户邮箱参与。
- 三站 GSC 展现量偏低 = 权重瓶颈，非技术可抓取性问题；外链建设是当前最高杠杆，待用户推进。
