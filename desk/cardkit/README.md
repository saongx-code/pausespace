# 抓周卡文字層（v3：poem.py；舊版 ink.py 保留不用）
先讀 RULES.md。
python3 poem.py spec.json → 1080x1920 透明 PNG（深藍 #22345e）。需要 Noto Serif CJK（/usr/share/fonts/opentype/noto/，Black/Regular，第 3 個＝TC）。

# 抓周卡文字層產生器
python3 ink.py spec.json [seed] → 1080x1920 透明 PNG（深藍 #22345e）
- glyphs：每個字一筆 {ch,size,x,y,rot,ink}；font:"hand" = 手寫落款（Klee One），其餘 = Noto Serif CJK TC 復古印刷斑駁
- 主題字每個字大小要不一樣（約 110–170），輕微旋轉 ±1.5°；落款「島主項項」直寫 4 字約 46–53px
- slashes：[x1,y1,x2,y2,粗細]
- 需要 Noto Serif CJK（/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc，第 3 個＝TC）
- 產出後 push 到 desk/ → raw.githubusercontent 網址 → Canva upload-asset-from-url → update_fill 文字層
範例：example_cai.json（蔡欣妤）
