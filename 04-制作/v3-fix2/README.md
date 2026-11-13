# v3-fix2｜两处定向返修待验

完整片：`output/ai-funnel-v3-fix2-review-150s.mp4`。150 秒、1080×1920、原生 60fps、9000 帧。

SHA256：`17fbb4955849347a09d2364924a3809a575ce5a441b730a5cff4a8e6b67aa434`。

| 问题 | 实际修改与帧范围 | 自检结果 |
|---|---|---|
| Q1 25%标错方向 | 23≤t<27，F1380—1619；文字移到左上 (248,562)，短引线终点 (278,674) 落在灰色25%弧 | 23秒首帧、23.5、24、26.9833秒和27秒退场实际原尺寸已看，灰弧归属明确，不穿字 |
| Q2 内部路径终点裁切 | 镜头133/138秒key改为 x−280/y−90/z0.64；实际源差异F7885—8459；装配替换131.4≤t<141（F7884—8459） | 131、131.4前后、132、133、136、138、139、141前后实际原尺寸已看；H、金路径、选择器、标签可辨，边界回接无采样错位 |

原输入与旧版本保留。仅重渲240+576帧，耗时7.099+13.395秒；其他8184帧从唯一v3-fix1基底按帧取回。整流H264重新编码，非压缩视频字节不变。未修改区间SSIM 0.999811；原AAC包哈希一致，34 SFX原样复制。比例、中心人数、角标删除、必要标尺/放大解释、124/128/131三档切换和139—144退环保留。

## 已核与未核

- `qc/geometry-check.json`：源代码全9000帧比例几何未变；Q2全区间H圆、选择器圆、路径101点/帧及标签保守包围盒均在原工作视窗，未扩大裁剪区。最小目标范围y558.42，高于y540裁切线；Q1引线末端在灰弧半径范围。
- `qc/export-frame-index.json` 与 `qc/visual-review.json`：18张同版本实际导出原尺寸均已查看；另保留源渲染样本、联系表以便复核。
- `qc/ffprobe.json`、`qc/technical-check.json`、`qc/protected-ssim.log`、`qc/audio-check.json`：规格、全流解码及保护范围对比、音轨包一致。
- 正常速度连续观看、直接审听未完成；独立05、PMO验收及用户终审待进行。只交局部问题的04自检证据，不自行PASS全片或派下游。

## 工程与复现

当前修改源 `src/World.ts`；`qc/source-diff.txt` 两处源差异；`source-map.json` 保留准确组件来源，历史证据与当前变更分开；`screen-text-index.json`记录新位置。输入内容/数据/kit/字幕/脚本/事件哈希保留于 `qc/preserved-inputs.json`。

既有运行库/字体通过node_modules和public链接复用，无安装。命令按顺序：`node check-geometry.cjs`；`node render-stills.cjs`；`node render-canvas.cjs q1 23 27`；`node render-canvas.cjs q2 131.4 141`；`python3 assemble.py`；最后用现有带Pillow的Codex Python运行`validate.py`。输出存在时编码/提帧脚本拒绝覆盖。后续复现应在获授权的新目录调整输出位置，勿覆盖本交付。

`file-inventory.json`列全部当前文件及SHA/用途。临时bundle、局部MP4与采样仍用于复现/05对照，全部保留；未清理、无新增费用/云传/发布/子agent，不改共享状态/05/付费库。磁盘df为15%使用、约1.6Ti可用。实际模型、effort、speed UNKNOWN，目标Astra/medium；未重置额度。
