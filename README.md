# api-lab-lmstudio-local-minimal

> 最小化体验：调用本机 **LM Studio** 启动的 OpenAI-compatible 本地服务。

## 它在做什么

LM Studio 是一个图形界面工具，主要做两件事：

1. 帮你下载/加载本地模型（GGUF 等格式）
2. 启动一个兼容 OpenAI 协议的本地 server（默认 `http://localhost:1234/v1`）

所以本仓库的代码，本质上和 `api-lab-openai-compatible-minimal` 几乎一样——
只是把 `AI_BASE_URL` 指向了本机端口而已。这正是「OpenAI-compatible 是个事实标准」的真实证据。

## 准备工作（必须按顺序）

1. 装 LM Studio：https://lmstudio.ai/
2. 在它里面 **Search/Download** 一个模型（推荐选小模型，比如 1B～3B 量级，文件名带 `Q4_K_M` 这类量化级别）
3. **加载** 这个模型（点 Load）
4. 切到 **Local Server** 面板，点 **Start Server**
5. 看面板上显示的：
   - server URL（默认 `http://localhost:1234/v1`）
   - 当前 model 标识符
6. 把这两个值填进 `.env`

## 运行步骤

```bash
cd api-lab-lmstudio-local-minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env：
#   LMSTUDIO_BASE_URL=http://localhost:1234/v1
#   LMSTUDIO_MODEL=（LM Studio 面板上显示的 model identifier）
#   LMSTUDIO_API_KEY=lm-studio       # 本地不验证，占位符即可

python3 main.py
cat output/result.json
```

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `无法连接到 LM Studio local server` | 没启动 server | 在 LM Studio 'Local Server' 面板点 Start |
| `HTTP 404` model not found | 模型名拼错 | 直接复制 LM Studio 面板上显示的字符串 |
| `请求超时` | 模型太大本机扛不住 | 换更小模型、或在 LM Studio 设置里降低 context window |
| `Connection refused` | 端口被改了 / 防火墙 | 看面板显示的实际端口，更新 `LMSTUDIO_BASE_URL` |

## 核心思考点

**为什么 LM Studio 能模拟 OpenAI-compatible？**

因为 OpenAI 的 `/v1/chat/completions` 协议是开放的、文档化的。任何团队只要：

- 接受同样形状的 JSON
- 返回同样形状的 JSON

就可以"看起来像 OpenAI"。LM Studio 在本地跑一个 HTTP server，
内部把请求转成对 GGUF/llama.cpp 的调用，再把结果包装回 OpenAI 形状。

所以"OpenAI-compatible"不是 OpenAI 的特权，是协议形态。
**这一仓库就是要让你亲手摸到这件事。**

## .env.example

```
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=填入LM Studio当前加载的模型名
LMSTUDIO_API_KEY=lm-studio
```

## 不会做的事

- 不会自动下载模型
- 不会自动启动 LM Studio
- 不会反复重试
