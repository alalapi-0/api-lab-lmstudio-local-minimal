"""api-lab-lmstudio-local-minimal

调用本机 LM Studio 启动的 OpenAI-compatible local server。

LM Studio 是一个 GUI 工具：
- 你在它里面下载/加载一个模型
- 它会在本机起一个兼容 OpenAI /v1/chat/completions 的 server（默认 1234 端口）
- 这样你就能用任何"标准 OpenAI 客户端"打它，包括本脚本

API Key 部分通常是占位符 'lm-studio'，因为本地不验证。
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROMPT = "请解释为什么 LM Studio 可以模拟 OpenAI-compatible API。"
TIMEOUT_SECONDS = 30
MAX_TOKENS = 100


def main() -> int:
    load_dotenv()

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1").rstrip("/")
    model = os.getenv("LMSTUDIO_MODEL", "").strip()
    api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio").strip()

    if not model:
        print("[错误] 未在 .env 中检测到 LMSTUDIO_MODEL。")
        print("       请打开 LM Studio，加载一个模型，然后把它显示的模型标识填进 .env。")
        return 2

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
    }

    print(f"[信息] endpoint = {url}")
    print(f"[信息] model    = {model}")
    print(f"[信息] prompt   = {PROMPT}")

    started = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.ConnectionError:
        print("[失败] 无法连接到 LM Studio local server。")
        print("       1) 打开 LM Studio 应用")
        print("       2) 加载一个模型")
        print("       3) 在 'Local Server' 面板点 'Start Server'")
        print("       4) 确认 .env 中的 LMSTUDIO_BASE_URL 与它显示的端口一致（默认 1234）")
        return 1
    except requests.exceptions.Timeout:
        print(f"[失败] 请求超时（{TIMEOUT_SECONDS}s）。本地小模型偶尔很慢。")
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"[失败] 网络请求异常: {exc}")
        return 1
    elapsed = time.time() - started

    if resp.status_code != 200:
        print(f"[失败] HTTP {resp.status_code}")
        print(f"        响应片段: {resp.text[:300]}")
        print("        提示：LM Studio 的 server 启动后应能 curl 通 /v1/models")
        return 1

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        print("[失败] 响应结构与 OpenAI-compatible /chat/completions 预期不符。")
        print(f"        原始响应片段: {resp.text[:300]}")
        return 1

    print()
    print("[成功] 模型返回内容：")
    print(content)
    print()
    print(f"[信息] 耗时 {elapsed:.2f}s（含本地推理）")

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    result = {
        "provider": "lmstudio-local",
        "base_url": base_url,
        "model": model,
        "prompt": PROMPT,
        "elapsed_seconds": round(elapsed, 3),
        "content": content,
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
