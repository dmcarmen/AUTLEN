import ast
import inspect
import unittest

from ast_utils import ASTRemoveConstantIf

def simple_fun() -> int:
    if True:
        return 1
    else:
        return 0

def more_simple_fun() -> int:
    if False:
        return 1
    elif False:
        return 2
    elif True:
        return 3
    else:
        return 4

def nested_fun() -> int:
    if True:
        if False:
            return 1
        else:
            return 2
    else:
        return 0

def more_nested_fun() -> int:
    if True:
        if False:
            return 1
        else:
            return 2
        a = 5
    else:
        return 0

def not_if() -> int:
    if False:
        return 1
    return 0

class TestIfASTRemoveConstantIf(unittest.TestCase):
    """Tests for ASTRemoveConstantIf."""

    def _assertNumNodeValue(self, node: ast.AST, value: float) -> None:
        self.assertIsInstance(node, (ast.Num, ast.Constant))
        if isinstance(node, ast.Num):
            self.assertEqual(node.n, value)
        else:
            self.assertEqual(node.value, value) # type: ignore

    def test_simple(self) -> None:
        """Test optimization simple case."""
        source = inspect.getsource(simple_fun)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)

        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 1)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 1)

    def test_more_simple(self) -> None:
        """Test optimization simple case."""
        source = inspect.getsource(more_simple_fun)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)

        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 1)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 3)

    def test_nested(self) -> None:
        """Test case with nested ifs."""
        source = inspect.getsource(nested_fun)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)

        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 1)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 2)

    def test_more_nested(self) -> None:
        """Test case with nested ifs with other stuff inside the if."""
        source = inspect.getsource(more_nested_fun)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)
        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 2)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 2)

    def test_not(self) -> None:
        """Test optimization simple case."""
        source = inspect.getsource(not_if)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)

        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 1)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 0)

if __name__ == "__main__":
    unittest.main()
