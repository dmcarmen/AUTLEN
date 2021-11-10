"""Automaton implementation."""
from typing import Collection

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # TODO: states_in: Collection["State"]

    def __init__(self, name: str, *, is_final: bool = False) -> None:
        super().__init__(
            name=name, is_final=is_final
        )
        self.states_in = set()

    def add_in_state(self, state):
        if not self.is_final and state.is_final:
            self.is_final = True
        self.states_in.add(state)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return (
                self.name == other.name
                and self.is_final == other.is_final
                and self.states_in == other.states_in
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.name!r}, is_final={self.is_final!r})" #, states_in={self.states_in!r}
        )

    def __hash__(self) -> int:
        return hash((self.name, self.is_final))


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

        self.number_states_deterministic = 0
        self.sumidero = None

        # Add here additional initialization code.
        # Do not change the constructor interface.

    def to_deterministic(
            self,
    ) -> "FiniteAutomaton":
        new_transitions = set()

        # Creamos el estado inicial y computamos su clausura lambda
        new_initial_state = State("q0_0", is_final=self.initial_state.is_final)
        new_initial_state.add_in_state(self.initial_state)
        self._complete_lambda(new_initial_state)

        new_states_set = {new_initial_state}
        new_states_list = [new_initial_state]
        self.number_states_deterministic = 1
        i = 0

        # Recorremos la lista de nuevos estados hasta que no lleguemos a ninguno nuevo
        while i < len(new_states_list):
            # Computamos a las transiciones a las que se puede llegar desde el nuevo estado i
            trans, states_compute = self._new_transitions(new_states_list[i])
            print(trans)
            print()

            # De las nuevas transiciones añadimos los estados que no se habían encontrado previamente
            for s in states_compute:
                found = False
                for new_state in new_states_set:
                    if s.states_in == new_state.states_in:
                        found = True
                        break
                if not found:
                    new_states_set.add(s)
                    new_states_list.append(s)
                    for t in trans:
                        if t.final_state == s:
                            new_transitions.add(t)

            # TODO: Parche a arreglar
            for t in trans:
                if t.final_state == self.sumidero:
                    new_transitions.add(t)

            i += 1

        # Si hay un sumidero añadimos las transiciones del sumidero al sumidero
        if self.sumidero is not None:
            for s in self.symbols:
                new_transitions.add(Transition(self.sumidero, s, self.sumidero))

        '''
        print("new states: ", new_states_set)
        print("new transitions", new_transitions)
        '''
        return FiniteAutomaton(initial_state=new_initial_state, states=new_states_set, symbols=self.symbols,
                               transitions=new_transitions)

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

        # Computamos las nuevas transiciones
        for s in self.symbols:
            state_reached_with_s = None
            for t in self.transitions:
                if t.initial_state in state.states_in and t.symbol == s:
                    if state_reached_with_s is None:
                        state_reached_with_s = State(
                            name=t.final_state.name + "_" + str(self.number_states_deterministic),
                            is_final=t.final_state.is_final
                        )
                        state_reached_with_s.add_in_state(t.final_state)
                    else:
                        state_reached_with_s.add_in_state(t.final_state)
            #print("Trans: ", Transition(state, s, state_reached_with_s))

            # Computamos la clausura del estado al que se puede llegar con el símbolo s
            if state_reached_with_s is not None:
                self._complete_lambda(state_reached_with_s)
                next_states_to_compute.add(state_reached_with_s)
                new_transitions_set.add(Transition(state, s, state_reached_with_s))
                self.number_states_deterministic += 1

            else:
                if self.sumidero is None:
                    self.sumidero = State("empty", is_final=False)
                    next_states_to_compute.add(self.sumidero)
                new_transitions_set.add(Transition(state, s, self.sumidero))

        return new_transitions_set, next_states_to_compute

    def _complete_lambda(self, state: State) -> None:
        """
        Añade al atributo states_in del estado pasado como argumento todos los estados
        que sean alcanzables mediante un número arbitrario de
        transiciones lambda.

        Args:
            state: State del que se calculan las transiciones lambda
        """
        # Añadimos al propio estado lambda
        list_reachable = [state.states_in]

        length_list = len(list_reachable)
        i = 0
        # Iterar mientras haya estados de los que no se ha calculado las transiciones lambda
        while i < length_list:
            for tr in self.transitions:
                if tr.initial_state == list_reachable[i] and \
                        tr.symbol is None and tr.final_state not in state.states_in:
                    state.add_in_state(tr.final_state)
                    list_reachable.append(tr.final_state)
                    length_list += 1
            i += 1
