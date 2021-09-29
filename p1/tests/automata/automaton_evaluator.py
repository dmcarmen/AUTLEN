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

    # tiene automaton (con initial state, states, symbols, transitions) + current_states (set de states)

    def process_symbol(self, symbol: str) -> None:
        """
        Process one symbol. Procesa un símbolo de la cadena (y cualquier número
        de transiciones lambdas inmediatamente después, mediante la llamada a
        _complete_lambdas).

        Args:
            symbol: Symbol to consume.

        """
        print(self.current_states)
        if symbol in self.automaton.symbols:
            new_states = set()
            for st in self.current_states:
                for tr in self.automaton.transitions:
                    if tr.initial_state == st and tr.symbol == symbol:
                        new_states.add(tr.final_state)
        self.current_states = new_states.copy()
        self._complete_lambdas(new_states)

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        """
        Add states reachable with lambda transitions to the set.
        Añade al conjunto de estados pasado como argumento todos los estados
        que sean alcanzables mediante un número arbitrario de
        transiciones lambda.

        Args:
            set_to_complete: Current set of states to be completed.
        """
        #print(self.current_states)
        list_to_complete = list(set_to_complete)
        length_list = len(list_to_complete)
        for i in range(length_list):
            for tr in self.automaton.transitions:
                if tr.initial_state == list_to_complete[i] and tr.symbol == None and not tr.final_state in self.current_states:

                    self.current_states.add(tr.final_state)
                    list_to_complete += tr.final_state
                    length += 1

    def is_accepting(self) -> bool:
        """Check if the current state is an accepting one."""
        for state in self.current_states:
            if(state.is_final):
                return True
        return False
