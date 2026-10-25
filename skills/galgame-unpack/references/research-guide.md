# 联网资料导航与可执行检查

资料总计 251 个独立原始正文页，覆盖 68 个正文域名；排除 GitHub 仓库、raw 和 github.io 后仍有 186 页。首轮核读于 2026-10-21，保留 129 项；第二轮核读于 2026-10-21 至 22 日，去重新增 122 项。只计实际读到的相关正文；同页锚点、译文、镜像和薄目录不重复计数。首轮资料在本轮未逐项重新核读，使用时仍需匹配版本。

用于已验证路径失败、版本差异、位置/透明度异常或新增引擎调查。先使用匹配的本机已验证方案，只读取下表命中的资料。各条“应用”是基于来源提出的检查步骤，本轮没有新增游戏验收。

## 按问题查资料

已有游戏或工具的具体路线先查 [ztj 离线记录](ztjal-records.md)：111 篇作者正文整理成 6,592 个记录块，按需检索。它与研究摘要目录部分重叠，单独计数；作者记录不等于本机支持。

第二轮针对内层格式、底图依赖、引擎状态和渲染误差的新检查，先读[第二轮归纳与排查表](research2-guide.md)。

| 资料 | 何时阅读 |
|---|---|
| [博客与论坛实录](research-blogs.md) | 特定游戏、改版差异、工具失败、坐标丢失、名称恢复 |
| [引擎机制与官方/项目手册](research-engines.md) | 资源覆盖、图层状态、脚本语义、语言与语音关联 |
| [图像还原与音视频](research-render-media.md) | 图集/网格、alpha、材质、动作模型、循环与流完整性 |
| [工具作者文档与格式研究](research-tools.md) | 候选工具、原件保留、子命令、版本和结构校验 |

