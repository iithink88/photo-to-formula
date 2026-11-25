#!/usr/bin/env python3
"""Extract a faithful six-color palette and candidate detail crops from a photo.

Usage:
    python analyze_photo.py <image> --out palette.json --crop-dir crops \
        [--k 6] [--crops "x1,y1,x2,y2; x1,y1,x2,y2"] [--max-pixels 60000]

Outputs a JSON with image dimensions, dominant colors (HEX + Chinese name +
share + usage hint) and detail crop file paths / center percentages.

No third-party dependency beyond Pillow + numpy. Works with the managed venv:
    C:/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/python.exe
"""
from __future__ import annotations

import argparse
import colorsys
import json
import os
import sys

import numpy as np
from PIL import Image

BASIC_HUES = [
    (15, "红"), (45, "橙"), (70, "黄"), (160, "绿"),
    (200, "青"), (250, "蓝"), (290, "紫"), (330, "品红"), (360, "红"),
]


def hue_name(h: float, s: float, v: float) -> str:
    """Map HSV to a concise Chinese color name."""
    if v < 0.16:
        return "近黑"
    if v > 0.95 and s < 0.08:
        return "近白"
    if s < 0.12:
        return "浅灰" if v > 0.6 else ("中灰" if v > 0.32 else "深灰")
    deg = h * 360
    base = "灰"
    for upper, name in BASIC_HUES:
        if deg < upper:
            base = name
            break
    prefix = ""
    if v < 0.35:
        prefix = "深"
    elif v > 0.8 and s < 0.55:
        prefix = "浅"
    elif s < 0.3:
        prefix = "灰调"
    return prefix + base if prefix else base


def usage_hint(rank: int, share: float, name: str) -> str:
    """Give each swatch a short visual-usage note."""
    if rank == 0:
        return "画面主色 / 背景基调"
    if rank == 1:
        return "主要辅助色"
    if rank == 2:
        return "主体或大面积色块"
    if share < 0.06:
        return "强调色 / 局部点缀"
    if "近白" in name or "浅" in name:
        return "高光或明亮区域"
    if "深" in name or "近黑" in name:
        return "阴影或暗部层次"
    return "过渡色 / 环境色"


def kmeans_colors(pixels: np.ndarray, k: int, iters: int = 24, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = len(pixels)
    k = min(k, n)
    centers = pixels[rng.choice(n, k, replace=False)].astype(np.float64)
    for _ in range(iters):
        dist = ((pixels[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = dist.argmin(axis=1)
        new = centers.copy()
        for i in range(k):
            mask = labels == i
            if mask.any():
                new[i] = pixels[mask].mean(axis=0)
        if np.allclose(new, centers, atol=0.5):
            centers = new
            break
        centers = new
    dist = ((pixels[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    labels = dist.argmin(axis=1)
    counts = np.bincount(labels, minlength=k).astype(np.float64)
    return centers, counts


def extract_palette(img: Image.Image, k: int, max_pixels: int) -> list:
    rgb = img.convert("RGB")
    arr = np.asarray(rgb, dtype=np.float64)
    h, w = arr.shape[:2]
    if h * w > max_pixels:
        flat = arr.reshape(-1, 3)
        idx = np.random.default_rng(7).choice(len(flat), max_pixels, replace=False)
        sample = flat[idx]
    else:
        sample = arr.reshape(-1, 3)
    centers, counts = kmeans_colors(sample, k)
    order = np.argsort(-counts)
    total = counts.sum()
    palette = []
    for rank, i in enumerate(order):
        r, g, b = (int(round(float(x))) for x in np.clip(centers[i], 0, 255))
        hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        palette.append({
            "hex": f"#{r:02X}{g:02X}{b:02X}",
            "rgb": [r, g, b],
            "name": hue_name(hh, ss, vv),
            "share": round(float(counts[i] / total), 4),
            "usage": usage_hint(rank, float(counts[i] / total), hue_name(hh, ss, vv)),
        })
    return palette


def auto_crop_boxes(img: Image.Image, count: int = 5, grid: int = 4) -> list:
    """Pick visually busy, non-adjacent cells as detail crop candidates."""
    gray = np.asarray(img.convert("L"), dtype=np.float64)
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    edge = gx + gy
    h, w = gray.shape
    cells = []
    for row in range(grid):
        for col in range(grid):
            y1, y2 = row * h // grid, (row + 1) * h // grid
            x1, x2 = col * w // grid, (col + 1) * w // grid
            e = float(edge[y1:y2, x1:x2].mean())
            cells.append((e, row, col, x1, y1, x2, y2))
    cells.sort(key=lambda c: -c[0])
    chosen = []
    for cell in cells:
        _, row, col, x1, y1, x2, y2 = cell
        if any(max(abs(row - r), abs(col - c)) < 2 for _, r, c, *_ in chosen):
            continue
        chosen.append(cell)
        if len(chosen) == count:
            break
    # fill up if grid constraints left us short
    for cell in cells:
        if len(chosen) >= count:
            break
        if cell not in chosen:
            chosen.append(cell)
    boxes = []
    for _, row, col, x1, y1, x2, y2 in chosen[:count]:
        boxes.append((x1, y1, x2, y2))
    return boxes


def parse_crops(text: str | None) -> list:
    if not text:
        return []
    boxes = []
    for part in text.split(";"):
        part = part.strip()
        if not part:
            continue
        nums = [float(x.strip()) for x in part.split(",")]
        if len(nums) != 4:
            raise ValueError(f"Invalid crop box: {part}")
        boxes.append(tuple(int(round(n)) for n in nums))
    return boxes


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract palette + detail crops from a photo")
    ap.add_argument("image", help="path to reference photo")
    ap.add_argument("--out", required=True, help="output JSON path")
    ap.add_argument("--crop-dir", default=None, help="directory to write detail crops")
    ap.add_argument("--k", type=int, default=6, help="number of palette colors")
    ap.add_argument("--crops", default=None, help="semicolon-separated x1,y1,x2,y2 boxes")
    ap.add_argument("--max-pixels", type=int, default=60000)
    args = ap.parse_args()

    if not os.path.isfile(args.image):
        print(f"ERROR: image not found: {args.image}", file=sys.stderr)
        return 2

    img = Image.open(args.image)
    img.load()
    w, h = img.size
    palette = extract_palette(img, args.k, args.max_pixels)
    boxes = parse_crops(args.crops) or auto_crop_boxes(img, count=5)

    crops = []
    crop_dir = args.crop_dir
    if crop_dir:
        os.makedirs(crop_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(args.image))[1] or ".png"
    for i, (x1, y1, x2, y2) in enumerate(boxes, start=1):
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2 or w), min(h, y2 or h)
        if x2 <= x1 or y2 <= y1:
            continue
        entry = {
            "index": i,
            "box": [x1, y1, x2, y2],
            "center_pct": [round((x1 + x2) / 2 / w * 100, 1),
                           round((y1 + y2) / 2 / h * 100, 1)],
        }
        if crop_dir:
            path = os.path.join(crop_dir, f"detail_{i}{base}")
            img.crop((x1, y1, x2, y2)).save(path, quality=92)
            entry["path"] = os.path.abspath(path)
        crops.append(entry)

    result = {
        "source": os.path.abspath(args.image),
        "width": w,
        "height": h,
        "aspect_ratio": round(w / h, 4),
        "palette": palette,
        "crops": crops,
        "note": "HEX values are k-means approximations; label as approximate in the board.",
    }
    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({"ok": True, "out": os.path.abspath(args.out),
                      "palette": [p["hex"] for p in palette],
                      "crops": len(crops)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
