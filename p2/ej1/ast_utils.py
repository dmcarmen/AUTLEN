import numbers
import ast
import inspect
import types
from typing import List, Union, Optional, Callable, Any

class ASTMagicNumberDetector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.magic_numbers = 0

    def _check_magic_number(self, number: complex) -> bool:
        if isinstance(number, numbers.Number) and number != complex(0) and number != complex(1) and number != (1j):
            return True
        else:
            return False

    # Para Python < 3.8
    def visit_Num(self, node: ast.Num) -> None:
        if self._check_magic_number(node.n):
            self.magic_numbers += 1

    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> None:
        if self._check_magic_number(node.value):
            self.magic_numbers += 1


class ASTDotVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.n_node = 0

    def visit(self, node: ast.AST, parent: Optional[int] = None, field_name: str = "", level: int = 0) -> None:
        this_node = self.n_node
        if self.n_node == 0:
            print('digraph {')
        self.n_node += 1

        n = f's{this_node}[label="{type(node).__name__}('

        if parent != None:
            print(f's{parent} -> s{this_node}[label="{field_name}"]')

        n_args = ''

        for field, value in ast.iter_fields(node): # Itera por los hijos
            field_name = field
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, this_node, field_name, level + 1)
            elif isinstance(value, ast.AST):
                self.visit(value, this_node, field_name, level + 1)
            else:
                if len(n_args) == 0:
                    n_args = f'{field}={value}'
                else:
                    n_args += f', {field}={value}'

        print(n + n_args + ')"]')

        level -= 1
        if level == -1:
            print("}")


def transform_code(f: Callable[...,Any], transformer: ast.NodeTransformer) -> Callable[...,Any]:
    f_ast = ast.parse(inspect.getsource(f))

    new_tree = ast.fix_missing_locations(transformer.visit(f_ast))

    old_code = f.__code__
    code = compile(new_tree, old_code.co_filename, 'exec')
    new_f = types.FunctionType(code.co_consts[0], f.__globals__) # type: ignore

    return new_f

class ASTReplaceNum(ast.NodeTransformer):
    def __init__(self , number: complex):
        self.number = number

    # Para Python < 3.8
    def visit_Num(self, node: ast.Num) -> ast.AST :
    # devolver un nuevo nodo AST con self.number
        return ast.Num(self.number)

    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> ast.AST :
    # devolver un nuevo nodo AST con self.number si la constante es un número
        if isinstance(node.value, numbers.Number):
            return ast.Constant(self.number)
        else:
            return node

class ASTRemoveConstantIf(ast.NodeTransformer):
    def visit_If(self, node: ast.If) -> Union[ast.AST, List[ast.stmt]]:
        while(True):
            if(isinstance(node,ast.If)):
                if(isinstance(node.test, ast.Constant)):
                    if(str(node.test.value) == "True"):
                        nodes = []
                        for elem in node.body:
                            nodes.append(self.visit(elem))
                        return nodes
                    elif(str(node.test.value) == "False"):
                        if len(node.orelse) > 0:
                            node = node.orelse[0]
                        else:
                            return None
                    else:
                        break
            else:
                break
        return node
