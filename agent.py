import json
from llm import chat
from tools import TOOLS, call_tool

SYSTEM_PROMPT = "你是智能助理。需要查时间或算数时，先用对应工具，再把结果告诉用户。"
HISTORY_LIMIT = 6

def trim(messages):
    return [messages[0]] + messages[1:][-HISTORY_LIMIT:]

def run():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("AI Agent 就绪（输入 q 退出）")
    while True:
        user = input("你: ").strip()
        if user.lower() == "q":
            break
        messages.append({"role": "user", "content": user})
        messages = trim(messages)

        data = chat(messages, tools=TOOLS)
        msg = data["choices"][0]["message"]
        messages.append(msg)   # 保存 assistant 回复（可能带 tool_calls）

        while msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                name = tc["function"]["name"]
                args = json.loads(tc["function"]["arguments"])
                result = call_tool(name, args)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": result})
            data = chat(messages, tools=TOOLS)
            msg = data["choices"][0]["message"]
            messages.append(msg)

        print("AI:", msg["content"])

if __name__ == "__main__":
    run()