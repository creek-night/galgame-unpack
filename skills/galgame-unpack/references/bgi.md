# BGI / Ethornell

根据实际签名分流：`BURIKO ARC20` 为本次验证的归档，`CompressedBG___` 为图片；无扩展名不能当作未知文件忽略。

本技能的 C# 桥接器仅调用现有 GARbro 解码库，不加载或运行游戏程序集。工具目录作为 AssemblyResolve 来源，游戏始终作为数据读取。

构建（输出目录中的 EXE 已存在时拒绝覆盖；改用新构建目录）：
```powershell
& "$taskSkill\scripts\build_garbro_bridge.ps1" -Garbro $taskGarbro -Output (Join-Path $taskRoot '_tools\garbro-bridge')
```

桥接 CLI：
```text
garbro_bridge.exe <GARbro目录> list <归档>
garbro_bridge.exe <GARbro目录> entry <归档> <精确条目名> <输出.png>
garbro_bridge.exe <GARbro目录> image <独立图片> <输出.png>
garbro_bridge.exe <GARbro目录> raw <归档> <精确条目名> <输出文件>
```
输出以 JSON 写到 stdout；调用者保存到本次 logs，并检查退出码。输出文件使用 CreateNew。从 list 选择精确条目，避免靠通配符整包导出或名字直接拼接为可逃逸的输出路径。

真实样本：巧可甜恋的 `data02250.arc/ev101a`、`data02200.arc/mik01A_base` 与 `mik01A_001`、包内及外置 `hv001a`。基础解码及零偏移表情叠加已验证；这些文件名不适用于其他游戏。

CG 与立绘的判断仍需图像和引用证据。相同尺寸的透明画布可支持零偏移组合，但不能由“尺寸相同”单独推断任意组合。外置同名文件与包内文件可能像素不同，保留二者，直到覆盖关系有依据。

官方实现参考：[GARbro](https://github.com/morkt/GARbro)、[ArcBGI.cs](https://github.com/morkt/GARbro/blob/master/ArcFormats/Ethornell/ArcBGI.cs)。本桥接器不是新的全格式 GARbro CLI，未验证加密变体和交互式解码选项。
