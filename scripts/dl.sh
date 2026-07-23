#!/bin/bash
# 读取 /tmp/photomap.txt，下载并裁剪每张图
IMG=/Users/dawei/CodeBuddy/aitool-picks/images
ok=0; fail=0
while IFS=$'\t' read -r fn pid theme dim; do
  tw=${dim%x*}; th=${dim#*x}
  url="https://images.unsplash.com/photo-${pid}?w=1400&q=80&auto=format&fit=crop"
  tmp="/tmp/dl_${fn}.jpg"
  code=$(curl -sL -A "Mozilla/5.0" "$url" -o "$tmp" -w "%{http_code}")
  if [ "$code" = "200" ] && [ -s "$tmp" ]; then
    python3 - "$tmp" "$IMG/$fn" "$tw" "$th" <<'PY'
import sys,io
from PIL import Image
src,outp,tw,th=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
im=Image.open(src).convert("RGB")
w,h=im.size
scale=max(tw/w,th/h)
nw,nh=int(w*scale),int(h*scale)
im=im.resize((nw,nh),Image.LANCZOS)
im=im.crop(((nw-tw)//2,(nh-th)//2,(nw-tw)//2+tw,(nh-th)//2+th))
im.save(outp,"JPEG",quality=85)
PY
    if [ -s "$IMG/$fn" ]; then
      echo "[OK] $fn <- $theme/$pid ($tw x $th)"
      ok=$((ok+1))
    else
      echo "[FAIL-crop] $fn"; fail=$((fail+1))
    fi
    rm -f "$tmp"
  else
    echo "[FAIL-dl $code] $fn ($theme/$pid)"
    fail=$((fail+1))
  fi
done < /tmp/photomap.txt
echo "完成: 成功 $ok, 失败 $fail"
