# 补充格式路线与资料使用

检索日期：2026-10-19。用于已验证路径之外的格式、专用工具选择或版本相关失败。以下是有来源的候选路线；实际通过范围以 validated-samples.md 和匹配的 profile 为准。

2026-10-21 的扩展目录与按症状检查见[资料导航](research-guide.md)。PFS-rs、BGI-Hazuki、QLIE、CatSystem2 等新增作者资料仍是候选；已验证范围以既有记录为准。

## 先把资料转成可验证条件

按游戏原文名、发行版／补丁、包头和失败阶段搜索。先查[ztj 离线记录](ztjal-records.md)，保留原文参数和限制；需要新记录或版本核对时查[在线分类](https://blog.ztjal.info/category/acg/acg-data)及[标签](https://blog.ztjal.info/tag/gal-unpack)。旧入口在 2026-10-25 返回 404，现有分类和 116 篇文章已读取；网络失败与快照无命中均不表示无记录。按[社区经验](community-experience.md)核对版本、原帖回复及失败条件；转载和搜索片段只作线索。

每个新方案记下：来源 URL、查询日、提交／版本（未固定则注明）、输入特征、依赖／参数、实际输出及验证状态。将“工具识别索引”“图像可解码”“组合正确”分别验收。采用网页建议前核对本机命令行；需要用户完成不可代办操作时请求协助；启动游戏、注入或执行游戏代码前进入主流程确认分支。普通解码器及可代办的 GUI 操作沿用已有授权。

QLIE 的 FilePack 变体、AOS 多层解码、Innocent Grey／Noesis 的容器与脚本工具分工，见[社区候选路线](community-experience.md#容器之后仍需处理的格式)。这些路线尚未在本机验收。

## 通用容器与加密包

- [GARbro 官方说明](https://github.com/morkt/GARbro#operation)：文件类型可能只按扩展名分配，图片分类仍要看包头与实际解码；加密方案依赖游戏。无扩展名 BGI、假后缀和能列目录却打不开图像都不能靠扩展名筛选。
- [GARbro Mod 1.0.2.2](https://github.com/crskycode/GARbro/releases/tag/GARbro-Mod-1.0.2.2) 是检索时上游标签；本机已测副本另见 local-toolbox.md。程序、Formats.dat、名称字典分别固定，数据库可独立变化。[维护者说明](https://github.com/crskycode/GARbro/releases/tag/GARbro-Mod-1.0.1.6)。G14 的具体线索见 xp3.md。
- [GalArc](https://github.com/detached64/GalArc) 可作为容器候选。官方搜索索引仍展示 [AdvHD ARC V1/V2 实现](https://github.com/detached64/GalArc/blob/master/GalArc/Models/Formats/AdvHD/ARC.cs)，但本次仓库／发布页直读失败，CLI 未确认；不把索引中的当前代码视为本机 2.0.4 的保证。
- [arc_unpacker](https://github.com/vn-tools/arc_unpacker#usage) 遇多解码器碰撞时需要明确 --dec，部分格式还需插件选项；内存失败先减少并发和递归。上游已于 2022-04-25 归档，本机旧 exe 尚不能启动，见 local-toolbox.md。

## KRKR 的 PBD、PIMG 与 M2 PSB

PBD／txt／json 图层规则：按 [krkrfgformat 作者说明](https://github.com/Hitachi-Momoka/krkrfgformat) 核对规则名、层代号和透明 PNG 的名称映射；保留原名，在工作副本转换。某些 KrkrExtract JSON 不兼容，批量组合规则也不统一。只有层序／坐标／组合关系确认后才转成合成配方；修改扩展名不等于修复规则。

PIMG／PSB：先确认 M2 的 PSB、PSZ、mdf 等头与对象结构，再考虑 [FreeMote/PsbDecompile](https://github.com/UlyssesWu/FreeMote) 导出 JSON 和资源；避免把其他厂商的同名后缀套进去。检索到 [v4.9.0](https://github.com/UlyssesWu/FreeMote/releases/tag/v4.9.0)，本次未安装或验收该路线。

遇到 *_info.psb.m 和 *_body.bin，保留配对和原始文件名，按 [作者格式说明](https://github.com/UlyssesWu/FreeMote/wiki/PSB-Shells%2C-Types%2C-Platforms) 检查 info-psb 路线；部分外壳种子与文件名相关，外壳 key 与 PSB key 分开。推断 key 长度并不提供 key。导出零散图层不能直接宣布动态人物已经正确渲染。

## Ren'Py

确认 Ren'Py 目录结构和 RPA 头后，先列资源，再使用 [unrpa](https://github.com/Lattyware/unrpa/blob/master/README.md) 的显式输出目录解包。文档示例为 `python -m unrpa -mp <运行输出目录> <资源包.rpa>`；使用前以已安装版本帮助确认参数。[2.3.0 发布说明](https://github.com/Lattyware/unrpa/releases/tag/2.3.0) 增加 RPA-4.0；本机未验收，不据此强制猜 offset/key。

RPYC 是编译脚本；需要剧情或人物组合调用证据时再考虑 [unrpyc](https://github.com/CensoredUsername/unrpyc#compatibility)。匹配 Ren'Py 版本，复制到 work 后离线反编译，因为 CLI 默认在输入旁写文件；检查未知 AST、占位符和警告。注入到游戏内的使用方式仍需事前确认。仅要 CG／立绘时不默认交付剧情。

## NScripter／ONScripter

按 [维护者工具说明](https://github.com/Galladite27/ONScripter-EN/blob/master/tools/readme.txt) 区分 nsadec／ns2dec／sardec 容器解包和 nscdec 脚本解码，输出指向本次工作目录。*conv 工具含尺寸转换用途，不能作为无损素材链的默认一步。容器成功后仍需核对图像尺寸、图像单元和透明信息。本机尚未验收。

## Siglus

同构建 Gameexe.dat 与 Scene.pck 可参考 [siglus_static_key_tool](https://github.com/xmoezzz/siglus_static_key_tool) 的静态恢复／验证路线；官方同时提供 PE32 字节分析模式。它解决的是 key 候选验证，不是图像还原，本机未构建验收。

[SiglusExtract](https://github.com/xmoezzz/SiglusExtract#how-to-use) 的原用法要启动游戏并加入 DLL；这属于需用户确认的动态路线。启动前应制定工作副本方案，保持原游戏目录只读。

## Unity 与渲染

缺失 MonoBehaviour typetree、AssetRipper 版本问题见 [Unity](unity.md)；Naninovel 组合表达式、Render Only／Camera Rendering 和材质边界见 [合成](composition.md)。切片还原、人物选层、最终混色分别核对，不能由其中一步成功推导全部通过。
