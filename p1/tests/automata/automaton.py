"""Automaton implementation."""
from typing import Collection

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


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

        self.sumidero = None
        # Add here additional initialization code.
        # Do not change the constructor interface.

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        new_transitions = set()
        # Creamos el estado inicial y computamos su clausura lambda

        list_reachable, final = self._complete_lambda(self.initial_state)
        new_initial_state = State(self._joint_name(list_reachable), is_final=final)

        new_states_dic = {new_initial_state.name: list_reachable}
        new_states_list = [new_initial_state]
        i = 0

        # Mientras aparezcan nuevos estados iteramos por ellos
        while i < len(new_states_list):
            state = new_states_list[i]
            trans_dic = {}
            # Para los estados que componen el estado encontramos todas las transiciones
            for st in new_states_dic[state.name]:
                for tr in self.transitions:
                    if tr.initial_state == st and tr.symbol in self.symbols:
                        if tr.symbol not in trans_dic:
                            trans_dic[tr.symbol] = {tr.final_state}
                        else:
                            trans_dic[tr.symbol].add(tr.final_state)

            # Completamos lambdas de los nuevos estados alcanzados y cambiamos is_final si es necesario
            for symbol in trans_dic.keys():
                is_final = False
                for st in trans_dic[symbol]:
                    list_reachable, final = self._complete_lambda(st)
                    if final is True:
                        is_final = final
                    trans_dic[symbol] = trans_dic[symbol].union(set(list_reachable))

                # Guardamos el nuevo estado en la lista si no lo hemos analizado antes
                new_state = State(self._joint_name(list(trans_dic[symbol])), is_final=is_final)
                if new_state.name not in new_states_dic:
                    new_states_dic[new_state.name] = list(trans_dic[symbol])
                    new_states_list.append(new_state)
                tr = Transition(state, symbol, new_state)
                new_transitions.add(tr)

            # Para los símbolos sin transiciones los llevamos al sumidero
            for symbol in self.symbols:
                if symbol not in trans_dic.keys():
                    if self.sumidero is None:
                        self.sumidero = State('empty', is_final = False)
                    new_transitions.add(Transition(state, symbol, self.sumidero))

            i += 1

        # Creamos los bucles del sumidero
        if self.sumidero is not None:
            for s in self.symbols:
                new_transitions.add(Transition(self.sumidero, s, self.sumidero))
            new_states_list.append(self.sumidero)


        return FiniteAutomaton(initial_state=new_initial_state, states=new_states_list, symbols=self.symbols,
                                transitions=new_transitions)


    def _joint_name(self, state_list):
        sorted_list=sorted(state_list, key=lambda st: st.name)
        joint_name = ''
        for st in sorted_list:
            joint_name += st.name
        return joint_name

    def _complete_lambda(self, state: State): # TODO que devuelve
        # Añadimos al propio estado lambda
        list_reachable = [state]

        length_list = len(list_reachable)
        i = 0
        # Iterar mientras haya estados de los que no se ha calculado las transiciones lambda
        final = state.is_final
        print(self.transitions)
        while i < length_list:
            for tr in self.transitions:
                if tr.initial_state == list_reachable[i] and \
                        tr.symbol is None and tr.final_state not in list_reachable:
                    list_reachable.append(tr.final_state)
                    if tr.final_state.is_final:
                        final = True
                    length_list += 1
            i += 1
        return list_reachable, final

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
