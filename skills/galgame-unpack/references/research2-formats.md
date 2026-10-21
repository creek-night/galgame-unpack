# 第二轮资料：工具实现与格式结构

核读于 2026-10-21 至 22 日。本页收录 35 个新增独立正文资料；同页章节、转载、镜像和旧目录重复不计数。以下是作者或规范支持的事实与据此形成的检查建议；本轮没有新增本机游戏验收。

<a id="t201"></a>
## T201 — Entis 官方：ERI/ERINA/MIO 层级区分

原文：[Entis 官方：ERI/ERINA/MIO 层级区分](https://www.entis.jp/eridev/about_eri.html) · 作者：L.Entis · 语言：ja · 类型：official-documentation

- 第 1、2 水准分别是 ERI 与 ERINA 无损图像，第 3 水准是有损图像，第 4 水准是 MIO 音频。
- 标准 ERI 使用 gamma 编码，ERINA 使用 Huffman；MEI 是动画容器名称。

**应用：** 按内部头部和水准选择解码器；导出为 PNG 不代表源图本来无损，音频水准另走音频路径。

**限制：** 旧版官方概述，不覆盖全部后续 ERISA 扩展；性能宣传不作为本机结论。

<a id="t202"></a>
## T202 — Entis 官方：ERI 文件与记录结构

原文：[Entis 官方：ERI 文件与记录结构](https://www.entis.jp/eridev/technique/file-structure.html) · 作者：L.Entis · 语言：ja · 类型：official-specification

- 开头为 8 字节 Entis/1A/00/00 头码，后有 32 位文件 ID、32 位扩展信息及 48 字节格式名。
- 信息记录内除文件头记录必须最先外，其余可选记录没有固定顺序；记录可以嵌套。
- 流记录按播放顺序存储，音频先于图像仅是建议，不是强制规范。

**应用：** 先验证 64 字节总头部，再按记录标识与长度遍历；不要给可选图片/音频记录写死偏移或顺序。

**限制：** 该页是结构概要，具体各记录编码仍须完整规范或解码实现；魔数只证明容器家族。

<a id="t203"></a>
## T203 — Entis 官方：图像解码接口与输出像素布局

原文：[Entis 官方：图像解码接口与输出像素布局](https://www.entis.jp/eridev/technique/decode-eri.html) · 作者：L.Entis · 语言：ja · 类型：official-documentation

- ERIAnimation::Open 可解出静态图，GetImageInfo 返回像素信息，但接口没有解码进度通知。
- 低层路径组合 ERIFile、EFileDecodeContext、ERIDecoder；可处理头信息加裸压缩流，也能通过回调观测块/行。
- 高层输出按 Windows DIB 排列；低层派生解码器可指定 RGB 排列。

**应用：** 移植时明确通道排列、stride 和缓冲区尺寸；解析器已有元信息但无完整文件封装时，可按低层接口设计转换。

**限制：** 这是 ERINA-Library 时代的 C++ 接口说明；没有在本机编译或验证现代 Windows 兼容性。

<a id="t204"></a>
## T204 — Entis 官方：MIO 分块音频及结束条件

原文：[Entis 官方：MIO 分块音频及结束条件](https://www.entis.jp/eridev/technique/play-mio.html) · 作者：L.Entis · 语言：ja · 类型：official-documentation

- MIODynamicPlayer 从 ERI 容器内选择音频流，GetNextWaveBuffer 返回下一个 PCM 数据块。
- GetChannelCount、GetFrequency、GetBitsPerSample、GetTotalSampleCount 提供输出音频参数；IsNextDataRewound 判断下一块是否回到开头。

**应用：** 用户选音频时按声道、采样率、位深建立 WAV 输出并核对样本数，遇回绕停止，防止把循环播放当无限新数据。

**限制：** 参考代码是 WinMM 播放器，不是现成批量导出器；本轮只读，不启动播放器。

<a id="t205"></a>
## T205 — Entis 官方：公开库版本与格式能力边界

原文：[Entis 官方：公开库版本与格式能力边界](https://www.entis.jp/eridev/download/index.html) · 作者：L.Entis · 语言：ja · 类型：official-release-documentation

- ERISA-Library 1.07e 页面日期为 2005-05-23，列出第 1、2、4、5 水准编解码。
- ERINA-Library 1.0A 页面日期为 2002-05-28，列出第 1–4 水准，并说明附样例和源码。
- 格式规范另提供 Word/RTF 文档下载，图像转换样例名为 ericvt。

**应用：** 候选库清单记下具体版本及水准，遇有损第 3 水准不可只凭较新的 ERISA 名称宣称覆盖。

**限制：** 只核读作者发布说明，未下载/运行二进制，未把下载列表当实现验收。

<a id="t206"></a>
## T206 — CMVS 作者分析：封包导出还会改变资源内部状态

原文：[CMVS 作者分析：封包导出还会改变资源内部状态](https://www.cnblogs.com/Dir-A/p/16552781.html) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- 作者样本中 PS3 的 0x30 字节头之后先 XOR 再解压；GARbro 输出可已完成内部解密。
- PB3 从包中直接读取的状态与 GARbro 导出的状态不同；CMV 内部被作者识别为压缩 JBP 图像而非普通 JPEG。

**应用：** 记录 archive-raw、decoded-intermediate、viewable 三种阶段，保留来源；PB3/PS3 不应因仍有专用扩展名就重复解密。

**限制：** 2022 年特定 CMVS 样本的作者观测；不承诺所有 PS3/CMV 版本相同，文中动态操作未执行。

<a id="t207"></a>
## T207 — CMVS 作者分析：四路资源读取与更新包优先级

原文：[CMVS 作者分析：四路资源读取与更新包优先级](https://www.cnblogs.com/Dir-A/p/18093497) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- クナド国記样本每种资源类型可注册四个读取项；目录路径与封包路径走不同读取函数。
- 外置 start.ps3 可先注册 update.cpz 再 script.cpz，缺少条目才继续下一路；相同文件名的外置与包内脚本可能不同。

**应用：** 先离线记录 cmvs.cfg、外置 start.ps3 和包内同名资源；只有读到注册顺序证据才合并覆盖，否则并列保留。

**限制：** 四项结构和优先级是该样本实现，不把 update 命名顺序推广到所有游戏。

<a id="t208"></a>
## T208 — YU-RIS 作者分析：YPF 解压与 YBN 解密应分层

原文：[YU-RIS 作者分析：YPF 解压与 YBN 解密应分层](https://www.cnblogs.com/Dir-A/p/16907255.html) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- YBN 扩展名下有多种文件头，yst_list、yscfg 和剧情 yst 文件用途不同；YPF zlib 解压不等于脚本文本已解密。
- 第三方工具可能继续以默认密钥处理 YBN，因此输出可能混有原始态与已解密态。
- 作者指出某些 Whirlpool 版本把文本另存 sc.ypf 内的 scenario TXT，编译脚本仍在 YBN。

**应用：** 先按 YBN 魔数分类，并抽取数个不同大小脚本核对内部结构及 CP932 文本；把外层包解压、脚本解密分别记入流水线。

**限制：** 密钥和结构依版本/厂商修改变化；可读字符串只是抽样信号，不作为完整剧情解析成功。

<a id="t209"></a>
## T209 — YU-RIS 作者分析：yscfg 的读取优先级与启动例外

原文：[YU-RIS 作者分析：yscfg 的读取优先级与启动例外](https://www.cnblogs.com/Dir-A/p/18096964) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- yscfg.ybn 的 YSCF 结构包含开发、调试、发布三种 filePriority 字段。
- 同一游戏的不同资源可采用不同松散文件读取规则；部分样本加载 yscfg 前已先选择封包，外置同名配置不会生效。

**应用：** 遇本体/补丁/松散文件冲突时读取并记录配置与版本条件，优先级无法证实时分开保存，不能默认松散文件总覆盖封包。

**限制：** 作者用特定版本调试说明；只把结构与读取依赖用于离线判断，不自动修改 yscfg 或可执行文件。

<a id="t210"></a>
## T210 — HorkEye 作者示例：保留行号的剧情筛选与遗漏点

原文：[HorkEye 作者示例：保留行号的剧情筛选与遗漏点](https://www.cnblogs.com/Dir-A/p/18096931) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- 作者明确示例仅展示效果，未用于完整项目；未知用途字符串可能是音频名或资源路径。
- 仅按行首高位字节筛选会漏掉 ASCII 开头的 SELECT 选项和部分 ruby 文本；示例增加 CS/SELECT 条件。
- 导出保留 LineCount 与 Raw，且强调零起始行号与编辑器显示差一。

**应用：** 可选剧情导出需保留源文件、字节编码、行号、原始行及未知语句；对选项、ruby、音频标记做单独覆盖抽样。

**限制：** 示例不是完整语法解析器，find 检查非行首严格匹配，不能直接当全引擎文本提取器。

<a id="t211"></a>
## T211 — Malie 作者分析：密钥表与首块验证

原文：[Malie 作者分析：密钥表与首块验证](https://www.cnblogs.com/Dir-A/p/18096803) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- 作者对照 GARbro/exdieslib 用解密后的 LIB 头验证密钥候选；部分游戏使用每 16 字节块的解密。
- 运行时使用的展开密钥表与传入初始化函数的字符串不是同一表示，表顺序也需对照工具。
- 作者指出更新版本可能不存在同样的字符串到密钥表生成入口。

**应用：** 保存游戏/包指纹、密钥表示与工具版本；验证候选需同时检查首块、索引结构和样本资源，不能用相似游戏名直接复用。

**限制：** 作者动态分析的历史样本；仅提炼版本与验证策略，不收录游戏密钥、不在本轮启动游戏。

<a id="t212"></a>
## T212 — PJADV 作者分析：PAC2 索引与相对偏移的证据

原文：[PJADV 作者分析：PAC2 索引与相对偏移的证据](https://www.cnblogs.com/Dir-A/p/17993483) · 作者：Dir-A · 语言：zh · 类型：original-reverse-analysis

- ティンクル☆くるせいだーすPSS v1.19 样本以 GAMEDAT PAC2 头识别，文件数后是每项 32 字节的名字表，再接每项 8 字节的 offset/size 表。
- 条目偏移从索引结束后的数据区计算；作者由多包对照再调试确认，.dat 与 .pak 可为相同容器。
- 作者观察 VFS 先尝试松散路径，失败再查询指定封包。

**应用：** 实现候选探针时联检文件数、0x10+40*N 索引终点、相对偏移范围和多个条目魔数；目录优先规则只在匹配样本条件时使用。

**限制：** 明确限定 PAC2 与作者样本；文章另提旧格式分支但未详细证明，不能把字段套到全部 PJADV。

<a id="t213"></a>
## T213 — Majiro ARC：版本、索引与 CP932 文件名

原文：[Majiro ARC：版本、索引与 CP932 文件名](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/majiro/arc_archive_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 识别 MajiroArcV 字头，但只接受版本 2/3；V2 哈希为 32 位，V3 为 64 位。
- 文件名区按独立 names_offset 读取零终止 SJIS 字符串，资源按每项 offset/size 直接取出。

**应用：** 记录 magic 与版本，验证两种索引宽度，保持 SJIS 原名映射；容器成功后再调用 RCT/RC8 图像解码。

**限制：** 本模块不接受 V1，也不保证所有 ARC 都是 Majiro；没有资源语义分类。

<a id="t214"></a>
## T214 — Majiro RCT：加密标志、底图和独立 mask

原文：[Majiro RCT：加密标志、底图和独立 mask](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/majiro/rct_image_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- S/C 标志区分加密与未加密，版本只接受 0/1；加密路径需要显式 rct-key。
- V1 引用 base_name 底图，同 stem 加下划线的资源可作为 mask；mask 解码后会反相。
- 底图与差分使用非透明像素覆盖，再应用 mask。

**应用：** 保留同目录依赖与命名；在缺底图/遮罩时标记不完整，检查透明边缘和底图解析链。

**限制：** 该实现缺少依赖时仍可能输出图像，不能以生成 PNG 就宣称完整；关键条件必须用样本复核。

<a id="t215"></a>
## T215 — Will ARC：无魔数索引校验与脚本轮转

原文：[Will ARC：无魔数索引校验与脚本轮转](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/will/arc_will_archive_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 按扩展名分目录，每目录含数量与偏移，文件名定长候选为 9 或 13 字节。
- 识别依赖索引可解析及 offset/size 范围；WSC/SCR 输出会逐字节右旋 2 位。

**应用：** 无签名 ARC 用目录计数、表长、数据区范围联合验证；输出脚本记录已轮转状态，防止重复变换。

**限制：** 这是旧 Will 布局，不覆盖所有 AdvHD/Pulltop ARC；候选字段碰巧通过仍需检查实际资源。

<a id="t216"></a>
## T216 — Will PNAP：一个容器可含多个图像条目

原文：[Will PNAP：一个容器可含多个图像条目](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/will/pnap_archive_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 以 PNAP 签名识别；0x10 读取条目数，每个表项跳 36 字节再读大小。
- 忽略零大小项，数据紧接索引按大小顺序存放，并按资源内容猜扩展名。

**应用：** 提取 PNAP 时报告有数据和空记录数量；保留原索引元数据供坐标合成，不把整个 PNA 当一张 PNG。

**限制：** 此实现跳过多数表项字段且未做布局合成，导出图片不代表已还原完整立绘。

<a id="t217"></a>
## T217 — Will WIPF：平面颜色、调色板和 MSK 配对

原文：[Will WIPF：平面颜色、调色板和 MSK 配对](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/will/wipf_image_archive_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 支持 8 位调色板或 24 位平面 B/G/R 数据，使用改动字典起点和最小匹配长度的 LZSS。
- 查找同文件名 .msk，按相同条目序号解码后附加透明遮罩。

**应用：** 将 WIP 与 MSK 视为依赖组；检查帧数量匹配、颜色通道与透明度，保留容器内多帧。

**限制：** 其他位深明确拒绝；元数据中被跳过的坐标不会自动恢复，本模块输出不能替代人物组合关系。

<a id="t218"></a>
## T218 — YU-RIS YPF：版本相关名字表与 zlib 条目

原文：[YU-RIS YPF：版本相关名字表与 zlib 条目](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/yuris/ypf_archive_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 从 YPF\0 头读取版本、文件数与表大小；根据版本选择附加字段长度，尝试多组名称长度置换表。
- 通过已知扩展名猜文件名 XOR 字节并转 SJIS；只有 compressed 标记为 1 的资源走 zlib。

**应用：** 把置换表、文件名 key、压缩标志与原始/压缩长度记录到探针结果；无常见后缀导致的猜测失败需区别于包损坏。

**限制：** 只涵盖代码列出的置换/头长规则，不继续解释 YBN 内容；新变体可能需新增方案。

<a id="t219"></a>
## T219 — YU-RIS YCG：两段压缩流构成 BGRA 图像

原文：[YU-RIS YCG：两段压缩流构成 BGRA 图像](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/yuris/ycg_image_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 识别 YCG\0；从 0x38 读取两段压缩数据分别 zlib 解压并拼接。
- 仅接受压缩方法 1 与 32 位图像，输出 BGRA8888。

**应用：** 按头部两段大小分别解压，检查拼接结果与 width*height*4；不要把第二流误判为额外文件。

**限制：** 其他位深或压缩方法不在实现范围；重命名成 PNG 无法转换。

<a id="t220"></a>
## T220 — NSystem FJSYS：独立名字区与 64 位偏移

原文：[NSystem FJSYS：独立名字区与 64 位偏移](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/nsystem/fjsys_archive_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- 魔数为 FJSYS 加零字节；名字区起点等于 header_size-file_names_size。
- 每项含名字偏移、32 位大小和 64 位资源偏移，数据直接返回并关联 MGD 解码器。

**应用：** 探针分别验证名称表和 64 位数据范围；容器层完成后再检查 MGD/MSD，避免将直接导出误判成最终可用素材。

**限制：** 这个模块没有处理所有潜在脚本加密或名字编码变种；保留原始名字字节更稳妥。

<a id="t221"></a>
## T221 — NSystem MGD：raw/SGD/PNG 三分支与区域元数据

原文：[NSystem MGD：raw/SGD/PNG 三分支与区域元数据](https://github.com/vn-tools/arc_unpacker/blob/456834ecf2e5686813802c37efd829310485c57d/src/dec/nsystem/mgd_image_decoder.cc) · 作者：rr- / arc_unpacker contributors · 语言：en/C++ · 类型：source-code

- MGD 内部压缩类型 0/1/2 分别走 BGRA 原始数据、SGD、自含 PNG。
- SGD 将 alpha 与颜色分开解码，alpha 会与 FF 异或；尾部区域表检验 meta_format=4。
- 区域表虽然被读取校验，但 decode_impl 最终只返回整张图像。

**应用：** 按内部类型选择解码；检测透明度反向和压缩尺寸；将区域表作为切片候选元数据额外保存。

**限制：** 读取区域表不等于已切片或已认定 CG/立绘；未知区域格式会失败。

<a id="t222"></a>
## T222 — CMVS CPZ：容器加密之后还有 PS2/PB3 处理

原文：[CMVS CPZ：容器加密之后还有 PS2/PB3 处理](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Cmvs/ArcCPZ.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 索引先经头部校验再尝试解密，条目解析包含目录名、相对数据区偏移、大小与每条目 key。
- OpenEntry 在容器数据解密后还根据 PS2A/PB3B 头调用脚本解包或图像解密。
- 该快照声明 CPZ5/6/7 签名，但实际 TryOpen 使用固定 CreateCpz5Scheme(Mirai)，遍历 KnownSchemes 的语句被注释。

**应用：** 记录工具 commit 和实际采用的 scheme；保留内层处理阶段，CPZ 解开后仍需判断输出是否原始态。

**限制：** 签名列表不能等同该快照对全部版本可用；缺方案数据库会直接拒绝；本次未验收任何 CPZ 样本。

<a id="t223"></a>
## T223 — CMVS PB3：按 Type/SubType 分派解码

原文：[CMVS PB3：按 Type/SubType 分派解码](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Cmvs/ImagePB3.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- PB3B 头解析 Type、SubType、宽高与位深；Type 1 仅接受 SubType 0x10。
- Type 2/3 走 JBP 解码及可选 alpha，Type 5 与 6/8 走不同实现；Type 4/7 明确不支持。

**应用：** 样本覆盖按 Type/SubType 分桶，成功样本不得代表整个 PB3；检查 JBP stride 与独立 alpha，给不支持类型单列原因。

**限制：** 模块输出可用图像但不提供人物组合关系，Write 未实现；外层 CPZ 解密需先完成。

<a id="t224"></a>
## T224 — QLIE PACK：尾部版本、外部 key 与一名多布局

原文：[QLIE PACK：尾部版本、外部 key 与一名多布局](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Qlie/ArcQLIE.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 识别标志位于文件末尾 0x1C 字节处，读取 FilePackVer，而非固定文件头。
- FilePackVer1.0 注释列出三种索引/加密搭配，代码会顺次尝试；同一个版本字串不能唯一确定布局。
- 版本 3 相关分支查找 key.fkey；条目先解密，再按 1PC/FF 压缩头还原。

**应用：** 探针保留头尾与 key.fkey 相对位置；记录实际通过的布局和 scheme，对每条资源再验证魔数/尺寸。

**限制：** key.fkey 与游戏方案并非所有版本都必需；不覆盖官中额外包裹层，不根据扩展名或 FilePackVer 单项宣布可拆。

<a id="t225"></a>
## T225 — QLIE DPNG：带 PNG 扩展名的切片容器

原文：[QLIE DPNG：带 PNG 扩展名的切片容器](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Qlie/ImageDPNG.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 格式登记扩展名 png，但实际魔数为 DPNG；元信息含 tile 数与完整画布尺寸。
- 每块提供 x/y、宽高和字节大小，内层 PNG 转成 Pbgra32 后按坐标写回完整画布；零大小块跳过。

**应用：** 先查文件签名，保留各块坐标并核对覆盖范围；PNG 导出前处理预乘 alpha，验收透明边缘和空块。

**限制：** 模块仅还原切片，不决定 CG/立绘分类，也不枚举表情；未知额外语义需其他证据。

<a id="t226"></a>
## T226 — QLIE ABMP：图像、声音与元数据嵌套容器

原文：[QLIE ABMP：图像、声音与元数据嵌套容器](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Qlie/ArcABMP.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- abmp10–12 与 ABMP7 由独立入口处理；.b 文件可含 abdata、abimage、absound 多类记录。
- 新记录可能带 UTF-16 名称，旧记录读窄字符串；没有名称时生成序号名，非法路径字符被替换。
- 资源还可有 1PC/FF 内层压缩，提取时继续解压。

**应用：** 对 .b 保留父包、记录标签、原名与导出名的映射，递归验证图片和声音；不要将 b 后缀仅归成一帧位图。

**限制：** 此模块不恢复动画时序或人物组合；未知记录降级成数据，不是完整语义支持。

<a id="t227"></a>
## T227 — Malie LIB/LIBP/LIBU：递归目录、块解密和文本压缩

原文：[Malie LIB/LIBP/LIBU：递归目录、块解密和文本压缩](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Malie/ArcLIB.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 普通 LIB 递归读取子目录；加密入口逐个方案验证解密后首块是 LIBP 或 LIBU，再选择索引读法。
- 加密读取按 16 字节对齐处理；LIBP 数据偏移经方案对齐并按偏移表项左移 10 位计算。
- 解密后的 txtz 还走 zlib，psbz 检查 PSBZ 头后再解压。

**应用：** 保持虚拟目录与相对路径；把块解密、容器索引、txtz/psbz 二次解压记成独立步骤并校验边界。

**限制：** KnownSchemes 为空或缺少匹配游戏规则会失败；LIBP 与 LIBU 不可只凭后缀混用，输出文本不等于完整剧情。

<a id="t228"></a>
## T228 — Malie DZI：256 网格、tex 依赖与画布裁切

原文：[Malie DZI：256 网格、tex 依赖与画布裁切](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Malie/ImageDZI.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- DZI 是 UTF-8 文本描述，要求相邻 tex 目录；按逗号分隔块名，x/y 每格递增 256。
- 可读入多组 tile 描述，但 Read 只使用 Tiles.First()；块图由 filename.* 查找。
- 输出可能按实际覆盖到的最大宽高裁切，而非始终保留声明画布。

**应用：** 同目录保留 DZI 与 tex；抽样比对原画布、首组块与边缘空白，显式记录裁切偏移，缺块应列为未完成。

**限制：** 不能把多组描述直接当人物差分，也不能把工具裁切结果当原始完整尺寸；此实现只恢复第一组。

<a id="t229"></a>
## T229 — Nitroplus NPA：游戏方案、名字和内容分层

原文：[Nitroplus NPA：游戏方案、名字和内容分层](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/NitroPlus/ArcNPA.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- NPA/01 头分别记录 compressed 与 encrypted，必要时选择游戏级加密方案。
- 索引名字经变换后以 CP932 解码，数据偏移基于 dir_size+41；Lamento 的 archive key 合成分支不同于其他列举游戏。
- 输出先解密再按 IsPacked 走 zlib；此实现把类型为 image 的条目排除在整体压缩标志之外。

**应用：** 记录准确游戏方案与头部两种标志；核对目录/文件总数和数据边界，图像不要因包标 compressed 就强行 zlib。

**限制：** NPA 后缀存在不同变体；这里指该魔数布局，不证明所有 Nitroplus 或 Steins;Gate NPA 通用。

<a id="t230"></a>
## T230 — Nitroplus/Mware NPK2：独立分段 AES 与 Deflate

原文：[Nitroplus/Mware NPK2：独立分段 AES 与 Deflate](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/NitroPlus/ArcNPK.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- NPK2 用游戏 key 与头部 IV 做 AES-CBC/PKCS7；索引使用 UTF-8 文件名。
- 一个文件可含多个 segment，每段有 offset、AlignedSize、Size、UnpackedSize。
- 各段分别建立解密流；Size<UnpackedSize 的段再经 Deflate，最后顺序拼成文件。

**应用：** 段级校验边界与输出长度，最后核对整文件 UnpackedSize；不能把 AES padding 或分段边界当资源末尾。

**限制：** key 不匹配时无法打开，分段成功不证明最终媒体完整；源码的写包功能本轮未使用。

<a id="t231"></a>
## T231 — AI6WIN/Silky AKB：增量底图、矩形与色键

原文：[AI6WIN/Silky AKB：增量底图、矩形与色键](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Silky/ImageAKB.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- AKB+ 比 AKB 多 base filename，头部给出整图尺寸、内部矩形与背景色；标志决定 24/32 位及 alpha 语义。
- 图像先 LZSS 解压并倒序读取行，再恢复像素差分；增量叠加以绿色像素作保留底图的色键。
- ReadBaseImage 中明确留下基图自身为增量时的 FIXME。

**应用：** 保留 AKB+ 依赖链和内部矩形，在合成前检查尺寸/位深匹配；嵌套增量底图需单列候选并比较最终透明边缘。

**限制：** 现成实现未递归保证增量基图正确，丢底图仍可能输出背景色图；不能以可打开来认定还原完整。

<a id="t232"></a>
## T232 — AI5WIN ARC：无签名方案匹配与启发式边界

原文：[AI5WIN ARC：无签名方案匹配与启发式边界](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/elf/ArcAi5Win.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 没有固定魔数，索引名字、size、offset 各有 XOR 参数，读完后检验数据区与文件边界。
- 候选名字宽度为 0x14/0x1E/0x20/0x100，猜测依赖至少两个条目；已知方案为空时入口提前返回。
- mes/lib/a/a6/msk/x 在 OpenEntry 中走 LZSS，其余直接返回。

**应用：** 结合已知方案、文件数、索引终点和解压后签名评分；把只有单条目或空方案库的失败与坏包区分。

**限制：** 启发式不保证可覆盖新游戏；AI5WIN 容器与 AI6WIN AKB 图片应分开匹配。

<a id="t233"></a>
## T233 — NScripter NSA：大端索引与分类型压缩

原文：[NScripter NSA：大端索引与分类型压缩](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/NScripter/ArcNSA.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 索引数量、基础偏移及条目 size/offset 使用大端，条目各带压缩类型和展开尺寸。
- 压缩编号 0/1/2/4 分别是 none/SPB/LZSS/NBZ；NBZ 跳过头 4 字节再用 BZip2。
- 代码有带前置零字节和加密输入分支；某些 .nsa 实际可包装单个 MP3。

**应用：** 在探针中将扩展名降为提示，按索引结构和压缩类型解码，核对展开字节数与媒体头。

**限制：** 未知压缩类型可能原样返回，不能因此标记资源可用；本文件不是所有 ONScripter 扩展的保证。

<a id="t234"></a>
## T234 — LiLiM AOS/AOSv2：链式索引与 CMP→ABM

原文：[LiLiM AOS/AOSv2：链式索引与 CMP→ABM](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/ArcFormats/Lilim/ArcAOS.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 旧 AOS 使用 0x20 字节记录与全 FF 的索引跳转标记，偏移以当前记录末尾为基准。
- AOSv2 从 0x111 开始按 0x28 字节表项读索引，并加统一 base_offset。
- SCR 资源经 Huffman 展开；V2 的 CMP 同样标为压缩并重命名 ABM。

**应用：** 用两套结构分别做索引校验，记录 CMP 到 ABM 的变换与原始名称；内层 ABM 仍需图像解码。

**限制：** 无固定魔数要求严格结构与样本验证；这套 LiLiM 格式不要与另一个名为 AOS 的引擎混用。

<a id="t235"></a>
## T235 — AOS 引擎 DAT/PACK：必须配套 index.idx

原文：[AOS 引擎 DAT/PACK：必须配套 index.idx](https://github.com/morkt/GARbro/blob/b09ee4570ccb1daf6ac56710ee8934dc0b8baeb0/Legacy/Aos/ArcDAT.cs) · 作者：morkt / GARbro contributors · 语言：en/C# · 类型：source-code

- 此 Legacy/Aos 模块要求 .dat 旁有 index.idx，而不是把索引从 DAT 本体中猜出。
- index.idx 每项以 0x34 字节定长名字开头，后接 32 位 offset/size，逐项校验 DAT 边界。
- 文件注释给出 Luna Season ~150 Bun no 1 no Koibito~ 样本。

**应用：** 接到单独 DAT 时先检查伴随 index.idx 是否缺失，保留两文件配对指纹；报告依赖缺失而非盲试 LiLiM AOS 算法。

**限制：** 仅是该 AOS 历史布局的候选，名字近似不代表与 .aos 或 AosTools 同一协议。

