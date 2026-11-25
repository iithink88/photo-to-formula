---
name: photo-to-formula
description: Turn any reference photo into a reproducible "creative formula" — a professional 16:9 visual analysis board with annotations, composition sketch, detail crops, lighting/color analysis, six-color palette, and Chinese+English reverse-engineered generation prompts. Use when the user uploads a photo and asks to 拆解/反推/分析图片、提取创作公式、生成视觉分析板、图片逆向工程、复刻拍照风格、从照片反推提示词, or wants to understand and recreate a photo's visual recipe. Not for pure image editing (use image tools) or OCR-only text extraction.
agent_created: true
---

# Photo To Formula · 把任何照片拆成可复制的创作公式

## Overview

Analyze any uploaded reference photo and produce a single, publication-quality **16:9 visual analysis board** that reverse-engineers the photo into a reusable creative formula. Seven modules surround the original image: visual annotations, core keyword anchors, composition/camera sketch, key detail crops, lighting & color, six-color palette, and faithful Chinese + English generation prompts.

The methodology follows the "UNIVERSAL PHOTO VISUAL ANALYSIS SYSTEM V2.0" (see `references/analysis-framework.md`). Golden rule: **the reference photo decides the analysis content; the system decides information organization; editorial design decides presentation.** Never preset the subject, conclusions, or techniques.

## When to Use

Trigger on requests like:
- "把这张照片拆成创作公式 / 视觉分析板"
- "分析这张图的构图、光影、配色，反推提示词"
- "我想复刻这张照片的风格，帮我拆解"
- "图片逆向工程 / 摄影分析图 / 视觉基因解析"
- Any uploaded image where the goal is understanding/recreating its visual recipe rather than editing pixels.

## Workflow Decision Tree

Choose one of two output paths before starting:

| Path | When to use | Pros / Cons |
|------|-------------|-------------|
| **A. HTML 精排（默认推荐）** | User wants accurate Chinese text, exact HEX values, crisp lines, reproducible layout. Also the default when no preference stated. | Pixel-perfect text & data; real 16:9; needs script run. AI image gen credit cost = 0. |
| **B. AI 直出（ImageGen）** | User explicitly wants the article's AI-generated infographic aesthetic, or says "用AI直接生成分析图". | Faithful to the source article look; Chinese small text and HEX may be garbled; consumes ~5–10 credits per image. |

If uncertain, choose **Path A**. If the user asks for both, do A first, then B.

## Core Workflow (both paths)

### Step 1 · Acquire the photo

- Accept a local path, a pasted image, or a URL. If URL, download to a working directory first.
- Confirm the image is readable. Record its width/height for the `IMAGE_META` field.

### Step 2 · Deep visual analysis (before touching layout)

Read the full methodology in `references/analysis-framework.md` and analyze ONLY visible evidence. Internally determine:

1. Subject type and visual genre; main + secondary subjects and their relationship.
2. 5–8 annotation regions with exact positions (as % of image width/height) and concise observations.
3. 7–9 generation keywords, with dimensions chosen to fit THIS photo (portrait / architecture / product / landscape / animal / etc.).
4. Composition method actually present (rule of thirds, symmetry, leading lines, vanishing point, frame, negative space…) — only what applies.
5. Camera/lens/DOF: use tentative wording ("视觉上接近""推测") for anything not provable.
6. 5 distinct detail regions worth magnifying (structure, texture, reflection, light-shadow boundary, narrative detail…).
7. Lighting logic: direction, hardness, contrast, shadow, highlight, color temperature, mood — no invented equipment.
8. Reverse-engineered prompts (CN + EN) that reconstruct the observable image faithfully, adding no absent people/props/scenes.

For focal length / aperture / camera body / post-processing: **tentative wording only**. Never fabricate.

### Step 3 · Extract palette + detail crops (deterministic)

Run the bundled script with a Python 3.10+ interpreter that has Pillow + numpy installed (see README for setup):

```bash
PY="python"   # or the absolute path to your Python executable
"$PY" scripts/analyze_photo.py "<photo>" \
  --out "<workdir>/palette.json" \
  --crop-dir "<workdir>/crops" \
  --k 6
```

- If the Step 2 analysis identifies specific detail regions, pass them explicitly:
  `--crops "x1,y1,x2,y2; x1,y1,x2,y2; ..."` (5 boxes). Otherwise the script auto-selects 5 busy, non-adjacent regions.
