# 图像还原与音视频

核读日期：2026-10-21。36 个独立页面。每条包含原文、作者、适用线索和限制；“应用”是建议的检查步骤，未在本轮执行游戏验收。

按症状先查 [资料导航](research-guide.md)，只读取与当前输入相关的条目。

## 目录

- [M01 AssetBundles](#m01) — Unity
- [M02 AssetBundle Dependencies](#m02) — Unity
- [M03 AssetBundle compression](#m03) — Unity
- [M04 Sprite Atlas properties reference](#m04) — Unity
- [M05 Sprite.vertices](#m05) — Unity
- [M06 Texture Import Settings window](#m06) — Unity
- [M07 Optimizing AssetBundle memory usage](#m07) — Unity
- [M08 Characters](#m08) — Naninovel
- [M09 Backgrounds](#m09) — Naninovel
- [M10 Special Effects](#m10) — Naninovel
- [M11 Custom Actor Shader](#m11) — Naninovel
- [M12 About Models (Native)](#m12) — Live2D Cubism
- [M13 DrawableVertexPositions Range](#m13) — Live2D Cubism
- [M14 Mask Preprocessing Methods (Native)](#m14) — Live2D Cubism
- [M15 About Motion](#m15) — Live2D Cubism
- [M16 Blend mode (Unity)](#m16) — Live2D Cubism
- [M17 Atlas export format](#m17) — Spine
- [M18 JSON export format](#m18) — Spine
- [M19 Loading Skeleton Data](#m19) — Spine
- [M20 Runtime Skins](#m20) — Spine
- [M21 Runtime Skeletons](#m21) — Spine
- [M22 Unity integration](#m22) — SpriteDicing
- [M23 AWB File](#m23) — CRI ADX
- [M24 Build (Export data)](#m24) — CRI ADX
- [M25 vgmstream Usage](#m25) — vgmstream
- [M26 TXTP format](#m26) — vgmstream
- [M27 ffprobe Documentation](#m27) — FFmpeg
- [M28 ffmpeg Documentation](#m28) — FFmpeg
- [M29 FFmpeg Filters Documentation](#m29) — FFmpeg
- [M30 Portable Network Graphics (PNG) Specification (Third Edition)](#m30) — PNG
- [M31 Ogg framing format](#m31) — Ogg/Vorbis
- [M32 Ogg Vorbis I comment field and header specification](#m32) — Ogg/Vorbis
- [M33 Extensions to the PNG 1.2 Specification, Version 1.4.0](#m33) — PNG
- [M34 Programming Guide for DDS](#m34) — Direct3D / DDS
- [M35 Texture Block Compression in Direct3D 11](#m35) — Direct3D / BCn
- [M36 Effective ASTC Encoding](#m36) — ASTC / astcenc

<a id="m01"></a>
## M01 — AssetBundles

原文：[AssetBundles](https://docs.unity3d.com/2022.3/Documentation/Manual/AssetBundlesIntro.html) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- AssetBundle 可包含序列化对象文件，以及纹理、音频等独立资源数据。
- 资源包针对平台构建，且可跨包引用其他资源。

**应用：** 清点容器、序列化对象和外部资源文件，保留它们的来源映射；孤立导出对象不等于取得完整纹理或音频。

**边界：** 版本化文档为 Unity 2022.3；未证明任一第三方拆包工具对具体游戏可用。


<a id="m02"></a>
## M02 — AssetBundle Dependencies

原文：[AssetBundle Dependencies](https://docs.unity3d.com/2022.3/Documentation/Manual/AssetBundles-Dependencies.html) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- 引用另一资源包中的对象会形成依赖；未分配到包的共用资源也可能被复制进多个包。
- 加载对象前需满足其依赖，Unity 不自动加载外部依赖包。

**应用：** 恢复立绘材质时追踪跨包纹理引用；同图多份不直接判为多套差分，并保留每个来源。

**边界：** Unity 2022.3 资产依赖规则；对象与包的身份仍须从实际数据确认。


<a id="m03"></a>
## M03 — AssetBundle compression

原文：[AssetBundle compression](https://docs.unity3d.com/2022.3/Documentation/Manual/AssetBundles-Cache.html) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- LZMA 对整包压缩，读取任一资源需要展开整段；LZ4 以块为单位解压。
- 缓存可能把下载包重压为 LZ4；未压缩包有不同布局要求。

**应用：** 遇到磁盘包与缓存包哈希不同，先核对压缩层和解压后对象内容，避免把重压误判为资源版本差异。

**边界：** Unity 2022.3 手册中的缓存与压缩行为；不保证各发行版或自定义封装一致。


<a id="m04"></a>
## M04 — Sprite Atlas properties reference

原文：[Sprite Atlas properties reference](https://docs.unity3d.com/2022.3/Documentation/Manual/class-SpriteAtlas.html) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- Atlas 可旋转精灵，并按轮廓紧密排布；相邻精灵间还有 padding。
- Atlas 自身可指定 sRGB、过滤和平台纹理设置。

**应用：** 切片还原需结合旋转、轮廓、间隔和纹理设置；按肉眼矩形批量裁切可能带入邻图或错误朝向。

**边界：** Unity 2022.3；需读取实际 Sprite/Atlas 元数据，本文不提供二进制字段布局。


<a id="m05"></a>
## M05 — Sprite.vertices

原文：[Sprite.vertices](https://docs.unity3d.com/2022.3/Documentation/ScriptReference/Sprite-vertices.html) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- Sprite 的显示形状由顶点与三角形索引构成。
- 示例同时使用 bounds、rect 和 textureRectOffset 处理顶点与图像区域关系。

**应用：** 非矩形或 diced 精灵要保存网格，并按三角形及 UV 映射重建；不能仅保留整张 Atlas PNG。

**边界：** Unity 2022.3 的 API 与示例；API 示例不是跨版本序列化布局规范，也不是通用坐标转换公式。


<a id="m06"></a>
## M06 — Texture Import Settings window

原文：[Texture Import Settings window](https://docs.unity3d.com/2022.3/Documentation/Manual/class-TextureImporter.html) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- 导入设置可限制最大尺寸并缩放纹理，目标平台还能覆盖格式与压缩。
- 部分移动平台支持拆分 alpha 通道。

**应用：** 导出尺寸应按构建资产记录；发现缺透明度时检查伴随 alpha 资源，避免声称已恢复美术原始分辨率。

**边界：** Unity 2022.3；玩家构建通常不含完整源导入资产，不能据此逆推出被降采样前的像素。


<a id="m07"></a>
## M07 — Optimizing AssetBundle memory usage

原文：[Optimizing AssetBundle memory usage](https://docs.unity.com/en-us/engine/7000.0/manual/assets-and-media/assets-managing-runtime/assetbundles-section/optimizing) · 作者：Unity Technologies · 语言：en · 类型：official-doc

来源依据：Unity Technologies 在其维护的官方站点发布。

- TypeTree 描述序列化对象布局；构建可禁用或剥离它。
- 目录表与预加载表承担命名入口和依赖信息，不能互相替代。

**应用：** 解析失败时分别记录版本、TypeTree 是否存在和依赖表；缺树的对象需匹配其真实类型定义，不能猜字段。

**边界：** 核读的是 Unity 7.0 Alpha 页面；只用于理解结构与排错，具体旧游戏必须复核其版本。


<a id="m08"></a>
## M08 — Characters

原文：[Characters](https://naninovel.com/guide/characters) · 作者：Naninovel / Elringus · 语言：en · 类型：official-doc

来源依据：Naninovel / Elringus 在其维护的官方站点发布。

- 分组选择、单层启停和组合别名有不同语义；默认外观来自 prefab 初始状态。
- 相机模式允许粒子、遮罩等复杂内容，并使用独立渲染画布。
- 当前文档警示内置 Live2D 集成不兼容 Unity R5 SDK。

**应用：** 解析 Composition Map、层级和初始启用状态生成立绘组合；碰到相机渲染时单纯叠 PNG 只能列为部分还原。

**边界：** 官网当前文档标记 v1.21；其内置 Live2D 集成不支持 Live2D SDK for Unity R5，旧游戏和自定义实现需独立确认。


<a id="m09"></a>
## M09 — Backgrounds

原文：[Backgrounds](https://naninovel.com/guide/backgrounds) · 作者：Naninovel / Elringus · 语言：en · 类型：official-doc

来源依据：Naninovel / Elringus 在其维护的官方站点发布。

- 背景可来自 diced 图像、图层或循环视频，外观名还可禁用循环。
- WebGL 视频资源可能位于 StreamingAssets，且不按编辑器选项转码。

**应用：** 背景分类先检查 actor 实现；视频保留流文件和循环标记，分层背景按其表达式组合，不能全当作静态 CG。

**边界：** Naninovel v1.21 文档；各平台可播放格式和实际编码仍需探测。


<a id="m10"></a>
## M10 — Special Effects

原文：[Special Effects](https://naninovel.com/guide/special-effects) · 作者：Naninovel / Elringus · 语言：en · 类型：official-doc

来源依据：Naninovel / Elringus 在其维护的官方站点发布。

- 转场参数和时长由脚本控制；灰度 dissolve 图描述像素切换时机。
- 相机组件及自定义 shader 也能改变最终画面。

**应用：** 把转场遮罩与普通立绘透明遮罩分开；需要复现剧情画面时记录脚本参数、相机效果与 shader。

**边界：** Naninovel v1.21 文档；转场中间帧不宜作为原始素材颜色或完整性的唯一参照。


<a id="m11"></a>
## M11 — Custom Actor Shader

原文：[Custom Actor Shader](https://naninovel.com/guide/custom-actor-shader) · 作者：Naninovel / Elringus · 语言：en · 类型：official-doc

来源依据：Naninovel / Elringus 在其维护的官方站点发布。

- 大多数角色和背景通过专用 shader 处理半透明叠画与转场。
- 纹理材质和场景精灵材质是不同配置入口。

**应用：** 叠图出现透明度或色彩不符时检查 actor 材质、shader 属性及渲染路径，不直接修改原纹理补偿。

**边界：** 官网当前为 v1.21；generic actor 与自定义实现需单独确认。


<a id="m12"></a>
## M12 — About Models (Native)

原文：[About Models (Native)](https://docs.live2d.com/en/cubism-sdk-manual/model/) · 作者：Live2D Inc. · 语言：en · 类型：official-doc

来源依据：Live2D Inc. 在其维护的官方站点发布。

- 模型与渲染器关联后还要按模型纹理编号绑定 Atlas。
- 显示位置和比例通过画布尺寸及矩阵处理；参数变化需更新到顶点。

**应用：** 可用模型交付应保留 moc3、纹理编号与引用关系，并用合适画布及更新顺序验证；单导 Atlas 不能证明人物还原。

**边界：** 本页是 Native SDK 流程，示例图形 API 不等于 Unity 或其他平台的具体实现。


<a id="m13"></a>
## M13 — DrawableVertexPositions Range

原文：[DrawableVertexPositions Range](https://docs.live2d.com/en/cubism-sdk-manual/drawablevertexpositions/) · 作者：Live2D Inc. · 语言：en · 类型：official-doc

来源依据：Live2D Inc. 在其维护的官方站点发布。

- 导出时设置的模型中心和单位影响顶点原点、范围与尺度。
- Native 返回的坐标遵循其图形坐标约定；换坐标系需检查 Y 方向。

**应用：** 恢复原生坐标时记录画布中心、单位和轴方向；先用已知点核对，避免用图片左上角直接套模型顶点。

**边界：** 页面更新于 2019-11-07，讨论 Cubism Core for Native；其他 SDK 与投影方式须另验。


<a id="m14"></a>
## M14 — Mask Preprocessing Methods (Native)

原文：[Mask Preprocessing Methods (Native)](https://docs.live2d.com/en/cubism-sdk-manual/ow-sdk-mask-premake/) · 作者：Live2D Inc. · 语言：en · 类型：official-doc

来源依据：Live2D Inc. 在其维护的官方站点发布。

- Native 可在单一纹理的不同通道和分区预生成多个遮罩。
- 遮罩区域根据被裁对象范围变换；高精度路径在每次绘制时生成遮罩。

**应用：** 眼部等异常优先检查遮罩引用、通道、区域矩阵和精度模式；把遮罩当普通灰度层叠加会产生错误。

**边界：** 文中注明 Cubism 5 类名变化，并区分 R5/R6 等能力；限制数量不能跨版本照搬。


<a id="m15"></a>
## M15 — About Motion

原文：[About Motion](https://docs.live2d.com/en/cubism-sdk-manual/motion/) · 作者：Live2D Inc. · 语言：en · 类型：official-doc

来源依据：Live2D Inc. 在其维护的官方站点发布。

- 现代动作由 motion3.json 驱动，Cubism 2.1 的 mtn 不能直接混用。
- Unity 使用转换后的 AnimationClip；Native 等直接插值，循环与淡入淡出行为存在版本差异。

**应用：** 动画验证需绑定正确 SDK、动作时间、循环和淡入淡出配置；只生成一张静态图不足以确认动作可用。

**边界：** 页面更新于 2026-01-29，含多个 SDK/版本分支；按目标游戏实际版本选择。


<a id="m16"></a>
## M16 — Blend mode (Unity)

原文：[Blend mode (Unity)](https://docs.live2d.com/en/cubism-sdk-manual/blend-mode-unity/) · 作者：Live2D Inc. · 语言：en · 类型：official-doc

来源依据：Live2D Inc. 在其维护的官方站点发布。

- Cubism 5 SDK for Unity R5 beta1 开始支持 Cubism 5.3 新混合模式。
- 颜色混合与 alpha 混合的组合由相应材质承载，并在导入时应用。

**应用：** 新模型出现异常透色时核对 SDK 与每个 ArtMesh 的混合组合；旧渲染器成功加载并不证明效果正确。

**边界：** 本页针对 Unity R5 beta1 及 Cubism 5.3 新功能，不能反推旧 Cubism 模型字段。


<a id="m17"></a>
## M17 — Atlas export format

原文：[Atlas export format](https://esotericsoftware.com/spine-atlas-format) · 作者：Esoteric Software · 语言：en · 类型：official-doc

来源依据：Esoteric Software 在其维护的官方站点发布。

- Atlas 的区域记录包含旋转、裁切范围、原尺寸和裁边偏移。
- 同名区域可用 index 区分；page 的 pma 标记表示纹理预乘 alpha。

**应用：** 按 page、name、index 定位切片，恢复旋转及透明边距后再组合；保留 pma 并匹配混合方式。

**边界：** 官网描述所示 Atlas 格式；旧版字段表示法须以匹配 runtime 为准。


<a id="m18"></a>
## M18 — JSON export format

原文：[JSON export format](https://esotericsoftware.com/spine-json-format) · 作者：Esoteric Software · 语言：en · 类型：official-doc

来源依据：Esoteric Software 在其维护的官方站点发布。

- 骨骼是父子局部变换，slot 顺序决定初始绘制顺序。
- slot 还保存颜色、当前 attachment 和混合模式；部分导出信息为可选项。

**应用：** 从骨骼、slot、skin 和 attachment 关系重建人物，保留版本和可选数据缺失情况；不按图块名称推断层序。

**边界：** JSON 导出格式会随 Spine 版本变化；示例版本不是所有数据的统一版本。


<a id="m19"></a>
## M19 — Loading Skeleton Data

原文：[Loading Skeleton Data](https://esotericsoftware.com/spine-loading-skeleton-data) · 作者：Esoteric Software · 语言：en · 类型：official-doc

来源依据：Esoteric Software 在其维护的官方站点发布。

- 加载需要骨骼 JSON/二进制以及 Atlas 的各 page 图片。
- attachment 的 path 负责查找区域；加载缩放会改变骨骼和图像尺寸单位。

**应用：** 先核对所有依赖和区域路径，再确认 loader scale；丢失图片、裁边元数据或缩放会造成可加载但不可正确显示。

**边界：** 解释官方 runtime 的加载机制；第三方导出器或自定义 AttachmentLoader 可能改变映射。


<a id="m20"></a>
## M20 — Runtime Skins

原文：[Runtime Skins](https://esotericsoftware.com/spine-runtime-skins) · 作者：Esoteric Software · 语言：en · 类型：official-doc

来源依据：Esoteric Software 在其维护的官方站点发布。

- skin 的键是 slot 与占位名，未必等于图像 attachment 名。
- 当前 skin 查找失败可回退到 default；运行时还可组合多个来源 skin。

**应用：** 枚举服装或表情时按占位映射和默认回退生成组合，并重置 slot 状态，避免把无效混搭计为立绘。

**边界：** 文档说明一般 runtime 行为；游戏代码可动态增添或替换 attachment。


<a id="m21"></a>
## M21 — Runtime Skeletons

原文：[Runtime Skeletons](https://esotericsoftware.com/spine-runtime-skeletons) · 作者：Esoteric Software · 语言：en · 类型：official-doc

来源依据：Esoteric Software 在其维护的官方站点发布。

- 动作修改局部变换后，应更新骨骼世界变换再绘制。
- 按 drawOrder 遍历 attachment；mesh 已带顶点与三角形，无需重新剖分。

**应用：** 动画或静态 pose 还原遵循变换更新、层序及 blendMode；网格人物不能当作独立矩形 PNG 相贴。

**边界：** 页面为通用 runtime 指导；完整 runtime 还承担具体图形平台的渲染职责。


<a id="m22"></a>
## M22 — Unity integration

原文：[Unity integration](https://dicing.elringus.com/guide/unity) · 作者：Elringus / SpriteDicing · 语言：en · 类型：author-doc

来源依据：SpriteDicing 作者 Elringus 的文档站；Naninovel 角色文档直接链接此页。

- diced 输出是原生 Unity Sprite 及网格，Atlas 可以跨多张纹理。
- 透明裁剪、pivot、PPU、padding 与 UV inset 都影响还原位置和边缘。

**应用：** 切片还原同时读取网格、Atlas、pivot 与 PPU；序列帧需保留原尺寸和相对位置，薄缝先检查 UV 与间隔。

**边界：** 当前文档标记 v4.0.0，最低 Unity 6.3 LTS；旧版需查 arch/v1，不能把新配置套旧游戏。


<a id="m23"></a>
## M23 — AWB File

原文：[AWB File](https://game.criware.jp/manual/native/adx2_en/latest/criatom_tools_atomcraft_awb_file.html) · 作者：CRI Middleware · 语言：en · 类型：official-doc

来源依据：CRI Middleware 在其维护的官方站点发布。

- AWB 存放编码波形，播放参数仍可来自 ACB。
- CueSheet 全部使用内存播放时，不一定生成外部 AWB。

**应用：** ACB/AWB 成对清点，但缺 AWB 不直接判损坏；保留 Cue 元数据与波形身份，区分裸波形和游戏播放效果。

**边界：** 核读的是 ADX 1.9.1 文档页面，未描述所有历史私有变种。


<a id="m24"></a>
## M24 — Build (Export data)

原文：[Build (Export data)](https://game.criware.jp/manual/adx2_tool_en/latest/criatom_tools_atomcraft_build.html) · 作者：CRI Middleware · 语言：en · 类型：official-doc

来源依据：CRI Middleware 在其维护的官方站点发布。

- 构建输出按平台、语言和 CueSheet 组织，并可附带 Cue ID 头文件。
- 工具可输出 ACB/ACF 的 XML 或 JSON 信息作为辅助元数据。

**应用：** 清点时保留语言和平台目录及辅助映射，避免同名音频覆盖；若随游戏附带映射可用于恢复 Cue 名称。

**边界：** 描述制作工具输出，发行包不保证带 XML、JSON 或头文件；不可假定缺省文件都能重新生成。


<a id="m25"></a>
## M25 — vgmstream Usage

原文：[vgmstream Usage](https://github.com/vgmstream/vgmstream/blob/master/doc/USAGE.md) · 作者：vgmstream maintainers · 语言：en · 类型：author-doc

来源依据：vgmstream 官方仓库中的维护者使用文档。

- CLI 可只报告信息、按 subsong 解码，并控制循环与淡出。
- 支持 Cue 容器时通常播放波形，不完整模拟 Cue 的随机、音高等行为。
- 极短音频可能是预取片段；内部名称也不一定是独立文件名。

**应用：** 先清点 subsong 和循环点，再以含 subsong 编号的文件名导出；报告原始波形覆盖与 Cue 复现为不同能力。

**边界：** 维护分支文档会变化；默认循环会改变导出时长，具体容器仍要样本核验。


<a id="m26"></a>
## M26 — TXTP format

原文：[TXTP format](https://github.com/vgmstream/vgmstream/blob/master/doc/TXTP.md) · 作者：vgmstream maintainers · 语言：en · 类型：author-doc

来源依据：vgmstream 官方仓库对其自定义 TXTP 格式的作者文档。

- TXTP 可串接 intro/loop 段或叠加多条音轨。
- 可选择 subsong、指定循环段，并保留原段内部循环点。

**应用：** 保留原文件并用单独 TXTP 记录已确认的顺序、循环和声道关系，制作可复核的整曲试听。

**边界：** TXTP 是播放编排，不自动发现游戏真实 Cue；混合采样率或声道仍需检查。


<a id="m27"></a>
## M27 — ffprobe Documentation

原文：[ffprobe Documentation](https://ffmpeg.org/ffprobe.html) · 作者：FFmpeg project · 语言：en · 类型：official-doc

来源依据：FFmpeg project 在其维护的官方站点发布。

- 可按 format、stream、packet、frame 等层次输出元数据。
- 可统计帧数和包数，并筛选需要的字段与标签。

**应用：** 为导出视频和音频生成机器可读清单，核对流数量、时长、像素格式与帧数；只读到容器头不算完整解码验证。

**边界：** 官网文档跟随开发版本；实际安装版本和编译选项决定可用功能。


<a id="m28"></a>
## M28 — ffmpeg Documentation

原文：[ffmpeg Documentation](https://ffmpeg.org/ffmpeg.html) · 作者：FFmpeg project · 语言：en · 类型：official-doc

来源依据：FFmpeg project 在其维护的官方站点发布。

- streamcopy 复制压缩数据包，不经过解码、滤镜和重新编码。
- map 决定选取哪些输入流；默认流选择未必涵盖所有素材。

**应用：** 优先保存全部已确认流的原始副本；需要透明帧或像素检查时另做解码验证，区分封装转换与画面恢复。

**边界：** 目标容器必须兼容被复制的流；复制成功不能证明每帧可解码。


<a id="m29"></a>
## M29 — FFmpeg Filters Documentation

原文：[FFmpeg Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html) · 作者：FFmpeg project · 语言：en · 类型：official-doc

来源依据：FFmpeg project 在其维护的官方站点发布。

- alphaextract 可取出透明通道，alphamerge 可将独立灰度视频并回 alpha。
- unpremultiply 可处理预乘颜色；输入维度和像素格式须匹配。

**应用：** 检查透明视频是否双流存储；在已确认 alpha 约定后重建并验证透明边缘，同时保留原流。

**边界：** 功能取决于实际 FFmpeg 构建；不能把颜色键控当作恢复原始 alpha。


<a id="m30"></a>
## M30 — Portable Network Graphics (PNG) Specification (Third Edition)

原文：[Portable Network Graphics (PNG) Specification (Third Edition)](https://www.w3.org/TR/png-3/) · 作者：W3C PNG Working Group · 语言：en · 类型：specification

来源依据：W3C 发布的 PNG 第三版规范，直接定义格式与显示语义。

- PNG 标准颜色样本不预乘 alpha；sRGB、iCCP、gAMA 等承载颜色解释。
- 颜色块有优先级和共存限制，单看像素数值不足以判断显示一致。

**应用：** 将游戏预乘纹理输出为通用 PNG 前明确转换；保留可确认的颜色标记，并在透明与纯色背景下核对边缘。

**边界：** 标准规定文件语义；某些游戏仍把预乘像素塞进 PNG，需结合资产元数据识别。


<a id="m31"></a>
## M31 — Ogg framing format

原文：[Ogg framing format](https://xiph.org/ogg/doc/framing.html) · 作者：Xiph.Org Foundation · 语言：en · 类型：specification

来源依据：Ogg 维护方 Xiph.Org 发布的 framing 规范。

- Ogg 页通过分段表组装 packet，packet 可跨页。
- 序号、逻辑流 serial、首尾标记和 granule position 各有不同作用。

**应用：** 从大包定位 Ogg 时校验完整页和跨页 packet，按逻辑流分组；不能只用 OggS 字节头与下个字节头截断。

**边界：** granule 的具体语义由 codec 定义；此页是 framing 规范而非循环点规范。


<a id="m32"></a>
## M32 — Ogg Vorbis I comment field and header specification

原文：[Ogg Vorbis I comment field and header specification](https://xiph.org/vorbis/doc/v-comment.html) · 作者：Xiph.Org Foundation · 语言：en · 类型：specification

来源依据：Vorbis 维护方 Xiph.Org 发布的 comment/header 规范。

- comment 是长度前缀 UTF-8 数据，字段名不区分大小写且允许重名。
- 规范允许非标准字段；注释包可跨页，不能按行或零结尾解析。

**应用：** 保留重复标签和原始字节长度；发现 LOOPSTART 等扩展时记录来源约定，不把扩展标签误称为 Vorbis 通用循环规范。

**边界：** 页面没有规定游戏循环标签的单位或算法；必须结合使用它的引擎或工具文档。


<a id="m33"></a>
## M33 — Extensions to the PNG 1.2 Specification, Version 1.4.0

原文：[Extensions to the PNG 1.2 Specification, Version 1.4.0](https://www.libpng.org/pub/png/spec/register/pngext-1.4.0-pdg.html) · 作者：PNG specification maintainers; editors Glenn Randers-Pehrson and Tom Lane · 语言：en · 类型：specification

来源依据：PNG 官方站点发布的扩展规范正文，列明规范维护者与编辑。

- oFFs 的 X/Y 为四字节有符号数；单位 0 表示像素，1 表示微米，坐标从左上角向右、向下计算。
- oFFs 允许负偏移并须位于首个 IDAT 之前，也可用于较大屏幕或应用自定义坐标系。

**应用：** 切片还原时保存偏移和单位，确认像素单位与共同画布后再定位；不能仅从偏移推断完整画布尺寸。

**边界：** 扩展规范版本 1.4.0，读取器对扩展块的支持并不普遍；本条只依据 oFFs 正文，不给 vpAg 赋予语义。


<a id="m34"></a>
## M34 — Programming Guide for DDS

原文：[Programming Guide for DDS](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide) · 作者：Microsoft · 语言：en · 类型：official-doc

来源依据：Microsoft Learn 发布 Direct3D DDS 文件布局与兼容性规则。

- DDS 的魔数和基础头后可有 DX10 扩展头；数据可能包含 mip 层、立方体面、体纹理或数组。
- 文档建议按格式重算行跨度，因为 dwPitchOrLinearSize 可能不可靠；基础 DDS 文件至少 128 字节，含 DX10 扩展头时至少 148 字节。

**应用：** 先核对头长度、格式和各子资源边界，再解码主图与伴随层；保留 sRGB 等格式标记，不能把头部识别成功记为完整像素解码通过。

**边界：** 这是 DDS 布局规则，未验证游戏自定义封装或解码器；部分旧 FourCC 枚举有歧义，不能只凭数值猜 DXGI 格式。


<a id="m35"></a>
## M35 — Texture Block Compression in Direct3D 11

原文：[Texture Block Compression in Direct3D 11](https://learn.microsoft.com/en-us/windows/win32/direct3d11/texture-block-compression-in-direct3d-11) · 作者：Microsoft · 语言：en · 类型：official-doc

来源依据：Microsoft Learn 的 Direct3D 纹理格式文档直接列出通道、块大小及 alpha 约定。

- BC1 的 alpha 可为一位，BC2/BC3 使用不同 alpha 编码；BC4/BC5 分别为单通道和双通道。
- BC 格式按 4×4 像素块存储，表中区分线性与 sRGB 格式；DXT2/4 的预乘语义需由渲染侧处理。

**应用：** 按实际 BC 型号核对块字节数、颜色解释和预乘约定，再检查透明边缘；单/双通道纹理要结合材质判断是否为蒙版等数据。

**边界：** 格式与渲染语义文档；识别压缩型号不证明像素已完整解码，且不能从通道数单独推断游戏中的纹理用途。


<a id="m36"></a>
## M36 — Effective ASTC Encoding

原文：[Effective ASTC Encoding](https://github.com/ARM-software/astc-encoder/blob/main/Docs/Encoding.md) · 作者：Arm Limited and contributors · 语言：en · 类型：official-doc

来源依据：Arm 官方 astc-encoder 仓库维护的编码与解码语义指南，署名 Arm Limited and contributors。

- ASTC 解码产生四通道，但单/双通道数据可映射到亮度与 alpha；恢复含义需结合编码和采样 swizzle。
- sRGB 解码校正只影响 RGB，alpha 保持线性；解码模式影响精度与舍入，astcenc 输出八位图时会启用对应模式。

**应用：** 还原移动平台纹理时记录 profile、通道映射与输出位深；结合原材质区分颜色、蒙版和法线数据，并检查透明边缘。

**边界：** 维护分支指南会更新；文中 swizzle 是推荐映射，不是所有游戏资产的默认值。未运行 astcenc 或验证真实纹理。
