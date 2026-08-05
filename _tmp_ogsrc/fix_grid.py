#!/usr/bin/env python3
"""
棋盘格修复 - 只消除 step=2 像素级网格，不动底图/文字/颜色。
PIL composite(image1=overlay, image2=base, mask):
  mask=0 → image2(base纯底图·亮)    ← 缺遮罩的错误像素
  mask>0 → image1*α+image2*(1-α)    ← 正确复合像素

棋盘格分布：
  (even,even)=暗(有遮罩✓)  (even,odd)=亮(缺遮罩✗)
  (odd,even)=亮(缺遮罩✗)   (odd,odd)=暗(有遮罩✓)

修复：(even,odd)用左右两个(even,even)邻居平均
      (odd,even)用上下两个(even,even)邻居平均
"""
import sys
import numpy as np
from PIL import Image

def fix_grid(img_path, out_path=None):
    if out_path is None:
        out_path = img_path
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    h, w, _ = arr.shape
    fixed = arr.copy()

    for y in range(h):
        for x in range(w):
            if x % 2 == 0 and y % 2 == 0:
                continue  # (even,even) 正确，跳过
            if x % 2 == 1 and y % 2 == 1:
                continue  # (odd,odd) 正确，跳过

            neighbors = []
            if x % 2 == 1 and y % 2 == 0:
                # (odd, even): 取左右水平邻居 (even,even)
                for nx in (x - 1, x + 1):
                    if 0 <= nx < w:
                        neighbors.append(arr[y, nx])
            elif x % 2 == 0 and y % 2 == 1:
                # (even, odd): 取上下垂直邻居 (even,even)
                for ny in (y - 1, y + 1):
                    if 0 <= ny < h:
                        neighbors.append(arr[ny, x])

            if neighbors:
                fixed[y, x] = np.mean(neighbors, axis=0)

    fixed = np.clip(fixed, 0, 255).astype(np.uint8)
    Image.fromarray(fixed).save(out_path, "JPEG", quality=92)
    return out_path

def check_grid(arr):
    c00 = arr[::2, ::2].mean()
    c01 = arr[::2, 1::2].mean()
    c10 = arr[1::2, ::2].mean()
    c11 = arr[1::2, 1::2].mean()
    return max(c00,c01,c10,c11) - min(c00,c01,c10,c11)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            fix_grid(p)
            print(f"OK {p}")
    else:
        import glob
        files = sorted(glob.glob("images/og-*.jpg"))
        fixed_count = 0
        for f in files:
            img = Image.open(f).convert("L")
            arr = np.array(img, dtype=np.float32)
            before = check_grid(arr)
            if before <= 1.0:
                continue
            print(f"  {f} grid: {before:.1f}", end="")
            fix_grid(f)
            img2 = Image.open(f).convert("L")
            arr2 = np.array(img2, dtype=np.float32)
            after = check_grid(arr2)
            status = "✅" if after < 1.0 else "🔴"
            print(f" → {after:.1f} {status}")
            fixed_count += 1
        print(f"\n共修复 {fixed_count} 张")