- The JSON contains `palette` (HEX + Chinese name + share + usage hint) and `crops` (paths + center percentages).
- HEX values are k-means approximations — in the board label them "配色参考（近似）".

### Step 4A · Path A — build the HTML board

1. Copy `assets/board-template.html` into the working directory as `board.html`.
2. Copy/link the original photo into the same directory so `<img src>` resolves (or use a relative path).
3. Replace every `{{...}}` placeholder with the Step 2/3 content:
   - `{{IMAGE_META}}`, `{{DATE}}`, `{{ORIGINAL_IMG}}`
   - `{{KEYWORDS}}` — rows of `<div class="kw-row"><span class="pill">关键词</span><span>描述</span></div>`
   - `{{COMPOSITION_SVG}}` — an inline SVG sketch: light gray-white paper, fine dark-gray subject contours, pale-red guide lines. Draw only relevant guides.
   - `{{COMPOSITION_NOTES}}`, `{{CAMERA_NOTES}}`
   - `{{DETAILS}}` — 5 `<div class="detail">` blocks using crop paths
   - `{{LIGHT_TAGS}}`, `{{LIGHT_TEXT}}`
   - `{{SWATCHES}}` — 6 `<div class="swatch">` blocks from palette.json
   - `{{PROMPT_CN}}`, `{{PROMPT_EN}}`
4. For Module A annotations: add `.anchor` dots (percentage-positioned) + `.leader` lines + `.tag` cards inside `.overlay`. Match them to the real image positions; do not cover the main subject.
5. Follow `references/build-guide.md` for layout, anchor technique and the QA checklist. Compress wordy text rather than shrinking fonts.

Render to PNG:

```bash
"$PY" scripts/render_board.py --html "<workdir>/board.html" \
  --out "<workdir>/视觉分析板.png" --width 1920 --height 1080 --scale 2
```

The renderer auto-detects Chrome; override with `--chrome` or `CHROME_PATH`. Output defaults to 3840×2160 (crisp 2×).

### Step 4B · Path B — AI direct board

1. **Inform the user of ImageGen credit cost (~5–10 credits) before calling.**
2. Open `references/imagegen-prompt.md`. Fill the master prompt template with the Step 2 analysis results (concise, concrete, evidence-based).
3. Call `ImageGen` in image-to-image mode: `image1` = absolute photo path, `prompt` = filled template, `input_fidelity` = `high`, `size` = `1536x1024`, `quality` = `high`, `output_dir` = user's chosen folder.
4. Accept the generated image as the board. Note in the reply that small Chinese text / HEX may be imprecise; offer Path A if accuracy matters.

### Step 5 · Quality check

Before delivering, verify against Section 7 of `references/analysis-framework.md`:
- Original photo preserved faithfully; modules match real content; no fabricated camera parameters.
- Leader lines and anchors hit correct positions; sketch corresponds to the image; crops come from the photo; palette reflects real colors.
- CN/EN prompts are faithful and text is readable (no clipping/overflow). For Path A, re-render after fixing any layout issue.

### Step 6 · Deliver

- Present the final PNG with `present_files`.
- Keep the reply short: state what the board contains (7 modules) and any notable visual finding. Do NOT dump a long text report unless the user also asks to save prompts as a separate `.md`.

## Resources

| File | Purpose |
|------|---------|
| `references/analysis-framework.md` | Full V2.0 methodology — read before any analysis. |
| `references/imagegen-prompt.md` | Master ImageGen prompt templates (EN + CN) for Path B. |
| `references/build-guide.md` | HTML grid spec, per-module fill rules, anchor technique, QA checklist for Path A. |
| `scripts/analyze_photo.py` | Extract 6-color palette + 5 detail crops → JSON. Pillow+numpy only. |
| `scripts/render_board.py` | Screenshot HTML board to 16:9 PNG via Playwright + Chrome. |
| `assets/board-template.html` | Ready-to-fill 1920×1080 HTML scaffold with all 7 modules and `{{...}}` placeholders. |

## Environment Requirements

- Python 3.10+ with `Pillow` and `numpy` (for `analyze_photo.py`).
- `playwright` Python package + a locally installed Google Chrome (for `render_board.py`). Chrome is auto-detected; override with `--chrome` or `CHROME_PATH`.
- Path B additionally requires WorkBuddy's built-in `ImageGen` tool (consumes credits).
- Install location: user-level skill dir `~/.workbuddy/skills/photo-to-formula/`. See README.md for step-by-step installation on Windows / macOS / Linux.
