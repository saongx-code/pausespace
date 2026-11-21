# 抓周卡 v4（島主 2026-11-21 定稿；範例：desk/cardkit/ref_v4_full.jpg「孤狼」卡）
**以 v4 為準**。下面 v3 的 Canva 母版、文字層流程照用，但「畫風」和「文字樣式」改成 v4：

## v4 畫風（插畫）
- **單色印刷**（島主 11/21 確認）：整張只用一個墨色（灰藍 #1f2b45），像孔版印刷／絹印印在米白紙上：墨色有深淺、顆粒與網點、邊緣微微暈開、偶爾輕微錯版，沒有第二種顏色。霧氣、動態模糊也都是同一個墨色的深淺表現。不是銅版畫、不是細線素描、不是彩色水彩。大量留白。
- **只有主體是清楚的**：主角（人／動物／物件）放在畫面中央偏上，線條清楚、有質感。
- **四周是強烈的動態模糊**：和故事有關的元素（人群、車流、浪、風、鳥群…只要是故事裡有的）從主體兩側高速掠過，像長曝光的拖影，越靠近畫面邊緣越模糊，可以一路延伸到畫面下方、壓在文字區的兩側邊緣。
- **遠景淡淡的**：城市、海平線、山…在霧裡只剩輪廓，往中央消失點收過去，製造縱深。
- 畫面上沒有任何文字。上方約 55% 是主要畫面，往下自然淡進米白紙。
- 不要：亮鈷藍色、整齊排排站（像軍隊）、細到像版畫的線條、每個角落都畫滿。
- Canva 產圖的風格參考：先用 upload-asset-from-url 上傳 https://raw.githubusercontent.com/saongx-code/pausespace/main/desk/cardkit/ref_v4_art.jpg（只取畫面、沒有字），拿到 media id 放進 imageReferences；舊的 MAHauCcplIM 不要再用。
- 提示詞範本（英文給產圖工具）：「single-color risograph / screen print on cream paper, one muted indigo-gray ink only, visible print grain and halftone texture, slightly soft ink edges, misty atmosphere, [主體] in sharp focus at center, surrounded by strong motion blur streaks of [故事裡的元素] rushing past on both sides, long-exposure ghost trails, faded [遠景] in fog converging to a vanishing point, lots of negative space, bottom 45% fades into plain cream paper, no text」

## v4 文字（poem.py 已改好，照 spec 寫就會是這個樣子）
- 關鍵字：粗宋體、輕微斑駁；細字：黑體（不是宋體）。
- 整塊詩句比 v3 高一點，主題字更大（七個字約占畫面寬度七成）。
- 墨色灰藍 #1f2b45，不是亮藍。
- 落款：島主的親筆簽名＋「｜精油抓周」。

---

# （舊版紀錄）抓周卡 v3（島主 2026-11-13 定稿）
同一種風格、版面、顏色；內容（插畫意象、詩句、主題字）每位客人都依精油抓周的逐字稿重新設計。

## Canva（Julialangosh403 的團隊）
- 母版 DAHauC7UhDg【母版 v3】精油抓周卡（請勿刪除）；作品集資料夾 FAHauH645BQ
- 頁 PBMl7rpb6QnmLZvg：背景＝插畫（update_fill locator＝頁 id）
- 文字層 PBMl7rpb6QnmLZvg-LBCYn2sKMx7JD2hJ（整頁透明 PNG；update_fill 後 crop_media 0,0,1080,1920）
- 卡片上沒有客人名字；落款固定「島主項項｜精油抓周」（在文字層裡）
- 插畫風格參考：改用 v4（見最上面），MAHauCcplIM 停用

