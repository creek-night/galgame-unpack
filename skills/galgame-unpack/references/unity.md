# Unity 资源和切片

使用隔离的 UnityPy 1.25.4。先给定一个具体 .assets 或 bundle 做 inventory；不要把整个大型游戏目录传入 UnityPy。保持 .assets 与引用的 .resS/.resource 相邻，外部流也属于来源。

```powershell
& $taskPy -B "$taskSkill\scripts\unity_extract.py" inventory '<文件>' --out "$taskRun\work\inventory.json"
& $taskPy -B "$taskSkill\scripts\unity_extract.py" export '<文件>' --path-id '<整数>' --out "$taskRun\assets\cg\sample.png"
```
对象 ID 是 64 位整数，使用 Python/原始 JSON 或字符串传递，不经 JavaScript Number 舍入。多个 serialized file 中 ID 相同时加 `--serialized`。同名 Texture2D 可能有多个 container 路径；两者不能相互覆盖。

导出的 sidecar JSON 记录源文件、serialized file、path ID、container、尺寸、输出哈希和工具版本。调用者补充源文件及外部流哈希、类别依据和版本关系。

## 图集与 SpriteDicing

普通 Sprite 导出通过元数据裁切 Texture2D；图集本身留在 work。若 Sprite 拥有数千顶点/UV 或来源是 DicedSpriteAtlas，检查网格，而非按 textureRect 矩形截图。

```powershell
& $taskPy -B "$taskSkill\scripts\unity_extract.py" export '<bundle>' --path-id '<整数>' --restore-dicing --out "$taskRun\assets\sprites\restored.png"
```
该选项使用 `sprite_mesh.py`，限定为整数像素、无旋转缩放的矩形切片：读取顶点、UV、pivot、PixelsToUnits，将原 RGBA 切片贴入 m_Rect 完整画布并处理 Y 轴方向。超出该结构会失败，需要另行实现解析，不静默套用。

真实 CreatureAlisa 样本有 5036 顶点、1259 个切片，原画布 2894×4093。UnityPy 默认结果为 2240×3904，裁掉了透明边距；本适配器恢复原画布，内容区与默认结果逐像素一致，切片无重叠。该案例不能证明所有 SpriteDicing 版本都支持。

## 补丁与黑图

星空列车样本的同一个补丁 bundle 中含两个名为 evcg04a 的 Texture2D：container 指向 patch 的对象有图像，另一对象是全黑占位。按名字挑第一个或“解码成功就算完成”会产生错误交付。

保存 container 与对象 ID，分别验证内容；没有加载器证据时不宣布哪个版本实际生效。完整立绘已烘焙进 Texture2D 时，合成可记为该样本不适用。

官方资料：[UnityPy](https://github.com/K0lb3/UnityPy)、[Sprite Dicing](https://github.com/elringus/sprite-dicing)、[Naninovel 角色](https://naninovel.com/guide/characters)。Unity 版本号和某工具宣称支持不能代替真实图片验收。

## 缺失类型结构与工具版本

[UnityPy 官方说明](https://github.com/K0lb3/UnityPy#monobehaviour) 提供 TypeTreeGeneratorAPI 的可选路线，从同一游戏的程序集或 IL2CPP 数据构建缺失 typetree。先确认类型结构确实缺失，再按所用 UnityPy 版本检查接口；类型结构恢复不等于 Shader 或最终画面还原。静态读取程序集字节与执行游戏代码分别判断；后者仍需事先确认。

原生 typetree 读取器导致进程直接退出时，可在新子进程针对同一小样本关闭加速读取重试。本机 1.25.4 的 `UnityPy.helpers.TypeTreeHelper.read_typetree_boost` 可设为 None，走 Python 读取分支；记录两次错误和依赖版本。只适用于 typetree 路径，不把任意崩溃都归因于它。[官方故障说明](https://github.com/K0lb3/UnityPy#crash-without-warningerror)。

维护者的 AssetRipper 1.3.14 历史本地日志（未随仓库发布）包含 Dummy shader 和 SerializeReference 错误。上游 [2.0.0 发布记录](https://github.com/AssetRipper/AssetRipper/releases/tag/2.0.0) 与 [PR #2342](https://github.com/AssetRipper/AssetRipper/pull/2342) 已加入该字段的读取支持；若遇到同类失败，优先调查隔离的新版本小样本，而不是认定永久不支持。本轮未安装或测试 2.0.0，G16 的材质／遮罩问题仍未解决。

仅需要素材时继续按具体 bundle／assets 读取；需要组件／材质关系时才考虑 AssetRipper 的项目级输出，并逐项核对导出警告。Dummy 占位 shader 不能作为原始混色逻辑的证据。
