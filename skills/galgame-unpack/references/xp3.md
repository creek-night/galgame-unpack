# XP3 / KiriKiri

先确认 XP3 文件头、版本和补丁来源。成功列出目录只证明索引可读；至少实际解码一个已确认用途的条目。

## GARbro 的已有方案

使用新版桥接器，构建命令见 windows-tools.md。显式指定方案只影响当前进程，不使用全局环境变量：

```powershell
& $taskBridge $taskGarbro schemes
& $taskBridge $taskGarbro list $taskArchive --scheme 'Shugaten! -sugarfull tempering-'
& $taskBridge $taskGarbro entry $taskArchive 'evk01a.png' "$taskRun\assets\cg\evk01a.png" --scheme 'Shugaten! -sugarfull tempering-'
```

`schemes` 从所指定 GARbro 的 `GameData/Formats.dat` 读取精确名称；未知方案报错。`--scheme NoCrypt` 仅用于证实无加密的重打包或索引诊断，不是通用解密。省略选项保留原有自动检测路径。读包失败时保留内层错误，分别判断缺方案、索引异常和图片解码失败。

真实样本：《糖调》需要上述方案；《少女领域》的本地重打包可用 NoCrypt。其他版本重新核对，不按游戏标题直接套用密钥。

## Hxv4 静态入口

维护者历史验收使用了 WSL 上的定制 bounded decoder，外部程序、补丁源码和锁定构建树没有随本 skill 发布。原始上游工具不保证兼容此包装器；没有匹配实现时走其他候选路线，不能直接宣称本分支可用。EXE 仅作为静态字节输入，不执行游戏。

高级用户提供匹配实现后，通过 `--tool <tool.json>` 或 `GALGAME_HXV4_TOOL_MANIFEST` 指定清单；`find` 只需已验证索引。清单格式与命令协议见 [外部解码器契约](hxv4-tool-contract.md)。下面的 `$taskHxTool` 为该清单的实际路径。

```powershell
& $taskPy -B "$taskSkill\scripts\hxv4.py" index --tool $taskHxTool --exe $taskGameExe --archive $taskArchive --out "$taskRun\work\index.tsv"
& $taskPy -B "$taskSkill\scripts\hxv4.py" find --index-file "$taskRun\work\index.tsv" --name 'ren_01a.png'
& $taskPy -B "$taskSkill\scripts\hxv4.py" extract --tool $taskHxTool --exe $taskGameExe --archive $taskArchive --index-file "$taskRun\work\index.tsv" --entry-index 738 --out "$taskRun\work\ren_01a.png"
```

示例序号只对应已记录的《永不枯萎》版本；实际序号取当前索引与明确名称的唯一匹配。`find` 使用该变体的 `xp3hnp` 名称域；重名或未知映射保留未解决，不猜定条目。

入口验证工具、EXE、包、索引的哈希，要求索引完成标记、连续序号与计数一致；单条目需要原始资源尺寸和 Adler32 相符后才发布输出。底层工具可能自动解除 KiriKiri type-1 脚本外壳：若输出为 UTF-16LE，入口仅在可逆重建外壳后与原始尺寸/Adler32 完全一致、转换往返一致时接受；sidecar 分列重建原件与已转换输出的哈希，并标记 reconstructed_type1_payload。不是对校验失败通用放行；type-0/type-2 或其他转换仍需自己的字节证据。失败记录与 `.partial` 是诊断，不能作为已完成缓存。重试用新输出名；复用完整索引仍需相同源/工具哈希。工具位置改变用 `--tool` 指定新清单；需要重建时使用外部工具提供的源码和构建说明，更新清单前重新验收。

真实边界：《永不枯萎》CG 与立绘样本通过；G14 的特定本地 EXE 构建仅作为静态字节输入，先生立绘通过；其他 EXE 的 salt 适配保持未验证，开场 CG 后续记录见本页末尾。当前入口只读一个指定包和索引/一个指定条目。

## 分层立绘

保留 TLG 原层及 .txt / .info / .sinfo / PBD 元数据。分别确认服装、姿势、表情组合，以及层序、原生画布、偏移；按证据生成 compose_layers.py 的 recipe。PBD 图层顺序在本次先生样本为从数组末尾向前绘制，不能推广为所有格式规则。原生画布的透明边距不裁掉，场景相机位移不写入人物原图。

## 新发现的 Hxv4 方案与图层工具

2026-10-19 查到 [GARbro Mod PR #88](https://github.com/crskycode/GARbro/pull/88) 已加入 G14 对应标题，合并提交 034811b，且 [改动只有 Formats.dat](https://github.com/crskycode/GARbro/pull/88/files)；[1.0.1.6 发布记录](https://github.com/crskycode/GARbro/releases/tag/GARbro-Mod-1.0.1.6) 包含该项。作者方案指定 HxNames.lst，讨论中 Steam 版使用不同参数。

这是一条待验收路线：先匹配本地 EXE／资源版本、数据库方案和名称字典，再对一个已知 CG 验证名称映射、解码及分类。数据库更新先放隔离目录，保留旧哈希；更换数据库后重新检查 scheme 名称。该 2026-10-19 资料本身不证明 CG 通过；独立后续验收见本页末尾，不能由 PR 标题直接提升范围。原帖中的动态取 key 方法仍受启动游戏前确认的约束。

匿名条目、SCN／PBD／TJS 名称线索不齐、PIMG 重名或运行时抓取缺覆盖时，读[社区经验](community-experience.md)。PBD／PIMG 规则无法直接转换时读[补充格式路线](format-research.md)；本地规则查看器与合并脚本位置见[本地工具箱](local-toolbox.md)。

2026-10-20 的 G14 后续离线试验已定位开场 CG 的 .dref → DPAK 间接关系，复用入口见 [PSB 与差分还原](psb-dref.md)。历史 partial 记录保留；新证据只提升明确条目，不扩大到全游戏。
