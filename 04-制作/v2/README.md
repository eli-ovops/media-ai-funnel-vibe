# AI认知漏斗｜04 v2 集中返修内部母版

Owner：04 `01a11a6f-49ef-7653-934a-4312979fd4e7`。本目录是 v2；父目录 v1 原件保留。依据本期 `04-v1集中返修.md` 一次处理四项，不放行05、不代表用户终审或发布。

## 交付入口

- `output/ai-funnel-v2-review-150s.mp4`：150s、9000帧、1080×1920、原生60fps；完整内部视觉母版与代码音效。实际规格/SHA以完成后的 `delivery.json`、`qc/final-review/export-check.json` 为准。
- `output/covers/`：3:4、9:16、16:9、4:3，英语文件名。沿用v1已检查的纯代码封面图，标题内容未变；逐文件新路径与相同SHA见 `qc/covers-reuse.json`。仍为候选，未倒填用户批准。
- `source-map.json`：准确Fred/sy源码、实际调用与未调用的边界。
- `qc/rework-review.json`：四项返修、具体时点、实际抽帧及未核层。

## 四项修正

1. 四组为相互独立、等权的编辑观察位；约人数按原时序出现，读完缩到左侧保留到75秒。同一任务纸进入原因段。面积不对应人口比例，没有漏下人群、精确嵌套、人口模拟或新增百分比。
2. 全片唯一任务纸/根任务坐标状态；同一三功能载体重排；单个事项保留复选框行的几何，沿步骤连续缩放传递；保存后的窗口变成条件检查窗口。取消整场叠化。图形逐对象引入/退场仍存在，不把每个新增对象强行当作同一个对象。
3. 分支原点按当前纸张实际仿射轮廓、边缘法线外移18px；线绘于纸张之前，厚度之外留间隔。访问总线y1540，窗口底y1360，间隔180px；没有横穿窗口的顶部总线或背景遮线补丁。
4. 免费版/付费版/内部系统三标签对应同一工作区的短答、任务纸、分工关系三个观察区域；用不同可见内容解释访问条件。没有性能、价格、付费必正确的补充结论，也未模拟真实内部产品UI。

## 保持及变化范围

02 v3全部22拍、文案语义、阅读时段、总时长不变。`content-package.json`、`screen-copy-review.srt`与上游SHA一致。人数主字112px；旧数字导航46px、说明44px；访问标签60px；归因44px。没有真人、原声、旁白或TTS。全片重新布局/状态连接属于本轮实际修改，不能宣称只改了两条线。

准确使用T04b的分段间隔/宽度/内圆角、T05h的三次路径、T20m的窗口展开，以及sy17的对数缩放/三次缓动。sy20透视投影在kit中保留来源但本版不调用，不冒称已用。纸面是本期自制仿射几何，不是原作逐帧复刻。

## 验收范围与剩余缺口

自检先实际导出22秒分支样段、16秒访问样段并提帧查看；没有把提帧当作连续看听。分支样段后还完成sy17相机插值与T04b分段宽度改动，以最终完整导出的抽帧为验收对象；短片旧编译体单独保留。渲染器改为编译开始前记录源码SHA，避免结束时读到较新源码。

9000帧几何检查、字体阅读窗口实际度量、源码调用检查属于技术证据。最终MP4实际抽帧与原尺寸高风险图片另核。正常速度连续视觉、直接审听仍未完成；Nico原作挂载曲目已由PMO原生音乐面板确认：《We Never（Vibe知识大赏）》/阿布学长；04已查看截图。仍缺可混音音频文件，也未核独立音源剪辑/速度一致，沿PMO收取，不另找替代曲。34个离线代码SFX只记合成/峰值/解码，不记听感PASS。整体正式声画验收不通过，05独立质检与用户终审待PMO安排。

## 本地复现

本目录 `node_modules` 与 `public` 指向既有授权依赖/字体，不安装、不修改共享库。

```sh
node render-canvas.cjs full
/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 audio.py
/Users/USER/.local/bin/ffmpeg -nostdin -i output/canvas-full-visual.mp4 -i output/code-sfx-v2.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -t 150 -movflags +faststart output/ai-funnel-v2-review-150s.mp4
/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 verify-final-review.py
```

源时钟frame/60，单Chrome顺序生成每一帧；不是30fps补帧。实际运行记录见 `qc/canvas-full-receipt.json`。不要覆盖已有完整输出；后续改版应使用新目录/版本名。

本次导出在全片基础渲染期间补正了90–103.5秒的事项几何。只重渲染5400–6209这810帧，再按精确帧范围合回9000帧；基础视频、补正短片、两个编译时源码SHA和合成命令均保留在qc，最终MP4是唯一待审版本。后续从当前源码完整重渲染可直接得到同样的对象行为。

最后自检还精确补正了82–89.5、103–103.5、139–139.5秒，共510帧；第一份完整候选及其75帧采样全部保留。当前唯一待审视频是 `output/ai-funnel-v2-review-150s.mp4`，SHA `9a3ce43284d15afa47178e7e188d8baca3d17b2aedee5c64eab45a50ec3da537`。当前视频另查看25个重点时点及其中8张原尺寸图。最后源、补正视频和装配命令见 `qc/final-transition-fixes.json`、`qc/final-assembly.json`。
