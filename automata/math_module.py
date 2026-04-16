from __future__ import annotations

import ast
import operator as op
from typing import Any, Optional

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval_ast(node: ast.AST) -> Any:
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only int/float constants allowed")
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not allowed")
    raise ValueError(f"Unsupported expression: {type(node)}")


def safe_eval_expr(expr: str) -> float:
    expr = expr.strip()
    parsed = ast.parse(expr, mode="eval")
    return float(_eval_ast(parsed.body))


def try_solve_math(text: str) -> Optional[str]:
    expr = text.strip()
    allowed_chars = "0123456789+-*/(). ^"
    for ch in expr:
        if ch not in allowed_chars:
            return None
    expr = expr.replace("^", "**")
    try:
        result = safe_eval_expr(expr)
    except Exception:
        return None
    return f"The result of `{text}` is **{result}**."
