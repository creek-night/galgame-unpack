# 工具选择与备用调用

使用用户明确提供或另行安装的工具目录。公开包不假定某个盘符或工具合集存在；先检查实际版本、许可、命令接口和输入输出行为。

## GARbro Mod 备用路径

维护者在 2026-10-19 使用过一套标为 1.0.0.8 的本地库：GameRes 1.5.44.324、ArcFormats 1.2.48.2266，以及 ArcExtra/ArcLegacy。G06 BGI、G15 显式方案 XP3 共 11 对代表 PNG 与普通版新鲜输出完整 RGBA 一致。文件夹名不证明与某个上游发布包字节相同，其他版本需重验。

设 `$taskMod` 为实际 Mod 目录，使用 [构建脚本](../scripts/build_garbro_bridge.ps1) 的 `-Garbro` 和 `-Output` 生成独立桥接器；不能混用旧桥接器与新 DLL。除基础 tool.json 外，还应记录实际插件、配置和数据库指纹。

```powershell
& $taskModBridge $taskMod schemes
& $taskModBridge $taskMod entry $taskArchive $taskEntry "$taskRun\assets\cg\sample.png" --scheme $taskScheme
```

方案名来自当前库的 `schemes` 与版本证据；普通 BGI 不传方案。历史环境的 GARbro.Console.exe --help 曾无文本，自动入口使用已核对的桥接器，MCP 单独确认。

## 按问题选择候选

| 情况 | 候选及边界 |
|---|---|
| 已识别资源包但当前解码器失败 | GalArc 或另一 GARbro 分支；CLI 与数据库参数需核实，不从 GUI 启动成功推导素材通过 |
| PBD 加规则和人物图层 | krkrfgformat、pbd_jsonTotxt；核对后缀、规则版本与实际图层名，见 [格式路线](format-research.md) |
| PIMG 内图层 | FreeMote 或旧 expimg；核对父容器隔离、原名、图层坐标及输入清理行为 |
| Unity 组件、材质和引用 | AssetRipper；Dummy shader 和导出警告不代表原始渲染已还原，见 [Unity](unity.md) |
| IL2CPP 自定义类型缺失 | Il2CppDumper / 同版类型生成器；重新匹配 GameAssembly 与 metadata，类型输出不等于完整 CG |
| 旧引擎格式 | arc_unpacker、asmodean 工具；按具体格式、版本和本地许可选取，失败构建先诊断，不重复盲试 |
| 只有运行时路线 | Extract / Dump / Viewer；涉及启动游戏、执行游戏代码或注入时按主流程询问 |

## 合成器与转换器的输入行为

首次接入第三方工具，在 work 副本固定 cwd 运行，保留原名与来源映射。检查移动输入、删除临时目录、覆盖重名、路径字符和数量限制；结束后核对输入副本及原件哈希。[社区经验](community-experience.md) 记录了具体反例。

PNG comment 中身体/表情坐标可供核对，但缺坐标不能默认为已证实的 (0,0)，任意身体×表情枚举也不等于实际组合。CSV 合成器的 `paste(image, position, image)` 不等同 RGBA alpha-over；透明素材不要默认铺白底。明确的 normal alpha-over 配方使用 [compose_layers.py](../scripts/compose_layers.py) 并独立验证。

完整来源和新增工具候选见 [研究导航](research-guide.md)。资料支持、维护者历史样本、当前用户输入实测分别记录。
