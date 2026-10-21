# galgame-unpack

面向 Windows 的 Galgame / 视觉小说素材拆包 Agent Skill。让 Codex 按游戏格式选择工具，提取可用 CG 与立绘，保留来源，并区分解码成功、图像还原、人物合成和未解决项。

Windows-focused agent skill for extracting and verifying visual-novel assets. Instructions are primarily in Chinese. This is an agent workflow plus helper scripts, not a standalone GUI or a universal extractor.

## 能做什么

- 默认交付剧情 CG（含差分）与立绘；背景、文本、音频等按需选择。
- 图集切片默认还原；人物图层是否合成单独确认，保留原层与组合依据。
- 提供 GARbro 桥接、PF8、Light.vn、HZC、普通 PSB、DREF/DPAK、Unity 切片等辅助入口，按实际格式和局限使用。
- 每次运行独立目录，保留哈希、来源、配方、预览和未完成项；验证后才保存可复用 profile。
- 收录 129 项原始资料的摘要和链接，按问题加载，覆盖博客、论坛、引擎文档与工具作者研究。

**兼容性是按样本记录的。** 维护者曾检查 14 款游戏的 16 个安装版本中的代表素材，不是这些游戏全量通过，也不是全引擎支持。真实范围见 [历史样本](skills/galgame-unpack/references/validated-samples.md)。Hxv4 包装器需要另备兼容外部工具；Live2D、Spine、复杂 shader 等研究路线不等于开箱即用。

## 安装 skill

仓库内可安装的目录是 `skills/galgame-unpack`，包含 SKILL.md、scripts、references、agents 和依赖清单。

在 Codex 中发送：

```text
使用 $skill-installer 安装 https://github.com/creek-night/galgame-unpack/tree/main/skills/galgame-unpack
```

也可以下载本仓库，或执行 `git clone https://github.com/creek-night/galgame-unpack.git`，然后在仓库根目录执行以下 PowerShell：

```powershell
$skillParent = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills'
$skillDest = Join-Path $skillParent 'galgame-unpack'
if (Test-Path -LiteralPath $skillDest) { throw '已存在同名 skill，请先备份再更新。' }
New-Item -ItemType Directory -Path $skillParent -Force | Out-Null
Copy-Item -LiteralPath '.\skills\galgame-unpack' -Destination $skillDest -Recurse
```

当前 Codex 的用户技能目录见 [OpenAI 官方说明](https://learn.chatgpt.com/docs/build-skills)。已有旧版安装可继续使用其实际技能目录；避免同时放置两份同名 skill。没有显示时重启 Codex。

## 准备运行环境

Windows 10/11 x64，Python **3.11+（推荐 3.12）**。基础图像功能需要 Pillow；Unity 和音频分支分别有可选依赖。在仓库根目录可建立独立环境：

```powershell
py -3.12 -m venv .venv
$taskPy = '.\.venv\Scripts\python.exe'
& $taskPy -m pip install -r '.\skills\galgame-unpack\requirements.txt'
# 需要 Unity 或音频时，分别安装对应清单：
& $taskPy -m pip install -r '.\skills\galgame-unpack\requirements-unity.txt'
& $taskPy -m pip install -r '.\skills\galgame-unpack\requirements-audio.txt'
```

GARbro 及其 DLL、WSL 和各候选工具按所选格式另备，不随仓库分发。GARbro 桥接需要 .NET Framework 4.x 的 C# 编译器与 WPF。完整配置与构建命令见 [Windows 环境](skills/galgame-unpack/references/windows-tools.md)，外部工具及来源见 [THIRD_PARTY.md](THIRD_PARTY.md)。

输出根优先使用本次传入的 `--root`，其次环境变量 `GALGAME_UNPACK_OUTPUT_ROOT`，最后为用户主目录下的 `galgame-unpack-output`。路径可包含空格和中文。指定输出根时，新增工具、缓存和临时文件也放在该根下。

## 使用

向 Codex 提供游戏的实际路径和目标，例如：

```text
使用 $galgame-unpack 处理 D:\Games\某游戏。
只要 CG 和立绘，需要合成立绘；输出到 D:\Extracted。
先验证代表样本，再完成已选范围。
```

流程：识别版本与补丁 → 查询资料/匹配方案 → 少量真实提取 → 解码与布局验证 → 完成所选范围 → 交付素材、报告和可复用方案。

离线工具把游戏文件当数据读取。启动游戏、执行游戏脚本、加载游戏 DLL 或动态分析前会另行询问。请仅处理你有权访问和处理的资源；本项目的许可不授予游戏素材的再分发权。

## 限制与验证

- 默认验收单位是明确资源或代表样本；全量完整性需要独立清单和覆盖证明。
- 加密变体、体验版/正式版、补丁和不同平台必须重新识别，文件名不能单独证明分类或覆盖关系。
- 复杂蒙版、shader、骨骼动画和未知图层组合可能只能部分还原，输出会保留 inferred/未解决状态。
- GARbro MCP 与传统 GARbro 不同；仅安装本 skill 不会配置 MCP。
- 本仓库测试使用自行生成的微型夹具，不含游戏内容；它验证安装、路径、无覆盖输出、PF8 解码与 alpha 合成等行为，不增加真实游戏支持统计。

```powershell
& $taskPy -B -m unittest discover -s tests -v
& $taskPy -B tools/check_package.py
```

[研究导航](skills/galgame-unpack/references/research-guide.md) · [输出契约](skills/galgame-unpack/references/output-contract.md) · [贡献指南](CONTRIBUTING.md)

## License

本仓库原创代码与文档采用 [MIT License](LICENSE)。依赖、链接资料和游戏内容各自保留原许可；研究目录是带来源的摘要，不包含原文全文。外部工具没有随本仓库打包。
