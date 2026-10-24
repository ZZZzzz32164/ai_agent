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
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "获取指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名，如 杭州"}},
                "required": ["city"],
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
    if name == "get_city_weather":
        city = args.get("city", "未知")
        # 演示用示例数据：接入真实天气 API（如和风天气 QWeather，免费额度）时，
        # 用 requests 请求其接口替换这里的字典即可。
        mock = {
            "杭州": "多云 18℃ 微风",
            "北京": "晴 15℃ 西北风3级",
            "上海": "小雨 20℃ 东南风2级",
            "深圳": "多云 26℃ 南风2级",
        }
        return mock.get(city, f"{city}：晴 20℃（示例数据，暂未收录该城市）")
    return f"未知工具: {name}"