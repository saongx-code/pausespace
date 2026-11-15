# 活動快剪工具（參考用）

2026-11-15「數字酒夜」第二版用的程式。路徑是當時工作區的路徑，新專案使用前要改。

- `asr_sensevoice.py`：旁白聽寫（離線 SenseVoice 模型，從 GitHub k2-fsa/sherpa-onnx releases 的 asr-models 下載 int8 版；用 onnxruntime 執行）
- `heic2jpg.py`：iPhone HEIC 照片轉 JPG（環境沒有 HEIC 套件時用；自己拆 HEVC 圖塊再用 ffmpeg 解）
- `music_lofi.py`：lo-fi lounge 配樂＋缽聲合成（84 BPM、電鋼琴、貝斯、刷鼓；缽聲只在重點處）
- `render_quickcut.py`：9:16 1080×1920 24fps 渲染：每鏡曲線運鏡、甩鏡轉場、光痕、暖琥珀＋湖水藍調色、字幕、片頭標題、結尾 Logo

不放任何客人資料、素材或成品；這個 repo 是公開的。
