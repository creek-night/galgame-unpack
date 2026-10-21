# 博客与论坛实录

核读日期：2026-10-21。35 个独立页面。每条包含原文、作者、适用线索和限制；“应用”是建议的检查步骤，未在本轮执行游戏验收。

按症状先查 [资料导航](research-guide.md)，只读取与当前输入相关的条目。

## 目录

- [B01 SPEED UP！与 galgame 解封包](#b01) — QLIE / SoftPal / Artemis / XP3
- [B02 DC5PH_D.C.5PlusHappiness_初音岛5 (HXV4还原计划1）](#b02) — Hxv4 / XP3 / 名称恢复
- [B03 Galgame 汉化](#b03) — KiriKiriZ / XP3 / SCN
- [B04 Galgame 引擎免封包略谈](#b04) — BGI / Artemis / CMVS / AdvHD / 免封包
- [B05 YuzuMerge[2.0.0.1]](#b05) — PIMG / CG合成
- [B06 【KrkrExtract】喫茶ステラと死神の蝶 イベントCG抽出方法](#b06) — XP3 / PIMG / CG合成
- [B07 AosTools](#b07) — AOS / ABM / MSK / SCR
- [B08 游戏汉化笔记](#b08) — BGI / Yuka / Artemis / 版本差异
- [B09 Galgame解包](#b09) — KiriKiri / 立绘合成 / PIMG
- [B10 Reverse engineering visual novels 101](#b10) — Yuka / YKC / 离线解析
- [B11 ハミダシクリエイティブ（Artemis Engine）高画質化](#b11) — Artemis / PNG坐标 / 立绘
- [B12 StandPdbJson2TxT[1.3.0.1]](#b12) — PBD / 立绘合成 / 名称映射
- [B13 如何用GARbro批量转换pimg文件](#b13) — PIMG / 名称冲突
- [B14 Parsing PFS Files Used by the Artemis Engine](#b14) — Artemis / PFS / pf8
- [B15 Artemis引擎游戏去假名标注(ruby)](#b15) — Artemis / PFS / 文本提取
- [B16 Galgame汉化中的逆向（四）：IDA静态分析psv游戏](#b16) — GSS / LSDARC / BIN索引 / 离线解析
- [B17 Innocent Grey和Noesis社GalGame工具](#b17) — InnocentGrey / IGA / DAT / 脚本
- [B18 gal解包系列Ⅲ：解包通用流程](#b18) — 工具选择 / 版本识别
- [B19 [Case Study][KirikiriZ] Tsumugi no Hanayome](#b19) — KiriKiriZ / SCN / PSB / PIMG
- [B20 (Help!) AQUARIUM - The Hololive VN [.pac files]](#b20) — PAC / 资源雕刻 / 部分成功
- [B21 GAL解包的那些事儿](#b21) — XP3 / 补丁包 / 覆盖率
- [B22 水贴：fvp的立绘合成](#b22) — Favorite / HZC / 立绘合成
- [B23 Obey Me Sprite Assembling?](#b23) — E-mote / PSB / 纹理关联
- [B24 [QLIE] 封包接口Hook](#b24) — QLIE / 外层封装 / ABI
- [B25 04——让萌新也能学会的AI翻译教程——SoftPal引擎](#b25) — SoftPal / SCRIPT.SRC / TEXT.DAT
- [B26 关于以krkr为引擎的galgame解包经验分享](#b26) — KiriKiri / 动态提取 / 覆盖率
- [B27 Ren'Py学习笔记（一）使用layeredimage构建多图层立绘](#b27) — Ren'Py / 立绘合成 / 坐标
- [B28 GalGalgame汉化中的逆向（八）_哈希算法分析_以krkrz_hxv4为例](#b28) — Hxv4 / KiriKiriZ / 名称恢复
- [B29 站在前人的肩膀上对柚子社新作《Limelight Lemonade Jam》进行CG以及立绘合成](#b29) — KiriKiri / PBD / PIMG / 立绘合成
- [B30 【KRKR】拯救老Galgame——老游戏画质提升计划？（智以类聚）](#b30) — KiriKiri2 / 画布 / 层坐标 / 场景坐标
- [B31 《天使騒々RE-BOOT!》解包及CG、立绘合成浅谈](#b31) — KiriKiri / PBD / PIMG / 版本差异
- [B32 GARbro Formats.dat文件格式学习](#b32) — XP3 / GARbro / 索引与内容
- [B33 【解包】获取GalGame类文本、音频方法及格式化对应](#b33) — KiriKiri / SCN / PSB / 文本音频映射
- [B34 [Case Study][KirikiriZ] Koakuma-chan no Yuuwaku](#b34) — KiriKiriZ / XP3 / 验证 / 覆盖率
- [B35 求一个Wild Bug引擎的封包方法](#b35) — Wild Bug / WBP / 版本差异

<a id="b01"></a>
## B01 — SPEED UP！与 galgame 解封包

原文：[SPEED UP！与 galgame 解封包](https://absx.pages.dev/articles/speedup) · 作者：绝对值_x · 语言：zh · 类型：author-blog

来源依据：作者逐作尝试解封包，记录失败工具、错误与成功构建。

- QLIE 包尾的 3.0/3.1 需要记录；同标记作品仍可有不同结果。
- GARbro 导出 OGG 仍可能未解密；应实际解码验证。

**应用：** 路由同时记录包尾、key 文件和工具构建，输出按可解码性验收。

**边界：** 作者的具体作品结果；新作与相同标记不能继承成功。


<a id="b02"></a>
## B02 — DC5PH_D.C.5PlusHappiness_初音岛5 (HXV4还原计划1）

原文：[DC5PH_D.C.5PlusHappiness_初音岛5 (HXV4还原计划1）](https://www.kungal.com/topic/1939) · 作者：devseed / YuriSizuku · 语言：zh · 类型：firsthand-forum

来源依据：作者对 D.C.5 Plus Happiness 的 Hxv4 插件与路径哈希进行分析。

- 包中只有哈希时，内容解密与名称恢复是两项任务。
- 作者将初步 dump 获得的引用字符串与哈希计算结合，仍留下个别语音未匹配。

**应用：** 分别统计解码、原名匹配、目录匹配与未覆盖条目；动态取名另行授权。

**边界：** 该作分析实录，未证明全部资源或其他 Hxv4 版本。


<a id="b03"></a>
## B03 — Galgame 汉化

原文：[Galgame 汉化](https://www.nimisora.top/blog/Galgame/%E6%B1%89%E5%8C%96/) · 作者：Nimisora · 语言：zh · 类型：author-blog

来源依据：作者记录多个游戏的实际提取、翻译与回封尝试。

- D.C.4 Sweet Harmony 中 GARbro 导出的 SCN 疑似解密错误，而另一工具可用。
- Ambitious Mission FD2 的静态路线失败后，作者依赖实际走过流程获得脚本。

**应用：** 为 SCN 增加内容结构检查；动态提取须记录剧情覆盖，不能以文件出现判成功。

**边界：** 只采用作者亲测段落；文末明确复制的区域处理不作证据。


<a id="b04"></a>
## B04 — Galgame 引擎免封包略谈

原文：[Galgame 引擎免封包略谈](https://www.cnblogs.com/Dir-A/p/18096904) · 作者：Dir-A · 语言：zh · 类型：author-blog

来源依据：作者总结自己分析和处理过的引擎读取分支。

- 目录读取可因优先级、配置和读取函数分支不同而表现不同。
- 游戏可能仍期待压缩/加密层；把工具解码后的文件直接交回引擎可失败。

**应用：** 把容器输出、解码输出和引擎期待输入分别标记，禁止推断免封包普遍可用。

**边界：** 作者涉及的变体，非所有同名引擎保证；本轮未修改游戏。


<a id="b05"></a>
## B05 — YuzuMerge[2.0.0.1]

原文：[YuzuMerge[2.0.0.1]](https://ginoaai.seesaa.net/article/471753951.html) · 作者：水瀬 / Ginoa AI · 语言：ja · 类型：author-blog

来源依据：工具作者说明跨游戏实测及自己修复的底图误判。

- 同尺寸差分可能被误当底图；透明底图又使单看透明度不可靠。
- 作者列出空格/符号路径和超过 1000 差分的限制。

**应用：** 底图以元数据与图像关系确认；记录工具版本及路径限制。

**边界：** 2.0.0.1 的修订说明，不应推广为全部 PIMG 正确合成。


<a id="b06"></a>
## B06 — 【KrkrExtract】喫茶ステラと死神の蝶 イベントCG抽出方法

原文：[【KrkrExtract】喫茶ステラと死神の蝶 イベントCG抽出方法](https://note.com/null_base/n/ncdf566875c1a) · 作者：ぬる · 语言：ja · 类型：author-blog

来源依据：作者自己的 Cafe Stella 实践备份，正文有操作及生成目录观察。

- YuzuMerge 完成后会删除临时目录并把输入 PIMG 移至 Clear。
- A 版本合成异常时作者建议对该样本尝试 B 版本。

**应用：** 旧合成器仅在工作副本运行，并记录输入移动及输出映射。

**边界：** 原文归档当前不可达；本人备份只计此一条，未采用其全柚子社泛化。


<a id="b07"></a>
## B07 — AosTools

原文：[AosTools](https://lasriel.moe/posts/AosTools/) · 作者：Lassi Ahonen · 语言：en · 类型：author-blog

来源依据：工具作者陈述自己逆向 AOS 与各子格式的过程和结果。

- SCR 为 Huffman 压缩脚本；ABM 可含压缩图像或多帧。
- MSK 是灰度遮罩，应按用途区分而非判坏图。

**应用：** AOS 拆出后继续识别子格式、帧数与遮罩用途，保留原件。

**边界：** 作者没有完整游戏矩阵；只提供格式候选与核查方向。


<a id="b08"></a>
## B08 — 游戏汉化笔记

原文：[游戏汉化笔记](https://blog.gyx.moe/archives/1293) · 作者：Tabing010102 · 语言：zh · 类型：author-blog

来源依据：作者按具体作品记录自己的提取与汉化失败。

- BGI 脚本可能存在工具未支持的 opcode。
- Artemis 某作 AST 版本不被既有工具支持；引擎名称不足以确定脚本兼容。

**应用：** 记录脚本签名与版本，未知 opcode 停止并保留，不照搬作者跳过策略。

**边界：** 文章含作者称由 AI 操作的后期记录；仅将失败现象作候选，需本机验证。


<a id="b09"></a>
## B09 — Galgame解包

原文：[Galgame解包](https://alzt02.github.io/2025/07/17/%E9%83%A8%E5%88%86gal%E7%9A%84%E8%A7%A3%E5%8C%85/) · 作者：ALZT02 · 语言：zh · 类型：author-blog

来源依据：作者配合自己产出的图示说明姿势与图层分组。

- 先核对立绘规则文件分别对应正身还是侧身。
- 一个表情组不一定覆盖全部；头发遮眼关系可作层序抽查。

**应用：** 按姿势与规则分组，预览头发/眼睛遮挡，记录未组合组。

**边界：** 只采纳具体合成观察；不采用文中万能工具、按年份划分等泛化断言。


<a id="b10"></a>
## B10 — Reverse engineering visual novels 101

原文：[Reverse engineering visual novels 101](https://hackernoon.com/reverse-engineering-visual-novels-101-d0bc3bf7ab8) · 作者：Masumi Nakamura · 语言：en · 类型：author-blog

来源依据：作者从 Koisuru Shimai no Rokujuso 试用版逐字段分析 YKC 容器。

- 用多个容器比较表项及名字位置，验证偏移与长度假设。
- 容器能拆出条目不等于 YKG 图像和 YKS 脚本已解析。

**应用：** 离线解析必须校验字节边界与跨条目一致性，分开容器和子格式验收。

**边界：** 文章只完成 YKC；Windows/CPU/编码推测仍需目标证据。


<a id="b11"></a>
## B11 — ハミダシクリエイティブ（Artemis Engine）高画質化

原文：[ハミダシクリエイティブ（Artemis Engine）高画質化](https://ginoaai.seesaa.net/article/477487124.html) · 作者：水瀬 / Ginoa AI · 语言：ja · 类型：author-blog

来源依据：作者在 Hamidashi Creative 缩放素材后观察错位，并编写坐标迁移工具。

- 该作立绘坐标存于图片注释，重采样会丢失。
- 坐标和画布缩放应一起处理，同时保存原图元信息。

**应用：** 转码前盘点 PNG 文本块/注释；元信息提取为 sidecar 后才缩放或转码。

**边界：** 作者明确仅按此作制作，其他 Artemis 游戏不保证。


<a id="b12"></a>
## B12 — StandPdbJson2TxT[1.3.0.1]

原文：[StandPdbJson2TxT[1.3.0.1]](https://ginoaai.seesaa.net/article/471766432.html) · 作者：水瀬 / Ginoa AI · 语言：ja · 类型：author-blog

来源依据：工具作者记录 Cafe Stella 错位修复与跨盘拖放修复。

- 图层后缀为 .tlg.png 而规则期待 .png，可导致不显示或错位。
- 1.3.0.1 修复从另一磁盘拖入无法输出的行为。

**应用：** 合成前校验规则到实际文件的完整映射；跨盘失败先核对版本和工作目录。

**边界：** 只对应此工具修订；不得无记录直接改原图文件名。


<a id="b13"></a>
## B13 — 如何用GARbro批量转换pimg文件

原文：[如何用GARbro批量转换pimg文件](https://www.kungal.com/topic/2692) · 作者：aquber；kazukikkk · 语言：zh · 类型：firsthand-forum

来源依据：提问者描述自己遭遇的同名子文件，并在后续回复确认 FreeMote 路线解决。

- 不同 PIMG 的子文件可同名，批量平铺易覆盖。
- JSON 保留坐标；帖中的另一份清理脚本没有被提问者采用。

**应用：** 按来源包隔离图层，保留 JSON 与映射；只把已确认路线记为社区报告。

**边界：** 不把未执行的 Python 建议当成功证据。


<a id="b14"></a>
## B14 — Parsing PFS Files Used by the Artemis Engine

原文：[Parsing PFS Files Used by the Artemis Engine](https://sakari.top/posts/2025/artemis-pfs/) · 作者：Sakari · 语言：en · 类型：author-blog

来源依据：pf8/pfs-rs 作者公布自己逆向所得格式布局。

- 名称长度按字节计算，数据偏移为相对整个容器的绝对位置。
- pf8 内容异或以索引 SHA-1 为键，每个文件重新计数；分块需延续文件内位置。

**应用：** 解析时验证索引范围、字节长度与每文件流位置，跨文件不可连续使用异或游标。

**边界：** 作者描述的 pf8/pf6 范围，其他魔数或变体需再核验。


<a id="b15"></a>
## B15 — Artemis引擎游戏去假名标注(ruby)

原文：[Artemis引擎游戏去假名标注(ruby)](https://iloli.one/artemisyin-qing-you-xi-qu-jia-ming-biao-zhu-ruby/) · 作者：Chenx221 · 语言：zh · 类型：author-blog

来源依据：作者用遥かなるニライカナイ展示修改前后提取结果。

- 文本缺失可能是 ruby 标签处理造成，资源容器本身已能拆开。
- 该作脚本定位在 system/extend/script.lua，作者以实际运行对比确认。

**应用：** 区分容器解码与文本语义提取失败；先检查标签保留，不因缺字重复更换解包器。

**边界：** 文章明确非全 Artemis 兼容；修改游戏不属于本轮。


<a id="b16"></a>
## B16 — Galgame汉化中的逆向（四）：IDA静态分析psv游戏

原文：[Galgame汉化中的逆向（四）：IDA静态分析psv游戏](https://blog.schnee.moe/posts/GalgameReverse4/) · 作者：YuriSizuku / devseed · 语言：zh · 类型：author-blog

来源依据：作者对 PSV 的 BIN/ARC 配对及压缩分支进行分析。

- GARbro 能列名但打不开内容，表明索引和压缩支持应分别验收。
- BIN 是索引，ARC 是数据；压缩长度与对齐长度不可混用。

**应用：** 保持关联索引和数据包，分别检查压缩标志、真实长度、对齐和未实现分支。

**边界：** PSV 样本，不迁移为 Windows 全引擎保证。


<a id="b17"></a>
## B17 — Innocent Grey和Noesis社GalGame工具

原文：[Innocent Grey和Noesis社GalGame工具](https://www.cnblogs.com/bl4nk/archive/2011/11/13/2909125.html) · 作者：bl4nk · 语言：zh · 类型：author-blog

来源依据：工具作者本人博客备份，给出手测脚本数量和分工具支持列表。

- 容器工具 igtool 与脚本工具 igscript 的支持列表不同。
- 作者将空脚本作为该样本正常现象；不能统一将零字节判失败。

**应用：** 按容器/子格式分开验证并记录预期空条目；游戏支持以具体列表与样本为准。

**边界：** 2011 年旧记录；未列游戏和新变体不继承支持。


<a id="b18"></a>
## B18 — gal解包系列Ⅲ：解包通用流程

原文：[gal解包系列Ⅲ：解包通用流程](https://blog.illlights.com/archives/2021/games/gal3.html) · 作者：illlights · 语言：zh · 类型：author-blog

来源依据：作者陈述自己查找游戏与解包路线的搜索习惯。

- 作者先收集日文名、罗马字、厂商与发行日期再搜索工具。

**应用：** 把这些字段加入诊断搜索串，并补当前平台、版本与签名。

**边界：** 只采纳作者搜索流程；不采用按厂商大小/年份断言兼容的经验泛化。


<a id="b19"></a>
## B19 — [Case Study][KirikiriZ] Tsumugi no Hanayome

原文：[[Case Study][KirikiriZ] Tsumugi no Hanayome](https://www.anime-sharing.com/threads/case-study-kirikiriz-tsumugi-no-hanayome.1772084/) · 作者：Entai2965 · 语言：en · 类型：firsthand-forum

来源依据：作者以制作该作翻译概念验证为线索逐步展示命令与结果。

- TXT.SCN 与 PIMG 都可能有 PSB 头，须再识别类型和用途。
- 作者观察到同套工具解编译与编译使用不同输出目录。

**应用：** 以签名和结构识别用途；命令记录工作目录及实际输出路径。

**边界：** 只对应该作案例；PSB 不等于动画或图像。


<a id="b20"></a>
## B20 — (Help!) AQUARIUM - The Hololive VN [.pac files]

原文：[(Help!) AQUARIUM - The Hololive VN [.pac files]](https://reshax.com/topic/87-help-aquarium-the-hololive-vn-pac-files/) · 作者：MuSeR；BanBi；NeoGT404 · 语言：en · 类型：firsthand-forum

来源依据：当事人报告 X-Ripper 得到图片但得不到脚本，工具作者后续提交支持并限定旧版未测。

- 签名扫描提取图片成功不能证明 PAC 索引或脚本完整。
- 后续作者明确旧版仅推测兼容，未测试。

**应用：** 把 carving 标为部分恢复，分别统计图片、脚本、原名与索引覆盖。

**边界：** 初帖引擎名称是猜测，不能登记为 Softpal 已识别。


<a id="b21"></a>
## B21 — GAL解包的那些事儿

原文：[GAL解包的那些事儿](https://www.bilibili.com/opus/952945950435835913) · 作者：yx-mgl · 语言：zh · 类型：author-blog

来源依据：作者展示自己的拆包操作与文件目录观察。

- 同一类 CG 可同时分布在 event 与 patch 包；只取主包会遗漏。

**应用：** 清点主包和补丁包，导出时保留来源与同名覆盖关系。

**边界：** 仅为作者列出的作品经验；补丁优先级仍需逐作核对。


<a id="b22"></a>
## B22 — 水贴：fvp的立绘合成

原文：[水贴：fvp的立绘合成](https://www.kungal.com/topic/886) · 作者：listder · 语言：zh · 类型：firsthand-forum

来源依据：作者比较自己分析的 bgm.bin 与 graph_bs.bin，并给出解析代码。

- 先用结构较简单的 BGM 包核对索引，再分析图像包。
- 拆出 HZC 后仍需要图像解码，不能当成可用图片。

**应用：** 区分容器提取、图像解码与立绘合成三个阶段。

**边界：** 对应作者展示的 FVP 包；未证明所有 Favorite 版本兼容。


<a id="b23"></a>
## B23 — Obey Me Sprite Assembling?

原文：[Obey Me Sprite Assembling?](https://archive.vg-resource.com/thread-40298.html) · 作者：*Asuka*；RiffOsci · 语言：en · 类型：firsthand-forum

来源依据：提问者实际尝试重建，并反馈静态组装成功、动画仍不顺畅。

- 保留纹理与 bytes 配对，重建主 JSON 后再关联纹理。
- 静态显示成功不代表动画完整。

**应用：** 保存配对映射，分别验收组装结果和动画。

**边界：** 此例来自 Obey Me；不能推断其他 PSB 类型可同样处理。


<a id="b24"></a>
## B24 — [QLIE] 封包接口Hook

原文：[[QLIE] 封包接口Hook](https://www.cnblogs.com/Dir-A/p/18096946) · 作者：Dir-A · 语言：zh · 类型：author-blog

来源依据：作者分析自己遇到的汉化版封包与引擎读取接口。

- 外加整包封装可让已有解析器只显示部分乱码名字。
- 复用接口涉及 Delphi 调用约定、字符串布局及释放函数。

**应用：** 乱码列表标记为解析失败；动态接口适配单列版本与 ABI 条件。

**边界：** 特定修改版案例；本轮仅研究，不执行 Hook。


<a id="b25"></a>
## B25 — 04——让萌新也能学会的AI翻译教程——SoftPal引擎

原文：[04——让萌新也能学会的AI翻译教程——SoftPal引擎](https://www.kungal.com/topic/3496) · 作者：是幼微鸭mua · 语言：zh · 类型：firsthand-forum

来源依据：作者以自己处理的 Dimension Lovers 展示工具操作与失败分支。

- SCRIPT.SRC 与 TEXT.DAT 应成对保留。
- 按场景拆分失败时，完整文本表仍可能可读。

**应用：** 区分索引关联失败和正文解码失败，记录范围与总条目数。

**边界：** 具体作品和作者工具版本；全文导出不等于场景映射已恢复。


<a id="b26"></a>
## B26 — 关于以krkr为引擎的galgame解包经验分享

原文：[关于以krkr为引擎的galgame解包经验分享](https://www.bilibili.com/opus/885261397615706131) · 作者：人活着就是为了祈妹 · 语言：zh · 类型：author-blog

来源依据：作者描述自己处理《馆死》的提取经过。

- 实际捕获随已播放场景增加；导出的立绘还需后续格式处理及组合。

**应用：** 动态提取记录访问场景和缺失资源，不能凭输出目录判定完整。

**边界：** 只采用亲测现象；不采用文章的广泛兼容性推测及关闭防护建议。


<a id="b27"></a>
## B27 — Ren'Py学习笔记（一）使用layeredimage构建多图层立绘

原文：[Ren'Py学习笔记（一）使用layeredimage构建多图层立绘](https://www.cnblogs.com/eslzzyl/p/17219130.html) · 作者：Eslzzyl · 语言：zh · 类型：author-blog

来源依据：作者在实践段落用《天色幻想岛》的差分重新构建立绘。

- 姿势、服装和分辨率变体应分组；不同服装宽度不一定相同。
- 推定的摆放位置要与原始画布和已知坐标区分。

**应用：** 合成清单记录姿势、分辨率、层序及坐标来源。

**边界：** 采用作者实践部分；人工摆放不能宣称恢复原始规则。


<a id="b28"></a>
## B28 — GalGalgame汉化中的逆向（八）_哈希算法分析_以krkrz_hxv4为例

原文：[GalGalgame汉化中的逆向（八）_哈希算法分析_以krkrz_hxv4为例](https://blog.schnee.moe/posts/GalgameReverse8/) · 作者：YuriSizuku/devseed · 语言：zh · 类型：author-blog

来源依据：作者在此前动态调用研究后，继续静态分析哈希输入、结构与算法。

- 文件名哈希与目录哈希是不同函数，应分别验证。
- Unicode 字节长度、salt/seed 与算法变体均影响匹配。

**应用：** 名称恢复保存输入编码、算法分支和实测向量；未匹配项保留哈希名。

**边界：** 该作 Hxv4 变体；2026 静态分析是此前动态帖的新增研究，不是镜像。


<a id="b29"></a>
## B29 — 站在前人的肩膀上对柚子社新作《Limelight Lemonade Jam》进行CG以及立绘合成

原文：[站在前人的肩膀上对柚子社新作《Limelight Lemonade Jam》进行CG以及立绘合成](https://www.bilibili.com/opus/1118323047690928132) · 作者：゚゚゚松坂砂糖 · 语言：zh · 类型：author-blog

来源依据：作者给出自己转换坐标、差分并合成该作素材的截图与结果。

- 作者将 PBD 坐标与 TLG 差分配对，分开处理身体和表情组。
- 没有坐标的像素对齐与有坐标的重建应分别标记。

**应用：** 优先保存坐标及分组；启发式合成输出标记为推定并抽样核对。

**边界：** 该作与所用工具版本；不继承文章对系列作品的广泛推断。


<a id="b30"></a>
## B30 — 【KRKR】拯救老Galgame——老游戏画质提升计划？（智以类聚）

原文：[【KRKR】拯救老Galgame——老游戏画质提升计划？（智以类聚）](https://www.bilibili.com/opus/579304892542122649) · 作者：史大林小同志 · 语言：zh · 类型：author-blog

来源依据：作者记录自己放大该作素材后的偏移与截断故障及定位过程。

- 把输出画布改小可暂时掩盖偏移，却会截掉人物下半身。
- 素材内偏移与 charinit.csv 中场景定位是不同参数。

**应用：** 保留原始画布，分别验证图层边界与场景放置，不能裁图掩盖错位。

**边界：** 对应该作数据组织；不把文件名和表结构外推到全部 KiriKiri。


<a id="b31"></a>
## B31 — 《天使騒々RE-BOOT!》解包及CG、立绘合成浅谈

原文：[《天使騒々RE-BOOT!》解包及CG、立绘合成浅谈](https://www.bilibili.com/opus/791058256610984007) · 作者：不是鼠的仓鼠 · 语言：zh · 类型：author-blog

来源依据：作者实际组合体验版规则与正式版差分，并补记失败结果。

- 体验版和正式版差分编号不同，直接复用规则会错位。
- 跑完一条路线仍有规则引用的素材缺失。

**应用：** 规则与图像绑定同一版本；统计缺失引用并隔离跨版本推定。

**边界：** 作者明确体验版规则完整性未知；不能把所述方案视为完整成功。


<a id="b32"></a>
## B32 — GARbro Formats.dat文件格式学习

原文：[GARbro Formats.dat文件格式学习](https://esperz.top/index.php/archives/lang/587) · 作者：Esper · 语言：zh · 类型：author-blog

来源依据：作者记录自己在 ATRI 上可列名却不能读取内容的失败。

- 目录名可见与内容解码是两个不同结果；方案数据库也是排查对象。

**应用：** 失败报告同时保存 GARbro 构建、方案数据库版本及预览结果。

**边界：** 初步分析没有给出成功修复；不采用文中把 Deflate 称作加密的说法。


<a id="b33"></a>
## B33 — 【解包】获取GalGame类文本、音频方法及格式化对应

原文：[【解包】获取GalGame类文本、音频方法及格式化对应](https://elix.homes/2025/11/29/%E3%80%90%E8%A7%A3%E5%8C%85%E3%80%91%E8%8E%B7%E5%8F%96GalGame%E6%96%87%E6%9C%AC%E3%80%81%E9%9F%B3%E9%A2%91%E6%96%B9%E6%B3%95%E5%8F%8A%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%AF%B9%E5%BA%94/) · 作者：ELIX · 语言：zh · 类型：author-blog

来源依据：作者以自己提取的 Senren Banka 文件树与 JSON 片段说明关联方法。

- SCN 解编译后，还要按结构关联角色、对话语言和 voice 标识。
- 拖放窗口闪退时，应在终端保留实际错误。

**应用：** 保留主 JSON 与资源描述，按结构建立映射，记录错误而非仅看窗口消失。

**边界：** 只采用其展示的结构与操作；AI 生成脚本未在本机验证，闪退不能直接判为加密。


<a id="b34"></a>
## B34 — [Case Study][KirikiriZ] Koakuma-chan no Yuuwaku

原文：[[Case Study][KirikiriZ] Koakuma-chan no Yuuwaku](https://www.anime-sharing.com/threads/case-study-kirikiriz-koakuma-chan-no-yuuwaku.1551382/) · 作者：Entai2965 · 语言：en · 类型：firsthand-forum

来源依据：作者逐项记录同系方案失败、动态提取与实际转换过程。

- 列出名称但图片/脚本无法预览时，不能认定内容已正确解码。
- 作者尝试同集团多个方案仍失败，品牌相同不足以确认适配。

**应用：** 有限候选试验后按错误转路由，并分别保存可列名与可解码状态。

**边界：** 仅针对该作；区别于作者另文的 SCN/PIMG 案例。


<a id="b35"></a>
## B35 — 求一个Wild Bug引擎的封包方法

原文：[求一个Wild Bug引擎的封包方法](https://www.ai2.moe/topic/46646-%E6%B1%82%E4%B8%80%E4%B8%AAwild-bug%E5%BC%95%E6%93%8E%E7%9A%84%E5%B0%81%E5%8C%85%E6%96%B9%E6%B3%95/) · 作者：tdgwsqsdgj · 语言：zh · 类型：firsthand-forum

来源依据：提问者提供自己的工具错误，并回报未修改资源重新封包仍失败。

- 引擎已识别，现成 WBP 工具仍可拒绝特定包。
- 重建包与原包结构不同，不能仅改签名假定兼容。

**应用：** 记录原始头与工具版本；需要回封时先验证不修改内容的往返。

**边界：** 最后仍未解决；回复中的修改文件头建议未获成功验证。
