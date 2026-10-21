# 工具作者文档与格式研究

核读日期：2026-10-21。21 个独立页面。每条包含原文、作者、适用线索和限制；“应用”是建议的检查步骤，未在本轮执行游戏验收。

按症状先查 [资料导航](research-guide.md)，只读取与当前输入相关的条目。

## 目录

- [T01 GARbro README](#t01) — multi-engine / GARbro
- [T02 arc_unpacker README](#t02) — multi-engine / XP3
- [T03 FreeMote README](#t03) — PSB / PIMG / E-mote
- [T04 unrpa README](#t04) — RenPy / RPA
- [T05 unrpyc README](#t05) — RenPy / RPYC
- [T06 krkrfgformat README](#t06) — KiriKiri / sprite-composition
- [T07 pfs-rs README](#t07) — Artemis / PFS
- [T08 BGI-Hazuki README](#t08) — BGI / Ethornell / CBG / DSC
- [T09 QLIE Unpacker README](#t09) — QLIE / FilePack / ABMP / DPNG
- [T10 SiglusExtract README](#t10) — Siglus / G00 / OMV
- [T11 siglus-static-key-tool README](#t11) — Siglus / offline
- [T12 Siglus Resource-Key Recovery Writeup](#t12) — Siglus / validation
- [T13 KrkrExtract README](#t13) — KiriKiri / XP3
- [T14 TriggersTools.CatSystem2 README](#t14) — CatSystem2 / HG2 / HG3 / CST
- [T15 omvdecoder README](#t15) — Siglus / OMV / video
- [T16 PSB Shells, Types, Platforms](#t16) — PSB / MDF / MZS
- [T17 FreeMote CommandLine Usage for Tools](#t17) — PSB / PIMG / E-mote
- [T18 FreeMote Plugins & External Tools](#t18) — PSB / TLG / ASTC / BC7
- [T19 About the CST format](#t19) — CatSystem2 / CST / text
- [T20 HG-3 Image format research](#t20) — CatSystem2 / HG3 / alpha
- [T21 CGList Data format research](#t21) — CatSystem2 / CGList / classification

<a id="t01"></a>
## T01 — GARbro README

原文：[GARbro README](https://github.com/morkt/GARbro) · 作者：morkt · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Usage / Requirements

- 加密格式可能需要选对作品；识别到类型后才适合批量转换。
- 无扩展名或类型未知的条目不能直接按后缀排除。

**应用：** 记录游戏版本和类型识别证据；先探测，再筛选 CG／立绘。

**边界：** 作者的支持表和转换能力不等于当前游戏已通过验收。


<a id="t02"></a>
## T02 — arc_unpacker README

原文：[arc_unpacker README](https://github.com/vn-tools/arc_unpacker) · 作者：vn-tools · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Usage / Troubleshooting

- 同一输入可有多个解码器候选，CLI 允许显式指定 --dec。
- XP3 的游戏特定 --plugin 需要匹配；命令行错误信息比拖放窗口更适合诊断。

**应用：** 把解码器、插件和完整失败日志纳入工具尝试记录。

**边界：** 不能将一个解码器成功泛化为全部同后缀包。


<a id="t03"></a>
## T03 — FreeMote README

原文：[FreeMote README](https://github.com/UlyssesWu/FreeMote) · 作者：UlyssesWu · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Introduction / Tools / Features

- M2 PSB 与 Photoshop PSB 等同扩展名格式不同；先看魔数和内部结构。
- 反编译资源、查看 E-mote、处理压缩壳属于不同功能。

**应用：** PSB 路由先区分壳、内部类型、平台和所需插件。

**边界：** Viewer 对纯净 E-mote 输入的要求不能套到全部 PSB。


<a id="t04"></a>
## T04 — unrpa README

原文：[unrpa README](https://github.com/Lattyware/unrpa) · 作者：Lattyware · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Usage / Supported formats

- 提供 list/tree 目录查看和显式输出目录；默认提取位置受当前工作目录影响。
- 强制版本、偏移和 key 选项会覆盖头信息，应由格式证据驱动。

**应用：** RPA 先列目录，指定独立输出；强制参数写入 recipe 及依据。

**边界：** 作者列出的归档版本不是对任意修改版 RPA 的保证。


<a id="t05"></a>
## T05 — unrpyc README

原文：[unrpyc README](https://github.com/CensoredUsername/unrpyc) · 作者：CensoredUsername · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Usage / Compatibility

- Ren'Py 代际对应不同反编译器和 Python 环境；很早的版本有专用参数。
- --try-harder、并行数和 --clobber 各有性能或覆盖影响。

**应用：** 先识别 Ren'Py／工具版本，优先离线 CLI；保持原 RPYC。

**边界：** 注入运行式方案与离线反编译分开；未验证当前游戏。


<a id="t06"></a>
## T06 — krkrfgformat README

原文：[krkrfgformat README](https://github.com/Hitachi-Momoka/krkrfgformat) · 作者：Hitachi-Momoka · 语言：zh · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：使用说明 / 注意事项

- 不同游戏的规则 TXT／JSON 并不完全通用，部分导出 JSON 还可能损坏。
- 合成依赖图层命名、顺序和透明 PNG；示例顺序不能视为所有引擎规范。

**应用：** 把规则文件与层图配套验证；不从文件名盲目枚举全组合。

**边界：** 工具是特定规则的浏览／合成入口，不能证明批量规则兼容。


<a id="t07"></a>
## T07 — pfs-rs README

原文：[pfs-rs README](https://github.com/sakarie9/pfs-rs) · 作者：sakarie9 · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Extract command / Output directory behavior

- 多包输入默认可能归到同一输出根；--separate 可分包保留。
- 目录裁剪和 system.ini 智能检测会影响输出路径。

**应用：** 先分包提取并保存原内部路径；证明补丁优先级后再生成当前视图。

**边界：** 仅作者文档核读；与作者 PFS 格式博客是不同资料。


<a id="t08"></a>
## T08 — BGI-Hazuki README

原文：[BGI-Hazuki README](https://github.com/ArisuMika520/BGI-Hazuki) · 作者：ArisuMika520 · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Output Rules / Standalone Tools

- 输出位于当前工作目录的 unpack；自动转换后会删除该输出中的 CBG 原件。
- BF_Movie 可导出带时序的帧；DSC、bw 音频仍需保留原二进制以维持关联。

**应用：** 候选工具只在副本和独立 cwd 试用；转换前保留 raw 并记录 CP932 等参数。

**边界：** 未安装或实测；作者的游戏根目录建议不作为本 skill 的默认执行方式。


<a id="t09"></a>
## T09 — QLIE Unpacker README

原文：[QLIE Unpacker README](https://github.com/rafi441/qlie-unpack) · 作者：rafi441 · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Compatibility / CLI / Features

- 作者区分 FilePack 1.0／2.0／3.0／3.1 的 key 路径；EXE key 提取限定于适用的 3.0。
- 作者声明可处理嵌套 ABMP、DPNG 和 IMOAVI；--list --json 给出目录元数据，提取 JSON 另含输出路径、解码大小与 SHA-256。

**应用：** 作为 QLIE 候选路线：核对包版本、同版本 key 来源，先 list 再小样本。

**边界：** README 安装示例仍有占位仓库说明；作者测试名单不是本机验收，不能直接执行未核对命令。


<a id="t10"></a>
## T10 — SiglusExtract README

原文：[SiglusExtract README](https://github.com/xmoezzz/SiglusExtract) · 作者：xmoezzz · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：How to use / Supported resource types / OMV

- 主程序需要启动游戏相关运行流程；Scene.pck 和 Gameexe.dat 有精确命名要求。
- 32 位 OMV 含透明数据，普通视频输出可能无法保存；PNG 帧路线更适合检查。

**应用：** 保留当前的启动前询问边界；离线候选先行，视频检查透明度与体积。

**边界：** 作者已声明停止开发；本轮没有运行游戏或工具。


<a id="t11"></a>
## T11 — siglus-static-key-tool README

原文：[siglus-static-key-tool README](https://github.com/xmoezzz/siglus_static_key_tool) · 作者：xmoezzz · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Recovery modes / Usage

- 资源模式使用同一游戏构建的 Gameexe.dat 和 Scene.pck，不要求启动 EXE。
- 静态 PE32 分析是另一条路线，资源可用于校验候选 key。

**应用：** Siglus 解密失败时先找配套资源和离线候选；记录模式及双资源校验结果。

**边界：** 只适用于作者说明的标准 Siglus EXE-key 流，改版不能直接套用。


<a id="t12"></a>
## T12 — Siglus Resource-Key Recovery Writeup

原文：[Siglus Resource-Key Recovery Writeup](https://github.com/xmoezzz/siglus_static_key_tool/blob/main/writeup.md) · 作者：xmoezzz · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Scene Header Constraints / Hard Validation

- 结构验证检查偏移、数量、范围和引用关系，不能靠猜测固定头字段。
- 候选 key 要通过完整 Gameexe 解码及多 Scene 解压与结构校验，而非只看一个前缀。

**应用：** 把独立资源、完整流和尺寸检查作为新离线解析器验收原则。

**边界：** 作者实录的样本数与耗时不代表本机结果；本条是方法参考。


<a id="t13"></a>
## T13 — KrkrExtract README

原文：[KrkrExtract README](https://github.com/xmoezzz/KrkrExtract) · 作者：xmoezzz · 语言：zh · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Maintenance / Universal Dumper / Separated tools

- 作者说明停止维护、定制引擎兼容有限；Universal Dumper 有速度和内存代价。
- 可先检查配套独立工具，不应把动态抓取作为每次首选。

**应用：** 将动态流程列为需用户决定的后备；失败日志注明引擎定制与工具版本。

**边界：** 不把作者的修改 EXE 建议转成自动步骤；未执行动态方案。


<a id="t14"></a>
## T14 — TriggersTools.CatSystem2 README

原文：[TriggersTools.CatSystem2 README](https://github.com/trigger-segfault/TriggersTools.CatSystem2) · 作者：trigger-segfault · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Features

- 该库分别覆盖 KIF 归档、HG 图片及 CST／FES／ANM 脚本；作者注明仍在开发。

**应用：** 将 CatSystem2 拆成容器、图片和脚本三个候选适配点。

**边界：** 没有本机 CatSystem2 新验收；功能声明仅用于寻找实现入口。


<a id="t15"></a>
## T15 — omvdecoder README

原文：[omvdecoder README](https://github.com/xmoezzz/omvdecoder) · 作者：xmoezzz · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Usage / Piped PNG Stream Protocol

- 文档给出 RGBA PNG 帧、分数帧率、PTS 和帧字节数的管道协议。
- README 的文件输出用法与后文 stdout 协议有不一致，需核对固定版本和 --help。

**应用：** 候选适配按二进制帧长度读取并保留透明度、时序；实现前先解清接口差异。

**边界：** 未下载或运行；文档冲突未解决前不生成可直接执行的通用命令。 PTS 默认取 frame_id，文档未独立定义时间单位，不能直接当作秒或其他时间基准。


<a id="t16"></a>
## T16 — PSB Shells, Types, Platforms

原文：[PSB Shells, Types, Platforms](https://github.com/UlyssesWu/FreeMote/wiki/PSB-Shells,-Types,-Platforms) · 作者：UlyssesWu · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Shells / Archive

- MDF／MFL／MZS／MXB 壳与内部 PSB 加密是不同层。
- MT19937 的 seed 可依赖原文件名；info.psb.m 与 body.bin 必须配套。

**应用：** 保留原 basename、壳参数及配对关系；先拆壳，再按内部类型选择操作。

**边界：** key buffer 长度的常见值不能当常量；本轮不扩大 PSB 支持声明。


<a id="t17"></a>
## T17 — FreeMote CommandLine Usage for Tools

原文：[FreeMote CommandLine Usage for Tools](https://github.com/UlyssesWu/FreeMote/wiki/CommandLine-Usage-for-Tools) · 作者：UlyssesWu · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：PsbDecompile image / unlink / info-psb

- image、unlink 和 info-psb 的输入与用途不同；单独 body.bin 不是 info-psb 入口。
- 外置纹理顺序有 Name／Order／Convention 等选择，不能随意排序。

**应用：** 按资源类型调用子命令，并在 recipe 记录纹理顺序及 body 配对。

**边界：** CLI 示例存在拼写差异，执行前以本机固定版本帮助为准。


<a id="t18"></a>
## T18 — FreeMote Plugins & External Tools

原文：[FreeMote Plugins & External Tools](https://github.com/UlyssesWu/FreeMote/wiki/Plugins-&-External-Tools) · 作者：UlyssesWu · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Image Formatter / Shell / Enable Plugins

- 启用 TLG 插件后可能只留 PNG；没有插件时 TLG 与预览 PNG 的引用关系不同。
- 图像解码与编码对外部依赖的要求不同，不能因缺编码工具就断言不能解码。

**应用：** 盘点插件及架构，先保留 raw，再按当前功能缺口决定依赖。

**边界：** 插件存在不等于当前文件可解；本轮未改变本机依赖。


<a id="t19"></a>
## T19 — About the CST format

原文：[About the CST format](https://github.com/trigger-segfault/TriggersTools.CatSystem2/issues/2) · 作者：AtomCrafty · 语言：en · 类型：firsthand-forum

来源依据：维护者或原研究者直接发布的正文；定位：Original disassembly findings

- 原研究者更正所谓 Input Offset Table 为脚本块列表；一个块可含多条 message。
- 行类型、脚本名和行号元数据需要分别处理。

**应用：** 文本提取保留块和行顺序，避免把任意字符串拼接当作剧情阅读顺序。

**边界：** 这是原作者针对所分析编译器的发现；新版本仍需样本确认。


<a id="t20"></a>
## T20 — HG-3 Image format research

原文：[HG-3 Image format research](https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki/HG%E2%80%903-Image) · 作者：Robert Jordan / trigger-segfault · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：Frame Structure / stdinfo / img_jpg / img_al

- HG-3 可包含多个按 ID 引用的帧；stdinfo 保存裁剪尺寸、偏移和完整画布信息。
- JPEG 图像可能依赖独立 img_al 遮罩，不能只 carving JPEG 就判完整。

**应用：** 交付按帧计数并恢复画布，检查独立 alpha；未知标签保留并标记。

**边界：** 部分标签和含义在原文仍未确定；不能把推测字段当通用规范。


<a id="t21"></a>
## T21 — CGList Data format research

原文：[CGList Data format research](https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki/Format:-CGList-Data) · 作者：Robert Jordan / trigger-segfault · 语言：en · 类型：author-doc

来源依据：维护者或原研究者直接发布的正文；定位：CGTable / CGFrame

- CGList 使用表、帧组和文件规格列表；表号不一定是数组下标，文件规格也不一定是单个文件名。

**应用：** 可用 CG 菜单索引建立分类和差分候选关系，解析相对偏移时核对边界。

**边界：** 原文对部分名称关联保留推测；菜单索引不是全资源覆盖证明。
