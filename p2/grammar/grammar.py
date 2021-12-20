from __future__ import annotations

from typing import AbstractSet, Collection, MutableSet, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Production:
    """
    Class representing a production rule.

    Args:
        left: Left side of the production rule. It must be a character
            corresponding with a non terminal symbol.
        right: Right side of the production rule. It must be a string
            that will result from expanding ``left``.

    """

    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.left == other.left
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.left!r} -> {self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.left, self.right))

class Grammar:
    """
    Class that represent a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Production rules of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Collection[Production],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        for p in productions:
            if p.left not in non_terminals:
                raise ValueError(
                    f"{p}: "
                    f"Left symbol {p.left} is not included in the set "
                    f"of non terminals.",
                )
            if p.right is not None:
                for s in p.right:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"{p}: "
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )
    
    def compute_first_aux(self, sentence: str, computed: list[str]) -> AbstractSet[str]:
        """
        Auxiliar function to compute first without checking elements are valid each iteration
        
        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """
        
         # Si la produccion es lambda, devolvemos lambda
        if sentence == '':
            return {''} 

        primero: set[str] = set()
        lambda_flag = False

        for ch in sentence:

            # Si ya hemmos añadido elementos al set de primeros y
            # el primero del ultimo simbolo no terminal no tenia lambda
            # o el siguiente caracter es terminal.
            if len(primero) > 0:
                if lambda_flag is False:
                    return primero - {''}
                elif ch in self.terminals:
                    return primero.union({ch}) - {''}

            # Si es un caracter lo devolvemos.
            if ch in self.terminals:
                return set(ch)

            # Si es terminal recorremos sus producciones.
            elif ch in self.non_terminals:
                lambda_flag = False
                for pr in self.productions:
                    if pr.left == ch:
                        # Calculamos el primero de cada produccion y lo añadimos.
                        # Guardamos si alguna de estas producciones es lambda.
                        if(pr.right not in computed):
                            n_first = self.compute_first_aux(pr.right, computed + [pr.right])
                            if '' in n_first and lambda_flag is False:
                                lambda_flag = True
                            primero = primero.union(n_first)

        # Si la sentencia no puede ser lambda la quitamos.
        if lambda_flag is False:
            return primero - {''}
        return primero

    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """
        #Comprobamos que todos los elementos de la cadena son válidos
        for ch in sentence:
            if not (ch in self.terminals or ch in self.non_terminals):
                raise ValueError

        return self.compute_first_aux(sentence, [sentence])
    
    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """
        
        if not symbol in self.non_terminals:
            raise ValueError
        return self.compute_follow_aux(symbol, [symbol])


    def compute_follow_aux(self, symbol: str, computed: list[str]) -> AbstractSet[str]:
        """
        Auxiliar function to compute the following of a non-terminal.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """
        siguiente: set[str] = set()

        # Si es el axioma añadimos el fin de cadena.
        if symbol == self.axiom:
            siguiente = {'$'}

        # Buscamos el simbolo en cada produccion.
        for pr in self.productions:
            dcha = pr.right
            index = dcha.find(symbol)
            # Mientras encontremos el simbolo en una produccion
            while index != -1:
                # Si esta al final de la cadena añadimos siguientes de su izda.
                if index == len(dcha) - 1 and pr.left not in computed:
                    siguiente = siguiente.union(self.compute_follow_aux(pr.left, computed + [pr.left]))
                # Si no, añadimos los primeros del siguiente simbolo sin lambda
                # y, si tenia lambda y era el ultimo caracter, calculamos el
                # siguiente de la izda.
                else:
                    n_first = self.compute_first(dcha[index + 1:])
                    siguiente = siguiente.union(n_first - {''})
                    if '' in n_first and pr.left not in computed:
                        siguiente = siguiente.union(self.compute_follow_aux(pr.left, computed + [pr.left]))
                dcha = dcha[index+1:]
                index = dcha.find(symbol)
        return siguiente



    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

        table = LL1Table(self.non_terminals, self.terminals, set())

        for pr in self.productions:
            n_first = self.compute_first(pr.right)

            for t in n_first:
                if t != '':
                    cell = TableCell(pr.left, t, pr.right)
                    try:
                        table.add_cell(cell)
                    except RepeatedCellError:
                        return None

            if '' in n_first:
                n_next = self.compute_follow(pr.left)
                for t in n_next:
                    if t != '':
                        cell = TableCell(pr.left, t, pr.right)
                        try:
                            table.add_cell(cell)
                        except RepeatedCellError:
                            return None
        return table

    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None

class TableCell:
    """
    Cell of a LL1 table.

    Args:
        non_terminal: Non terminal symbol.
        terminal: Terminal symbol.
        right: Right part of the production rule.

    """

    def __init__(self, non_terminal: str, terminal: str, right: str) -> None:
        self.non_terminal = non_terminal
        self.terminal = terminal
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.non_terminal == other.non_terminal
            and self.terminal == other.terminal
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.non_terminal!r}, {self.terminal!r}, "
            f"{self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.non_terminal, self.terminal))

class LL1Table:
    """
    LL1 table.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.
        cells: Cells of the table.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
        cells: Collection[TableCell],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        for c in cells:
            if c.non_terminal not in non_terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.non_terminal} is not included in the set "
                    f"of non terminals.",
                )
            if c.terminal not in terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.terminal} is not included in the set "
                    f"of terminals.",
                )
            for s in c.right:
                if (
                    s not in non_terminals
                    and s not in terminals
                ):
                    raise ValueError(
                        f"{c}: "
                        f"Invalid symbol {s}.",
                    )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.cells = {(c.non_terminal, c.terminal): c.right for c in cells}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, cell: TableCell) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            cell: table cell to be added.

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if (cell.non_terminal, cell.terminal) in self.cells:
            raise RepeatedCellError(
                f"Repeated cell ({cell.non_terminal}, {cell.terminal}).")
        else:
            self.cells[(cell.non_terminal, cell.terminal)] = cell.right

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        # Iniciamos la pila con el simbolo de fin de cadena y el simbolo de entrada
        pila = [('$',-1), (start, 0)]
        next = 0
        tree = ParseTree(root = start)
        list_tree = [tree]

        # Mientras la pila tenga elementos (y la string) analizamos
        while len(pila) > 0 and next < len(input_string):
            # Cogemos el ultimo elemento de la pila.
            elem, pos = pila.pop()

            # Si es terminal, comprobamos la cadena y pasamos al siguiente
            # caracter si son iguales. Si no, SyntaxError.
            if elem in self.terminals or elem == '$':
                if elem == input_string[next]:
                    next += 1
                else:
                    raise SyntaxError

            # Si es no terminal, comprobamos las celdas de la tabla LL1
            # y sustituimos por la expresion derecha si existe.
            # Si no, SyntaxError.
            elif elem in self.non_terminals:
                cell_key = (elem, input_string[next])
                if cell_key in self.cells:
                    right = self.cells[cell_key]
                    children = []
                    if(right == ""):
                        node = ParseTree(root = "λ")
                        children.append(node)
                    else:
                        right_list = list(right)
                        right_list.reverse()
                        for elem in right_list:
                            node = ParseTree(root = elem)
                            length = len(list_tree)
                            list_tree.append(node)
                            pila += [(elem, length)]
                            children.append(node)
                    children.reverse()
                    list_tree[pos].add_children(children)
                else:
                    raise SyntaxError            
            # Si no esta en la lista de simbolos, SyntaxError.
            else:
                raise SyntaxError

        # Si la pila o la cadena tienen elementos por analizar, SyntaxError.
        if next < len(input_string) or len(pila) > 0:
            raise SyntaxError

        return tree # Return an empty tree by default.


class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
