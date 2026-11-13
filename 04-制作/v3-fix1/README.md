# v3-fix1：去除固定角标

仅删除「Karpathy 粗估」「Karpathy 观点」「各项独立比较 · 非四块相加」。保留“约”、数值、比例标尺、整体与细节参照及放大说明，不添加替代文字。原 v3 保留。

完整片：`output/ai-funnel-v3-fix1-review-150s.mp4`，150 秒，1080×1920，原生 60fps / 9000 帧。SHA256 见 `output/SHA256SUMS.txt`。

## 实现与证据

`src/World.ts` 删除对应绘字，导出既有背景函数。`qc/source-diff.txt` 保存差异。逐帧证明 y=150..239 与 y=1750..1839 两区域始终只有原代码背景后，使用相同画布坐标的渐变与确定性噪点合成；不是纯色填充、模糊或裁切。视频重新编码，不能声称压缩视频字节未变。

- 源代码 9000 帧背景精确比较通过：`qc/static-background-proof.json`。
- 实际导出 9000 帧区域检查通过，最大亮度差 4/255：`qc/export-background-check.json`。
- 区域外全片 SSIM 0.999733：`qc/outside-ssim.txt`。黑遮罩仅用于比较，不存在于交付片。
- 音轨直接复制，包哈希完全一致，34 处 SFX 保留：`qc/audio-check.json`。
- 19 张实际导出采样均已查看，另看 65s、75s、最后一帧原尺寸：`qc/visual-review.json` 与 `qc/frame-index.json`。
- 内容、数据、kit、字幕、脚本和音效事件文件与 v3 哈希一致：`qc/preserved-inputs.json`。

完整正常速度连续观看、直接审听未完成；独立 05、PMO 验收与用户终审仍待进行。上述检查仅为本次三处角标返修，不替代全片声画验收，也不重复声明组件库新验收。

## 复现

依赖链接复用既有本地运行库及字体。`node verify-background.cjs` 验证代码背景；随后 `python3 compose.py` 合成；验证使用项目 package.json 指定的带 NumPy/Pillow Python 执行 `validate.py`。已完成的输出和采样存在时，脚本的 `-n` 会拒绝覆盖，复现须在另行授权的新目录调整路径，勿覆盖本交付。`render-stills.cjs` 为保留的历史辅助脚本，不是本次复现入口。

首两次背景比较未通过及稳定 CPU canvas 读取修正记录保留于 `qc/background-check-diagnosis.json`；最终精确比较通过后才合成。无新付费、云端上传、发布或删除。完整证据与文件索引见 `delivery.json`、`file-inventory.json`。
