# aitool-picks 图片授权留痕（IMAGES-MANIFEST）

> 规则来源：评测文上线前检查表 §一（13.1）。每张图必须记录：文件名 / 来源 URL / 授权类型。缺即重做。
> 最后更新：2026-07-30 22:40

| 文件名 | 用途 | 来源 URL | 授权类型 |
|---|---|---|---|
| og-best-ai-tools-for-affiliate-marketers-2026.jpg | 联盟营销者评测文 og/hero/封面 | https://images.unsplash.com/photo-1460925895917-afdab827c52f (Unsplash, analytics dashboard 场景) | Unsplash License（免费商用，站点规则 §13.1 允许） |
| og-best-ai-tools-for-solopreneurs-2026.jpg | 独立创业者评测文 og/hero/封面 | https://images.unsplash.com/photo-1517245386807-bb43f82c33c4 (Unsplash, 独处笔记本工作场景) | Unsplash License（免费商用，站点规则 §13.1 允许） |
| og-taskade-review-2026.jpg | Taskade 评测文 og/hero/封面（en+zh 共用） | https://live.staticflickr.com/697/33286674502_4fa8d4e22f_b.jpg (Openverse/Flickr, 团队会议协作场景) | CC0（Openverse license=cc0 检索） |
| og-mindmapai-review-2026.jpg | MindMapAI 评测文 og/hero/封面（en+zh 共用） | https://live.staticflickr.com/65535/51612081969_92a127258a_b.jpg (Openverse/Flickr, 头脑风暴场景) | CC0（Openverse license=cc0 检索） |

> 说明：以上 og 图均为「真实场景图（Unsplash / Openverse CC0 免费商用）+ 品牌模板叠加（半透明渐变遮罩 alpha150 深蓝 #0f172a→#1e3a8a + 左侧品牌竖条 #60a5fa + 白色标题 46px + AI Tool Picks 标）」，非纯渐变、非 AI 生成图，符合 13.1「og 社交图…非纯渐变、含真实场景图」要求。

## 标准模板（唯一做法，新文章一律照此执行）

生成脚本：`_tmp_ogsrc/gen_og_compliant.py`（2026-07-29 首版）/ `_tmp_ogsrc/gen_og_today.py`（2026-07-30 带 Openverse 自动取图版）。

参数固定：画布 1200×630；真实场景照 LANCZOS 铺满；深蓝渐变遮罩 (15,23,42)→(30,58,138) alpha 150；左侧竖条 rect[80,90,88,540] 填充 (96,165,250)；标题白色 46px 从 y=200 起、行距 54、x=112、`textwrap.wrap(title, 30)` 最多 5 行；底部 (112,560) 品牌标 "AI Tool Picks" 26px (148,163,184)；JPEG quality=88。

验收基线（与本文件已登记图对比）：唯一色 4000–6000、均亮 60–85、标准差 30–36、竖条实测色 ≈(99,164,246)。**禁止 AI 生成图、禁止纯渐变图。**
