# 第二轮资料：图像、图集、渲染与音频

核读于 2026-10-21 至 22 日。本页收录 16 个新增独立正文资料；同页章节、转载、镜像和旧目录重复不计数。以下是作者或规范支持的事实与据此形成的检查建议；本轮没有新增本机游戏验收。

<a id="m201"></a>
## M201 — WebP Container Specification

原文：[WebP Container Specification](https://developers.google.com/speed/webp/docs/riff_container) · 作者：Google / WebP · 语言：en · 类型：official-spec

- ANMF 存帧矩形、偏移、时长及 blend/dispose；帧坐标字段需乘 2，实际画布按顺序累积。
- RIFF chunk 长度不包含头与奇数字节补齐。

**应用：** 对动画 CG 保留完整容器；按帧矩形、blend/dispose 重建显示帧，并记录循环与时间，不能把局部帧直接当完整差分。

**限制：** 只说明标准 WebP；引擎额外容器、私有头与定制渲染仍需单独核对。

<a id="m202"></a>
## M202 — cwebp — encoding options

原文：[cwebp — encoding options](https://developers.google.com/speed/webp/docs/cwebp) · 作者：Google / WebP · 语言：en · 类型：official-tool-doc

- lossless 编码默认不承诺保留完全透明像素下的 RGB，需 exact。
- near_lossless 预处理会改变像素；cwebp 文档说明不支持动画 PNG/WebP 输入。

**应用：** 原始导出保留字节；确需转成 WebP 时区分视觉无损与 RGBA 精确相等，并为动画使用专门的多帧流程。

**限制：** 这是可选转换检查，不要求下载或执行编码器，也不改变默认 PNG 交付。

<a id="m203"></a>
## M203 — Addressables 1.21 — Manage catalogs at runtime

原文：[Addressables 1.21 — Manage catalogs at runtime](https://docs.unity3d.com/Packages/com.unity.addressables@1.21/manual/LoadContentCatalogAsync.html) · 作者：Unity · 语言：en · 类型：official-engine-doc

- 运行期可从本地或远程装载额外内容目录，增加资源键。
- 同位置同名 hash 文件参与目录缓存与更新判断。

**应用：** 采集 catalog 与配套 hash、目录版本和内部依赖；本地资源不足时区分缺少额外目录、缺少 bundle 与解码失败。

**限制：** 对应 Addressables 1.21.21；文档不证明某游戏使用默认加载逻辑，不据此自动联网下载游戏资源。

<a id="m204"></a>
## M204 — TexturePacker — Texture Settings

原文：[TexturePacker — Texture Settings](https://www.codeandweb.com/texturepacker/documentation/texture-settings) · 作者：CodeAndWeb · 语言：en · 类型：author-tool-doc

- 打包支持正反向 90 度旋转，方向由导出格式决定；多个逻辑 sprite 可共享一个物理区域。
- Trim、CropKeepPos、Crop 的原始位置语义不同；extrude 与 padding 不是人物图像新增边缘。

**应用：** 先读图集元数据确定旋转、原尺寸、偏移与别名，再裁切还原；保持逻辑名字到共享区域的多对一关系。

**限制：** 同名字段在不同导出器可能不同；不能凭 png 看上去像图集就假设 TexturePacker 规则。

<a id="m205"></a>
## M205 — Pillow — Concepts: modes and coordinates

原文：[Pillow — Concepts: modes and coordinates](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) · 作者：Pillow contributors · 语言：en · 类型：official-library-doc

- RGBA 与预乘 RGBa 含义不同，数值不能当成相同颜色空间。
- 坐标按像素角点定义，原点位于左上；多通道超过 8 位的支持有限。

**应用：** 在合成记录中写明直通/预乘 alpha、位深和坐标约定；原始高位深素材不静默降到 8 位。

**限制：** 本轮读取 stable 13.0.0；本机依赖版本另行核对，不据文档擅自升级。

<a id="m206"></a>
## M206 — Pillow — Image file formats: APNG and metadata

原文：[Pillow — Image file formats: APNG and metadata](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) · 作者：Pillow contributors · 语言：en · 类型：official-library-doc

- APNG 可有不参与动画的默认图，n_frames 因此可能比动画帧数多 1。
- APNG loader 返回已按 blend/dispose 合成的显示帧；保存多帧及 ICC 等元数据要使用相应参数。

**应用：** 避免对已合成显示帧再次叠加；核对默认图、实际帧数、时间和 ICC 保留策略。

**限制：** 只归纳本页的 PNG/APNG 与元数据行为；其他格式须查各自条目，stable 版本不能代替本机行为验证。

<a id="m207"></a>
## M207 — KTX 2.0.4 — orientation and channel swizzle

原文：[KTX 2.0.4 — orientation and channel swizzle](https://registry.khronos.org/KTX/specs/2.0/ktxspec.v2.html) · 作者：Khronos Group / Mark Callow · 语言：en · 类型：official-spec

- KTXorientation 描述逻辑轴向，不改变字节到纹理坐标的映射。
- KTXswizzle 可重排通道或填常量；单通道纹理可能按不同规则解释为灰度或 alpha。

**应用：** 解码 KTX 时保存轴向与 swizzle，避免固定翻转或把单通道遮罩当灰色立绘；导出同时记录所选层和 mip。

**限制：** 标准元数据不足以证明游戏 shader 的最终效果；Basis/超压缩还需相应解码器。

<a id="m208"></a>
## M208 — Addressables 1.21 — Content Packing and Loading schema

原文：[Addressables 1.21 — Content Packing and Loading schema](https://docs.unity3d.com/Packages/com.unity.addressables@1.21/manual/ContentPackingAndLoadingSchema.html) · 作者：Unity · 语言：en · 类型：official-engine-doc

- Address、GUID、Label 可按构建选项省略；internalId 命名模式也可改变。
- AssetBundle CRC 校验针对解压后数据，与简单对压缩文件求 CRC 不同。

**应用：** 目录没有可读名字时报告命名信息被省略的可能性；校验值必须注明算法和作用对象，不能混用文件 SHA256 与 bundle CRC。

**限制：** 对应 1.21.21；私有 provider 可改加载行为，不能据 catalog 键缺失直接判资源丢失。

<a id="m209"></a>
## M209 — Spine — Export

原文：[Spine — Export](https://esotericsoftware.com/spine-export) · 作者：Esoteric Software · 语言：en · 类型：official-tool-doc

- 数据导出版本须与运行库匹配；图片序列帧数受导出 FPS 与是否包含末帧影响。
- 加色附件在透明背景与实体背景上的表现可能不同。

**应用：** 动态立绘导出记录运行库版本、姿态、采样 FPS、透明背景与混合模式；加色特效同时生成棋盘格和实体底色检查图。

**限制：** 不能从打包纹理推断动画全貌；文档不代表已安装或获准使用 Spine 编辑器。

<a id="m210"></a>
## M210 — Adobe Photoshop File Formats Specification

原文：[Adobe Photoshop File Formats Specification](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/) · 作者：Adobe · 语言：en · 类型：official-spec

- 图层记录含矩形、通道、混合模式、透明度、裁剪与遮罩；PSD/PSB 部分长度字段不同。
- 合并预览位于独立数据段，关闭兼容选项时可能没有。

**应用：** 遇到 PSD 或导出 PSD 中间件时保留图层及混合信息；没有合并预览时明确需要重新渲染，不把单层像素导出称为完整合成。

**限制：** 规范描述结构，不提供所有渲染语义；按 PSD/PSB 与位深分别解析，禁止猜测长度。

<a id="m211"></a>
## M211 — Spine — Clipping attachments

原文：[Spine — Clipping attachments](https://esotericsoftware.com/spine-clipping) · 作者：Esoteric Software · 语言：en · 类型：official-engine-doc

- 裁剪是可随骨骼和动画变形的多边形，作用范围由绘制顺序与 end slot 决定。
- 绘制顺序变化会改变受裁剪的附件；多个裁剪的受影响区间不能重叠。

**应用：** 离线渲染先求当前时间的网格与绘制顺序，再应用对应范围的裁剪；保留裁剪区间作为合成证据。

**限制：** 矩形切片加 alpha 叠图无法替代这套模型；未实现裁剪时只能交付素材和部分预览。

<a id="m212"></a>
## M212 — psd-tools — Usage

原文：[psd-tools — Usage](https://psd-tools.readthedocs.io/en/latest/usage.html) · 作者：psd-tools contributors · 语言：en · 类型：author-library-doc

- 图层迭代顺序在 1.7.x 前后反转；现代版本从后景到前景。
- 作者说明合成支持有限，重新渲染结果可能不同于 Photoshop；智能对象可内嵌或链接外部文件。

**应用：** 固定解析器版本，记录图层层序；优先保留已有合并预览并与重绘比较，对缺少的链接对象单列依赖。

**限制：** 本轮文档为 1.26.0，未安装运行；不能把库成功保存等同于视觉正确，不能追随文档内任意绝对链接路径。

<a id="m213"></a>
## M213 — wwiser — Wwise bank explorer and simulator

原文：[wwiser — Wwise bank explorer and simulator](https://github.com/bnnm/wwiser) · 作者：bnnm · 语言：en · 类型：author-tool-doc

- bnk 包含 HIRC 音频脚本，相关 bank 可相互引用；作者建议先载 init.bnk 再载关联 bank。
- 配套 SoundbanksInfo.xml 等有助命名；生成 TXTP 可模拟多 wem 组合，但不能覆盖全部 Wwise 特性。

**应用：** 用户选择音频时一起登记 bank、wem、命名表和语言；区分原始媒体文件、事件组合与模拟播放输出。

**限制：** 候选工具未本地验证；成功导出 wem 不等于还原游戏中每个事件或动态混音。

<a id="m214"></a>
## M214 — PixiJS 8.2.3 — Spritesheet parser source

原文：[PixiJS 8.2.3 — Spritesheet parser source](https://pixijs.download/v8.2.3/docs/spritesheet_Spritesheet.ts.html) · 作者：PixiJS contributors · 语言：en · 类型：official-source

- 解析器分别构造 frame、orig、trim，旋转帧会交换宽高，并按 resolution 换算。
- 动画顺序来自命名帧列表，不能用物理图集顺序代替。

**应用：** 匹配到 PixiJS 图集后按该版本实际字段语义还原；区分像素裁切坐标与显示缩放，保持动画列表顺序。

**限制：** 固定引用 8.2.3；其他版本或自定义加载器需另查，不假设网页游戏都采用此格式。

<a id="m215"></a>
## M215 — PixiJS 8 — Scene Objects

原文：[PixiJS 8 — Scene Objects](https://pixijs.com/8.x/guides/components/scene-objects) · 作者：PixiJS contributors · 语言：en · 类型：official-engine-doc

- 位置、缩放、旋转与 alpha 受父容器层级影响。
- anchor 使用归一化比例，pivot 使用像素；两者都会改变可见位置。

**应用：** 合成网页引擎立绘时保存父子关系和局部变换；从图集恢复纹理后，再依场景变换定位，避免把 pivot 当裁边偏移。

**限制：** 仅针对 PixiJS v8 语义，读取旧版游戏先确定版本；场景状态未恢复时只声明纹理还原。

<a id="m216"></a>
## M216 — RFC 7845 — Ogg Encapsulation for Opus

原文：[RFC 7845 — Ogg Encapsulation for Opus](https://www.rfc-editor.org/rfc/rfc7845.html) · 作者：IETF / T. Terriberry, R. Lee, R. Giles · 语言：en · 类型：official-spec

- Ogg Opus 的 granule position 按每声道 48 kHz 样本计，不随解码器采样率变化。
- pre-skip 表示解码后丢弃的前置样本；末页 granule 可要求丢弃尾部填充。

**应用：** 可选音频导出校验有效时长和首尾样本，避免将编码延迟计入对白对齐或 BGM 循环点。

**限制：** Ogg 是容器，必须先辨别 Opus/Vorbis；私有包内裸 Opus 与外部循环标记另行处理。

