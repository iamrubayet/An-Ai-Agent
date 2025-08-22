import ast
import operator
import time
import logging
from typing import Any, Callable, Union
from functools import wraps


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Safe evaluation for mathematical expressions
ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def safe_eval(expr: str) -> float:
    """
    Safely evaluate a mathematical expression.
    Only supports numbers and basic operators.
    
    Args:
        expr: Mathematical expression as string
        
    Returns:
        Result of the calculation
        
    Raises:
        ValueError: If expression is invalid or contains unsupported operations
    """
    try:
        # Parse the expression into an AST
        node = ast.parse(expr.strip(), mode="eval").body
        return _eval_node(node)
    except Exception as e:
        raise ValueError(f"Invalid expression '{expr}': {e}")


def _eval_node(node) -> Union[int, float]:
    """Recursively evaluate AST nodes."""
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    elif isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        left_val = _eval_node(node.left)
        right_val = _eval_node(node.right)
        op = ALLOWED_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(left_val, right_val)
    elif isinstance(node, ast.UnaryOp):
        operand_val = _eval_node(node.operand)
        op = ALLOWED_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op(operand_val)
    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")


def log_execution_time(func: Callable) -> Callable:
    """Decorator to log function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = (time.time() - start_time) * 1000
            logger.info(f"{func.__name__} completed in {duration:.1f}ms")
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"{func.__name__} failed after {duration:.1f}ms: {e}")
            raise
    return wrapper


def normalize_text(text: str) -> str:
    """Normalize text for processing."""
    return text.strip().lower()


def extract_number_from_text(text: str) -> float:
    """Extract the first number found in text."""
    import re
    match = re.search(r'-?\d+(?:\.\d+)?', text)
    if match:
        return float(match.group())
    raise ValueError(f"No number found in text: {text}")