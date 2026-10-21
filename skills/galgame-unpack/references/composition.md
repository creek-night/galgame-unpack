# 立绘合成

选择合成后，依据真实图层、坐标、层序、预制体或脚本组合规则设计算法。区分两类证据：
- 组合证据：哪些身体、衣服、表情可以一起使用。
- 渲染证据：偏移、pivot、缩放、遮罩、混色和透明通道怎样形成最终图像。

有组合规则但缺少材质还原，仍然只能算部分完成。优先输出有依据的组合；未经证实的排列放 inferred，保留原始层、依据和预览，不枚举所有笛卡尔积。

PIMG 底图误判、画布裁切、元数据缺失或第三方合成器结果异常时，读[社区合成反例](community-experience.md#图层合成与画布)。先从反例定位缺失条件，再调整配方。

## 普通 RGBA 图层

`compose_layers.py` 执行明确给出的原分辨率 alpha-over：
```json
{
  "canvas": [600, 884],
  "evidence": "说明具体组合与位置证据",
  "layers": [
    {"file": "../assets/layers/body.png", "position": [0, 0]},
    {"file": "../assets/layers/face.png", "position": [0, 0]}
  ]
}
```
列表按从底到顶排序，路径相对 recipe。只接受 normal 混色、整数坐标和完整落在画布内的图层，输出不覆盖已有文件。

默认先建立透明画布再逐层合成。如果证据要求保留底图 alpha=0 像素中的 RGB，可在 recipe 顶层显式设 `"preserve_base_rgba": true`；此时第一层必须与画布同尺寸、位于 [0,0]，从底图副本开始叠加。两种方式的隐藏 RGB 可能不同；不得仅因画面一致就声称 RGBA 一致。
```powershell
& $taskPy -B "$taskSkill\scripts\compose_layers.py" "$taskRun\work\recipe.json" --out "$taskRun\assets\sprites\composed.png"
```
巧可甜恋 mik01A 的身体+表情已经用真实图层验收；同尺寸、零偏移和面部边界吻合共同支持该组合，剧情中的实际出现位置未验证。

## Naninovel 分层预制体

先检查 MonoBehaviour 的 compositionMap/defaultAppearance，SpriteRenderer 的启用状态、SortingOrder、颜色，以及 Transform、Sprite pivot。素材使用 Dicing 不代表人物组合规则也已解析。

`naninovel_layers.py <bundle> --out <run>/inferred/<name>` 是**诊断性近似合成器**：
- 展开默认外观别名及分组选择，保留元数据和所选原图层。
- 使用共同父坐标系保留原生像素，处理颜色系数与 alpha-over。
- 限定本地对象引用、无局部旋转缩放、统一像素比例；遇到不支持结构报错。
- 尚未还原自定义 multiply/overlay/softlight 和 stencil 材质，强制写入 inferred；不能将其预览称为通过的完整渲染。

真实 Alisa 已读取默认组合并生成 14 层预览；因材质限制，状态为部分成功。后续可离线检查 Shader、材质参数并实现对应混色与遮罩，再与可靠参考图核对；必要的游戏运行仍先询问。

## Naninovel 资料中的额外分岔

本节核对官方文档 v1.21（2026-10-19）；实际游戏组件与版本需另行匹配。

[官方角色说明](https://naninovel.com/guide/characters#layered-characters) 区分 `group>layer` 的组内选择、`group+layer` 的启用和 `group-layer` 的关闭；`group>` 并不表示隐藏该组。解析别名、嵌套分组和初始 Renderer 状态时，结合本地组件字段与实际版本，不凭表情文件名枚举。

同页的 Render Only 可把外观管理交给 Animator／自定义逻辑，Camera Rendering 可使用独立相机处理复杂渲染。遇到这些字段，compositionMap 可能不足以描述实际状态；继续解析相关控制器、相机、材质和遮罩，缺少证据的预览保留 inferred。官方流程还可能先渲染到临时 RenderTexture；因此正确图层与坐标并不足以保证最终 RGBA。现有 naninovel_layers.py 仍只是其已列条件内的诊断器。
