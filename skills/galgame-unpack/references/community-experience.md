# 社区实务与失败反例

检索日期：2026-10-19。遇到名称缺失、PIMG 重名、合成异常、旧工具副作用或补充格式时读取。下面的游戏现象来自原作者博客、论坛实录或工具作者说明；本轮未在本机复现，不能登记为已验证适配。

2026-10-21 扩展资料见[资料导航](research-guide.md)与[逐条博客/论坛记录](research-blogs.md)；本页保留前轮经验及其检索日期。

## 把经验变成当前输入的检查

按“原文名／罗马字 + 厂商 + 发行版／平台 + 文件签名或报错”搜索，结合中、日、英关键词。先看作者做了什么、失败在哪里，再看正文修订和后续回复；记录具体游戏与工具版本，缺失则写未知。同作者转贴、本人备份、同帖回复只是一条证据链。空白页、搜索摘要和视频标题保留为线索；全文可读仍不等于本地成功。

同厂商旧作只提供候选工具。[illlights 的搜索流程](https://blog.illlights.com/archives/2021/games/gal3.html)可用于找入口；[Tabing010102 的实践](https://blog.gyx.moe/archives/1293)记录 Strawberry Nauts 原版 Yuka、FHD 版 BGI。重制、Plus、汉化版应重新核对实际包头与指纹。若文本看似可解码却内容错乱，旧汉化的自定义字形映射是另一种候选原因；原始字节、字体关系与映射需核实，恢复不了的文字保留未解决。

## 哈希名称与脚本内容

[KiriKiriZ/Cxdec 讨论](https://www.kungal.com/topic/2670)中，正文的脚本扫描由回复补充了 PBD layer_id，作者又指出 TJS 生成名可能遗漏。遇匿名条目时：

- 把 SCN 引用、PBD 图层 ID、TJS 字符串或生成规则分别列为候选来源；静态可解析的部分先处理。
- 保存容器条目／哈希、候选原名、依据、输出路径及未匹配项；重名歧义单列，已匹配数量不能证明全集。
- 用实际日文路径做编码往返检查。帖内 UTF-16 与 UTF-8-SIG 是不同条件下的报告，以当前工具输入格式为准。
- 动态取名、执行脚本遵守主流程的确认分支。上面的资料属于 2026-10-19 研究；G14 开场 CG 的后续独立本机验收见[最新样本记录](validated-samples.md)，其他未映射条目不能据此视为已解决。

[《紬の花嫁》实录](https://www.anime-sharing.com/threads/case-study-kirikiriz-tsumugi-no-hanayome.1772084/)还出现小型 KS 为系统宏、正文在带 PSB 头的 TXT.SCN。结合文件头和结构确认角色：PSB 可能装脚本，后缀不能代替用途判断。

## 工具副作用与输出重名

[PIMG 批处理讨论](https://www.kungal.com/topic/2692)的失败来自多个来源包具有相同子文件名；提问者确认 FreeMote 路线有效，但没有采用帖内另一份 Python 示例。在 work 中按“来源包身份／图层 ID 或子名”隔离输出，保留 JSON 坐标与资源映射，检测重名冲突；未采用的清理脚本仍是未验证建议。

[ぬる的 Cafe Stella 实录](https://note.com/null_base/n/ncdf566875c1a)记录 YuzuMerge 会把输入 PIMG 移到 Clear，并删除自己的临时目录；[工具作者 2.0.0.1 说明](https://ginoaai.seesaa.net/article/471753951.html)列出空格／符号及超过 1000 差分的已知限制。只在独立工作副本调用这些旧工具，记录其版本、工作目录、输入输出变化。路径问题先排查工具限制，不能直接判游戏格式不支持；改名之前检查原名是否参与 key 或关联查找。

## 图层合成与画布

- **底图身份**：[YuzuMerge 修订](https://ginoaai.seesaa.net/article/471753951.html)修过“同尺寸差分被选成底图”，之后又补了透明底图。按元数据、引用和图像关系选底图；尺寸、文件大小、不透明程度都只能筛候选。
- **有坐标与图像推断**：[Limelight Lemonade Jam 实践](https://www.bilibili.com/opus/1118323047690928132)分别使用 PBD 坐标与 AutoCGAligner。前者保留 PBD→JSON→图层映射；后者记录匹配区域、歧义和预览，证据不足放 inferred。工具产出图片不证明组合在游戏中实际出现。
- **层序与分组**：[ALZT02 的实践](https://alzt02.github.io/2025/07/17/%E9%83%A8%E5%88%86gal%E7%9A%84%E8%A7%A3%E5%8C%85/)以姿势分组、头发遮眼等关系检查组合。抽查头发／眼睛／衣领、脸红和阴影，不把某个表情组当全部组合。
- **画布与定位**：[《智以类聚》改图记录](https://www.bilibili.com/opus/579304892542122649)曾因缩小输出画布而裁掉人物下半身。分别保留原生画布、图层偏移、人物场景定位；核对非透明边界和特殊姿势。先盘点原生分辨率变体，Large 名称本身不能证明当前版本优先。
- **多帧与配对**：[FVP 作者分析](https://www.kungal.com/topic/886)可作 HZC 帧、尺寸、偏移及身体／表情关系的排查线索。保持 [本机 HZC 支持范围](other-engines.md#favorite-view-point--hzc)，先检查帧数／解压长度，再验证所选帧和配对；该帖的字段解释不自动覆盖当前变体。

## 容器之后仍需处理的格式

以下为候选，不增加本机通过范围；不自动追加用户未选择的音频或剧情。

| 触发条件 | 从原作者经验提取的下一步 | 适用边界 |
|---|---|---|
| QLIE 包可列出，音频仍不可播放 | [绝对值_x 的 QLIE 日志](https://absx.pages.dev/articles/speedup)记录 FilePackVer3.0/3.1 与工具构建差异。检查包尾版本、相关 key 文件、实际工具构建与导出内容的可解码性；OGG 后缀不证明已解密。 | 作者也记录相同版本标记下的新作失败；exfp3 是候选而非通用保证。回封、音频加速不属当前默认目标。 |
| Innocent Grey／Noesis 的旧 DAT／IGA 与 .s | [bl4nk 的工具说明](https://www.cnblogs.com/bl4nk/archive/2011/11/13/2909125.html)区分 igtool 容器和 igscript 脚本；部分 IGA 另用 exiga，脚本有对应模式。分别核对目标支持列表与实际帮助。 | 2011 年资料；同厂商、脚本工具支持不能推出容器工具也支持。 |
| AOS 解开后还有 ABM／MSK／SCR | [AosTools 作者日志](https://lasriel.moe/posts/AosTools/)说明多帧 ABM、RLE 图像、灰度 MSK、Huffman 脚本等层次。保留原件并逐层判断压缩、帧、遮罩关系。 | 作者未给完整游戏矩阵；灰度遮罩不等于坏图，多帧不能只取首帧冒充完整。 |

## 离线解析的证据

[Yuka 容器分析](https://hackernoon.com/reverse-engineering-visual-novels-101-d0bc3bf7ab8)通过多个 YKC 核对表项、名称偏移与长度；[YuriSizuku 的静态分析](https://blog.schnee.moe/posts/GalgameReverse4/)把能列名却不能解内容作为独立问题，并联合 BIN 索引和 ARC 数据定位。

开发当前变体的离线解析时，验证偏移／长度边界、字节长度与字符数、编码及解压长度，再跨多个条目和可用的包交叉检查；保留关联索引和未解释字段。前者没有在该文完成 YKG/YKS，后者是 PSV 样本；两篇只提供分析方法，不能直接推广格式支持。

## 运行时抓取与渲染边界

获准使用动态路线后，[《紬の花嫁》](https://www.anime-sharing.com/threads/case-study-kirikiriz-tsumugi-no-hanayome.1772084/)与[B站《馆死》经验](https://www.bilibili.com/opus/885261397615706131)提示记录已访问场景、选择、鉴赏入口及过滤规则。分别验收内容可解码、文件名恢复、目录恢复；仅覆盖被触发素材时如实标注，文件数稳定不是全量证明。

[VG Resource 的当事人反馈](https://archive.vg-resource.com/thread-40298.html)中，Unity 的 texture 与 bytes 经处理可拼出 E-mote 人物，仍缺原有平滑动作。保留纹理、TextAsset 及引用关系，分开验收静态组合、动画和材质。它只是候选线索，不证明 G16 Alisa 的混色／stencil 已还原。

## 采用新路线时记录什么

在本次报告或诊断 sidecar 记：来源 URL／作者／日期与版本条件、自己的推断、当前源指纹、工具副作用及参数、预期成功现象、实际结果和未覆盖项。新方案只有在当前真实素材通过后才按 [profiles](profiles.md) 保存；资料研究本身不创建通过状态。
