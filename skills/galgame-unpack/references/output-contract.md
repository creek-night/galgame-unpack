# 输出与验收记录

输出根使用本次指定路径、`GALGAME_UNPACK_OUTPUT_ROOT` 或用户主目录下的 `galgame-unpack-output`，每个游戏每次运行独立目录。本次新增工具、依赖、缓存和临时文件均在此根下；用户指定的现有工具目录可作只读依赖并记录指纹，技能源码和安装副本沿用用户已确认的位置。

- `assets/cg`、`assets/sprites`、`assets/layers`：可用成品和保留原层。其他明确选择的类别单独建目录。
- `inferred`：推断组合、尚未还原的渲染；附依据及局限。
- `work`、`scripts`、`logs`、`previews`：过程、脚本快照、诊断、预览。
- `manifest.json`、`report.md`：机器可读来源及面向用户的结果。
- 根下 `_tools`、`_profiles`：可复用工具与经过验证的适配方案。

new_run 初始化 manifest；完成时补充 sources、outputs、unresolved 和真实 status，保留原始范围与选项。每个输出应可追溯到源文件、条目/对象、解码器或合成 recipe；记录 SHA256、分辨率、透明通道、分类依据和验证等级。源含外部资源流时一并列入。

报告至少说明：
1. 请求与实际完成范围，样本的选择依据及具体数量。
2. 成功、部分成功、未解决、不适用的能力；可解码文件不等于可用成品。
3. 版本/补丁的选择依据，未知覆盖关系、占位图和推断项。
4. 工具版本、脚本、关键诊断和预览路径。
5. 涉及匿名条目时，分别记录内容解码、名称与目录恢复状态。获准运行时抓取后，列出触发过的场景、分支与过滤规则；未建立完整清单时只报告已触发素材，见[社区经验](community-experience.md#运行时抓取与渲染边界)。

`verify_images.py <run> --tag <唯一名称>` 会解码 assets/inferred 内 PNG、记录哈希/尺寸/alpha，并将非 layers 图片合成带棋盘背景的预览。真实 PNG 保持 RGBA；直接查看透明图片时，某些查看器会显示隐藏的 RGB 扩边，需用 alpha 合成预览检查。

它不会判断剧情分类、原分辨率、补丁优先级或“是不是黑图占位”，这些由调查和图像检查补充。重复验收使用新的 tag，避免覆盖旧记录。

适配方案只在真实验证后保存：
```text
_profiles/<方案>/
  profile.json       游戏/版本、源文件大小和哈希、必要签名、工具/算法版本、已验证范围、局限、证据链接
  scripts/           本次成功代码快照
```
精确哈希匹配只允许复用该样本结论。新版本或文件不匹配可参考方案重新采样，不能直接继承已验证状态；结构通用的算法也需要对本次实际素材验收。

## 统一完成清单

新输出使用一种字段形式；历史字段只在 --legacy 读取时兼容。sources 中每项为 path、bytes、sha256；outputs 中每项至少含 path、sha256、category、complete，PNG 还须 size。完整 PNG 示例：

```json
{
  "path": "assets/sprites/character.png",
  "sha256": "<实际 SHA256>",
  "size": [1360, 2900],
  "alpha_extrema": [0, 255],
  "category": "sprites",
  "complete": true,
  "native_canvas_evidence": "原始层表/纹理矩形及对应位置",
  "classification_evidence": "人物用途、服装和脚本引用",
  "visual_review": "实际图像检查结果",
  "provenance": {"source": "<源包>", "entry": "<确切条目>"},
  "recipe": "work/recipe.json"
}
```

recipe 只用于有明确 normal alpha-over 配方的成品；其他图像省略。category 使用 cg / sprites / layers 或本次选择的其他类别。原层与 inferred 的 complete 为 false。unresolved 统一为对象数组，每项包含 category、reason，可附 next_step；passed/partial/blocked 描述实际范围。requested_categories 必须是明确、非空的类别数组，与 extras 合并作为验收范围；只选 CG 时无需立绘。passed 要求每个所选类别至少有可验证成品，并且该类别没有 unresolved；full 下的 coverage 未解决项也会阻止 passed。样本范围之外的限制可如实记录，不能移走实际未完成项以获得通过。类别数量满足只证明已有代表成品，不证明全量覆盖。

检查器自动验证 PNG 及明确合成配方；声明 media_type=audio/text 的条目按[媒体验证](media-validation.md)执行完整音频解码或严格文本解码，同时要求对应元数据、分类依据、内容检查和来源。尚无对应解码路径的其他文件必须 complete=false，会逐项记入 unverified_outputs/hash_only；选择了这些未完成类别时保留 partial／blocked。未解码辅助原件不妨碍已选类别通过。--legacy 仅读取旧记录。

```powershell
& $taskPy -B "$taskSkill\scripts\verify_run.py" "$taskRun\manifest.json" --out "$taskRun\logs\manifest-check.json"
```

该检查核对文件范围、重复条目、SHA256、尺寸、alpha、类别完成计数，并对声明的配方独立重合成逐像素比较。--sources 额外核对源 SHA256；保存 profile 时默认执行。它不替代目视、语义分类或补丁加载顺序证据。旧报告可用 --legacy 复核，未明确的完整性字段保持未知。
