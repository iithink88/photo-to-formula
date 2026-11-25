# photo-to-formula · 把任何照片拆成可复制的创作公式

一个 WorkBuddy 技能：上传任意照片，自动拆解为一张 16:9 的专业视觉分析板，并反推出可直接用于图像生成的中英文提示词。

灵感来自微信公众号「黑科技宝库」的 *UNIVERSAL PHOTO VISUAL ANALYSIS SYSTEM V2.0*，方法核心：**参考照片决定分析内容，视觉分析系统决定信息组织，专业编辑设计决定最终呈现**。只分析画面里真实可见的证据，焦距/光圈/器材等无法确认的信息一律用推测措辞，不编造、不套模板、不写空洞赞美。

## 它能做什么

输入一张照片（人物、风景、建筑、产品、美食、动物、街拍……任意题材），产出一张包含 **7 个模块** 的分析板：

| 模块 | 内容 |
|---|---|
| A · 原图主体与视觉标注 | 完整保留原图，5–8 处引线+圆形锚点中文标注 |
| B · 核心关键词锚点 | 7–9 个由照片真实内容决定的生成维度 |
| C · 构图与机位分析 | 忠于原图的构图线稿 + 构图要点 + 机位与镜头（推测措辞） |
| D · 关键细节参考 | 5 张来自原图的局部放大 + 中文说明 |
| E · 光影与色彩特征 | 光源方向、软硬、反差、色温、氛围 |
| F · 配色参考（近似） | 6 张实采样色卡（HEX + 中文色名 + 用途） |
| G · 完整反推提示词 | 中文 + English 两段，可直接用于图像生成 |

## 两条出图路径

- **路径 A · HTML 精排（默认）**：分析 → 脚本采样配色与细节 → 填 HTML 模板 → Chrome 截图为 3840×2160 PNG。文字清晰、HEX 精确、零生图成本。
- **路径 B · AI 直出**：把原图喂给 `ImageGen` 图生图，直接生成文章原版质感的分析板。中文小字和 HEX 可能不准，且会消耗约 5–10 credits/张。

## 目录结构

```
photo-to-formula/
├── SKILL.md                       # 技能主文件（WorkBuddy 读取的工作流）
├── README.md                      # 本说明
├── DEMO/                          # 示例：原图 + 成品分析板
│   ├── source.png
│   └── 视觉分析板.png
├── assets/
│   └── board-template.html        # 1920×1080 七模块 HTML 模板
├── references/
│   ├── analysis-framework.md      # 完整 V2.0 方法论（分析前必读）
│   ├── build-guide.md             # HTML 布局、锚点技巧、QA 清单
│   └── imagegen-prompt.md         # 路径 B 的中英提示词模板
└── scripts/
    ├── analyze_photo.py           # 六色采样 + 5 处细节裁切 → JSON
    └── render_board.py            # HTML → 16:9 PNG（Playwright + Chrome）
```

## 安装方法

### 方式一：直接复制到技能目录（推荐）

把整个 `photo-to-formula` 文件夹复制到你的 WorkBuddy 用户级技能目录：

| 系统 | 目标路径 |
|---|---|
| Windows | `C:\Users\<你的用户名>\.workbuddy\skills\photo-to-formula\` |
| macOS | `~/.workbuddy/skills/photo-to-formula/` |
| Linux | `~/.workbuddy/skills/photo-to-formula/` |

复制后重启 WorkBuddy 或刷新技能列表，技能即可被识别。

### 方式二：压缩包安装

如果拿到的是 `photo-to-formula.zip`，先解压，再把解压出的 `photo-to-formula` 文件夹按上表放到技能目录。注意不要多套一层目录（正确结构是 `skills/photo-to-formula/SKILL.md`）。

## 依赖环境

路径 A 需要本机具备：

1. **Python 3.10+**
2. **Pillow + numpy**：`python -m pip install Pillow numpy`
3. **playwright（Python 版）**：`python -m pip install playwright`
4. **Google Chrome**：需本机已安装（脚本会自动探测常见安装路径；也可通过环境变量 `CHROME_PATH` 或参数 `--chrome` 指定）。

> WorkBuddy 用户通常已有托管 Python 环境，可直接使用其解释器运行脚本，无需另行安装。

验证安装（可选）：

```bash
python scripts/analyze_photo.py DEMO/source.png --out /tmp/palette.json --crop-dir /tmp/crops
python scripts/render_board.py --html DEMO/../board.html --out /tmp/test.png
```

路径 B 无需本地依赖，但需要 WorkBuddy 内置 `ImageGen` 工具（会产生 credit 消耗）。

## 使用方法

安装好后，在 WorkBuddy 里直接发一张照片并说明诉求即可触发，例如：

- “把这张照片拆成可复制的创作公式”
- “分析这张图的构图、光影、配色，反推提示词”
- “我想复刻这张照片的风格，帮我拆解”

技能会按 SKILL.md 的工作流自动完成分析、采样、排版和出图。默认是路径 A（精排）；如果想要文章原版 AI 质感，可以说“用 AI 直接生成分析图”切到路径 B。

## 示例

| 文件 | 说明 |
|---|---|
| `DEMO/source.png` | 输入原图（暖调商业人像，204×375） |
| `DEMO/视觉分析板.png` | 路径 A 生成的成品分析板（3840×2160） |

## 注意事项

- 配色 HEX 由 k-means 近似采样得到，分析板中标注为“近似”；如需精确取色请用专业取色工具复核。
- 焦距、光圈、器材、后期等无法从画面确认的信息，技能只会给出视觉推测，不会写成事实。
- 竖版图片按 contain 居中留白，标注锚点采用与图片等尺寸的 SVG viewBox 贴合定位，避免错位。
- 细节裁切建议用 `--crops` 手动指定视觉重点；自动裁切对竖图可能选到重复的背景区域。
- 本技能不含任何 API Key 或外部凭证，路径 B 的图像生成由 WorkBuddy 平台内置能力完成。

## 许可

可自由复制、修改和分享。若二次分发，请保留本说明与方法来源致谢。
