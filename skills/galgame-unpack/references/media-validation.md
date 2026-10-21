# 可选音频与文本

只有用户选择附加类别或本次明确进行能力测试时使用；默认仍是 CG 与立绘。先按引擎入口取回原始条目，保留精确条目名、源包与补丁关系。

## 音频

在隔离 Python 环境中安装技能根的 `requirements-audio.txt`；参考 [Windows 工具环境](windows-tools.md)。历史音频样本使用 soundfile 0.13.1，升级后应重新验证。原始 Ogg/WAV 已可用时保持字节，不为统一扩展名有损转码。

```powershell
& $taskPy -B "$taskSkill\scripts\verify_media.py" '<音频文件>' --kind audio --out "$taskRun\logs\audio-check.json"
```

检查全流解码、采样率、声道、帧数、有限样本值，记录峰值、RMS 和静音提示。当前允许 OGG/WAV/WAVEX/FLAC/MP3/AIFF；具体编解码器仍需实测。上限 512 MiB、8 声道、384 kHz、6 小时，超出先另行评估。静音不自动判坏，须结合用途区分正常静音、占位与解码错误。自动解码不证明 BGM/语音分类或听感正确。

完成条目增加 media_type="audio"，audio 至少包含实际整数 samplerate、channels、frames，可附 format/subtype；complete=true 仍需 classification_evidence、content_review、provenance。content_review 明确区分实际试听与信号/来源检查，不编造试听。verify_run 会重新解码，不能只提交旧检查 JSON 充当证明。

## 文本

```powershell
& $taskPy -B "$taskSkill\scripts\verify_media.py" '<文本文件>' --kind text --encoding cp932 --out "$taskRun\logs\text-check.json"
```

编码以文件头、引擎资料及实际正文为依据，严格解码；不使用忽略错误或替换字符掩盖乱码。支持 UTF-8/UTF-16 与显式端序、CP932/Shift-JIS、GB18030、Big5，64 MiB 上限。拒绝空正文、替换字符和非换行/制表控制字符。编码通过不等于内容语义正确或完整剧情。

完成条目增加 media_type="text"，text={encoding, characters}，记录实际 Unicode 字符数；complete=true 需要分类、content_review 和来源。剧情另需引擎脚本解析、说话人/选项/控制指令处理与阅读抽查；二进制脚本不能改扩展名当正文。只读脚本或说明文本用于关系调查，不自动追加剧情交付。

## 当前证据

本轮调优素材：常轨脱离 hamidashi.pfs 的 sound\bgm\bgm01_a.ogg，及真实 readme 的 CP932/UTF-8 对照。WAV 为该音频的转换控制；这不新增某引擎的剧情解析能力。独立样本与具体结果以本次运行报告为准，未列出的格式保持候选状态。

接口依据：[python-soundfile 0.13.1 文档](https://python-soundfile.readthedocs.io/en/latest/)。依赖指纹及真实采样信息随运行保存到 manifest.tools；分发 skill 不包含音频、文本或二进制依赖。
