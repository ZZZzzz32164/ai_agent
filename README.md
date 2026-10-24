# AI Agent（Function Calling）

一个带工具调用（Function Calling）的 AI 助理 Agent，用 Python + DeepSeek 大模型实现。

## 功能
- 调用大模型 RESTful API，解析 JSON
- system prompt 人设 + 多轮对话 + 上下文窗口裁剪
- Function Calling：Agent 自主决定调用「查时间」「计算器」等工具
- 封装为可复用的 Agent 类
- RAG 检索增强：先检索知识库资料，再据此回答，减少幻觉

## 运行
```powershell
pip install requests python-dotenv
# 在 .env 填入 API_KEY / BASE_URL / MODEL
python agent_class.py
```

## 文件
- llm.py：LLM API 封装
- tools.py：工具定义与执行
- agent.py：交互式 Agent
- agent_class.py：可复用 Agent 类
- rag.py：RAG 检索增强问答
- knowledge.txt：知识库文档