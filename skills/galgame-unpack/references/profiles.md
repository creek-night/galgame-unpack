# 保存与复用已验证方案

使用之前先匹配本次源文件，再读取方案中的具体条目、工具条件和局限：

```powershell
& $taskPy -B "$taskSkill\scripts\profile.py" match --profiles "$taskRoot\_profiles" --source $taskGame
```

新格式 profile 先检查相对路径与大小，再逐个比对 SHA256；同一进程内共享重复文件哈希。匹配同时检查成功脚本、带哈希的配方快照和已声明的工具哈希。单份记录损坏、依赖缺失只使该项不匹配，其他记录继续检查；缺少工具指纹或旧配方哈希时返回警告，不能把来源匹配当成完整环境验证。旧格式只提示人工核对，不自动继承通过状态。

匹配只允许参考记录中的样本选择与参数。查看 selectors_and_provenance，把原输出目录替换为本次独立运行，重新从游戏源提取并验收。原图层、组合证据和补丁来源照常保留；不通过复制旧成品冒充新测试。新增版本、条目、人物组合或补丁顺序不继承旧结论。

完成验证后保存：

```powershell
& $taskPy -B "$taskSkill\scripts\profile.py" save "$taskRun\manifest.json" --out "$taskRoot\_profiles\<唯一方案名>" --scripts-root "$taskSkill\scripts"
```

该命令校验成品与源哈希，保存输入指纹、确切选择、验证范围、未解决项、证据路径和工具脚本快照；输出目录已存在则停止。--legacy 仅导入历史清单字段，不补造原清单没有的完整性证据。保存前在 manifest.tools 列出实际依赖的绝对 path、sha256，可附 bytes 与 kind；save 会核对并保留这些记录，指纹错误时不会创建方案目录。配方及图层相对位置写入 recipe_snapshots，按 from → to 复制到新运行相同位置，再重新提取原层并合成；不包含历史成品图片。持久依赖放 _tools，重用前核对工具清单；不要依赖计划清理的评估临时目录。

本轮新增方案位于 _profiles/allgames-20261018-G01 至 G16，来自 14 款游戏、16 个版本的代表样本。G14/G16 保持 partial；旧样本目录仍是可追溯证据，不属于技能分发包。

旧记录导入：`--legacy` 接受既有字段别名和 PBD 坐标配方，并重新验证图像；Naninovel 的 `partial-inferred-rendering` 配方只保留诊断元数据，不计为完整渲染或成功重合成。缺少的完成状态保持未指定。

2026-10-19 增加 `_profiles/toolbox-20261019-mod-G06` 与 `...-G15`：仅用于本地 Mod 库和配套桥接器。record 中 replay_commands 是已成功的 argv 数组；替换运行目录前缀，并按 recipe_snapshots 放入配方后执行，不能写回旧验收目录。其 tools 同时固定 Mod 插件／配置／数据库及运行时文件；这两份记录不替换已有普通版方案。
