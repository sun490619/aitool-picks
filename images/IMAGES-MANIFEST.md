# aitool-picks 图片授权留痕（IMAGES-MANIFEST）

> 规则来源：评测文上线前检查表 §一（13.1）。每张图必须记录：文件名 / 来源 URL / 授权类型。缺即重做。
> 最后更新：2026-08-05 01:10（08-05 01:10 新增⑧部署前强制检查铁律 + 竖条宽度坐标硬编码防手滑）

| 文件名 | 用途 | 来源 URL | 授权类型 |
|---|---|---|---|
| og-best-ai-tools-for-affiliate-marketers-2026.jpg | 联盟营销者评测文 og/hero/封面 | https://images.unsplash.com/photo-1460925895917-afdab827c52f (Unsplash, analytics dashboard 场景) | Unsplash License（免费商用，站点规则 §13.1 允许） |
| og-best-ai-tools-for-solopreneurs-2026.jpg | 独立创业者评测文 og/hero/封面 | https://images.unsplash.com/photo-1517245386807-bb43f82c33c4 (Unsplash, 独处笔记本工作场景) | Unsplash License（免费商用，站点规则 §13.1 允许） |
| og-taskade-review-2026.jpg | Taskade 评测文 og/hero/封面（en+zh 共用） | https://live.staticflickr.com/697/33286674502_4fa8d4e22f_b.jpg (Openverse/Flickr, 团队会议协作场景) | CC0（Openverse license=cc0 检索） |
| og-mindmapai-review-2026.jpg | MindMapAI 评测文 og/hero/封面（en+zh 共用） | 真实思维导图照片(Wikimedia Commons: "A Mind Map on ICT and Pedagogy", 作者 MuPaily, CC BY-SA 4.0) → 灰度反相成深色底 + 轻量深蓝品牌遮罩(alpha110) + 左侧竖条 + 标题；线条可见、主题贴合"思维导图" | CC BY-SA 4.0（署名 MuPaily / Wikimedia Commons，免费商用，已记录） |
| og-aiapply-review-2026.jpg | AIApply 评测文 og/hero/封面（en+zh 共用） | https://cdn.stocksnap.io/img-thumbs/960w/FBXB2DA8O7.jpg (Stocksnap CC0, 电脑笔记本办公桌场景照, 主题贴合"求职/在线工具/电脑工作") | CC0（Stocksnap, 免费商用） |
| og-mockey-review-2026.jpg | Mockey.ai 评测文 og/hero/封面（en+zh 共用） | https://cdn.stocksnap.io/img-thumbs/960w/13UNSPJHCZ.jpg (Openverse/Stocksnap, 工作桌/电商场景照, 主题贴合"产品图/mockup 生成器") | CC0（Openverse license=cc0 检索） | 2026-08-04 重做：原化妆品产品 mockup 照背景偏纯色(uniq=1129)触发留白铁律，换成更饱满场景照(uniq=4323) |
| og-neuronwriter-review-2026.jpg | NeuronWriter 评测文 og/hero/封面（en+zh 共用） | https://live.staticflickr.com/65535/53879850453_0e3a779d51_b.jpg (Openverse/Flickr, 内容营销/SEO 写作场景照, 主题贴合"SEO 内容优化") | CC0（Openverse license=cc0 检索） |
| og-coursebox-review-2026.jpg | Coursebox 评测文 og/hero/封面（en+zh 共用） | https://live.staticflickr.com/5169/5378305870_b02c3412da_b.jpg (Openverse/Flickr, 在线学习/课程场景照, 主题贴合"AI 课程生成") | CC0（Openverse license=cc0 检索） |
| og-chatgpt-alternatives-2026.jpg | ChatGPT替代品评测文 og/hero/封面（en+zh 共用） | https://images.unsplash.com/photo-1531746790095-e59a09f7c1c4 (Unsplash, 人指向笔记本屏幕/科技工作场景, 主题贴合"AI对话/聊天工具替代品") | Unsplash License（免费商用，08-05 从纯渐变重做为CC0真实照+径向暗角） |
| og-jasper-alternatives-2026.jpg | Jasper AI替代品评测文 og/hero/封面（en+zh 共用） | https://images.unsplash.com/photo-1501504905252 (Unsplash, 笔记本屏幕显示CMS/文本编辑器界面/咖啡厅创作场景, 主题高度贴合"AI文案工具/Copy.ai-Writesonic数字内容创作工作区") | Unsplash License（免费商用, 08-05 第三次修正: 从钢笔(弱相关)→清单(仍analog)→最终换为CMS编辑器界面(digital✅)） |