检索时同时记录游戏构建、工具版本与文档版本。当前文档可能晚于目标游戏：例如 SpriteDicing v4 文档指向旧 Unity 使用 arch/v1；Naninovel v1.21 对 Live2D SDK for Unity R5 有明确集成限制。先匹配版本再采用参数，参见 [SpriteDicing · M22](research-render-media.md#m22)、[Naninovel · M08](research-render-media.md#m08)。Light.vn 的 Wiki 由参与者维护，来源条目保留这一属性。

## 将资料转为处理步骤

默认资源范围和合成选项沿用主流程。为理解 CG/立绘而读取脚本或声音引用，不自动扩大交付范围。

| 触发情况 | 检查与处理 | 原文线索 |
|---|---|---|
| 转换工具写入、移动或清理输入 | 在 work 副本和独立 cwd 试跑；转换前单独保留原始资源，记录输入与输出清单。BGI-Hazuki 和 FreeMote 插件的原件保留行为有差异。 | [BGI 输出规则 · T08](research-tools.md#t08)；[FreeMote 插件 · T18](research-tools.md#t18) |
| 多包同名、补丁、语言替换 | 先按源包隔离并保留原路径，再依据已读到的配置或补丁状态生成有效版本视图。不能用解包顺序决定覆盖。 | [PFS 输出路径 · T07](research-tools.md#t07)；[RenPy 归档顺序 · E02](research-engines.md#e02)；[语言覆盖 · E05](research-engines.md#e05)；[Tyrano 补丁 · E22](research-engines.md#e22)；[KiriKiri 路径顺序 · E34](research-engines.md#e34)；[最终路径验证 · E35](research-engines.md#e35) |
| PSB 外壳、配对文件或名称错误 | 同时记录压缩壳、内部 PSB 类型、平台、插件和 key/seed 的用途；文件名参与 seed 时保留原 basename，重名用父目录隔离。 | [PSB 壳与原名 · T16](research-tools.md#t16)；[info-psb 与子命令 · T17](research-tools.md#t17) |
| 图像可开但位置错、透明度错 | 在转码前保存位置/画布/模式标签及伴随蒙版。KiriKiri 的 _p 是区域图；不要作为 alpha 使用。Artemis 的 PNG 注释也应先检查；PNG oFFs 区分有符号偏移与单位，不从偏移猜画布大小。 | [loadImages 元数据 · E13](research-engines.md#e13)；[转换器标签 · E14](research-engines.md#e14)；[Artemis 注释实录 · B11](research-blogs.md#b11)；[PNG oFFs · M33](research-render-media.md#m33) |
| 遮罩或半透明边缘不一致 | 区分红通道蒙版、alpha 蒙版、预乘颜色、整体透明度和逐层透明度；用实际接口与材质选择运算，不对全部图片统一反预乘。 | [AlphaMask 与 Composite · E09](research-engines.md#e09)；[旧 im.AlphaMask · E10](research-engines.md#e10)；[PNG alpha 规范 · M30](research-render-media.md#m30) |
| 经过旋转缩放或包含子图层的画面 | 按源裁剪矩形、局部原点、目标坐标、仿射参数、采样与混合模式还原；需要图层树时保留子图层关系，旧 API 的未实现模式不外推到新版。 | [operateAffine · E36](research-engines.md#e36)；[piledCopy · E37](research-engines.md#e37) |
| 一张容器图导出后仍漏内容 | HG-3 按帧 ID 盘点；恢复 stdinfo 的完整画布、偏移，并检查 JPEG 的独立 img_al。未知标签和帧数差异单列。 | [HG-3 原始研究 · T20](research-tools.md#t20) |
| 身体、表情、服装组合不确定 | 读取互斥组、默认项、无图项、状态延续和脚本实际引用；为每个组合保留选择依据。 | [RenPy 属性组 · E03](research-engines.md#e03)；[Tyrano 差分 · E19](research-engines.md#e19)；[Spine skin 回退 · M20](research-render-media.md#m20) |
| Unity 图集、切片、细缝或旋转 | 读取 Sprite 的网格、三角形、UV、旋转、裁边、pivot 和 PPU；跨 Atlas 纹理保留引用，按真实元数据检查边缘。 | [Atlas · M04](research-render-media.md#m04)；[Sprite 网格 · M05](research-render-media.md#m05)；[SpriteDicing · M22](research-render-media.md#m22) |
| Unity 缺对象、缺纹理或包哈希变化 | 分别检查跨包依赖、外部资源、TypeTree 与引擎版本。缓存重压可改变容器哈希；只有核对解压对象后才能判断内容关系。 | [容器组成 · M01](research-render-media.md#m01)；[依赖 · M02](research-render-media.md#m02)；[压缩 · M03](research-render-media.md#m03)；[TypeTree · M07](research-render-media.md#m07) |
| DDS、BC 或 ASTC 纹理颜色/透明度异常 | 核对容器头、格式、行跨度及 mip/数组子资源边界，再完整解码；按实际 BC 型号或 ASTC 通道映射、色彩空间与材质解释数据，不把单通道直接当灰度美术图。 | [DDS 布局 · M34](research-render-media.md#m34)；[BC 格式 · M35](research-render-media.md#m35)；[ASTC 解释 · M36](research-render-media.md#m36) |
| Naninovel 层图齐全但渲染仍不同 | 检查 Composition Map、初始状态、Render Only、相机和 shader。相机渲染涉及的 stencil/粒子等保持部分还原，未复现前不要用改色 PNG 掩盖差异。 | [角色实现 · M08](research-render-media.md#m08)；[Actor shader · M11](research-render-media.md#m11) |
| Live2D 或 Spine 的动作人物 | 保留模型、全部纹理、skin/attachment、骨骼或网格、遮罩、混合模式与动作时间。分别报告静态姿态、动画和最终渲染。 | [Live2D 模型 · M12](research-render-media.md#m12)；[遮罩 · M14](research-render-media.md#m14)；[动作 · M15](research-render-media.md#m15)；[Spine Atlas · M17](research-render-media.md#m17)；[骨骼绘制 · M21](research-render-media.md#m21) |
| 剧情缺行、译文错配或语音对不上 | 保留对白 ID、说话人、块/行顺序、语言与宏参数。Light.vn 的 CSV 行号和后续 unique_id 按版本区分；动态表达式保留未解析状态。 | [语音 ID · E06](research-engines.md#e06)；[Tyrano 自定义参数 · E21](research-engines.md#e21)；[Light.vn CSV · E31](research-engines.md#e31)；[版本更新 · E33](research-engines.md#e33)；[CST 脚本块 · T19](research-tools.md#t19) |
| 音频过短、循环错误或漏轨 | 在用户选择音频时清点 ACB/AWB、subsong、前奏/循环段、语言目录与扩展标签；完整解码原波形，再按有依据的播放关系生成试听副本。 | [AWB · M23](research-render-media.md#m23)；[vgmstream · M25](research-render-media.md#m25)；[TXTP · M26](research-render-media.md#m26)；[Vorbis 注释 · M32](research-render-media.md#m32)；[RenPy 播放片段 · E07](research-engines.md#e07) |
| 视频丢透明度、时间或流 | 在用户选择视频时清点所有流，区分复制封装与完整解码；透明视频保留原流和帧时间。OMV 候选文档有接口矛盾，先核对固定版本，PTS 不直接当秒。 | [Siglus OMV · T10](research-tools.md#t10)；[omvdecoder · T15](research-tools.md#t15)；[FFmpeg 流选择 · M28](research-render-media.md#m28)；[透明通道 · M29](research-render-media.md#m29) |
| 图层规则缺图、错位或跨盘失败 | 逐一核对规则名到实际文件名的映射，包括 .tlg.png 双后缀；体验版和正式版编号分别绑定。跨盘问题先检查工具版本与 cwd。 | [规则工具修订 · B12](research-blogs.md#b12)；[体验版/正式版差分 · B31](research-blogs.md#b31) |
| Hxv4 解码后仍是哈希名 | 文件名和目录名的恢复分别验证；记录输入编码、salt/seed、算法分支和已匹配向量，未匹配资源继续保留来源哈希。 | [Hxv4 动态实录 · B02](research-blogs.md#b02)；[后续静态哈希分析 · B28](research-blogs.md#b28) |
| 只有索引或扫描出的图片 | 把能列名、能解码和能恢复脚本分开记录；carving 得到图片只能代表部分恢复，数据库或子格式错误仍需查明。 | [AQUARIUM 部分恢复 · B20](research-blogs.md#b20)；[GARbro 数据库失败 · B32](research-blogs.md#b32)；[同系方案失败 · B34](research-blogs.md#b34) |
| 脚本文字缺失或遇未知 opcode | 先检查 ruby/标签与脚本结构；保留未知 opcode 和原始字节，换匹配解析器或继续离线研究，不能静默跳过后宣布剧情完整。 | [BGI/Artemis 脚本失败 · B08](research-blogs.md#b08)；[ruby 提取实录 · B15](research-blogs.md#b15) |
| 无法判断 CG 覆盖与差分分组 | 在存在 CGList 或脚本引用时，用表/帧组/文件规格建立候选映射，再与实际包项和解码结果交叉核对；菜单列出的条目也不能代替全量证明。 | [CGList 结构 · T21](research-tools.md#t21) |

## 候选路线的下一次验收

以下是研究后整理的验证任务，尚未实施。先选能覆盖结构差异的小样本，并留出独立样本；测试通过后才登记 profile。

| 候选 | 首个应证明的结果 | 未通过时保留什么 |
|---|---|---|
| BGI-Hazuki | 与现有 BGI 已验证输出对照像素/alpha；检查 CBG、BF_Movie 和原件保留行为 | 工具版本、输入/输出清单、删除/移动发生在工作副本的记录 |
| pfs-rs / Artemis | 多包同名不覆盖；路径与 PNG 定位元数据能追溯 | 每包源路径、裁剪参数、原始 PNG 注释、冲突表 |
| qlie-unpack | 匹配实际 FilePack 代际，列目录与提取 JSON 分别核对；所选图像可完整解码 | 包版本、key 来源条件、嵌套资源层次与原始文件 |
| CatSystem2 HG-3 / CGList | 多帧、独立 alpha 和完整画布逐项一致；CGList 映射有来源 | 未知标签、未解析规格、缺帧和映射歧义 |
| RenPy / Tyrano / Light.vn | 选一个有脚本依据的多层组合和一个默认/互斥状态，独立重建一致 | 属性/部件/命令状态、未求值表达式、引擎版本 |
| Live2D / Spine / Naninovel | 先对照一个明确姿态的网格/遮罩/混合，动画再验时序 | 静态、动作与最终材质分别标注，不由纹理成功升级渲染状态 |
| Siglus 静态 key | 同构建双资源与多个 Scene 完整解码、尺寸及引用边界均通过 | 候选 key、失败阶段、解压长度与结构诊断 |
| 选中的音频/视频 | 所有选定 subsong/stream 完整解码，循环与透明信息有出处 | 原始流、时序/循环 sidecar、未确定单位与缺依赖项 |

Siglus 的结构验证方法见 [原作者 writeup · T12](research-tools.md#t12)。新工具以固定版本 --help 和实际文件为准，文档中含占位或矛盾的示例不直接写成可复用命令。

## 记录、失败与既有边界

每次采用资料记录：来源编号/URL、游戏与工具版本、正文支持的事实、自己的推断、预期现象、实际结果、输出哈希和未覆盖项。能列名、能解码、能还原位置、能合成、能复现材质和全量覆盖分别记录。

旧作、体验版、不同平台或汉化版本的成功只提供候选线索；失败实录用于定位下一层问题，不推出整个引擎不可支持。打不开的页面保留访问失败原因，检索空结果不等于没有记录。

继续沿用 [社区经验](community-experience.md) 与 [输出契约](output-contract.md)。G14 的开场 CG 已有独立本机证据；它仍不代表全游戏 CG 完成。G16 的 Alisa 材质/stencil 仍需另验。当前结论以 [已验证样本](validated-samples.md) 中最新日期为准，资料目录不会提升这些状态。

启动游戏、执行游戏脚本、加载游戏 DLL、注入或动态分析仍按主流程询问；普通离线解码沿用授权。研究阶段未下载或执行这里新增的工具。
