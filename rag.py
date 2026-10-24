import jieba
from agent_class import Agent

STOPWORDS = {"的", "了", "是", "在", "和", "很", "也", "都", "就", "还", "有", "这", "那", "不", "上", "中", "为", "吗", "呢", "啊", "吧", "与", "或"}

def _tokenize(text):
    return [w for w in jieba.lcut(str(text)) if w not in STOPWORDS and w.strip()]

class RAGAgent(Agent):
    """在 Agent 基础上加检索增强：先检索知识库，再带资料回答。"""

    def __init__(self, knowledge_path="knowledge.txt", top_k=3, system_prompt=None):
        super().__init__(system_prompt or "你是智能助理，请优先依据参考资料回答；资料不足时如实说明。")
        with open(knowledge_path, encoding="utf-8") as f:
            text = f.read()
        self.chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
        self.top_k = top_k
        self.chunk_tokens = [set(_tokenize(c)) for c in self.chunks]

    def retrieve(self, question):
        """按「关键词重合数」检索最相关的 top_k 个文本块（轻量版，无向量库）。"""
        q = set(_tokenize(question))
        scored = sorted(
            ((len(q & ct), i) for i, ct in enumerate(self.chunk_tokens)),
            reverse=True,
        )
        return [self.chunks[i] for score, i in scored[: self.top_k] if score > 0]

    def ask(self, text):
        ctx = self.retrieve(text)
        context = "\n---\n".join(ctx) if ctx else "（未检索到相关资料）"
        grounded = f"[参考资料]\n{context}\n\n[问题]\n{text}\n请优先依据参考资料回答。"
        return super().ask(grounded)

if __name__ == "__main__":
    a = RAGAgent()
    print(a.ask("Function Calling 是怎么工作的？"))
    print(a.ask("什么是 Token 和上下文窗口？"))