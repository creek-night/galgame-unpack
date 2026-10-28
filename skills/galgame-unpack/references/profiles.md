# 保存与复跑已验证方案

先匹配来源和依赖，再决定能否复跑：

```powershell
& $taskPy -B "$taskSkill\scripts\profile.py" match --profiles "$taskRoot\_profiles" --source $taskGame
```

匹配检查源相对路径、大小、SHA-256，以及脚本、配方和已声明工具的哈希；重复来源哈希在同一进程内复用。坏记录单独报告。查看每项的 warnings、request、replay_plan_available 和 limitations：匹配成功只说明记录的条件一致，复跑产物仍需验证。

## 保存实际成功的步骤

完成当前任务的清单、来源与图像/配方验证后，将**本次实际执行成功的命令**整理为 JSON 计划。示例选择一张 PNG；路径、条目和工具依实际成功命令填写：

```json
{
  "schema_version": 1,
  "mode": "offline",
  "python_packages": ["Pillow"],
  "steps": [
    {
      "argv": [
        "{PYTHON}", "-B", "{PROFILE}/scripts/pfs_extract.py",
        "extract", "{SOURCE}/data.pfs", "--entry", "image/cg/example.png",
        "--image", "--out", "{RUN}/assets/cg/example.png"
      ],
      "timeout_seconds": 300
    }
  ]
}
```

- `{SOURCE}` 为本次匹配的游戏根，`{RUN}` 为新运行目录，`{PROFILE}` 为方案目录，`{PYTHON}` 为当前 Python。路径使用这些占位符，参数逐项组成 argv；不使用 shell 命令字符串。
- Python 步骤固定使用 `-B` 和已保存的 `scripts/<文件>.py`。外部解码器在 manifest.tools 中增加唯一 id，记录绝对 path、sha256 和 `kind: "offline-decoder"`；用 `{TOOL:id}` 调用，用 `{TOOL_DIR:id}` 引用该文件所在目录。其 DLL、配置等实际依赖仍按工具记录逐项固定。
- python_packages 填使用的 Python 分发包名称。保存时记录解释器哈希、版本、当前 PYTHONPATH 和这些包的版本；其他依赖的文件哈希由 manifest.tools 声明。复跑要求这些条件一致，不自动安装或替换工具。
- 步骤输出保持原来验证过的相对路径；合成配方中的图层路径以配方文件位置为基准。已验证的 JSON 配方由 save 单独保存，复跑先恢复配方，再从源包重新提取图层和合成。依赖移至持久工具目录，不依赖旧运行目录中的临时工具。
- 只收录已审阅的离线解码与合成命令。此入口不是不可信代码的沙箱；计划里的 offline 声明不授予运行游戏、加载游戏代码、注入或动态分析的权限。这些操作继续使用主流程的本次授权。

```powershell
& $taskPy -B "$taskSkill\scripts\profile.py" save "$taskRun\manifest.json" `
  --out "$taskRoot\_profiles\<唯一方案名>" --scripts-root "$taskSkill\scripts" `
  --replay-plan "$taskRun\work\replay-plan.json"
```

save 验证原清单和来源后，保存原请求（scope、requested_categories、extras、compose）、步骤、可重绑定清单、输出哈希、脚本和配方快照。要求清单字段完整；缺失请求不能从旧记录猜测。已有方案目录不会被覆盖。没有 --replay-plan 时仍可保存普通方案及已明确请求；匹配信息会说明它没有执行计划。

保存只验证步骤结构与现有产物，不证明步骤可自动重跑；至少完成一次下面的新目录复跑后，才把该计划记为可复跑成功。

## 在新目录复跑

先沿用用户已明确的本次选项，填写与记录一致的范围。默认命令只预览检查结果、展开的 argv 和限制，不创建运行目录：

```powershell
& $taskPy -B "$taskSkill\scripts\profile.py" replay `
  --profile "$taskRoot\_profiles\<方案>\profile.json" --source $taskGame `
  --run "$taskRoot\<游戏>\<新的运行目录>" `
  --scope sample --categories cg,sprites --compose yes
```

有额外类别时使用 `--extras bgm,voice`。核对计划与本次任务一致后，添加 `--execute` 执行；已经授权的普通离线任务无需再次询问。此入口自行创建新目录，不先用 new_run 创建同一个目录。

请求范围、合成选项、来源、脚本、工具或运行时不匹配时，在执行前停止；已有运行目录也拒绝使用。当前版本只复跑完全一致的选择，子集、全量扩展、新版本或新组合需整理新计划。旧方案里的运行时授权不会被继承。

执行按顺序记录每步 stdout、stderr 和返回码，遇失败或超时停止，保留诊断和部分文件，manifest 标为 blocked；重试使用新目录。成功后重新核对来源、依赖与全部声明输出的 SHA-256，调用 verify_run 独立解码、检查透明度并重合成配方；有未声明产物或验证不通过时不交付 passed。

复跑要求输出字节与已验收样本一致。报告区分新产物的程序校验与历史视觉/分类证据；它不声称新做了目视或游戏内渲染对比，也不扩大样本、补丁加载顺序和全量覆盖结论。查看新目录 manifest.json、report.md、logs/replay-result.json 和 logs/verification.json。

## 旧方案

schema 2 的旧方案仍按原条件匹配；无 request 或受校验的 replay 计划时，继续人工核对 selectors_and_provenance。历史 replay_commands、G14 手工 replay_plan 不能直接当作新入口的执行许可：整理成功步骤，在新任务输出上补齐清单和验证后另存。

--legacy 仅导入旧清单的字段别名，不补造请求、完整性或渲染证据，也不能与 --replay-plan 合用。旧 Naninovel partial-inferred-rendering 配方只作诊断元数据。_profiles/allgames-20261018-G01 至 G16 和 toolbox-20261019-mod-G06/G15 保留为历史证据；当前能力以各自版本与验收范围为准。方案及游戏成品留在用户本地，技能分发包不包含它们。
