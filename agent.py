import os
from llm import chat

SYSTEM_PROMPT = "你是一个乐于助人的中文助手，回答要简洁、准确。"
HISTORY_LIMIT = 6      # 最多保留最近 6 条消息，防止撑爆上下文窗口

def trim(messages):
    # 永远保留第一条 system，只截断后面的旧消息
    kept = [messages[0]] + messages[1:][-HISTORY_LIMIT:]
    return kept

def run():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("AI 助手已就绪（输入 q 退出）")
    while True:
        user = input("你: ").strip()
        if user.lower() == "q":
            break
        messages.append({"role": "user", "content": user})
        messages = trim(messages)
        data = chat(messages)
        reply = data["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("AI:", reply)

if __name__ == "__main__":
    run()