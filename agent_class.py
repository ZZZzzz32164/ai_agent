import json
from llm import chat
from tools import TOOLS, call_tool

class Agent:
    def __init__(self, system_prompt, history_limit=6, tools=TOOLS):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.history_limit = history_limit
        self.tools = tools

    def _trim(self):
        # 保留 system，只留最近 history_limit 条
        self.messages = [self.messages[0]] + self.messages[1:][-self.history_limit:]

    def ask(self, text):
        self.messages.append({"role": "user", "content": text})
        self._trim()
        data = chat(self.messages, tools=self.tools)
        msg = data["choices"][0]["message"]
        self.messages.append(msg)

        while msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                result = call_tool(tc["function"]["name"], json.loads(tc["function"]["arguments"]))
                self.messages.append({"role": "tool", "tool_call_id": tc["id"], "content": result})
            data = chat(self.messages, tools=self.tools)
            msg = data["choices"][0]["message"]
            self.messages.append(msg)
        return msg["content"]

if __name__ == "__main__":
    a = Agent("你是智能助理，需要查时间或算数时先调用工具。")
    print(a.ask("现在几点了？"))
    print(a.ask("帮我算 (12+34)*2 等于多少"))