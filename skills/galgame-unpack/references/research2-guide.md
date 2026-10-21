# 第二轮联网研究：归纳与排查表

核读于 2026-10-21 至 22 日，去重新增 **122 项资料**，来自 **38 个正文域名**；其中 **93 项不在 GitHub、raw 或 GitHub Pages**。分为一手博客/论坛 34 项、引擎文档 37 项、格式与工具实现 35 项、图像媒体 16 项。加上首轮 129 项，目录累计 **251 项**。

本轮面向已有路线失败后的具体分岔。默认仍处理 CG 与立绘；背景、剧情、音频等沿用已确认范围。读脚本以确定图像关系时，不额外导出剧情。这里新增的是资料与检查方法；工具是否支持目标游戏、合成结果是否正确，要以实际样本另行证明。

## 先按故障选择正文

| 分支 | 入口 | 重点 |
|---|---|---|
| 相同游戏换版本后失效、工具会修改输入、一个提取器只有部分素材正确 | [博客与论坛一手经验](research2-community.md) | 保留作者样本版本、失败条件和实际操作副作用 |
| 素材齐全却组合错误、名称映射不全、旧手册与发行版结构冲突 | [引擎资源、状态与版本](research2-engines.md) | 声明到文件的引用、宏与状态、版本和语言覆盖 |
| 包能列目录却解码失败、隐藏配对文件、同扩展名多种结构 | [工具实现与格式结构](research2-formats.md) | 固定源码版本、内层分派、长度/偏移与依赖 |
| 图集错位、透明边缘异常、动态立绘或媒体时间不正确 | [图像、图集、渲染与音频](research2-media.md) | 裁边/旋转/别名、预乘、绘制范围、帧与样本时间 |

仅阅读命中的条目。引用工具源码时使用条目中的固定 commit；手册使用 stable/latest 时，先记录页面版本并匹配目标游戏或本机依赖版本。

## 可以执行的检查

