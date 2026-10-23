import ast, operator, datetime

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算四则运算表达式，如 (12+34)*2",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
]

def _safe_calc(expr):
    # 用 ast 解析做安全计算，避免 eval 直接执行任意代码
    ops = {ast.Add: operator.add, ast.Sub: operator.sub,
           ast.Mult: operator.mul, ast.Div: operator.truediv}
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("不支持的表达式")
    return _eval(ast.parse(expr, mode="eval"))

def call_tool(name, args):
    if name == "get_current_time":
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name == "calculator":
        try:
            return str(_safe_calc(args["expression"]))
        except Exception as e:
            return f"计算失败: {e}"
    return f"未知工具: {name}"