# AI 直出版 · ImageGen 提示词模板

用于「AI 直出」路径：把参考照片作为输入图，让图像生成模型直接产出 16:9 视觉分析板。
适合想要文章原版那种"AI 生成质感"的分析板；精确文字/HEX 以 HTML 精排路径为准。

## 调用参数

- 工具：`ImageGen`（image-to-image 模式）
- `image1`：参考照片的本地绝对路径（必填）
- `prompt`：下方模板填入分析结果后的完整提示词
- `input_fidelity`：`high`（尽量贴近原图，避免模型改掉主体）
- `size`：`1536x1024`（ImageGen 最接近 16:9 的横向尺寸）
- `quality`：`high`
- `output_dir`：用户指定的输出目录（默认工作区 generated-images）

> 注意：ImageGen 对中文小字与精确 HEX 值的渲染不可靠。若用户要求文字/色值精确可读，改走 HTML 精排路径。

## 主提示词模板（英文，推荐）

```
Create a single, complete, high-end 16:9 horizontal photographic visual-research analysis board based on the input reference photo. Preserve the original photo faithfully and make it the visual center; arrange all analytical modules around it.

Overall design language: deep ink-green and charcoal-black background, low-saturation sage-green category tags, white and light-gray professional typography, ultra-thin white leader lines with small circular anchor dots, semi-transparent dark info cards, fine module dividers, clear visual hierarchy and grid system, generous white space, asymmetric modular layout, rigorous / refined / restrained / professional editorial quality.

The board must contain these 7 modules:

A. ORIGINAL IMAGE + ANNOTATIONS — top-left, largest area. Show the full original photo with its original aspect ratio, subject placement, crop, environment, lighting and color untouched. Add 5–8 fine white leader lines with small circular anchors pointing to the most meaningful visual regions, each with a concise Chinese title + one-line visual observation. Do not cover the main subject.

B. CORE KEYWORD ANCHORS — top-right. Vertical list of 7–9 green capsule keyword tags, each with a short professional description. Dimensions must be derived from the actual photo (e.g. for portraits: facial features, pose, wardrobe, expression, lens and light; for architecture: structure, geometry, perspective, facade material, spatial proportion, natural light; for products: form, material, surface reflection, lighting, background, commercial style; for landscapes: terrain, natural elements, spatial depth, sky, weather, color, ambient light). Never invent non-existent visual info.

C. COMPOSITION & CAMERA ANALYSIS — right-middle, titled "构图与机位分析". Draw a faithful composition line sketch: light gray-white paper background, fine dark-gray drawing lines, pale-red photographic guide lines. Show subject contours, proportions, perspective, foreground/midground/background, visual weight and leading lines. Use only the guide methods actually relevant to this photo (rule of thirds, center axis, symmetry, diagonal, leading lines, vanishing point, frame, curve, negative space). Beside it add two text blocks: "构图要点" (spatial layout and visual organization) and "机位与镜头" (angle, subject distance, lens perspective, framing, depth of field, focus). Do not fabricate camera parameters.

D. KEY DETAIL REFERENCES — bottom horizontal strip, titled "关键细节参考". Show ~5 compact thumbnails cropped from the actual photo, each with a short Chinese title and one-line visual explanation. Choose diverse, analytically valuable regions (structure, action, texture, material, reflections, light-shadow boundaries, background, environmental elements, color relations, narrative detail). Never repeat similar content and never invent details absent from the photo.

E. LIGHTING & COLOR — titled "光影与色彩特征". Short sage-green labels with professional notes on light direction, hardness, contrast, shadow character, highlights, color temperature, environmental reflection and mood. Adapt dimensions to the actual scene (natural light, special weather, artificial light, neon, backlight, hard flash). Never name specific灯具 or equipment that cannot be verified.

F. SIX-COLOR PALETTE — titled "配色参考（近似）". Six vertical swatches in a row from the photo's real dominant colors, each with HEX value + Chinese color name + short usage note. Mark HEX as approximate if not precisely sampled. For monochrome photos do not add artificial vivid colors.

G. FULL REVERSE ENGINEERING PROMPT — bottom-right, titled "完整反推提示词（可直接用于图像生成）". Write two faithful reconstruction prompts: one Chinese paragraph and one English paragraph, covering subject, appearance, action/state, relationships, environment, spatial layout, composition, camera, perspective, lighting, color, texture, photographic quality and mood. Do not add characters, props, scenes or plots that do not exist in the original. Avoid abstract praise; maximize observable visual fidelity.

Rules: analyze only visible visual evidence; use tentative wording for focal length / aperture / equipment / post-processing; no fixed photography-theory labels or empty compliments; all annotations, sketch, crops, palette and prompts must correspond to the real input photo. Prioritize fidelity, accuracy and readability. Output ONLY the finished 16:9 analysis board image, no separate text report, no extra canvases.
```

## 中文简版（当用户要求中文提示词时）

```
基于输入照片生成一张完整、专业的 16:9 横向摄影视觉研究分析板。忠实保留原图并作为视觉中心，七大模块环绕排布：
A 左上原图主体+5-8处细白引线圆形锚点中文标注（简洁标题+核心视觉观察，不遮挡主体，不修改原图）；
B 右上「核心关键词锚点」7-9个绿色胶囊标签+简短描述，维度由照片真实内容决定，不得编造；
C 右中「构图与机位分析」忠于原图的线稿（浅灰白纸张、深灰线条、淡红辅助线），只画相关的构图辅助方法，配「构图要点」「机位与镜头」两段文字，不得杜撰相机参数；
D 下方「关键细节参考」约5张来自原图的局部缩略图+中文标题+一句解释，避免重复与凭空创造；
E「光影与色彩特征」绿色标签+专业说明，自适应自然光/人工光/逆光/霓虹等场景，不虚构灯具；
F「配色参考（近似）」6张取自原图真实主色的纵向色卡，含HEX（近似需标注）、中文色名与用途，黑白照不要硬凑鲜艳色；
G 右下「完整反推提示词（可直接用于图像生成）」中文+英文两段忠实复刻原图的可重建提示词，不添加原图不存在的人物/道具/场景/剧情。
整体风格：深墨绿与炭黑背景、低饱和鼠尾草绿标签、白/浅灰专业排版、极细白引线、半透明深色卡片、精细分隔线、清晰网格与留白、非对称模块化、严谨精致克制专业。
只依据可见视觉证据分析，器材/焦距/光圈等用推测性措辞，禁止套用固定理论或空洞赞美。只输出这一张成品分析板，不输出文字报告。
```