| 观察到的情况 | 下一步与应留下的证据 | 来源 |
|---|---|---|
| 包已提取，内部文件仍打不开 | 为“包索引、条目解密/解压、图像/脚本内层”分别记状态。CMVS 导出器可能已经改过内层解密状态；MGD/PB3 等按内部类型分派。保留原始条目哈希，避免重复解密。 | [T206](research2-formats.md#t206)、[T221](research2-formats.md#t221)、[T222](research2-formats.md#t222)、[T223](research2-formats.md#t223) |
| 图像只剩表情、孔洞或透明度不对 | 建立底图、差分、遮罩的依赖清单，核对原名字和目录。RCT、WIPF、AKB+ 的依赖规则各自绑定格式；缺底图时交付局部层并报告缺项。 | [T214](research2-formats.md#t214)、[T217](research2-formats.md#t217)、[T231](research2-formats.md#t231) |
| 容器有多帧，工具只导出一张或画布变小 | 将条目/帧/图像 ID 分开清点。HG3 保存裁切前画布；PNAP 的导出路径可能跳过定位元数据；所读 DZI 实现只用第一组 tile，可能裁小画布。 | [E214](research2-engines.md#e214)、[T216](research2-formats.md#t216)、[T228](research2-formats.md#t228) |
| 两个工具输出互相矛盾 | 按素材类型分别比较完整解码、尺寸、alpha、位置和来源。成功导出一张背景不能替立绘通过；优先解释输出差异，再选工具或修复算法。 | [B217](research2-community.md#b217)、[B223](research2-community.md#b223)、[B233](research2-community.md#b233) |
| 格式名、后缀或一个魔数看起来匹配 | 同时检查索引边界、长度、头尾版本、压缩类型和伴随文件。QLIE 标志可能在末尾；NSA 用大端索引；旧 AOS DAT 需要 index.idx，与 LiLiM AOS 分别处理。 | [T224](research2-formats.md#t224)、[T233](research2-formats.md#t233)、[T234](research2-formats.md#t234)、[T235](research2-formats.md#t235) |
| 文件能解密但截断、分块错乱或脚本乱码 | 对每个分段验证解密后的长度、解压后长度和拼接顺序；分别验证文件名解码与资源正文。NPK2 的分段处理、YPF/YBN 的两层处理分别留日志。 | [T208](research2-formats.md#t208)、[T218](research2-formats.md#t218)、[T230](research2-formats.md#t230) |
| 有全套图片却无法确定人物组合 | 沿声明、宏调用、参数、显示/隐藏和分支维护资源状态，只保存有证据的组合；遇未知表达式留下未求值项。CatSystem2 差分位数、Monogatari layer 状态和 KAG/Tyrano 宏各自按文档处理。 | [E210](research2-engines.md#e210)、[E212](research2-engines.md#e212)、[E215](research2-engines.md#e215)、[E222](research2-engines.md#e222) |
| 图库数量与提取图片数量对不上 | 区分实际图、未解锁占位图、缩略图和脚本入口；将逻辑 CG 项映射到实际资源及差分。图库和回想可能有独立初始化，也可能混用背景图。 | [E218](research2-engines.md#e218)、[E220](research2-engines.md#e220)、[E235](research2-engines.md#e235) |
| Unity 或其他引擎目录缺资源名 | 检查资源 provider、额外 catalog、语言目录、hash 和依赖；address/GUID/label 可以被构建选项省略。区分缺依赖、未找到逻辑映射和解码失败。 | [E204](research2-engines.md#e204)、[E236](research2-engines.md#e236)、[M203](research2-media.md#m203)、[M208](research2-media.md#m208) |
| 图集裁切后位置或尺寸不对 | 保存 frame、原始尺寸、trim、旋转方向、resolution、别名和多页引用；先恢复纹理，再应用场景坐标。padding/extrude 不计入人物本体。 | [M204](research2-media.md#m204)、[M214](research2-media.md#m214)、[M215](research2-media.md#m215) |
| 透明边缘变黑、单通道图像意义不明 | 明确直通/预乘 alpha、位深、颜色空间和通道 swizzle。WebP 的视觉无损与透明区 RGB 保真分开验收；保留原始文件以便回退。 | [M202](research2-media.md#m202)、[M205](research2-media.md#m205)、[M207](research2-media.md#m207) |
| Photoshop PSD/PSB 或 E-mote/Spine 合成不符 | 分别核对层序、遮罩、裁剪区间、混合模式、模型变形和时间。PSD 合并预览与重新渲染分别保存；Spine end slot 的裁剪跟随当前绘制顺序。 | [B213](research2-community.md#b213)、[M209](research2-media.md#m209)、[M210](research2-media.md#m210)、[M211](research2-media.md#m211)、[M212](research2-media.md#m212) |
| 动态 CG 导出后漏帧或重复叠加 | 先区分原始局部帧与已重建显示帧，再应用时长和 blend/dispose。APNG 默认图可能不属于动画；记录帧数、循环与采样时刻。 | [M201](research2-media.md#m201)、[M206](research2-media.md#m206)、[M209](research2-media.md#m209) |
| 音频可播放但时长、循环或组合不对 | 在已选音频范围内清点 bank/wem/语言与事件依赖；保留原媒体和模拟播放结果的区别。Opus 核对 pre-skip、48 kHz granule 计数与尾部裁切。 | [M213](research2-media.md#m213)、[M216](research2-media.md#m216)、[T204](research2-formats.md#t204) |
| 官方旧帮助与实际目录不符 | 记录构建日期和运行时，交叉核对作者更新说明。Visual Novel Maker 的旧分组/运行时说明与后续子目录、Electron 更新要按版本分流。 | [E225](research2-engines.md#e225)、[E227](research2-engines.md#e227)、[E228](research2-engines.md#e228)、[E229](research2-engines.md#e229) |

工具作者若说明会删除、移动、改名或重写输入，先按 [GalPhotoAuto 的输入移动](research2-community.md#b222)、[DirectMuxer 的历史副作用](research2-community.md#b215)选择具体隔离方式，在运行目录的副本上操作，并保存输入/输出清单。保留关联文件的相对路径和原名，避免隔离时破坏依赖。

补充两类容易误诊的失败：

- [KrkrDump 过滤个案 · B234](research2-community.md#b234)表明允许列表能导致漏 CG；逐项核对过滤条件是否覆盖本次已选素材，保持未选类别不导出。
- [RPA 索引变体 · B228](research2-community.md#b228)与 [PCARC/ARC 嵌套 · B229](research2-community.md#b229)要求按实际字段和容器边界识别；作者的一次修改或按 magic 拆分只提供候选，验证范围和误匹配风险要单列。

## 下一轮实际验收的最小样本

以下是从资料推导的验收建议，尚未执行；不因加入此表就登记为已验证方案。

| 目标 | 样本必须覆盖 | 通过标准 |
|---|---|---|
| 差分依赖 | 底图、差分、独立 alpha，以及缺失依赖的情况 | 成品可完整解码、画布和边界一致；缺依赖明确报部分结果 |
| 多帧或分块容器 | 首末帧、非零偏移、空块、不同内部压缩类型 | 数量与索引对应，长度和坐标可追溯，没有静默跳过条目 |
| 状态化人物组合 | 宏参数、默认部件、隐藏/切换、分支后的状态 | 配方能说明每个部件来自哪条引用；未求值状态单列 |
| 图集与动画 | 旋转、trim、共享区域、多页、blend/dispose | 原尺寸可还原；逻辑别名完整；显示帧和时间有对应依据 |
| 版本兼容 | 同家族的另一个构建或独立资源 | 相同条件自动复用；不匹配条件会重新识别而非沿用旧参数 |

遵守[输出契约](output-contract.md)：列名、解码、布局、组合、材质/动画与全量覆盖分别记录。运行游戏或游戏代码前仍按主流程询问；本轮没有执行这些操作。

## 资料的计数与可信度

每条只计一个独立相关正文。长手册的多个锚点合并为一条；同文转载、译文、README/raw 镜像与同一模块不同引用不重复。独立源码模块仅在处理不同结构或不同资源层、有可提取的实现事实时单独计数。

作者自己的失败案例可证明“该作者、该版本、该样本失败过”，不能推出整个引擎不可支持。源码可证明某个实现如何处理数据及其遗漏，不替代格式全貌或本机验收。每项均附原文、归纳事实、应用和限制；本轮原始核读与排除记录保存在维护者的研究工作记录中，不随 skill 发布全文、私人路径或游戏素材。


