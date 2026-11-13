# AI 认知漏斗｜五项集中返修 v4-repair1

本目录承接 `04-v4整片五项集中返修.md`。唯一04制作Owner；冻结基底为 `../v4-complete/output/ai-funnel-v4-complete-150s-r5.mp4`，SHA256 `6ac2862d8b34a813ff471ff13d14a572bb77f35e0c5df78e1267bcaab343cbd0`。

完整候选输出：`output/ai-funnel-v4-repair1-150s-r1.mp4`。交付规格、最终SHA与检查状态以 `delivery-index.json` / `qc/verification.json` 为准。候选不等于05、PMO或用户终审通过。

本批只处理Q1—Q5。0—84秒画面从冻结r5继承，未重渲；后66秒按同一60fps时钟重编排并渲染。最终统一编码，因此不宣称保护段编码字节相同。源码中Intro/Population/Task/Roles文本完全相同，kit与原组件源码快照保留，核验见 `qc/source-protection.json`。

- `src/FullEpisode.tsx`：完整150秒入口。
- `src/RepairScenes.tsx`：事项状态、数学/编程、访问树与唯一结尾载体。
- `src/components/T03e-StepChain.tsx`：本期增加紧凑导航参数；S形拓扑保留。
- `Manifest.json` / `source-map.json`：准确源码及本期适配。
- `time-map.json`：旧→新语义与时码映射，非匀速拉伸。数学段125—132秒，访问树132—141秒。
- `screen-text-index.json` / `screen-script.txt`：22段语义及画面文字。具体事项为教学图形“01｜整理客户需求”，没有真实App实测或产品成功回执。
- `covers-index.json`：沿用既有四比例候选，不代表用户已认可。
- `qc/repair-review.md` / `qc/repair-evidence.json`：五项逐项前后原尺寸证据与读取边界。

重现使用既有本地Remotion依赖与授权字体，`runtime.json`记录真实位置；`node_modules`和`public`为现有资源的符号链接，本目录不是脱离本机即可运行的独立安装包。

从本目录运行 `node render.cjs patch r1` 生成84—150秒区间，再 `python3 assemble.py` 接入冻结r5前84秒，最后 `python3 verify.py`。这些命令不覆盖既有输出；已经完成时不要原样重跑，应先为新轮次改标签及对应装配输入/输出。需要从源码完整重渲时可用 `node render.cjs full <新标签>`。

没有音轨、无人像/配音、无烧入音乐；用户自行挂平台音乐。正常速度连续视觉与手机计时阅读未完成，不用解码或采样数量替代。05只需按本轮变化与必要接缝复核，PMO与用户终审另行记录。

新增文件用途：`src/`、`source/`、索引/脚本为工程及复现；`output/`为完整候选与必要补丁；`qc/`为原尺寸证据、缩略联系表、核验与发送回执；`planning/`为关键帧配置；`inputs/`为基底定位；`tmp/bundle-*`为本次渲染生成的本地bundle，仍保留供恢复与复现。未删除原件或本轮资产，未上传/发布，未修改共享状态。