## 版面
- 上方約六成：插畫（畫風以上面 v4 為準）。深藍單色印刷感、米白紙；一個清楚的主體（通常是一個人或一個物件，站在畫面中上方，腳要高於畫面 58% 的位置）＋各式各樣、大小方向不規則、有的清楚有的動態模糊的元素（速度感，不要排得像軍隊）。往下慢慢淡進米白紙。不要任何文字。
- 下方約四成：文字層（poem.py 自動排）
  - 詩句 3–5 行：從島主在逐字稿裡真的說過的話延伸；每行 1 個粗斑駁關鍵字（"b"）＋細字（"r"），也可以整行細字。關鍵字通常是主題字裡的詞（重複出現有節奏感）
  - 第一行後、最後一行後各一條淡虛線（自動）
  - 主題字：對客人說的短句，10 字以內，大號粗斑駁（自動置中）
  - 落款：島主項項｜精油抓周（自動）。desk/cardkit/signature.png 存在時，「島主項項」用島主的親筆簽名圖；沒有才用手寫字型。簽名照片用 python3 desk/cardkit/sig.py 照片.jpg 轉成 signature.png
- 插畫若讓人物腳太低，壓到第一行字：crop_media 頁背景往上移，再看縮圖確認

## 插畫主體：讓每位客人都有代入感（2026-11-19 島主定）
不要每張都畫女生。主體依下面的順序決定：
1. **先看案件資料夾裡的 人物.txt，再看 ready.txt 的「人物：」**（人物.txt 優先；兩者都是島主指定的）
   - 男生 → 主體畫一位男性（短髮或光頭、寬肩、中性長袍或襯衫；提示詞寫 a young man / male figure）
   - 女生 → 主體畫一位女性（提示詞寫 a young woman / female figure）
   - 不畫人 → 主體改成逐字稿裡的意象（一扇門、一艘小船、一棵樹、一隻鹿、一盞燈、一把鑰匙…），畫面裡不要出現人
   - AI（或沒寫）→ 照第 2、3 點自己判斷
2. **意象優先**：逐字稿裡有清楚的畫面或比喻（例：「像在海上漂」、「卡在門口」），就用那個物件或動物當主體，不畫人，人人都能代入。
3. **一定要畫人時**：從逐字稿的稱呼（先生、哥、姐、小姐）、名字和對話判斷性別；判斷不出來就畫**中性人物**：背影或剪影、光頭無五官、長袍，看不出男女（提示詞寫 androgynous figure seen from behind, no visible gender）。
4. 提示詞裡一定要寫清楚性別或「no human figure」，不要讓產圖工具自己預設成女生。
5. 留檔版（keep）寫一句：主體是什麼、為什麼這樣選。

## 畫面上每一樣東西都要跟客人的故事有關（2026-11-19 島主定）
- 主體以外的元素（背景、遠景、動態模糊的東西）也一定要來自這位客人的故事；故事裡沒有的東西不要畫，寧可留白。
- 例：佳鑫的故事是「孤狼」：習慣在旁邊觀察、需要時才衝進人群。畫一個人和一隻狼眺望遠方很好；但後面加一群鳥沒有意義。要表達就畫繁華城市、人群，人群之中一個人獨自站著。
- 動態模糊的「速度感」只用在和故事有關的元素上（例：流動的人群），不要為了填滿畫面亂加。
- 交卡前自己檢查：畫面上每一個元素都說得出「它代表故事的哪一段」，說不出來就重畫。留檔版（keep）逐一寫出每個元素代表什麼。
- 案件資料夾裡如果有 島主指示.txt，照它做（優先於一切）。

## 文字層產生
python3 poem.py spec.json → 1080×1920 透明 PNG
spec 範例：example_v3.json
{"out":"x.png","title":"你值得自由","seed":7,"lines":[[["自由","b"],["不用一直飛","r"]],[["自由","b"],["不用飛很遠","r"]],[["自由是你真的","r"]],[["聽見自己","b"],["心裡","r"]],[["想去的地方","r"]]]}
產出 → push 到 repo desk/cards/案件資料夾ID.png → raw.githubusercontent 網址 → Canva upload-asset-from-url → 上傳成功立刻從 repo 刪掉再 push