> 说明：以上 og 图均为「真实场景图（Unsplash / Openverse CC0 免费商用）+ 品牌模板叠加（**深蓝径向暗角遮罩**：中心 alpha≈0.45 → 四角≈0.70，颜色 B>G>R 的干净蓝 RGB≈(25,38,58)；+ 左侧品牌竖条 #60a5fa + 白色标题 46px + AI Tool Picks 标）」，非纯渐变、非 AI 生成图，符合 13.1「og 社交图…非纯渐变、含真实场景图」要求。

## 标准模板（唯一做法，新文章一律照此执行 · 2026-08-05 强化：径向暗角 + 蓝色调硬约束 + 量化验收）

> ⚠️ **2026-08-05 重大修正**：原「flat alpha150 深蓝渐变遮罩」参数会让人（和脚本）做出生硬/偏色图。线上用户认可的 3 张标准图（golden master，见 ⑦）实测是**径向暗角**（四角暗、中心亮），遮罩**必须是蓝色调**。本轮已用此参数重做 aiapply/mockey/mindmapai 三张并通过（部署 2a8058b）。

生成脚本：`_tmp_ogsrc/gen_og_today.py`（带 Openverse 自动取 CC0 真实场景照版；**须把遮罩逻辑改为下方②径向暗角**，旧版 flat 遮罩已作废）。

**① 底图（铁律·禁止 AI 生成图·高度相关·不重复）**：必须用 Unsplash / Openverse CC0 真实场景照（**主题必须与文章高度相关**——AI 工具文章配数字化场景，绝不用 analog 手写/纸笔），LANCZOS 铺满 1200×630。❌ 绝不用 image_gen / AI 合成图（案例 13 🔴；今天 aiapply/mockey/mindmapai 误用 AI 底图，须改回 CC0，见待办）。⚠️ **2026-08-05 用户确立·相关性铁律**：每张 og 图底图必须与文章主题**高度相关**——反例：AI 写作工具文章配钢笔手写（传统 analog ≠ AI digital，用户明确拒绝两次）；正例：AI 聊天工具配人机交互屏幕、AI 文案工具配 CMS 编辑器界面。如果实在找不到高度相关的可降级但**必须向用户说明**。⚠️ **不重复铁律**：不同文章的 og 图底图不能看起来基本一样/类似——全站已有 N 张图时新图必须有视觉区分度（如已有"笔记本工作区"就不要再选类似的）。

**② 品牌遮罩层（核心·颜色与形态硬约束）**：
- **形态 = 深蓝径向暗角**：中心 alpha ≈ 0.45、向四角递增到 ≈ 0.70（高斯模糊 30–40px 平滑过渡），中心稍亮、四角压暗。❌ **禁止 flat 均匀遮罩**（会像"均匀紫黑毯子"、标题区被压太暗，今天 v6 即此错）。
- **颜色 = 蓝色调，必须满足 B 通道 > G 通道 > R 通道**（R 最低）。✅ 验证值 RGB ≈ (25,38,58)（BGR 58,38,25）。❌ **绝不可用 R>B 的紫红/红调**（曾误做 RGB(35,18,25) → 用户评"发黑带红、不自然"）。判据口诀：遮罩色"蓝里发紫"=错；"干净蓝"=对。

**③ 左侧竖条（品牌标识·坐标铁律·2026-08-05 血的教训三次）**：rect[80, 90, **88**, **540**]（**宽 8px 细线，高 450px，距底边 90px 不触底！**），填充渐变蓝 (96,165,250) ↔ (108,161,236)（≈ #60a5fa）。⚠️ **2026-08-05 血的教训（累计 3 次错误）**：
1. **x2=168**（宽 88px 粗块，比 GM 粗 11 倍）→ 用户截图一眼识破
2. **y2=630**（触底/"入地"，比 GM 多 90px）→ 用户截图一眼识破  
3. **两次都是"给了参照物还做不好"** → 坐标必须死记：**x2=88, y2=540**，golden master 三张实测全一致。

