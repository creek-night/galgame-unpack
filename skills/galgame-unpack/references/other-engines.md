# 其他已验证格式

这些入口只验证了所列本地变体。先读取来源指纹和选择依据，再针对当前文件验证。

## Artemis PF8 / PFS

GARbro 报不支持但头部是 pf8 时，用 pfs_extract.py 检查原始索引。异常条目可以记录为越界；索引整体被截断时失败。解密密钥必须从完整原始索引计算，不能先删掉异常条目。

```powershell
& $taskPy -B "$taskSkill\scripts\pfs_extract.py" index $taskArchive --out "$taskRun\work\pfs-index.json"
& $taskPy -B "$taskSkill\scripts\pfs_extract.py" extract $taskArchive --entry $taskEntry --image --out "$taskRun\assets\layers\body.png"
```

只接受精确、唯一且在文件边界内的条目。--image 先实际解码，再保存原始图片字节，保留 PNG comment。PNG comment 的坐标可能是各图层的绝对基准，面部相对身体位置为二者之差。《保健室》与《常轨脱离》已验证此路径；分包与汉化补丁的覆盖顺序仍需独立证明。

## Light.vn mcdat

Data/_/0.mcdat 为本次三版本的名称映射。先恢复映射，再按逻辑路径选择原文件：

```powershell
& $taskPy -B "$taskSkill\scripts\lightvn_extract.py" index $taskGame --out "$taskRun\work\lightvn-index.json"
& $taskPy -B "$taskSkill\scripts\lightvn_extract.py" image $taskGame --entry 'images/ecg/ecg0-0.webp' --out "$taskRun\assets\cg\ecg0-0.png"
```

raw 模式用于读取为合成所需的文本元数据，不会执行脚本。人物组合从游戏脚本的 textureCreate、坐标表和调用关系确认；本次 Nagi 为 1360×2900 身体加面部偏移 (550,250)。该数值只用于匹配样本。EVB 或其他翻译补丁不能仅凭名称映射认定已覆盖。

算法来源：shiikwi/Light.VNRev，固定提交 d097884a5af32be37af5eaa058470d722271ba19；当前只实现已验证的有界文件解码。

## Favorite View Point / HZC

GARbro 可从 BIN 包读取 HZC。多帧表情先原样导出 .hzc，再指定一帧：

```powershell
& $taskBridge $taskGarbro raw $taskArchive $taskEntry "$taskRun\work\native\face.hzc"
& $taskPy -B "$taskSkill\scripts\hzc_frame.py" "$taskRun\work\native\face.hzc" --frame 1 --out "$taskRun\assets\layers\face.png"
```

当前支持 HZC1/NVSG 的 BGRA kind 2，核对解压长度和帧数。sidecar 保留原始偏移，区分表情相对位置与人物的屏幕位置。FHD ReEternity 已验证 34 帧表情中的所选帧与原生立绘画布。

## Softpal PAC / PGD3

先用桥接 raw 导出 PGD，保持其原始文件名。PGD3 是引用基础 PGD 的增量图：先按头部所指名称提取基础图，与差分放同一工作目录，再调用桥接 image。缺少基础图时继续取回依赖，不能把增量块当完整立绘。

《夏色心跳日志》ST01A_A020.PGD 引用 ST01A_A010.pgd，原生 1843×1843；变化区域为 (914,551) 的 36×39。原图与还原图在该区域外应逐像素相同。保留原生画布，源图人物到边界的构图不等于解码时被裁掉。
