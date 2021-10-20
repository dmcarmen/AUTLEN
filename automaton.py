"""Automaton implementation."""
from typing import Collection

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""
    #TODO: states_in: Collection["State"]

    def __init__(self, name: str, *, is_final: bool = False) -> None:
        super().__init__(
            name = name, is_final = is_final
        )
        self.states_in = set()

    def add_in_state(self, state):
        if(self.is_final == False and state.is_final == True):
            self.is_final = True
        self.states_in.add(state)


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface.

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        new_transitions = set()
        new_states_set = set([self.initial_state])
        new_states_list = [self.initial_state]
        length_list = 1
        i = 0

        while(i < length_list):
            trans, states_compute = self._new_transitions(new_states_list[i])
            new_transitions.update(trans)
            for s in states_compute:
                if s not in new_states_set:
                    new_states_set.add(s)
                    new_states_list.append(s)
            i += 1

        print(new_states_set)
        print()
        return FiniteAutomaton(initial_state = self.initial_state, states = new_states_set, symbols = self.symbols, transitions = new_transitions)


    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")

    def _new_transitions(
        self,
        state: State,
    ) -> (Collection[Transition], Collection[State]):
        new_transitions_set = set()
        next_states_to_compute = set()

        #Calculamos la clausura
        self._complete_lambda(state)

        #Computamos las nuevas transiciones
        for s in self.symbols:
            for t in self.transitions:
                if t.initial_state in state.states_in and t.symbol == s:
                    #Computamos la clausura del estado al que se puede llegar con el simbolo s
                    self._complete_lambda(t.final_state)
                    next_states_to_compute.add(t.final_state)

                    new_transitions_set.add(Transition(state, s, t.final_state))
        return (new_transitions_set, next_states_to_compute)


    def _complete_lambda(self, state: State) -> None:
        """
        Add states reachable with lambda transitions to the set.
        Añade al conjunto de estados pasado como argumento todos los estados
        que sean alcanzables mediante un número arbitrario de
        transiciones lambda.

        Args:
            set_to_complete: Current set of states to be completed.
        """
        list_reachable = [state]
        state.add_in_state(state)
        length_list = 1
        i = 0
        while(i < length_list):
            for tr in self.transitions:
                if tr.initial_state == list_reachable[i] and tr.symbol == None and not tr.final_state in state.states_in:
                    state.add_in_state(tr.final_state)
                    list_reachable.append(tr.final_state)
                    length_list += 1
            i += 1
