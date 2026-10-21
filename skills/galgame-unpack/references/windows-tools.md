# Windows 工具环境

先检查用户提供的运行时和工具路径，记录版本与依赖指纹。公开包包含 Python/C#/PowerShell 源码和研究摘要；游戏资源、GARbro DLL、MCP 服务、Hxv4 二进制均需另备。

## Python 与输出根

要求 Python 3.11+，推荐使用验收过的 Python 3.12。设置 `$taskSkill` 为本技能目录，`$taskSource` 为实际游戏目录或资源包；先确认 Python 可用。当前子进程环境即可，不修改系统 PATH。

```powershell
$taskRoot = if ($env:GALGAME_UNPACK_OUTPUT_ROOT) { $env:GALGAME_UNPACK_OUTPUT_ROOT } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) 'galgame-unpack-output' }
$taskVenv = Join-Path $taskRoot '_tools\python-venv'
$env:TEMP = Join-Path $taskRoot '_tools\temp'
$env:TMP = $env:TEMP
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
py -3.12 -m venv $taskVenv
$taskPy = Join-Path $taskVenv 'Scripts\python.exe'
& $taskPy -m pip --cache-dir (Join-Path $taskRoot '_tools\pip-cache') install -r "$taskSkill\requirements.txt"
```

已有可用环境可以直接指定 `$taskPy`。Unity 分支安装 `requirements-unity.txt`，音频验证分支安装 `requirements-audio.txt`；文本验证使用标准库。按所选分支安装，成功方案保留版本，不盲目升级。

```powershell
& $taskPy -B "$taskSkill\scripts\new_run.py" --root $taskRoot --game '游戏名' --source $taskSource --compose yes --scope sample
```

`--compose`、`--scope` 和 `--extras` 来自用户已明确的选择。`--root` 优先级最高；未传时读 `GALGAME_UNPACK_OUTPUT_ROOT`，否则用用户主目录。新运行返回路径，将它设为 `$taskRun`。

## GARbro 桥接器

从 [GARbro 上游](https://github.com/morkt/GARbro) 获取合适版本，用户已有安装也可使用。设 `$taskGarbro` 为含 `GameRes.dll`、`ArcFormats.dll` 和 `GameData/Formats.dat` 的目录。

```powershell
$taskBuild = Join-Path $taskRoot '_tools\garbro-bridge-v1'
& "$taskSkill\scripts\build_garbro_bridge.ps1" -Garbro $taskGarbro -Output $taskBuild
$taskBridge = Join-Path $taskBuild 'garbro_bridge.exe'
& $taskBridge $taskGarbro schemes
```

构建需要 Windows .NET Framework 4.x 的 x64 C# 编译器与 WPF；脚本从 `$env:WINDIR` 定位，缺依赖时先报错。它记录源码、DLL 和数据库哈希，拒绝覆盖已有 EXE。该桥接器只加载指定工具库，游戏文件作为数据读取。CLI 与边界见 [BGI](bgi.md)、[XP3](xp3.md)。

GARbro Mod 与原版并存，分别构建和验证。文件夹名、GUI 能启动或 `--help` 返回 0，都不能证明提取兼容；见 [工具选择](local-toolbox.md)。

## Hxv4 与可选 MCP

Hxv4 的 `index/extract` 需要与包装器协议匹配的外部 bounded decoder、清单和 WSL；本仓库没有打包维护者的本地二进制或完整构建树。配置方法与限制见 [XP3](xp3.md)。`find` 可独立使用已验证索引，不需要该二进制。

GARbro MCP 是独立实现，不能继承传统 GARbro 的实测结论。只有用户已配置该服务时才按实际 schema 使用；确认临时文件位置与清理策略，将最终素材复制到持久目录并复核。MCP 不是本技能必需依赖。

历史依赖基线：Python 3.12.14、Pillow 12.3.0、UnityPy 1.25.4、soundfile 0.13.1。依赖安装成功与游戏素材验收分开记录；真实范围见 [样本记录](validated-samples.md)。
