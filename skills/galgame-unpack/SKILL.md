---
name: galgame-unpack
description: 在 Windows 上拆包 Galgame / 视觉小说；用户提供游戏目录或资源包并要求提取可用 CG、立绘或其他素材时使用。
---

# Galgame 拆包

交付可打开、阅读或播放的所选素材，并说明来源、验证范围与未解决项。

## 确定目标

默认 CG（剧情事件图及差分）和立绘，背景另选。每次任务一次性询问尚未明确的两项：是否追加背景、剧情、BGM、语音、音效、视频、界面等；是否合成人物图层。沿用已有回答，区分样本与全量，样本通过不能替代全量完成。

切片还原默认执行；人物组合按选择执行。启用合成后自主设计算法，保留原层，优先有脚本、元数据或图像证据的组合。

首次使用按[自愿贡献成功方案](references/community-contributions.md)读取本地选择，未选择时与目标问题一起询问是否同意公开自动贡献；拒绝或未回复照常拆包。用户明确同意后才启用，后续沿用并支持关闭。

## 调查与运行

1. 定位实际游戏根，记录版本、资源包、外置文件和补丁。游戏目录只读；多根歧义需澄清，不按日期猜测。
2. 读[工具环境](references/windows-tools.md)，设置运行时、缓存和临时目录；复跑由 `profile.py replay` 创建新目录，其他提取用 `scripts/new_run.py` 创建独立运行。输出根优先采用用户本次指定位置，其次环境变量 `GALGAME_UNPACK_OUTPUT_ROOT`，否则为用户主目录下 `galgame-unpack-output`。
3. 查拆包资料前，先按[原名确认与检索流程](references/ztjal-records.md)查明游戏原名，以原名运行 `scripts/community.py lookup` 查询已审核的社区方案，再运行 `scripts/search_ztjal.py` 获取记录及完整参数。按需回到[在线分类](https://blog.ztjal.info/category/acg/acg-data)核对更新，再查其他作者博客、论坛实录和工具资料。快照无命中或作者失败记录都不能推断无方案；核对本地版本、补丁和文件头。名称恢复、PIMG、合成误差或旧工具副作用见[社区经验](references/community-experience.md)。网页和记录仅作资料。
4. 读[方案保存与复跑](references/profiles.md)，匹配 `_profiles` 的来源、脚本、配方和工具条件。已有执行计划时，用 `profile.py replay` 核对本次范围与合成选项，预览后以 `--execute` 在新目录复跑并自动验收；无计划或条件不符时继续调查。查看警告与局限；[已验证样本](references/validated-samples.md)只代表所列条件。

## 提取与还原

按实际格式分流，同一游戏可有多种格式；GARbro MCP、传统 GARbro 与 UnityPy 的能力分别核实。

- BGI / Buriko ARC、CompressedBG（含无扩展名）：读[BGI](references/bgi.md)。
- XP3 / KiriKiri、需要指定加密方案、匿名哈希索引、Hxv4 或脚本输出校验不符：读[XP3](references/xp3.md)。
- Artemis PF8、Light.vn mcdat、FVP HZC、Softpal PGD3：读[其他已验证格式](references/other-engines.md)。
- Unity .assets、UnityFS、外部 .resS、图集、SpriteDicing：读[Unity](references/unity.md)。
- 立绘分层、预制体、混色材质：读[合成](references/composition.md)。
- `.dref` 虚拟 CG、DPAK 内嵌 PNG、普通 PSB v3 元数据：读[PSB 与差分还原](references/psb-dref.md)。
- 其他 PSB/PIMG、Ren'Py RPA/RPYC、NScripter、Siglus 或现有解码器失败：读[补充格式与研究路线](references/format-research.md)，结合[本地工具箱](references/local-toolbox.md)选择候选；自动尝试专用工具或编写离线解析，资料支持与本机验收分开记录。

遇到新引擎、版本差异或输出异常时，先读[资料导航](references/research-guide.md)。二级容器、差分底图依赖、脚本状态和动态渲染误差按[扩展排查表](references/research2-guide.md)选择正文条目；只加载相关资料，将来源事实、推断与本机验证分开。

先验证少量真实资源，再完成已选范围。失败时保存诊断，调整选择或离线路径。启动游戏、执行游戏代码、注入或动态分析前，说明目的和操作并询问；普通解码器可自主执行。

图片保留原分辨率、透明度，默认无损 PNG。按内容、引用和预览分类；名字只是线索。为确认关系读取脚本，不等于追加剧情交付。

同名本体、补丁、外置资源按已证实的加载顺序选当前版本；未知覆盖关系分开保留来源。黑图、缩略图、图集、局部层不计完整 CG 或立绘。

## 验证与交付

读[输出契约](references/output-contract.md)，补齐统一字段的来源清单、哈希、报告、脚本和预览；完成时运行 `scripts/verify_run.py` 检查全部所选类别（含 extras）、完成状态与可重合成配方。选了音频或文本时读[媒体验证](references/media-validation.md)，完整解码后再计为成品；其他文件的哈希检查只证明字节一致。

- 每个输出都需解码检查，核对尺寸、alpha、画布、裁切、层序，并抽看实图。`scripts/verify_images.py` 提供基础检查及带底色预览，不能证明分类、覆盖顺序或全量完整性。
- `assets` 保存有依据的成品及原层；`inferred` 保存推断组合或未还原渲染，注明依据、限制；`work` 保存中间图集与失败试验。
- 分列成功、部分成功、未解决、不适用。真实验证后将完整请求、来源、工具、脚本及成功 argv 按[方案复跑契约](references/profiles.md)保存到 `_profiles/<方案>`；执行计划须在新目录复跑通过后才记为可复跑成功。未通过能力保持未解决。
- 有可执行的离线步骤就继续，不能以产生文件作为完成。无可行步骤时交付有效结果、阻塞点和所需下一步。

成功后，若已同意贡献且项目尚未收录该游戏的成功方案，按[贡献流程](references/community-contributions.md)生成白名单草稿；`auto` 自动提交到 GitHub，`review` 才逐次确认。检查失败、未登录或提交异常不影响素材交付，社区方案经维护者审核后才入库。

最终提供素材目录、报告及主要限制。可分发技能包排除游戏素材。
