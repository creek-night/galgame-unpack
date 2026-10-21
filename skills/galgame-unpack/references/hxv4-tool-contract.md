# Hxv4 外部 bounded decoder 契约

这是现有包装器所需接口，不是通用 Hxv4 工具的官方协议。维护者的定制实现未包含在公开包中；此分支需自行实现/提供兼容工具再验收。其他已支持格式不依赖它。

`tool.json` 位于解码器目录，含 `binary`（同目录下的相对路径）和 `binary_sha256`（实际 SHA-256）。包装器拒绝越出清单目录的程序或哈希不符的文件。

WSL 命令参数依次为：`<binary> <game-exe-as-data> <archive> <output.partial> --index`，提取时最后一项改为 `#<zero-based-entry-index>`。退出码非 0 表示失败；调用者还在 WSL 外验证结果。

索引为 UTF-8 TSV，表头必须是 `index\tname\tunpacked_size\tadler32\thx_info`（分隔符为实际 tab）。每行连续序号、未压缩长度、8 位十六进制 Adler32；stdout 恰有一条 `indexed N entries ->...` 完成标记。完整包装器会核对数量、尺寸范围，再保存索引 sidecar 与源/工具哈希。

提取输出须匹配选定索引的原始长度与 Adler32；仅明确的 KiriKiri type-1 可逆文本转换有专门重建校验。未知转换不能跳过校验。`find` 当前只实现历史变体的 `xp3hnp` 文件名域，不支持所有盐值或目录哈希。

工具的源码来源、版本、构建依赖和许可由提供方记录。升级或替换二进制后重建索引并用独立真实样本验证，不复用旧工具的成功状态。
