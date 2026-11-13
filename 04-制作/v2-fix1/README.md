# v2-fix1｜Q1/Q2定向返修交付

当前唯一完整内部版：[ai-funnel-v2-fix1-internal-150s.mp4](output/ai-funnel-v2-fix1-internal-150s.mp4)。SHA256 `758ab4d64be1aedbafdb4d1c444b34a39de79f7004581bb3f3b9a9882f282e63`。150秒，1080×1920，原生60fps，9000帧。状态：04修补及限定自检完成，待PMO审原件与05定向复核、用户终审；不标整片声画PASS。

## 本轮修改

- Q1仅40–40.5、54–54.5、68–68.5秒：同一人数先在上方收为轻量载体，沿左侧空白迁移，再在自身空行展开。运输时短暂缩至6px，稳定字号112/46px、终点与阅读时间不变；不是稳定信息缩小。已有组与说明保持显示，首组27–27.5秒未改。
- Q2仅117–117.5秒：保存块先下移到y1560，再横移，最后返回y1470；避让完成勾，未用绘制顺序掩盖穿透。117.5秒后终态与其他过程不变。
- 四段共120帧重新渲染，以完整v2基底按帧装配。其他区间来自原v2；视频重新编码，不宣称MP4或未改区间压缩像素字节相同。
- 22条文案/时间窗、SRT、kit、事件文件保持一致。34个SFX直接复制v2 AAC音轨，包流SHA完全一致，无混音/增益/重生成。原四比例封面沿用v2/output/covers，本轮不改封面。

## 实际证据

- `qc/per-frame-avoidance.json`：全部120帧，已加载实际字体的字形边界/纸面/视口与载体轮廓计算，无碰撞失败。Q2包含描边的保守矩形检查；不是连续观看证明。
- `qc/final/export-check.json`：完整解码通过；规格、时长与音频包流核验。最终导出64帧分8张联系表均已实际查看；四个原反例同钟帧F2421/F3255/F4095/F7035另按原尺寸查看。
- `qc/final/frame-index.json`：39.8–40.7、53.8–54.7、67.8–68.7、116.8–117.7秒的原片时钟/零基帧号，含紧邻拼接帧。每区间16帧；四张`compare-F*.jpg`保存原05反例与当前同钟帧对照。
- `qc/boundary-source-pixels.json`：16个边界/邻接源画布时点与首组3个对照时点，共19项与v2同字体源像素一致；不代替MP4压缩像素比对。
- `qc/protected-input-check.json`、`qc/source-diff.patch`、`qc/scope.json`、`qc/assembly.json`保存保护输入、修改与装配证据。World SHA `3d9cf1b267641364602417fcdc7665162cec1b47bf79b45c4b00d30d15507d2d`。

## 配乐与未验层

按用户最新明确决定，配乐状态为`USER_WILL_ADD_NATIVE_PLATFORM_MUSIC; NOT_REQUIRED_IN_MASTER`：用户发布时自行添加阿布学长《We Never（Vibe知识大赏）》同款平台音乐。旧任务单“缺音乐”的阻断已由本次决定解除；不等待音频、不找替代曲、不重试下载。母版保留SFX，未加入BGM；未拿到音轨，不宣称与指定歌曲精确逐拍同步。

本轮未完成正常速度连续视觉或直接SFX听音；05定向复核、PMO验收和用户终审仍待进行。上述层不补写PASS。未改范围沿用已有v2/05证据，不重验全片178帧。

## 复现与保护

运行入口是`render-canvas.cjs`（参数：mode/start秒/end秒）、`assemble.py`（逐帧9段装配）、`verify.py`（完整文件规格/解码/音轨与提帧）、`check-boundaries.cjs`（源像素边界比较）。当前版本原件全部保留。复现应在另建副本中执行，保留相邻v2基底、已有node_modules/public依赖；不要在本交付目录覆盖既有输出。依次四段命令：

```sh
node render-canvas.cjs q1a 40 40.5
node render-canvas.cjs q1b 54 54.5
node render-canvas.cjs q1c 68 68.5
node render-canvas.cjs q2 117 117.5
python3 assemble.py
python3 verify.py
node check-boundaries.cjs
```

v1/v2、05与PMO原件、组件库、共享状态均未写入。只交待验结果，不自行派05、发布、删除或启动其他任务。实际模型/effort路由不可见，记UNKNOWN。
