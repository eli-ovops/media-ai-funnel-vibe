# AI认知漏斗｜150秒内部视觉母版

本目录是 `ai-funnel-vibe-20261020` 的唯一04制作交付目录。状态以 `delivery.json` 为准。完整视频交内部审阅，不代表指定配乐、连续声画、05独立验收或用户终审完成。

## 交付入口

- `output/ai-funnel-v1-internal-150s.mp4`：完整150秒视频＋本地代码SFX；没有旁白/TTS/人声，也没有猜测的Nico替代曲。
- `output/covers/`：四比例、ASCII名、纯代码无人像封面候选；尺寸1080×1440、1080×1920、1920×1080、1440×1080。
- `content-package.json`、`screen-copy-review.srt`：02冻结输入的原样副本。SRT供审阅/无障碍，不作为第二层字幕烧入。
- `src/World.ts`：完整150秒确定性画面。`src/kit.ts`：准确Fred/sy机制的本期适配。`source-map.json`记录来源、SHA、符号、调用点、适配与真实读取范围。
- `events.json`、`audio.py`、`output/code-sfx-v1.wav`：37个帧级事件、固定seed本地PCM合成、独立声音轨。
- `qc/final/export-check.json`及同目录截图：最终文件技术检查与取帧；实际审图结论另见`qc/visual-review.json`。

## 最短恢复命令

以下从本目录执行，均只处理本期工程。Node 22.16；复用已有Remotion 4.0.451依赖，`node_modules`为外置既有工程的链接。新机器按package.json安装兼容依赖；不要复制完整付费素材库或原片。

```sh
node render-canvas.cjs full
/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 audio.py
/Users/USER/.local/bin/ffmpeg -nostdin -i output/canvas-full-visual.mp4 -i output/code-sfx-v1.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -t 150 -movflags +faststart output/ai-funnel-v1-internal-150s.mp4
/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 verify-export.py
```

上面命令不含覆盖既有交付的`-y`；返修请改版本文件名。重新导出后重新核SHA，不复用旧验收。`render.cjs preflight/full/stills`保留标准Remotion入口；整片实际选择同一`drawWorld`函数的Canvas直接捕获，减少全页PNG截图开销。逐帧调用0—8999，没有降帧、插帧或30fps复制。渲染器启动只监听本机回环地址的本期代码/字体，结束即关闭；不播放或外传任何媒体。

## 当前内容与验收边界

四组人数保留约数和完整定义。图形为任务/访问关系，没有人数比例、人口筛选或“5000=Agent使用者”的映射。“待办清单”是编辑性讲解对象；预期位置、刷新问句及失败回查均保留条件语义，不是实际产品测试成功。

22个知识拍由持续对象、空间纸层、分工、同源传递、条件回查和访问窗口承担。文字在各拍冻结阅读窗内固定位置与尺度；章节转场不挤占阅读窗。复杂关系段采用Fred T04b的分段/负责端关系、T05h的沿线同源传递、T20m的同载体扩容；sy17负责对数运镜，sy20负责空间投影。其余图形是本期原创，不能称原作者逐帧复刻。

指定Nico曲名/版本/音源仍缺，音乐总线留空。拿到经PMO核准的音源后只接续混音与受影响节奏；若语义时序不变，不重做整片。实际SFX峰值/响度只证明数值，不等于已听过。当前宿主的直接听音和正常速度连续视觉能力未成立，不部署旧音频模型，不用ASR或截图补写PASS。

组件默认门禁首次误判默认安装路径缺失，原始FAIL回执保留。本期`local-gates.py`与`local-library.py`只把与官方目录SHA完全一致的已授权本地源码绑定到实际路径，并复用现成TypeScript解析器；未修改验证器逻辑、共享库、账号或凭证。局部规划/源码/静帧门与正式动态声画门分别记录。

## 文件与角色

本期生成的tmp、bundle、捕获帧清单在`qc/file-inventory.json`；清理只能按精确记录执行。原片、333组件库、源码、字体许可、封面和证据不作缓存删除。完整视频没有发布，不能触发发布后视频清理。

唯一04 Owner：`01a11a6f-49ef-7653-934a-4312979fd4e7`。PMO：`01a11194-c40d-7bf0-8396-5bb5d6449444`。本岗只交待验版本，完成工具消息及回执在`qc/PMO-report-receipt.json`；发送成功不等于PMO已验收，不自行派05或改共享状态。

适用规则：CODEX-MEDIA-20261020-v1、PERMISSIONS-2026-10-14-v1、ROUTING-2026-10-13-v4、ELI-PRODUCTION-20261017-v2、ELI-REWORK-20261019-v1。目标Astra/high；本次实际model/effort/speed UNKNOWN。串行一个制作Owner，无新子agent。