**④ 文字**：标题白色 46px 从 y=200 起、行距 54、x=112、`textwrap.wrap(title, 30)` 最多 5 行；底部 (112,560) 品牌标 "AI Tool Picks" 26px (148,163,184)；JPEG quality=88。

**⑤ 量化验收线（部署前必测，缺一不可）**：
- 标题文字区（x80–700, y200–280）灰度亮度 **≈ 97–127**（白字清晰可读的硬指标；<~90 字糊、>~160 字融背景）。
- 四角（x30–50, y30–50）呈**深蓝色调**（B>G>R），亮度 ≤ ~95。
- 竖条实测色 ≈ (99,164,246)。
- 唯一色 4000–6000（证明是真实照片、非纯渐变）。**禁止 AI 生成图、禁止纯渐变图。**

**⑥ 流程铁律（避免反复涂抹）**：每次做图**从干净 CC0 底图重新生成**（遮罩+竖条+文字一次性套上），**绝不拿旧图反复 inpaint/涂抹修补**（今天 v1→v5 在旧图上反复涂 → 越涂越糊，v6 才换干净重生成思路）。改模板参数即整张重出，不留涂抹痕。

**⑦ Golden master 比对基准（肉眼 + 像素对照这 3 张用户认可的标准图）**：
- `og-taskade-review-2026.jpg`（Openverse CC0 协作场景）
- `og-best-ai-tools-for-affiliate-marketers-2026.jpg`（Unsplash 仪表盘场景）
- `og-best-ai-tools-for-solopreneurs-2026.jpg`（Unsplash 笔记本场景）
任何新 og 图上线前，与这 3 张并排比：暗角形态一致？遮罩是干净蓝（非紫红）？白字清晰度一致？不一致即重做。

**⑧ 部署前强制检查清单（2026-08-05 用户确立·每次生成/修改后必须逐条勾选，缺一不可部署）**

> **根因**：技术总监曾生成图后只跑脚本内置 verify() 就直接 push，**未做视觉比对**——导致竖条宽度 88px（应为 8px）这种肉眼一眼可见的错误上线、被用户截图抓包。**数值通过 ≠ 视觉正确。**

**生成或修改任何 og 图后，必须按以下顺序逐项检查，全部 ✅ 才可 git commit + push：**

| # | 检查项 | 方法 | 通过标准 |
|---|---|---|---|
| 1 | **竖条宽度** | 像素测量（蓝区 x 范围） | **7–10 px**（⚠️ 绝不是 88px！） |
| 2 | **标题区亮度** | crop(x80-700,y200-280) 灰度均值 | **97–127** |
| 3 | **四角色调** | 四角像素 B>G>R？ | **4/4 角通过**（容差：golden master taskade 自身也只有 3/4） |
| 4 | **遮罩形态** | 中心亮度 vs 四角亮度差 | 中心 > 四角（径向暗角证据） |
| 5 | **底图相关性** | 人眼判断：底图场景是否与文章主题**高度相关** | ❌ 反例：AI写作工具文章配钢笔手写（传统 analog ≠ AI digital）；✅ 正例：AI聊天工具配人用电脑对话 |
| 6 | **Golden master 并排肉眼看** | 新图与 §⑦ 三张标准图同时打开并排 | 暗角形态一致？色调一致？白字清晰度一致？**感觉"是一套的"？** |
| 7 | **线上实际效果** | curl 下载线上版本 + 浏览器打开卡片视图 | 与本地生成的一致？无 CDN 缓存旧版？ |

**执行纪律**：
- 脚本 verify() 输出只能作为第 2–4 项的参考，**不能替代第 1/5/6/7 项的人工检查**。
- 任何一项不通过 → **禁止 push** → 修完重跑全表。
- 检查结果必须记录在 commit message 中（格式：`Verify: bar=8px title_lum=105 corners=4/4 relevance=✅`）。
