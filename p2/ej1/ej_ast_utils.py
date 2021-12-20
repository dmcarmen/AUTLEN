# Ejemplos ejercicio 1
import ast
import inspect
from ast_utils import ASTMagicNumberDetector, ASTDotVisitor, ASTReplaceNum, transform_code, ASTRemoveConstantIf

# Ejemplo apartado (a)
def my_fun_a(p: complex) -> None:
    if p == 1:
        print(p + 1j)
    elif p == 5:
        print(0)
    else:
        print(p - 27.3 * 3j)

def test_a() -> None:
    source = inspect.getsource(my_fun_a)
    my_ast = ast.parse(source)

    magic_detector = ASTMagicNumberDetector()
    magic_detector.visit(my_ast)

    # Debería dar 3
    print(magic_detector.magic_numbers)

# Ejemplo apartado (b)
def print_next_if_pos(num: int) -> None:
    if num > 0:
        print(num + 1)

def test_b() -> None:
    source = inspect.getsource(print_next_if_pos)
    my_ast = ast.parse(source)

    dot_visitor = ASTDotVisitor()
    dot_visitor.visit(my_ast)
    # Debería generar este texto dot

'''
    digraph {
    s0[label="Module()"]
    s1[label="FunctionDef(name='print_next_if_pos', returns=None)"]
    s0 -> s1[label="body"]
    s2[label="arguments(vararg=None, kwarg=None)"]
    s1 -> s2[label="args"]
    s3[label="arg(arg='num', annotation=None)"]
    s2 -> s3[label="args"]
    s4[label="If()"]
    s1 -> s4[label="body"]
    s5[label="Compare()"]
    s4 -> s5[label="test"]
    s6[label="Name(id='num')"]
    s5 -> s6[label="left"]
    s7[label="Load()"]
    s6 -> s7[label="ctx"]
    s8[label="Gt()"]
    s5 -> s8[label="ops"]
    s9[label="Num(n=0)"]
    s5 -> s9[label="comparators"]
    s10[label="Expr()"]
    s4 -> s10[label="body"]
    s11[label="Call()"]
    s10 -> s11[label="value"]
    s12[label="Name(id='print')"]
    s11 -> s12[label="func"]
    s13[label="Load()"]
    s12 -> s13[label="ctx"]
    s14[label="BinOp()"]
    s11 -> s14[label="args"]
    s15[label="Name(id='num')"]
    s14 -> s15[label="left"]
    s16[label="Load()"]
    s15 -> s16[label="ctx"]
    s17[label="Add()"]
    s14 -> s17[label="op"]
    s18[label="Num(n=1)"]
    s14 -> s18[label="right"]
    }
'''

# Ejemplo apartado (c)
def my_fun_c(p): # type: ignore
    if p == 1:
        print(p + 1j)
    elif p == 5:
        print(0)
    else:
        print(p - 27.3 * 3j)

def test_c() -> None:
    num_replacer = ASTReplaceNum(3)
    new_fun = transform_code(my_fun_c, num_replacer)

    new_fun(1)
    # Debería imprimir -8

    new_fun(3)
    # Debería imprimir 6

# Ejemplo apartado (d)
def my_fun_d() -> int:
    if True:
        return 1
    else:
        return 0

def test_d() -> None:
    source = inspect.getsource(my_fun_d)
    my_ast = ast.parse(source)
    #dot_visitor = ASTDotVisitor()
    #dot_visitor.visit(my_ast)
    if_remover = ASTRemoveConstantIf()
    new_ast = if_remover.visit(my_ast)
    dot_visitor = ASTDotVisitor()
    dot_visitor.visit(new_ast)

# Ejemplo 2 apartado (d)
def my_fun_d2() -> int:
    if False:
        return 1
    elif False:
        return 2
    elif True:
        return 3
    else:
        return 4

def test_d2() -> None:
    source = inspect.getsource(my_fun_d2)
    my_ast = ast.parse(source)
    if_remover = ASTRemoveConstantIf()
    new_ast = if_remover.visit(my_ast)
    dot_visitor = ASTDotVisitor()
    dot_visitor.visit(new_ast)

test_a()
test_b()
test_c()
test_d()
test_d2()
