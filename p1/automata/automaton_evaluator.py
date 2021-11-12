"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def __init__(
        self,
        automaton: FiniteAutomaton
    ) -> None:
        super().__init__(
            automaton = automaton
        )

    def process_symbol(self, symbol: str) -> None:
        """
        Process one symbol. Procesa un símbolo de la cadena (y cualquier número
        de transiciones lambdas inmediatamente después, mediante la llamada a
        _complete_lambdas).

        Args:
            symbol: Symbol to consume.

        """
        new_states = set()
        # Comprobamos que el simbolo es válido
        if symbol in self.automaton.symbols:
            # Recorremos los estados (st) y transiciones (tr) para buscar:
            # tr: st -symbol-> final_state
            # Y anadir final_state a current_states y calcular sus trans lambda
            for st in self.current_states:
                for tr in self.automaton.transitions:
                    if tr.initial_state == st and tr.symbol == symbol:
                        new_states.add(tr.final_state)
        else:
            raise ValueError('Símbolo no recogido en el alfabeto')

        self.current_states = new_states
        self._complete_lambdas(self.current_states)

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        """
        Add states reachable with lambda transitions to the set.
        Añade al conjunto de estados pasado como argumento todos los estados
        que sean alcanzables mediante un número arbitrario de
        transiciones lambda.

        Args:
            set_to_complete: Current set of states to be completed.
        """
        # Creamos una lista que sera la clausura lambda
        list_to_complete = list(set_to_complete)
        length_list = len(list_to_complete)
        i = 0
        # Mientras encontremos nuevos estados buscamos sus trans lambda y las anadimos
        while(i < length_list):
            for tr in self.automaton.transitions:
                if tr.initial_state == list_to_complete[i] and tr.symbol == None and not tr.final_state in set_to_complete:
                    set_to_complete.add(tr.final_state)
                    list_to_complete.append(tr.final_state)
                    length_list += 1
            i += 1

    def is_accepting(self) -> bool:
        """Check if the current state is an accepting one."""
        for state in self.current_states:
            if(state.is_final):
                return True
        return False
