# LEARNING — api-lab-lmstudio-local-minimal

> 这份文件回答：「我跑完这个仓库，应该真的学到什么？」

## 你跑完应该能回答的问题

1. LM Studio 到底做了什么，让"本地模型"看起来像"OpenAI API"？
2. "OpenAI-compatible"为什么是个**协议形态**，而不是 OpenAI 公司的特权？
3. 既然有 Ollama，为什么还要 LM Studio？两者各擅长什么场景？
4. 我能用同一份 OpenAI-compatible 客户端代码"打"LM Studio 吗？

## 实操验证清单（务必动手）

### 阶段 A — 环境就绪（GUI 操作，不能跳过）
- [ ] 装 LM Studio：https://lmstudio.ai/
- [ ] 在它界面里 Search/Download 一个**小**模型（推荐：1B～3B、文件名带 `Q4_K_M` 这类量化级别）
- [ ] 在 Chat 面板里 **Load** 它，先用 GUI 聊一句确认能跑
- [ ] 切到 **Local Server** 面板，点 **Start Server**
- [ ] 看面板上显示的 server URL 和 model identifier
- [ ] 验证服务存活：`curl http://localhost:1234/v1/models` 应返回 JSON

### 阶段 B — 跑本仓库
- [ ] `cp .env.example .env`
- [ ] `pip install -r requirements.txt`
- [ ] 编辑 `.env`：
  ```
  LMSTUDIO_BASE_URL=http://localhost:1234/v1
  LMSTUDIO_MODEL=（直接粘贴 LM Studio 面板上的 model identifier）
  LMSTUDIO_API_KEY=lm-studio
  ```
- [ ] `python3 main.py`

### 阶段 C — 「这就是 OpenAI 协议化」实验（核心）
**这一步最能让你"信"OpenAI-compatible。**

- [ ] 不要改 LM Studio
- [ ] 切到 `api-lab-openai-compatible-minimal/` 仓库
- [ ] 把它的 `.env` 改成：
  ```
  AI_API_KEY=lm-studio
  AI_BASE_URL=http://localhost:1234/v1
  AI_MODEL=（同样的 model identifier）
  ```
- [ ] 在那个仓库跑 `python3 main.py` → **应该照样成功**
- [ ] 这意味着：**云端 OpenAI 客户端 + LM Studio 本地服务，零代码改动就能互通**

### 阶段 D — 网络通路理解
- [ ] 在另一个终端 `tcpdump`/`mitmproxy`（高级），或者只是想象一下：
  - 你的 `requests.post()` 把 JSON 发到 `localhost:1234`
  - LM Studio 进程接收 → 把 JSON 翻译成对内置 llama.cpp 的调用
  - llama.cpp 用本机 CPU/GPU 吐出 token → LM Studio 包成 OpenAI 形状的 JSON 返回
- [ ] **关键：你的请求从未离开本机**

### 阶段 E — 多模型切换
- [ ] 在 LM Studio 里 Eject 当前模型，加载另一个
- [ ] **不改代码、不改 .env**，再跑 `python3 main.py` → 应该立刻用新模型回答
  （注意：LM Studio 老版本是"当前加载的模型"，新版本会让你在 .env 里指定模型 identifier；按你装的版本走）

## 自检题

1. LM Studio 和 Ollama 看起来都"在本机起一个 server 跑模型"，它们的差别更多在 GUI 还是协议？
2. 我能不能让 LM Studio 把 server 监听到外网 IP？这样安不安全？
3. 如果我把 `LMSTUDIO_API_KEY` 留空（不传 Authorization），LM Studio 会拒绝吗？为什么？
4. 我用 LM Studio 跑了一个量化版的 Llama-3.2-3B，回答质量明显比云端 GPT-4o 差。这是模型本身、量化、还是协议带来的？

## 与其它仓库的连接

| 关系 | 仓库 | 为什么去看 |
| --- | --- | --- |
| **关键对照** | `api-lab-openai-compatible-minimal` | 把它的 base_url 指向 LM Studio 端口，就跑通了——**协议化的最强证据** |
| **同类不同形态** | `api-lab-ollama-local-minimal` | Ollama 默认走 `/api/chat`，LM Studio 走 `/v1/chat/completions`；两条路并存 |
| **客户端 vs 服务** | `api-lab-tool-calling-minimal` | tool-calling 仓库的 `.env` 三件套也可以改成 LM Studio 的端口，直接拿本地模型试 Agent 雏形 |

## 你应该感受到的"啊哈"瞬间

- 当你**没改一行代码**，把云端 OpenAI 客户端指向本机 LM Studio 跑通——你会真的相信"OpenAI-compatible"是个协议而非品牌。
- 当你看到本机 1.5B 量化模型也能勉强回答 prompt——你会更平等地看待"模型大小"与"任务匹配度"的关系。
- 当你发现把 LM Studio 关了，云端代码立刻报 connection refused——你会更深刻意识到 `base_url` 这个变量背后其实是一整个**进程**。
