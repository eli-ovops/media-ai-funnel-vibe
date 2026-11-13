# AI认知漏斗｜v4 完整150秒候选

唯一04沿PMO完整制作续接单完成本地制作。本目录的 `r5` 为完整候选；不代表05、PMO或用户终审通过，不发布。

成片：`output/ai-funnel-v4-complete-150s-r5.mp4`。1080×1920、60fps、9000帧、150秒。**静音**，没有旁白、人声、TTS、SFX或BGM音轨；用户自行挂平台音乐，没有声称对齐未知音乐。

实际文件哈希、大小、媒体参数和完整解码结果，以 `qc/verification.json` 为准。该文件需在渲染完成后生成；不能仅凭本说明认定导出成功。

## 完整工程与入口

- `src/index.tsx` → `src/FullEpisode.tsx`：本期完整时间线；`src/Magnified.tsx`：已认可的真实区间放大机制。
- `src/components/`：7个实际使用的完整TSX模块适配件；`src/kit/`：准确Fred kit及本地字体/竖屏/静音适配。
- `source/`：原始模块与kit快照，保留来源；`source-map.json`：实际调用、源文件与本期文件SHA、改动和旧问题帧的重映射。
- `Manifest.json`：当前版本、组件匹配与采样关键帧范围。`src/Episode.tsx`仅为复制保留的36秒基线，不是当前入口。
- `screen-text-index.json`、`screen-script.txt`：22/22拍语义与实际画面文字时间窗；具体首字出现以源码cue和导出帧为准，不冒充OCR逐字时间戳。
- `chart-data.json`、`content-package.json`、`inputs/`：当前数据及可恢复输入。人数/比例来自原作者近似估计，未独立普查；四组独立总体参照，不强拼100%。
- `covers-index.json`：已有v2四比例封面候选原件和SHA，未获本条用户认可，本次没有重生成。
- `runtime.json`：已存在依赖、字体实体、版本及SHA。node_modules/public为有效本地符号链接，不是便携离线依赖包。

在本目录重渲：`node render.cjs full r6`。tag须用新名称，脚本拒绝覆盖已有输出。`node render.cjs stills <新tag>` 按planning/keyframes.json输出关键帧；`previews`输出本期九个短动态窗口。不需要安装依赖。

## 核验范围

已读新增4个准确调用卡、完整源码、对应所有源预览时间网格；检查82张首轮关键帧、24张修订关键帧，以及九段本期短动态的74张实际导出采样。发现的步骤窗口白底重置、标题遮盖、汇合文字叠压、开头转环残边已集中修改。上述是采样和定向检查，不是连续看听。

`qc/library-keyframes-localpaths.json`仅核准确源码SHA、实际AST调用及采样关键帧材料。它使用本地精确SHA适配器，不改共享库、不伪装源路径，不提供连续观看或整片审美结论。

完整导出复核入口：
- `qc/verification.json`、`qc/ffprobe-full.json`、`qc/decode-full.log`
- `qc/export-frame-index.json`与`qc/export-frames-r5/`（变化区间）；完整r4采样在export-frame-index-r4.json与export-frames-r4/
- `qc/full-*.jpg`：全段及接缝的时间采样联系图
- `qc/visual-review.md`：实际查看范围、发现和未覆盖层
- `qc/motion-audit.json`、`qc/motion-review.md`：运动检测提示与逐项判断

正常速度全片连续观看、手机计时阅读、05独立质检、PMO完整片验收、用户终审仍待完成，不能用渲染或解码PASS替代。完成后向PMO发送一次工具报告，发送回执单独记录，不轮询其他Owner。


r5按原60fps时钟只重渲三个叠字区间，再与r4未变内容逐帧裁切拼接并统一编码。完整组装方法、输入/输出SHA见qc/assembly-r5.json及assemble-r5.py；r4原件及修改前的FullEpisode.tsx均保留。静音、150秒、22拍不变。运动检测原始20项阻断级和8项提醒未抹去，逐项保留理由见qc/motion-review.md；133.7–140.5的长阅读停留由05重点复审。
