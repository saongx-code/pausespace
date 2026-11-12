部署新櫃台時要一起改的排程規則：
- soul / oil100：要有 ready.txt 才處理（島主按「交給 AI 整理」）
- oil100：oils.txt = {like, ok, no}；transcript.txt 可能沒有
- oil100 抓周卡：主題字規則（只用島主說的話、轉折句→對客人說的短句≤10字、3–5 行延伸、重點字、意象、隱私）
- Canva：複製母版 → 換插畫（generate-image）＋換文字層 → 存檔（島主 2026-11-12 長期同意：只限抓周卡、存進「精油抓周作品集」）→ 匯出 PNG → 草稿 card / canva 欄位
- deskSend oil100：抓網址存進案件資料夾（cardFile）→ 開分享 → LINE 附圖

抓周卡 v2（島主 2026-11-12 定稿，對標：藍色印刷書封）
- 母版 DAHauEFjtFs【母版 v2】精油抓周卡（請勿刪除）；作品集資料夾 FAHauH645BQ
- 頁 PBMl7rpb6QnmLZvg；背景＝插畫（update_fill locator=頁 id）
- 文字層 PBMl7rpb6QnmLZvg-LBCYn2sKMx7JD2hJ（整頁透明 PNG，update_fill 後 crop_media 0,0,1080,1920）
- 署名小字 PBMl7rpb6QnmLZvg-LBKywcyznjJDF7Vh「名字　日期　·　精油抓周」20px，放在不擋插畫主體的地方
- （2026-11-13 起改用 Julialangosh403 的團隊；舊團隊的母版與作品集不再使用）

插畫規則
- 每位客人畫一張新的（作品集），圖案「從那位客人的逐字稿抓意象」，不是每次都畫鳥
- 固定風格：深藍單色印刷感、米白紙；一個清楚的主體＋幾個動態模糊的元素（速度感）；元素大小方向不規則，不要排得像軍隊
- 留一塊乾淨空白給主題字（預設畫面中段）
- generate-image 可用 MAHauNKao_w 當風格參考圖

文字層規則（desk/cardkit/ink.py，用法看 README）
- 主題字：復古印刷、墨色不均、斑駁，每個字大小不一、錯落排；1–2 條細斜線
- 「島主項項」＝手寫落款（直寫），放在主題字旁
- 字放在插畫的空白處，不能壓到鳥／主體／人物
- 產出 PNG → push 到 repo desk/ → raw.githubusercontent 網址 → upload-asset-from-url → update_fill 文字層
