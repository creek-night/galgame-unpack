# PSB v3、DPAK 与 DREF

当脚本引用的 CG 名称在 XP3 中找不到，先查加载模块和它使用的间接扩展名。G14 的 diffimage2.tjs 常量包含 .dref/PSBFile；eva01_01 的真实文件是 eva01_01.dref，按顺序引用一个 DPAK 内的底图和差分。先用当前索引的精确名称定位，不枚举解码匿名图片。Hxv4 文本外壳见 [XP3](xp3.md)。

## 提取与还原

```powershell
& $taskPy -B "$taskSkill\scripts\psb_extract.py" index '<包.dpak>' --out "$taskRun\work\psb-index.json"
& $taskPy -B "$taskSkill\scripts\psb_extract.py" extract '<包.dpak>' --entry '<精确条目.png>' --out "$taskRun\assets\layers\selected.png"
& $taskPy -B "$taskSkill\scripts\dref_restore.py" '<已解码.dref>' --package '<原名.dpak>' --out "$taskRun\assets\cg\<唯一场景名>"
```

索引只读普通、未加密 PSB v3 的名称树、对象表和资源表，保留完整名称与精确资源号。限制为 64 MiB、100 层嵌套和有界表长度；加密头、其他 PSB 版本及未知节点明确失败。不能把 PhotoShop PSB 或任意 .psb 都交给此入口。抽取资源保留原始字节及来源 sidecar，不自动猜测它是图片。

DREF 自动路径限定同一个包、底图加一个 PNG 差分：核对 PNG 全块 CRC、像素单位 oFFs、vpAg 原始画布、放置边界及二值 alpha，独立比较遮罩替换与 alpha-over。输出 result.png、原始 layers、带相对路径的 recipe.json 和来源记录。目录必须新建；按场景分目录，避免不同包内重名覆盖。运行 verify_run 再独立重合成，并补充 CG 分类和目视证据。

多层/多包、缺原生坐标、非二值 alpha、自定义混色、动画仍需调查对应加载器；不会套用本样本规则发布猜测成品。PSB 解析成功不等于动态人物渲染成功。

## 实证与来源

本地 G14 开场 eva01_01.dref → eva01__afbzat.dpak 中 eva01_02.png 与 2fc6aec7a5afdc3d5850e3a5b77b7786.png。底图 1920×1080，差分 304×275、位置 (478,162)；具体参数来自此版本元数据，不写死在算法中。原包资源、差分坐标及合成像素须在每次任务重新核对。

名称树逐层回溯参考 [FreeMote PSB.LoadNames](https://raw.githubusercontent.com/UlyssesWu/FreeMote/master/FreeMote.Psb/Psb.cs)，头部校验参考 [PsbHeader](https://raw.githubusercontent.com/UlyssesWu/FreeMote/master/FreeMote/PsbHeader.cs)。锁定 Cxdec_Tools 的一次性 PSB 导出存在名称丢隔字现象；名称异常时对照原表和上述结构，不能用残缺名选择文件。实现为本地有界 Python 解析器；未改动已有工具二进制。
