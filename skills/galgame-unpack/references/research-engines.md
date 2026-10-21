# 引擎机制与官方手册

核读日期：2026-10-21。37 个独立页面。每条包含原文、作者、适用线索和限制；“应用”是建议的检查步骤，未在本轮执行游戏验收。

按症状先查 [资料导航](research-guide.md)，只读取与当前输入相关的条目。

## 目录

- [E01 Building Distributions](#e01) — Ren'Py / RPA / RPYC
- [E02 Configuration Variables](#e02) — Ren'Py / RPA / patch
- [E03 Layered Images](#e03) — Ren'Py / portrait-composition
- [E04 Displaying Images](#e04) — Ren'Py / image-name / oversampling
- [E05 Translation](#e05) — Ren'Py / dialogue / localization
- [E06 Voice](#e06) — Ren'Py / voice / dialogue-id
- [E07 Audio](#e07) — Ren'Py / audio / loop
- [E08 Dialogue and Narration](#e08) — Ren'Py / dialogue / speaker
- [E09 Displayables](#e09) — Ren'Py / composition / mask
- [E10 Image Manipulators](#e10) — Ren'Py / legacy / mask
- [E11 ストレージシステム](#e11) — KiriKiri / XP3 / storage
- [E12 グラフィックシステム](#e12) — KiriKiri / TLG / alpha / blend
- [E13 Layer.loadImages](#e13) — KiriKiri / mask / metadata
- [E14 画像フォーマットコンバータ](#e14) — KiriKiri / TLG / metadata / PSD
- [E15 Releaser](#e15) — KiriKiri / XP3 / archive
- [E16 KAG3 タグリファレンス](#e16) — KAG3 / script / animation / portrait-composition
- [E17 ONScripter page](#e17) — ONScripter / NScripter / NSA / SAR / NBZ
- [E18 Artemis Engine について](#e18) — Artemis / layers / audio / script
- [E19 キャラ差分パーツ](#e19) — TyranoScript / portrait-composition
- [E20 レイヤーを理解しよう](#e20) — TyranoScript / layers / transition
- [E21 ローカライズ（翻訳）機能](#e21) — TyranoScript / dialogue / localization
- [E22 パッチアップデート機能](#e22) — TyranoScript / patch / TPATCH
- [E23 エクスポート](#e23) — TyranoScript / packaging
- [E24 キャラ差分メイカー](#e24) — TyranoStudio / portrait-composition / validation
- [E25 キャラの目パチ口パクしよう](#e25) — TyranoScript / animation / lip-sync
- [E26 音楽を再生しよう](#e26) — TyranoScript / audio / voice
- [E27 画面キャプチャープラグインが登場。キャラメイクアプリなどが簡単につくれる。無料。](#e27) — TyranoScript / runtime-capture / validation
- [E28 Light.vn入門（Ver：16.8.1）](#e28) — Light.vn / layout / encoding
- [E29 暗号化の除外とその活用](#e29) — Light.vn / encryption / loose-files
- [E30 カスタマイズ（Ver16.8.1）](#e30) — Light.vn / config / script
- [E31 テキスト表示関連コマンド（Ver16.6.1）](#e31) — Light.vn / dialogue / CSV
- [E32 イメージ表示コマンド（Ver16.9.2）](#e32) — Light.vn / image / lip-sync / nine-slice
- [E33 Light.vn 17.9.2 Released!](#e33) — Light.vn / versioning / dialogue-id / animation
- [E34 Storages.addAutoPath](#e34) — KiriKiri / resource-path / patch
- [E35 Storages.getPlacedPath](#e35) — KiriKiri / resource-resolution / verification
- [E36 Layer.operateAffine](#e36) — KiriKiri / affine / blend / sampling
- [E37 Layer.piledCopy](#e37) — KiriKiri / child-layers / coordinates / composition

<a id="e01"></a>
## E01 — Building Distributions

原文：[Building Distributions](https://www.renpy.org/doc/html/build.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- build.classify 决定哪些资源进入哪些 RPA，脚本与图像可能分别归档。
- RPYC 保存对白标识等信息，不能把编译脚本视为可随意丢弃的重复文件。

**应用：** 盘点全部 RPA 与散文件，并保留脚本版本、路径和标识；从打包规则解释资源为何不在预期归档中。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e02"></a>
## E02 — Configuration Variables

原文：[Configuration Variables](https://www.renpy.org/doc/html/config.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- config.archives 按列表次序查找，首个命中的资源生效。
- 默认会以逆 ASCII 顺序收集 game 目录中的归档，但项目能修改该列表。

**应用：** 同路径资源在多个包中出现时先保存各来源，再依据实际配置建立有效版本视图；不要按文件大小或解包先后决定覆盖。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e03"></a>
## E03 — Layered Images

原文：[Layered Images](https://www.renpy.org/doc/html/layeredimage.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- 普通 group 内的属性互斥，multiple 组不互斥；default、when 会影响实际显示。
- auto 组按图像名称模式匹配，variant 与自定义格式函数也会改变资源关联。

**应用：** 读取 layeredimage 声明后生成有依据的立绘组合，记录互斥组、默认状态和条件；不要对所有同名前缀图层做笛卡尔积。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e04"></a>
## E04 — Displaying Images

原文：[Displaying Images](https://www.renpy.org/doc/html/displaying_images.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- images 目录可自动建立图像名，显式 image 声明优先。
- 名称可脱离目录路径；@2 等倍率后缀使显示尺寸小于文件像素尺寸。

**应用：** 建立文件路径到图像名的映射时保留冲突和显式定义；合成坐标使用项目逻辑分辨率与 oversample，避免直接拿像素尺寸推断位置。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e05"></a>
## E05 — Translation

原文：[Translation](https://www.renpy.org/doc/html/translation.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- 对话翻译单元使用标识，并非总与原文逐行一一对应。
- tl/语言 下同相对路径的图像或其他文件可替换原资源。

**应用：** 导出时保留语言、翻译 ID、原脚本位置与原文/译文关系；资产清单同时列出语言覆盖，防止把译文注释重复算成对白。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e06"></a>
## E06 — Voice

原文：[Voice](https://www.renpy.org/doc/html/voice.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- 自动语音通过对白 ID 与 config.auto_voice 路径模板关联。
- 官方对白提取的制表文本包含 ID；多语言语音也可使用 tl 目录覆盖。

**应用：** 需要文本与语音对齐时同时解析显式 voice 指令和 auto_voice 模板；以对白 ID 连接，保留缺失音频与语言差异。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e07"></a>
## E07 — Audio

原文：[Audio](https://www.renpy.org/doc/html/audio.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- 播放路径可以带 from、to、loop 参数，单位为秒。
- 文件完整时长与脚本实际播放片段、后续循环起点可能不同。

**应用：** 导出原音频并额外保存片段及循环元数据；检查脚本前缀后再判断听感截断、循环错位是否属于解码问题。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e08"></a>
## E08 — Dialogue and Narration

原文：[Dialogue and Narration](https://www.renpy.org/doc/html/dialogue.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- 脚本说话人变量通过 Character 定义映射到显示名字，旁白可以没有名字。
- dynamic 名称按语句求值；extend 会延续上一段对白。

**应用：** 文本导出分别保留说话人变量、可静态解析名字和未知动态名字；对 extend 合并建立可追溯记录，避免把每个字符串都当独立台词。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e09"></a>
## E09 — Displayables

原文：[Displayables](https://www.renpy.org/doc/html/displayables.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- Composite 指定画布大小、每层坐标，并按从后到前的顺序组合。
- AlphaMask 使用蒙版 alpha；Flatten 与逐层 alpha 处理的结果可能不同。

**应用：** 按 Composite 的坐标和顺序恢复图像；核对蒙版通道、Flatten 与整体透明度，针对重叠处做像素和视觉检查。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e10"></a>
## E10 — Image Manipulators

原文：[Image Manipulators](https://www.renpy.org/doc/html/im.html) · 作者：Ren'Py 项目 / Tom Rothamel · 语言：en · 类型：official-doc

来源依据：维护方/引擎作者文档

- 旧 im.AlphaMask 使用蒙版红色通道替换 alpha，与新版 AlphaMask 的语义不同。
- 要求两图尺寸和采样倍率相同；多数旧图像操作已被 Transform 替代。

**应用：** 旧作脚本出现 im.AlphaMask 时按红通道还原，保留原蒙版；不要把新旧同名接口混用，先记录引擎代际。

**边界：** 当前读取为 Ren'Py 8.5.4 文档；旧版和游戏自定义代码须另核实。仅文档依据，未运行游戏或验证提取器。


<a id="e11"></a>
## E11 — ストレージシステム

原文：[ストレージシステム](https://krkrz.github.io/krkr2doc/kr2doc/contents/StorageSystem.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 统一存储名使用 URI 式路径，归档内部路径以 > 分隔。
- XP3 可附加到可执行文件，旧版本的归档分隔符曾为 #。

**应用：** 识别没有独立 XP3 的发行版时检查 EXE 内嵌归档；记录原始存储名、源容器与规范化路径，不把统一存储名直接当 Windows 路径。

**边界：** 这是吉里吉里 2 / KAG3 参考文档；商业插件、KrkrZ 和定制加密须单独确认。未做本机解码或合成验证。


<a id="e12"></a>
## E12 — グラフィックシステム

原文：[グラフィックシステム](https://krkrz.github.io/krkr2doc/kr2doc/contents/GraphicSystem.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- TLG5 与 TLG6 共用扩展名；颜色图与 _m 蒙版可分开储存。
- 普通 alpha、addalpha 及 Photoshop 风格混合并非同一种运算。

**应用：** TLG 转图后保留格式版本和混合模式；透明边缘发黑或光效不对时核对加算 alpha，不能只用标准 PNG 叠加判定已还原。

**边界：** 这是吉里吉里 2 / KAG3 参考文档；商业插件、KrkrZ 和定制加密须单独确认。未做本机解码或合成验证。


<a id="e13"></a>
## E13 — Layer.loadImages

原文：[Layer.loadImages](https://krkrz.github.io/krkr2doc/kr2doc/contents/f_Layer_loadImages.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- _m 是不透明度蒙版，_p 是区域图；颜色键也能决定透明区域。
- PNG/TLG 可附带位置与显示模式等标签，loadImages 返回这些信息。

**应用：** 导出图片时同时查找同名伴随文件和标签；区域图只保留为交互元数据，合成前核实蒙版和位置，避免把 _p 当 alpha。

**边界：** 这是吉里吉里 2 / KAG3 参考文档；商业插件、KrkrZ 和定制加密须单独确认。未做本机解码或合成验证。


<a id="e14"></a>
## E14 — 画像フォーマットコンバータ

原文：[画像フォーマットコンバータ](https://krkrz.github.io/krkr2doc/kr2doc/contents/TPC.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 官方转换器可处理主图/蒙版分离，并将显示信息写入 TLG/PNG 标签。
- TLG 的 mode 标签能成为 KAG image 未显式指定模式时的初值。

**应用：** 转成通用图片前保存标签侧车，合成取值顺序同时检查脚本与标签；不要把转换器输入输出格式列表误解为所有方向均支持。

**边界：** 这是吉里吉里 2 / KAG3 参考文档；商业插件、KrkrZ 和定制加密须单独确认。未做本机解码或合成验证。


<a id="e15"></a>
## E15 — Releaser

原文：[Releaser](https://krkrz.github.io/krkr2doc/kr2doc/contents/Releaser.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 打包可合并内容相同但名字不同的文件，也可输出附带归档的 EXE。
- Ogg 代码簿可在包内共享；压缩、排除和索引属性属于打包选项。

**应用：** 清点时区分逻辑文件数与独立数据块数，保留每个路径映射；音频导出不可播放时检查共享代码簿是否由解包器复原。

**边界：** 这是吉里吉里 2 / KAG3 参考文档；商业插件、KrkrZ 和定制加密须单独确认。未做本机解码或合成验证。


<a id="e16"></a>
## E16 — KAG3 タグリファレンス

原文：[KAG3 タグリファレンス](https://krkrz.github.io/krkr2doc/kag3doc/contents/Tags.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- image 可引用省略扩展名的资源，并自动关联 _m、_p、asd 与 ma 伴随数据。
- 页面、图层、颜色键与 mode 会改变显示，属性还可能是 TJS 表达式。

**应用：** 静态脚本分析保留完整 image 参数和伴随文件；追踪前后台页面与动画序列，对动态表达式标为未解析，不只靠图片文件名合成立绘。

**边界：** 这是吉里吉里 2 / KAG3 参考文档；商业插件、KrkrZ 和定制加密须单独确认。未做本机解码或合成验证。


<a id="e17"></a>
## E17 — ONScripter page

原文：[ONScripter page](https://ogapee.github.io/www/onscripter_en.html) · 作者：Ogapee / Studio OGA · 语言：en · 类型：author-doc

来源依据：维护方/引擎作者文档

- 游戏常含 0.txt/nscript.dat、SAR/NSA/NS2 和包外资源，分卷需一并保留。
- 面向掌机的转换可缩小图片；ns2/ns3 与 NBZ 扩展的兼容性有边界。

**应用：** 识别包版本时结合脚本命令，逐卷建清单并检查散文件；遇到小分辨率移植包不能宣称恢复原 PC 画质，NBZ 解码也需单独验证。

**边界：** 作者页面标注 2023-08-25；ONScripter 及其派生分支不是所有 NScripter 命令的完全替代。未运行转换器。


<a id="e18"></a>
## E18 — Artemis Engine について

原文：[Artemis Engine について](https://www.ies-net.com/?page_id=24) · 作者：Artemis Engine / ies-net（Kazu） · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 图层组可整体变换，画面并非一定对应单张原图。
- BGM 前奏与循环段可以分文件；KAG 语法相似仅表示有限脚本共用。

**应用：** 把图层组变换与音频分段纳入待还原信息；不能仅凭 KAG 风格脚本就套用 XP3 路线，先识别具体 Artemis 资源格式。

**边界：** 公开功能说明未给出归档字节格式或解密方法；仅用于识别和范围界定，不证明提取成功。


<a id="e19"></a>
## E19 — キャラ差分パーツ

原文：[キャラ差分パーツ](https://tyrano.jp/usage/tech/chara_layer) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 同尺寸透明 PNG 由 chara_layer 的 part/id 和 zindex 组合，数值大者更靠前。
- 首个注册项是默认差分；隐藏后重显可以保留上一状态，none 可代表不显示。

**应用：** 解析角色定义和差分状态，再生成脚本中有证据的组合；保留默认项、无图项和层序，避免把所有文件独立算为完整立绘。

**边界：** 页面要求 V470_rc4 以上；其示例不代表任意游戏实际使用该机制。官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。


<a id="e20"></a>
## E20 — レイヤーを理解しよう

原文：[レイヤーを理解しよう](https://tyrano.jp/usage/tech/layer) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 背景、前景、消息、free、fix 图层职责不同。
- 前后台页各自保存状态，后台内容在过渡前不会显示。

**应用：** 还原场景时记录页面与过渡完成点；图片存在或已被加载不等于在目标截图可见，提取目标应区分 CG、立绘和 UI。

**边界：** 官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。


<a id="e21"></a>
## E21 — ローカライズ（翻訳）機能

原文：[ローカライズ（翻訳）機能](https://tyrano.jp/usage/advance/translate) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 工具可抽取剧情、角色名和配置过的标签参数，并导出翻译 CSV。
- 自定义宏参数须登记才会进入翻译抽取范围。

**应用：** 核验对白完整性时检查正文、名字、选择项与宏参数；记录当前语言和翻译表，不能用默认抽取条数代替全部可见文本。

**边界：** 正文要求 V600，旧 V530 及以前另有插件；不能假定旧项目原生具备相同翻译系统。官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。


<a id="e22"></a>
## E22 — パッチアップデート機能

原文：[パッチアップデート機能](https://tyrano.jp/usage/studio/patch) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- V5 的补丁用于 PC 打包版，并按项目原目录层级放置更新文件。
- 补丁可能包含新增剧情、图像和相对于初版的累计修改。

**应用：** 拆包入口同时盘点 tpatch 与已展开更新目录，建立来源与覆盖关系；同名素材的有效版本须结合实际补丁应用状态确认。

**边界：** 页面明确针对 V5 以后 PC 包，浏览器和手机形式不适用。官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。


<a id="e23"></a>
## E23 — エクスポート

原文：[エクスポート](https://tyrano.jp/usage/studio/export) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 同一工程能导出不同平台包，桌面目标还区分位数。
- 打包选项可以隐藏素材与脚本，公开目录不是唯一发行形态。

**应用：** 识别引擎后继续查发行形式和包体，不能因看不到明文 data 就否认 Tyrano；隐藏方式需凭样本头和容器证据再选工具。

**边界：** 官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。 文档未说明具体隐藏算法，不能从此页推导解密支持。


<a id="e24"></a>
## E24 — キャラ差分メイカー

原文：[キャラ差分メイカー](https://tyrano.jp/usage/studio/charalayer) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 差分制作器管理部件和层序，可输出定义代码及当前组合代码。
- 当前预览组合可另存为带透明背景的单张图。

**应用：** 已有可读工程且后续授权验证时，可将官方预览导出作对照；独立合成结果应与已知组合比对，不把导入工具当自动恢复所有状态。

**边界：** 这是 TyranoStudio PRO 功能；需要可识别的项目与定义，不是通用解包器。官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。


<a id="e25"></a>
## E25 — キャラの目パチ口パクしよう

原文：[キャラの目パチ口パクしよう](https://tyrano.jp/usage/tech/pachi) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- 眨眼和口型差分与底图保持相同分辨率，帧路径通常相对同一目录。
- frame_image、frame_time 定义顺序和时长；口型还能与角色对白关联。

**应用：** 保存帧序列、时间和角色关联，分别交付静态组合与动画说明；不能把差分 PNG 全部导出就称动画已还原。

**边界：** 页面要求 V525 或 V600 以上；文本驱动和语音驱动口型仍需区分。官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。


<a id="e26"></a>
## E26 — 音楽を再生しよう

原文：[音楽を再生しよう](https://tyrano.jp/usage/tutorial/bgm) · 作者：STRIKEWORKS / シケモクMK · 语言：ja · 类型：official-doc

来源依据：维护方/引擎作者文档

- BGM 与音效/语音使用不同目录和播放标签。
- BGM 默认循环，loop=false 改为单次；可用编码随目标平台和版本而异。

**应用：** 按脚本 playbgm/playse 与实际目录关联音频类型，保存循环标记；导出后用真实解码器检测容器和编码，不只看后缀。

**边界：** 官方制作文档；实际游戏可能含自定义宏、插件或不同引擎版本。本文未安装或运行 Tyrano。 页面浏览器兼容性是特定时期说明，不作为当前所有浏览器保证。


<a id="e27"></a>
## E27 — 画面キャプチャープラグインが登場。キャラメイクアプリなどが簡単につくれる。無料。

原文：[画面キャプチャープラグインが登場。キャラメイクアプリなどが簡単につくれる。無料。](https://tyranos.me/archives/1415) · 作者：シケモクMK · 语言：ja · 类型：author-doc

来源依据：维护方/引擎作者文档

- 作者提供的 capimg 可按对象或图层捕获，并可选择是否包含 UI。
- 输出格式、保存路径与浏览器保存行为有各自参数。

**应用：** 仅在后续获得运行/修改工作副本授权时作为场景对照候选；把捕获分辨率、对象范围、UI 开关和输出格式写入证据，不能替代原资源完整性验证。

**边界：** 作者文章发表于 2019-02-22；插件未下载、未运行，兼容性和透明输出须在目标版本核实。


<a id="e28"></a>
## E28 — Light.vn入門（Ver：16.8.1）

原文：[Light.vn入門（Ver：16.8.1）](https://wikiwiki.jp/lightvn/tutorial) · 作者：Light.vn Wiki 维护组（项目列明 Yukihara Takashi 为 wiki manager） · 语言：ja · 类型：project-wiki

来源依据：Light.vn 官网链接的手册及配套 Wiki；项目发布页确认 Wiki 维护角色。属于项目文档，未推定每页由核心引擎作者署名。

- Data 分列图像、脚本、音频等资源，Config 与保存数据有不同职责。
- 脚本使用 UTF-8，示例说明坐标、层序与透明度共同决定图像显示。

**应用：** 初检按目录职责整理清单，以 UTF-8 读取候选脚本；保留配置与资源路径关系，避免把保存缩略图当原始 CG。

**边界：** 页面为 16.8.1；Wiki 由用户参与维护，版本以页面标题和实际游戏为准；未运行样本，不能据此认定已破解资源。


<a id="e29"></a>
## E29 — 暗号化の除外とその活用

原文：[暗号化の除外とその活用](https://wikiwiki.jp/lightvn/encrypt) · 作者：Light.vn Wiki 维护组（项目列明 Yukihara Takashi 为 wiki manager） · 语言：ja · 类型：project-wiki

来源依据：Light.vn 官网链接的手册及配套 Wiki；项目发布页确认 Wiki 维护角色。属于项目文档，未推定每页由核心引擎作者署名。

- 发布时 Data 通常被加密，但 encrypt_exclusions.txt 可以排除文件或整个目录。
- 明文 CSV 和附赠 CG 可与加密资源共存。

**应用：** 对 Data 同时检查明文与受保护内容；记录排除清单和实际可读范围，不能从少量 PNG/CSV 可读推断整个包都已解开。

**边界：** 排除功能从 16.2.0 起；文档说明打包行为而非解密算法。Wiki 由用户参与维护，版本以页面标题和实际游戏为准；未运行样本，不能据此认定已破解资源。


<a id="e30"></a>
## E30 — カスタマイズ（Ver16.8.1）

原文：[カスタマイズ（Ver16.8.1）](https://wikiwiki.jp/lightvn/customize) · 作者：Light.vn Wiki 维护组（项目列明 Yukihara Takashi 为 wiki manager） · 语言：ja · 类型：project-wiki

来源依据：Light.vn 官网链接的手册及配套 Wiki；项目发布页确认 Wiki 维护角色。属于项目文档，未推定每页由核心引擎作者署名。

- settings.xml 给出分辨率、入口脚本、项目名和保存位置等参数。
- Commands.xml 等配置影响命令和编辑器显示，过时字段不一定继续生效。

**应用：** 静态解析前读取入口、逻辑分辨率和命令配置；报告区分实际数据路径与用户存档路径，避免硬编码默认命令或入口。

**边界：** 页面为 16.8.1；历史字段有弃用说明。Wiki 由用户参与维护，版本以页面标题和实际游戏为准；未运行样本，不能据此认定已破解资源。


<a id="e31"></a>
## E31 — テキスト表示関連コマンド（Ver16.6.1）

原文：[テキスト表示関連コマンド（Ver16.6.1）](https://wikiwiki.jp/lightvn/commands/text) · 作者：Light.vn Wiki 维护组（项目列明 Yukihara Takashi 为 wiki manager） · 语言：ja · 类型：project-wiki

来源依据：Light.vn 官网链接的手册及配套 Wiki；项目发布页确认 Wiki 维护角色。属于项目文档，未推定每页由核心引擎作者署名。

- textTableLoad/textTableLine 可从 Scripts 内 CSV 取正文，首行是列名而数据行从零开始。
- textTableColumn 切换文本列，已有回看记录并不一定同步更新。

**应用：** 文本导出同时解析脚本与 CSV、列名和索引；保留所选语言及历史记录差异，不能只搜引号字符串。

**边界：** 此页为 16.6.1；17.8 作者更新又加入 unique_id，应按目标版本调整映射。Wiki 由用户参与维护，版本以页面标题和实际游戏为准；未运行样本，不能据此认定已破解资源。


<a id="e32"></a>
## E32 — イメージ表示コマンド（Ver16.9.2）

原文：[イメージ表示コマンド（Ver16.9.2）](https://wikiwiki.jp/lightvn/commands/image) · 作者：Light.vn Wiki 维护组（项目列明 Yukihara Takashi 为 wiki manager） · 语言：ja · 类型：project-wiki

来源依据：Light.vn 官网链接的手册及配套 Wiki；项目发布页确认 Wiki 维护角色。属于项目文档，未推定每页由核心引擎作者署名。

- 背景可自动适配窗口；普通图像带坐标与层序，不能用文件尺寸反推截图尺寸。
- sound_cg 可按语音音量切换口型，ninecg 可从九宫格生成不同尺寸 UI。

**应用：** 分类时用命令语义区分背景、立绘口型和 UI；九宫格与动态口型需保留参数，分别验证切片还原和动画。

**边界：** 页面为 16.9.2；部分目录名称文字存在 Image/Images 不一致，必须以实际项目核实。Wiki 由用户参与维护，版本以页面标题和实际游戏为准；未运行样本，不能据此认定已破解资源。


<a id="e33"></a>
## E33 — Light.vn 17.9.2 Released!

原文：[Light.vn 17.9.2 Released!](https://soulengineproject.itch.io/lightvn/devlog/1646828/lightvn-1792-released) · 作者：Soul Engine Project · 语言：en · 类型：author-doc

来源依据：维护方/引擎作者文档

- 17.8 为多种文本/语音查询命令增加 unique_id，官方样例给出对应 CSV。
- 17.8/17.9 调整动画、画面空间、遮罩和文件处理，旧版参数假设可能失效。

**应用：** 版本画像应记录引擎版本与模板；解析 CSV 时同时识别行号和 unique_id，并让静态还原结果受对应版本行为约束。

**边界：** 同页归纳 17.8 至 17.9.2，只算一个来源；作者更新记录不等同于对手头游戏的验证。


<a id="e34"></a>
## E34 — Storages.addAutoPath

原文：[Storages.addAutoPath](https://krkrz.github.io/krkr2doc/kr2doc/contents/f_Storages_addAutoPath.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：引擎作者的吉里吉里 2 API 文档，由 krkrz 项目发布。

- 自动搜索路径后注册的优先，项目目录的优先级还高于自动搜索路径。
- 归档根路径与普通目录使用不同结尾；旧版归档分隔符曾改变。

**应用：** 读取游戏脚本中的路径注册顺序，结合归档内部路径建立有效资源映射，核实补丁或散文件究竟覆盖哪一份资源，不能只按包名或解包顺序覆盖。

**边界：** 这是吉里吉里 2 文档；2.19 beta 14 前后的归档分隔符有差别，游戏自定义查找逻辑及后续引擎分支需另核对。本轮没有运行游戏验证优先级。


<a id="e35"></a>
## E35 — Storages.getPlacedPath

原文：[Storages.getPlacedPath](https://krkrz.github.io/krkr2doc/kr2doc/contents/f_Storages_getPlacedPath.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：引擎作者的吉里吉里 2 API 文档，由 krkrz 项目发布。

- 接口按自动搜索路径查找资源，命中时返回实际所在位置的统一存储名。
- 找不到时返回空字符串，可把资源查找失败与后续图像解码失败分开记录。

**应用：** 在还原计划中分别记录脚本逻辑名、候选存储位置与最终命中位置；以后获准做运行核验时，可用该接口的结果核对静态映射。当前仅建立验证依据，没有执行接口。

**边界：** 结果依赖当时的项目目录及已注册搜索路径；页面没有证明所有路径归一化操作都会检查资源存在。文档针对吉里吉里 2，不能据此宣布具体游戏可解包。


<a id="e36"></a>
## E36 — Layer.operateAffine

原文：[Layer.operateAffine](https://krkrz.github.io/krkr2doc/kr2doc/contents/f_Layer_operateAffine.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：引擎作者的吉里吉里 2 API 文档，由 krkrz 项目发布。

- 参数可表达仿射矩阵或目标三角点；矩阵形式以源矩形左上角作为局部原点。
- 自动混合采用源图层类型，透明度与采样设置会影响合成结果。
- 页面将部分混合模式及插值方式标为未实现，不能把枚举项全部视为可用功能。

**应用：** 还原切片或变换后的立绘时同时保存源裁剪矩形、坐标基准、矩阵、混合及采样参数，并以边缘像素和位置核验输出，避免仅按文件尺寸平铺。

**边界：** 属于旧吉里吉里 2 API 文档，列出的实现限制不能直接套用到所有新版 KiriKiri Z 或定制分支；本轮未执行仿射合成或比对游戏画面。


<a id="e37"></a>
## E37 — Layer.piledCopy

原文：[Layer.piledCopy](https://krkrz.github.io/krkr2doc/kr2doc/contents/f_Layer_piledCopy.html) · 作者：W.Dee / KiriKiri 文档（krkrz 维护发布） · 语言：ja · 类型：official-doc

来源依据：引擎作者的吉里吉里 2 API 文档，由 krkrz 项目发布。

- 该接口先合成源图层及其子图层，再把结果复制到目标。
- 目标坐标以目标图像位置为基准，源裁剪矩形则以源图层的显示位置为基准；两个坐标系不能混用。
- 复制不受源和目标图层的 face 属性影响。

**应用：** 复现截图或场景合成时把子图层树纳入，并分别标注源显示坐标与目标图像坐标；用于解释单层原图与最终画面不一致的原因。

**边界：** 输出只代表当时图层树的合成结果，不能替代原始图层清单或证明动画帧完整。文档针对吉里吉里 2，本轮未执行接口验证。
