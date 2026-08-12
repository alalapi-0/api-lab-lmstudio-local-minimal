# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 是否已运行真实本地模型 | 否 |
| 离线合同验证时间 | 2026-08-12 |
| 离线合同验证是否成功 | 是 |
| 模型名 | 未使用真实模型；测试占位符 `test-local` |
| 真实推理耗时 | — |
| 未实跑原因 | LM Studio 需所有者在 GUI 中加载模型并启动 server；本轮未获该外部状态授权 |

## 备注

LM Studio 是 GUI 应用，没有本仓库可依赖的标准 CLI 检测命令。本轮未打开 GUI、未点 Start Server、也未探测未确认的 localhost 服务。

在仓库外 disposable archive 中使用内存 stub 验证：缺少模型标识时 exit 2/no HTTP；本地 URL 归一化、占位 Bearer/body 与结果写入；connection error 的操作指引；响应结构异常失败。

下一步建议：

- 想体验：装 LM Studio → 下载小模型 → Start Server → 跑 `python3 main.py`
- 不想体验：跳过本仓库

## 运行日志（你跑完后手动追加）

```text
mock-contract-tests: PASS (missing model, success, connection error, malformed)
syntax: PASS
```
