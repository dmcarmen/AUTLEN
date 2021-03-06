import unittest

from grammar.grammar import Grammar, LL1Table, TableCell, ParseTree, SyntaxError
from grammar.utils import GrammarFormat, parse_tree_to_dot
from typing import Optional, Type

class TestAnalyze(unittest.TestCase):
    def _check_analyze(
            self,
            table: LL1Table,
            input_string: str,
            start: str,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            if exception is None:
                self.assertTrue(table.analyze(input_string, start) is not None)
            else:
                with self.assertRaises(exception):
                    table.analyze(input_string, start)

    def _check_analyze_from_grammar(
            self,
            grammar: Grammar,
            input_string: str,
            start: str,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            table = grammar.get_ll1_table()
            self.assertTrue(table is not None)
            if table is not None:
                if exception is None:
                    self.assertTrue(table.analyze(input_string, start) is not None)
                else:
                    with self.assertRaises(exception):
                        table.analyze(input_string, start)

    def _check_parse_tree(
            self,
            table: LL1Table,
            input_string: str,
            start: str,
            tree: ParseTree,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            if exception is None:
                self.assertEqual(table.analyze(input_string, start), tree)
            else:
                with self.assertRaises(exception):
                    table.analyze(input_string, start)

    def test_case1(self) -> None:
        """Test for syntax analysis from table."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [TableCell('E', '(', 'TX'),
                 TableCell('E', 'i', 'TX'),
                 TableCell('T', '(', '(E)'),
                 TableCell('T', 'i', 'iY'),
                 TableCell('X', '+', '+E'),
                 TableCell('X', ')', ''),
                 TableCell('X', '$', ''),
                 TableCell('Y', '*', '*T'),
                 TableCell('Y', '+', ''),
                 TableCell('Y', ')', ''),
                 TableCell('Y', '$', '')]
        table = LL1Table(non_terminals, terminals, cells)

        self._check_analyze(table, "i*i$", "E")
        self._check_analyze(table, "i*i+i$", "E")
        self._check_analyze(table, "i*i+i+(i*i)$", "E")
        self._check_analyze(table, "a", "E", exception=SyntaxError)
        self._check_analyze(table, "(i$", "E", exception=SyntaxError)
        self._check_analyze(table, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze(table, "i*i", "E", exception=SyntaxError)
        self._check_analyze(table, "+i*i", "E", exception=SyntaxError)

    def test_case2(self) -> None:
        """Test for syntax analysis from grammar."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)

        self._check_analyze_from_grammar(grammar, "i*i$", "E")
        self._check_analyze_from_grammar(grammar, "i*i+i$", "E")
        self._check_analyze_from_grammar(grammar, "i*i+i+(i*i)$", "E")
        self._check_analyze_from_grammar(grammar, "a", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "(i$", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "+i*i", "E", exception=SyntaxError)

    def test_case3(self) -> None:
        """Test for parse tree construction."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [TableCell('E', '(', 'TX'),
                 TableCell('E', 'i', 'TX'),
                 TableCell('T', '(', '(E)'),
                 TableCell('T', 'i', 'iY'),
                 TableCell('X', '+', '+E'),
                 TableCell('X', ')', ''),
                 TableCell('X', '$', ''),
                 TableCell('Y', '*', '*T'),
                 TableCell('Y', '+', ''),
                 TableCell('Y', ')', ''),
                 TableCell('Y', '$', '')]
        table = LL1Table(non_terminals, terminals, cells)

        t01 = ParseTree("??")
        t02 = ParseTree("X", [t01])
        t03 = ParseTree("??")
        t04 = ParseTree("Y", [t03])
        t05 = ParseTree("i")
        t06 = ParseTree("T", [t05, t04])
        t07 = ParseTree("*")
        t08 = ParseTree("Y", [t07, t06])
        t09 = ParseTree("i")
        t10 = ParseTree("T", [t09, t08])
        tree = ParseTree("E", [t10, t02])

        self._check_parse_tree(table, "i*i$", "E", tree)

    def test_case4(self) -> None:
        """Test for not LL1 grammar."""
        grammar_str = """
        X -> I*AD
        I -> A*I
        I -> a
        I ->
        A -> aa*A
        A ->
        A -> a
        D -> *
        D ->
        """
        grammar = GrammarFormat.read(grammar_str)
        table = grammar.get_ll1_table()
        self.assertEqual(table, None)

    def test_case5(self) -> None:
        """Test for syntax analysis from grammar."""
        grammar_str = """
        E -> XY
        X -> 
        Y -> yX
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)

        self._check_analyze_from_grammar(grammar, "$", "E")
        self._check_analyze_from_grammar(grammar, "y$", "E")
        self._check_analyze_from_grammar(grammar, "yy$", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "+i*i", "E", exception=SyntaxError)

    def test_case6(self) -> None:
        """Test for syntax analysis from grammar."""
        grammar_str = """
        E -> XY
        X -> 
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)

        self._check_analyze_from_grammar(grammar, "$", "E")
        self._check_analyze_from_grammar(grammar, "yy$", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "+i*i", "E", exception=SyntaxError)
    
    def test_case7(self) -> None:
        """Test for  LL1 grammar."""
        grammar_str = """
        S->V=E
        V->iR
        R->
        R->[E]
        E->k
        E->i
        E->f(k)
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_analyze_from_grammar(grammar, "i[i]=i$", "S")
        self._check_analyze_from_grammar(grammar, "i=f(k)$", "S")
        self._check_analyze_from_grammar(grammar, "i[f(k)]=f(k)$", "S")
        self._check_analyze_from_grammar(grammar, "i=i$", "S")
        self._check_analyze_from_grammar(grammar, "=i$", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "ii=i$", "E", exception=SyntaxError)

    def test_case8(self) -> None:
        """Test for parse tree construction."""
        grammar_str = """
        S->V=E
        V->iR
        R->
        R->[E]
        E->k
        E->i
        E->f(k)
        """
        grammar = GrammarFormat.read(grammar_str)
        table = grammar.get_ll1_table()
        tree = table.analyze("i=f(k)$","S")
        print(parse_tree_to_dot(tree))

if __name__ == '__main__':
    unittest.main()
