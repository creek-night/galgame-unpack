# 第二轮资料：引擎资源、状态与版本

核读于 2026-10-21 至 22 日。本页收录 37 个新增独立正文资料；同页章节、转载、镜像和旧目录重复不计数。以下是作者或规范支持的事实与据此形成的检查建议；本轮没有新增本机游戏验收。

<a id="e201"></a>
## E201 — Ren’Py — File Access

原文：[Ren’Py — File Access](https://www.renpy.org/doc/html/file_python.html) · 作者：Ren’Py / Tom Rothamel · 语言：en · 类型：official_manual

- 资源可能来自游戏目录、RPA 包或 Android assets；list_files 同时列出目录与归档资源。
- loadable 会考虑归档和可选翻译目录，exists 仅检测实际磁盘文件。

**应用：** 离线清单必须合并 loose files、归档条目和本地化候选；不能用磁盘文件不存在判为资源缺失。

**限制：** 文档为 8.5.4；这些是引擎资源语义，不代表离线工具能直接调用；禁止为探测资源而擅自运行游戏。

<a id="e202"></a>
## E202 — Ren’Py — Persistent Data

原文：[Ren’Py — Persistent Data](https://www.renpy.org/doc/html/persistent.html) · 作者：Ren’Py / Tom Rothamel · 语言：en · 类型：official_manual

- persistent 保存不属于某一剧情位置的数据，图库解锁可由其字段控制。
- 跨来源数据默认逐字段采用较新值，也可注册合并函数；双下划线字段带有文件名相关的名称改写。

**应用：** 区分 CG 原文件存在与图库是否解锁；公开包不得夹带用户 persistent、存档或由其泄露的进度。

**限制：** 8.5.4 文档；不同游戏可自定义字段/合并方式；研究不读取或改写玩家存档。

<a id="e203"></a>
## E203 — Ren’Py — Matrixcolor

原文：[Ren’Py — Matrixcolor](https://www.renpy.org/doc/html/matrixcolor.html) · 作者：Ren’Py / Tom Rothamel · 语言：en · 类型：official_manual

- 引擎上传纹理时使用预乘 alpha，颜色矩阵在这一表示上工作。
- 矩阵可组合且按从右到左顺序作用，ColorMatrix 可随 ATL 动画插值。

**应用：** 遇到同一立绘的色调差分，应记录 matrixcolor 与求值时点；合成器先明确直通/预乘 alpha，避免黑边与错色。

**限制：** 8.5.4 文档；静态原图导出不等于含着色/动画的屏幕结果；自定义矩阵需独立验证。

<a id="e204"></a>
## E204 — Naninovel — Resource Providers

原文：[Naninovel — Resource Providers](https://naninovel.com/guide/resource-providers) · 作者：Naninovel / Elringus · 语言：en · 类型：official_manual

- 每类资源的 Loader 具有 Path Prefix 与有顺序的 Providers List，可依次使用 Addressables、Project 或 Local 来源。
- 编辑器存在优先的 Editor provider；构建时才把所配置资源复制到临时 Resources 或编入 Addressables。

**应用：** Unity/Naninovel 侦察同时查资源地址、前缀和 provider 顺序；只凭编辑器目录/文件名不能证明发布版当前素材来源。

**限制：** 官网当前 v1.21；项目可自定义 provider 与远程资源，必须按实际构建配置核对。

<a id="e205"></a>
## E205 — Ren’Py — Transforms / ATL

原文：[Ren’Py — Transforms / ATL](https://www.renpy.org/doc/html/transforms.html) · 作者：Ren’Py / Tom Rothamel · 语言：en · 类型：official_manual

- at 后的多个 transform 从左到右应用；ATL 可放在 transform、image 或 show/scene 块中。
- ATL 表达式在 transform 首次执行时求值，而非执行到每一条语句才重新求值。

**应用：** 记录图像定义与调用处的变换链、参数和时间；不能把动画块内所有引用视为同时叠加的差分。

**限制：** 8.5.4 文档；事件驱动和 Python transform 可能不能静态求值，应标为待解析。

<a id="e206"></a>
## E206 — YU-RIS — ＣＧレイヤ

原文：[YU-RIS — ＣＧレイヤ](https://yu-ris.net/manual/yu-ris/html/basic/layer.html) · 作者：YU-RIS 项目（yu-ris.net 官方手册） · 语言：ja · 类型：official_manual

- CG 图层由 ID 管理，Z 值越大越靠前；相同 Z 的重叠次序不确定。
- ID 结尾斜杠表示图层集合，集合可整体蒙版/绘制；默认集合 W0，图层路径与磁盘文件路径是不同概念。

**应用：** 合成时建立图层树与集合蒙版，保留 Z；相同 Z 无其他证据时标记层序不确定，避免按文件名排序。

**限制：** 官网传统 YU-RIS 手册，页内未标全局版本；不能据此断言所有 ERIS 或定制版本一致。

<a id="e207"></a>
## E207 — YU-RIS — 基本文法

原文：[YU-RIS — 基本文法](https://yu-ris.net/manual/yu-ris/html/basic/basic.html) · 作者：YU-RIS 项目（yu-ris.net 官方手册） · 语言：ja · 类型：official_manual

- 命令键值可调换顺序，值可为算式，一行可以含多个命令并夹杂显示文本。
- 文本宏包含换行、分页、点击等待；_[表达式] 可插入变量值，半角假名显示规则具有版本变化。

**应用：** 文本提取采用词法/语法分离而非逐行删标签；保留未知表达式占位及版本信息，避免把控制符和变量名输出成对白。

**限制：** 文章举出 0.167/0.226 规则变化；CP932 是本页编码，不能因此推定所有游戏脚本编码。

<a id="e208"></a>
## E208 — Monogatari — Characters

原文：[Monogatari — Characters](https://monogatari.io/v2/building-blocks/characters) · 作者：Monogatari / Hyuchia · 语言：en · 类型：official_manual

- 角色 sprite ID 与真实文件名互相独立；directory 为 assets/characters 下的子目录。
- sprites 和对话侧头像 expressions 是不同表；默认 expression 可在未明确指定时生效。

**应用：** 为角色建 ID→文件路径映射，分开完整立绘与侧头像；不能靠对白中的标识符直接拼 PNG 名称。

**限制：** v2 文档；项目可改目录/代码，实验图层功能必须核对配置。

<a id="e209"></a>
## E209 — Monogatari — Variables & Data Storage

原文：[Monogatari — Variables & Data Storage](https://monogatari.io/v2/building-blocks/data-storage) · 作者：Monogatari / Hyuchia · 语言：en · 类型：official_manual

- storage.js 可声明需随存档保存的玩家变量及默认值。
- monogatari.storage 的对象更新会合并传入值，不是替换整个原对象。

**应用：** 分析可变角色名/资源引用时保留初始值与变更链；发布研究样本只用源码默认值，避免带上玩家保存数据。

**限制：** v2 文档；动态函数和存档分支不能仅由默认值确定。

<a id="e210"></a>
## E210 — Monogatari — Show Character Layer

原文：[Monogatari — Show Character Layer](https://monogatari.io/v2/script-actions/character-layers) · 作者：Monogatari / Hyuchia · 语言：en · 类型：official_manual

- 分层按 layers 数组从后到前叠放；添加图层前父角色必须已经显示。
- show/hide 可独立变更部件并带 CSS 动画；图层状态与回退历史分别保存。

**应用：** 按脚本执行顺序维护当前部件状态和隐藏操作；使用实际出现组合，保留 CSS/动画造成的未复现效果。

**限制：** 官网明确标为 Experimental 且须启用 ExperimentalFeatures；语法可能变化，不能外推至全部 v2 游戏。

<a id="e211"></a>
## E211 — TyranoScript — キャラクター操作

原文：[TyranoScript — キャラクター操作](https://tyrano.jp/usage/tech/chara) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official_manual

- chara_new 把逻辑角色名、文件 storage 和显示名 jname 绑定，定义本身不显示角色。
- chara_show 按在场人数自动计算位置；#角色 ID 用于发言者显示。

**应用：** 保留角色声明映射、显示/隐藏状态和自动布局依赖；分别标注角色 ID 与显示名。

**限制：** 官网教程未钉定精确版本；自定义 chara_config 和插件可改变布局。

<a id="e212"></a>
## E212 — TyranoScript — サブルーチンとマクロ

原文：[TyranoScript — サブルーチンとマクロ](https://tyrano.jp/usage/tech/macro) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official_manual

- call/return 会返回调用处，jump/button/link 跳转不会自动返回；storage 可指定其他场景文件。
- macro 可组合既有标签与文字形成新标签，并用 %参数 接受实参。

**应用：** 跨场景收集宏定义与调用链，展开已知参数后再提取资源；未知宏记录为覆盖缺口而不直接丢弃。

**限制：** 作者教程级语义；任意 JavaScript、插件或递归宏不能保证静态还原。

<a id="e213"></a>
## E213 — Naninovel — State Management

原文：[Naninovel — State Management](https://naninovel.com/guide/state-management) · 作者：Naninovel / Elringus · 语言：en · 类型：official_manual

- 运行状态分为每存档 Game state、跨会话 Global state 和 User settings；默认槽可为 .nson 或 .json，WebGL 使用 IndexedDB。
- Game state 可包含角色外观/位置、剧情命令位置及 BGM，而已读信息属于全局状态。

**应用：** 不能用一个存档的可见素材代表全游戏覆盖；公开研究目录排除存档和用户设置，只保留必要的去标识证据。

**限制：** v1.21；自定义序列化 handler 可改存储方式，不应把扩展名当普遍解析保证。

<a id="e214"></a>
## E214 — CatSystem2 — イメージファイル .hg3

原文：[CatSystem2 — イメージファイル .hg3](https://cs2.suki.jp/manual/data/image/img_file.html) · 作者：ARES / Windmill · 语言：ja · 类型：official_manual

- 一个 HG3 文件可含多个数字 ID 图像；普通场景脚本读取 ID 格式时仅显示 ID 0。
- 转换通常裁掉透明区域但保留原画布尺寸，并可写入 base 原点和图像属性。

**应用：** 核对导出器是否完整输出所有 image IDs、偏移和画布元数据；恢复画布与角色原点后再合成。

**限制：** 传统 CatSystem2 作者手册未标当前运行时版本；未证明任一第三方 HG3 导出器保留这些字段。

<a id="e215"></a>
## E215 — CatSystem2 — 差分形式画像

原文：[CatSystem2 — 差分形式画像](https://cs2.suki.jp/manual/data/image/plural.html) · 作者：ARES / Windmill · 语言：ja · 类型：official_manual

- 同一 base 名的图片才能按差分形式组合，差分由 base_差分名 表示。
- 差分名通过零补位区分层级，位数少的先叠放；脚本以逗号形式指定具体差分。

**应用：** 为 CatSystem2 合成解析 base、差分位数和脚本组合，避免字典序排序或枚举不属于同 base 的素材。

**限制：** 只适用于文档规定的差分命名；命名相似本身不足以证实定制游戏采用此约定。

<a id="e216"></a>
## E216 — CatSystem2 — ゲームテキストの記述

原文：[CatSystem2 — ゲームテキストの記述](https://cs2.suki.jp/manual/data/text/text.html) · 作者：ARES / Windmill · 语言：ja · 类型：official_manual

- 行首全角内容可为姓名，正文以半角空格/制表分隔；// 后为注释。
- [单词/ruby] 表示注音，圆圈数字可指外字；空行切分消息而非单纯排版。

**应用：** 可选剧情导出保留 speaker、ruby 和外字引用；不能统一删方括号或把注释里的旧台词计为已使用剧情。

**限制：** 作者场景源语法；编译 CST 的解码另需格式证据，单靠本页不能反编译。

<a id="e217"></a>
## E217 — CatSystem2 — 名前テーブル nametable.csv

原文：[CatSystem2 — 名前テーブル nametable.csv](https://cs2.suki.jp/manual/data/setup/nametable.html) · 作者：ARES / Windmill · 语言：ja · 类型：official_manual

- nametable.csv 虽名为 CSV，实际是 tab 分隔；映射姓名显示图和 face 窗图。
- 人物名可为简称，%f 代表立绘前缀、%n 代表数字部分，不能用显示名反推唯一文件。

**应用：** 检测 TSV 而非逗号拆分；借助表建立人物与头像/立绘映射，减少把 side image 当完整立绘。

**限制：** 文件只在相关姓名图/face 功能启用时需要，缺失不能作为拆包失败。

<a id="e218"></a>
## E218 — CatSystem2 — CGリストテーブル cglist.txt

原文：[CatSystem2 — CGリストテーブル cglist.txt](https://cs2.suki.jp/manual/data/setup/cglist.html) · 作者：ARES / Windmill · 语言：ja · 类型：official_manual

- 图库表定义 CG 与具体差分组合，但作者可以故意省略部分在剧情中使用的组合。
- cgflag/cgreg 还可注册未在剧情显示过的差分或奖励图；图库顺序由表中顺序决定。

**应用：** 将 cglist 作为高价值组合依据，同时与场景引用交叉验证；区分图库收录、剧情使用、奖励图三个证据类别。

**限制：** 图库不能单独证明全量覆盖或实际出场；编译 .dat 解析需另外核实。

<a id="e219"></a>
## E219 — TyranoScript — 変数と演算を活用する

原文：[TyranoScript — 変数と演算を活用する](https://tyrano.jp/usage/tech/hensuu) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official_manual

- f 随存档、sf 跨存档、tf 临时；加载不同存档会覆盖游戏变量。
- emb 用于显示变量，属性前缀 & 可把变量值注入标签，连续逻辑也可放在 iscript 中。

**应用：** 资源路径出现 & 时尝试有边界的常量传播，无法确定则保留表达式；不得执行任意 iscript 来做索引。

**限制：** 官方教程未钉定版本；同名 f/sf/tf 并不代表与 KAG 的 TJS 语言完全兼容。

<a id="e220"></a>
## E220 — TyranoScript — CG・回想モードをつくる

原文：[TyranoScript — CG・回想モードをつくる](https://tyrano.jp/usage/tech/cg) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official_manual

- V400+ 的模板通过 cg 标签解锁，cg_image_button 的 graphic、no_graphic、folder 分别表示实际图、未解锁占位图与目录。
- 回想可跳入指定 storage/target，tf.system.flag_replay 让其走不同初始化分支。

**应用：** 资源分类排除图库未解锁占位图，记录回想入口和专用初始化；不可只扫描主线即认定已覆盖全部组合。

**限制：** 模板可重写；页面 CG 示例甚至使用背景图，因此图库标签不自动等同于用户定义的事件 CG。

<a id="e221"></a>
## E221 — KAG — 変数を使おう

原文：[KAG — 変数を使おう](https://krkrz.github.io/krkr2doc/kag3doc/contents/Var.html) · 作者：W.Dee / KiriKiri 项目维护文档 · 语言：ja · 类型：official_manual

- KAG 的 f/sf/tf 分别对应存档、持久与临时变量，底层是 TJS2。
- & 后实际上是 TJS2 表达式，不只限单一变量；+ 可进行字符串拼接与类型转换。

**应用：** 静态资源解析识别表达式与字符串拼接；只求值白名单语法，未知 TJS 记为缺口，不用 JavaScript eval 替代。

**限制：** KAG3/TJS2 手册；变量名和表达式不是 JavaScript 的完整等价物。

<a id="e222"></a>
## E222 — KAG — マクロを使おう

原文：[KAG — マクロを使おう](https://krkrz.github.io/krkr2doc/kag3doc/contents/Macro.html) · 作者：W.Dee / KiriKiri 项目维护文档 · 语言：ja · 类型：official_manual

- 宏可通过 %属性 替换参数，* 透传全部属性，竖线提供未传参默认值。
- 宏中的其他宏会继续展开；属性名要求小写。

**应用：** 组合脚本解析应支持参数默认、透传和嵌套展开，并设置递归/展开预算；单纯搜索 image 标签会漏掉宏封装引用。

**限制：** KAG 宏语义；对运行时生成宏/自定义 TJS 仍需独立证据。

<a id="e223"></a>
## E223 — KAG — 画像形式について

原文：[KAG — 画像形式について](https://krkrz.github.io/krkr2doc/kag3doc/contents/GraphicFormats.html) · 作者：W.Dee / KiriKiri 项目维护文档 · 语言：ja · 类型：official_manual

- TLG5 与 TLG6 均用 .tlg，TLG6 自 KiriKiri2 2.21 beta3 起可用。
- JPEG 立绘须把主图与蒙版分离；color-key 透明与 alpha 半透明产生不同边缘。

**应用：** 按魔数/结构区分 TLG 版本，保留主图/蒙版对应关系并检查半透明边缘；扩展名不可当版本判定。

**限制：** 历史手册的速度/压缩比较不作为当代性能结论；插件可能增加格式。

<a id="e224"></a>
## E224 — KAG — KAG 3 未満からの移植と KAG 3 での新機能

原文：[KAG — KAG 3 未満からの移植と KAG 3 での新機能](https://krkrz.github.io/krkr2doc/kag3doc/contents/PortFromOldKAG.html) · 作者：W.Dee / KiriKiri 项目维护文档 · 语言：ja · 类型：official_manual

- KAG3 默认忽略场景物理换行，Config.tjs 可恢复旧行为；动画信息由 asq 改为 asd。
- 多数标签可带 cond 条件，文本输出支持 UTF-16；预渲染字体可包含环境本来没有的外字。

**应用：** 在文本和动画解析前读配置/版本线索，保留 cond 分支；不要统一按换行切句或把 asd 误当无关文件。

**限制：** 这是旧版迁移差异表，并非所有现代 KrkrZ 定制版本的完整规范。

<a id="e225"></a>
## E225 — Visual Novel Maker — Resource Manager

原文：[Visual Novel Maker — Resource Manager](https://asset.visualnovelmaker.com/help/Resource_Manager.htm) · 作者：DEGICA / Visual Novel Maker · 语言：en · 类型：official_manual

- 旧手册将资源组描述为纯逻辑组织，多个组也不能重复同名文件。
- 自动更名会尝试更新场景和数据库引用，但文本变量及脚本存在未覆盖例外。

**应用：** 对旧版资源索引区分逻辑组和磁盘目录；引用失配要检查重命名/动态变量，并与新版迁移公告交叉核对。

**限制：** 旧在线帮助；资源分组规则已在 1.0.1101 相关更新发生变化，不能作为新版本默认规则。

<a id="e226"></a>
## E226 — Visual Novel Maker — Resource Standards

原文：[Visual Novel Maker — Resource Standards](https://asset.visualnovelmaker.com/help/Resource_Standards.htm) · 作者：DEGICA / Visual Novel Maker · 语言：en · 类型：official_manual

- 角色动画使用逐帧图片，而 Pictures 动画使用 sprite sheet；UI frame/three-part 图则按边角和伸缩区拼接。
- 旧 Live2D 导入流程把模型、motions、expressions 收入 .live2d 归档，文档注明其为 ZIP。

**应用：** 按资源用途决定拆帧还是还原 UI；先检测 .live2d 容器结构并保持依赖文件，而非把单张纹理当可用角色。

**限制：** 旧帮助以 .model.json 时代为基准；后续 Live2D4 和新运行时需核对公告。

<a id="e227"></a>
## E227 — Visual Novel Maker — Create Game Package

原文：[Visual Novel Maker — Create Game Package](https://asset.visualnovelmaker.com/help/Create_Game_Package.htm) · 作者：DEGICA / Visual Novel Maker · 语言：en · 类型：official_manual

- 旧 Windows 发布包中的 Game.exe 是运行时入口，游戏资料位于 data/resources，HTML 入口是 index.html。
- 打包有 Encrypt Content 选项，平台会改变发布包结构。

**应用：** 侦察应先定位 data/resources 与配置，避免把 NW.js 附带 .pak 当游戏资源；记录加密选项的可能性而不直接宣称可解。

**限制：** 旧帮助描述 NW.js；2022 v1.0.1111 起有 Electron 迁移，必须检查实际版本。

<a id="e228"></a>
## E228 — Visual Novel Maker — Update to the stable branch（2020-08-07）

原文：[Visual Novel Maker — Update to the stable branch（2020-08-07）](https://steamcommunity.com/games/495480/announcements/detail/2744333355093681119) · 作者：DEGICA Dev（Visual Novel Maker 官方 Steam 公告） · 语言：en · 类型：author_release_note

- 新版资源管理取消固定目录，逻辑分组迁移为真实子目录，允许不同子目录同名文件。
- Show Picture/Background 不再绑定旧 Graphics 目录；Live2D 仍要求 resources/Live2D。

**应用：** 将引擎版本和实际资源路径加入侦察证据；保留完整相对路径用于去重与映射，避免套用旧帮助造成覆盖。

**限制：** 公告安排 v1101 稳定分支迁移；旧 v1093 分支仍可存在，不能按游戏发行年份单独判定。

<a id="e229"></a>
## E229 — Visual Novel Maker — Update to STABLE branch!（2022-06-22）

原文：[Visual Novel Maker — Update to STABLE branch!（2022-06-22）](https://steamcommunity.com/games/495480/announcements/detail/3362515187780900893) · 作者：Kentou（Visual Novel Maker 官方 Steam 公告） · 语言：en · 类型：author_release_note

- v1.0.1111 稳定更新把游戏运行时由 NW.js 迁移为 Electron，NW.js 专属扩展可能不再工作。
- 选择 App Data 存档时，Windows 位置从 AppData/Local 改为 AppData/Roaming。

**应用：** 识别 Web 桌面包时同时支持 NW.js 和 Electron 的结构线索；不要把运行时 DLL/.pak 误分类为游戏素材，也不要把存档混入发布资料。

**限制：** 只说明该上游更新；旧运行时游戏和作者定制包仍可能采用不同方式。

<a id="e230"></a>
## E230 — Suika3 — NovelML Syntax Reference

原文：[Suika3 — NovelML Syntax Reference](https://suika3.vn/en/docs/novelml-syntax/) · 作者：Suika3 / awemorris · 语言：en · 类型：official_manual

- NovelML 包括对白在内都写在标签中；async 动画可以与后续标签并行。
- 变量均按字符串保存，${...} 在标签执行时展开；load 可切到另一文件及标签。

**应用：** 为 .novel 解析建立标签/分支/跨文件依赖图，时间敏感效果单列；不能用删标签方式提取文本。

**限制：** 当前 Suika3 文档；不可套用于 Suika2 原场景语法，动态 Ray 扩展另需分析。

<a id="e231"></a>
## E231 — Suika3 — Anime

原文：[Suika3 — Anime](https://suika3.vn/en/docs/anime/) · 作者：Suika3 / awemorris · 语言：en · 类型：official_manual

- 动画文件描述图层变换序列，时间以秒表示，r 前缀表示相对偏移。
- 引擎规定背景、后景效果、角色/eye/lip、前景效果、UI 等层序；旋转与缩放带中心坐标。

**应用：** 分层还原记录原点、相对/绝对坐标与采样时刻；将 eye/lip 图层识别为角色差分而非独立角色。

**限制：** 官方当前章节；具体作品可用 Ray 自定义渲染，动画中间帧不应冒充原始静态 CG。

<a id="e232"></a>
## E232 — Suika3 — Lip Synchronization

原文：[Suika3 — Lip Synchronization](https://suika3.vn/en/docs/lip-sync/) · 作者：Suika3 / awemorris · 语言：en · 类型：official_manual

- 唇动素材位于角色图片目录下的 lip 子目录，沿用角色图文件名。
- 每帧尺寸与主角色图相同，多个差分帧水平排列，边缘 alpha 需要平滑。

**应用：** 按目录和同名关系建立 base↔lip 映射，按主图尺寸拆横向帧；保留原图集和帧索引，不将整幅长条当立绘。

**限制：** 本章配置文件称 project.txt，而同站 Config 章称 config.ini，存在文档不一致；解析前以实际构建和文件为准。

<a id="e233"></a>
## E233 — Suika3 — Config Reference

原文：[Suika3 — Config Reference](https://suika3.vn/en/docs/config/) · 作者：Suika3 / awemorris · 语言：en · 类型：official_manual

- config.ini 把消息框、选择框各状态和 click 动画图的路径与位置分开配置。
- 文本可切换多个字体，emoji 标识符映射到图片文件；字形图片并非独立 CG。

**应用：** 用配置引用辅助标注 UI/文字内图片，保留字体与 emoji 依赖用于可选剧情展示，避免纳入默认 CG/立绘结果。

**限制：** 同站存在 project.txt/config.ini 命名不一致；文档说明不构成对本机 Suika3 游戏的验证。

<a id="e234"></a>
## E234 — RenJS — Official Documentation（资源声明、图集与定位章节）

原文：[RenJS — Official Documentation（资源声明、图集与定位章节）](https://renjs.net/docs-page.html) · 作者：RenJS / lunafromthemoon · 语言：en · 类型：official_manual

- 故事引用 Setup YAML 中的逻辑 key，Boot 配置列出 GUI/Setup/Story 文件位置；looks 与 portraits 分别对应角色外观和对话侧头像。
- CG 可为 sprite sheet，帧由尺寸与动画起止编号定义；角色默认锚点为底部中心。

**应用：** 先解析 Boot→Setup→Story 引用链，保持 key/路径和 side-image 分类；合成位置不能一律按左上角。

**限制：** 一份长文档只计一条；引擎所谓 CG 范围比本 skill 的事件 CG 宽，自定义插件与 lazy loading 需单独核对。

<a id="e235"></a>
## E235 — Naninovel — Unlockable Items

原文：[Naninovel — Unlockable Items](https://naninovel.com/guide/unlockable-items) · 作者：Naninovel / Elringus · 语言：en · 类型：official_manual

- 默认图库从 CG 前缀的 unlockable 或 MainBackground 资源收集图像；_数字 后缀将多张图归入一个图库槽位。
- 槽位按资源路径名排序；混合来源时默认 unlockable 优先，Cg Sources 可自定义来源和顺序。

**应用：** 将图库组、来源优先和具体资源地址一同写入 manifest；核对 _数字 是变体组，而非盲目去掉尾号做去重。

**限制：** v1.21 默认实现；UI 和资源来源可完全替换，图库不自动代表全部剧情 CG。

<a id="e236"></a>
## E236 — Naninovel — Localization

原文：[Naninovel — Localization](https://naninovel.com/guide/localization) · 作者：Naninovel / Elringus · 语言：en · 类型：official_manual

- 本地化不仅替换文字，还可替换图像和语音；locale 资源可通过独立 Addressables 包按需提供。
- 剧本译文通过稳定 ID 对应源内容，; 行是注释；合并片段中的 | 还代表内嵌命令/表达式位置。

**应用：** 可选中文剧情导出按 ID 关联译文和源上下文；图像默认版本也要检查 locale 替换，缺远程语言包应单列缺口。

**限制：** v1.21；语言目录不是简单整段 .nani 替换，动态 provider 和地区标识差异必须核实。

<a id="e237"></a>
## E237 — YU-RIS — マクロ

原文：[YU-RIS — マクロ](https://yu-ris.net/manual/yu-ris/html/basic/macro.html) · 作者：YU-RIS 项目（yu-ris.net 官方手册） · 语言：ja · 类型：official_manual

- 宏通常定义在 macro.yst，调用以反斜线引出，可替换为一段命令文本。
- 宏后是全角字符或行尾时可省略方括号；r/p/c 系统宏分别控制换行、分页和点击等待。

**应用：** 收集 macro.yst 建字典，依据上下文识别无括号宏；不能对所有反斜线内容做相同删除操作。

**限制：** 传统 YU-RIS 文档；还需按游戏版本核对具体 MACRO 命令的扩展行为。

