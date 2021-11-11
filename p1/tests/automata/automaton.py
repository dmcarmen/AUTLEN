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

    sumidero: State

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
                name = self._joint_name(list(trans_dic[symbol]))
                if name not in new_states_dic:
                    new_states_dic[name] = list(trans_dic[symbol])
                    new_state = State(name, is_final=is_final)
                    new_states_list.append(new_state)
                    tr = Transition(state, symbol, new_state)
                else:
                    for st in new_states_list:
                        if st.name == name:
                            tr = Transition(state, symbol, st)
                            break
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


        return FiniteAutomaton(initial_state=new_initial_state, states=new_states_list,
                                symbols=self.symbols, transitions=new_transitions)


    def _joint_name(self, state_list: Collection[State]) -> str:
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
        accesibles, new_transitions = self._get_accesibles()
        self.states = accesibles
        self.transitions = new_transitions
        initial_state, new_states, new_transitions = self._set_equivalentes()
        return FiniteAutomaton(initial_state=initial_state, states=new_states,
                                symbols=self.symbols, transitions=new_transitions)

    #TODO: borrar, no need, test function
    def to_accesibles(
        self
    ) -> "FiniteAutomaton":
        accesibles, new_transitions = self._get_accesibles()
        return FiniteAutomaton(initial_state=self.initial_state, states=accesibles,
                                symbols=self.symbols, transitions=new_transitions)

    def _get_accesibles(
        self,
    ): #TODO:  -> Tuple[Collection[State], Collection[Transition]]
        accesibles = [self.initial_state]
        i = 0
        while i < len(accesibles):
            for tr in self.transitions:
                if tr.initial_state == accesibles[i]:
                    if tr.final_state not in accesibles:
                        accesibles.append(tr.final_state)
            i+=1
        new_transitions = []
        for tr in self.transitions:
            if tr.initial_state in accesibles and tr.final_state in accesibles:
                new_transitions.append(tr)

        return accesibles, new_transitions

    def _set_equivalentes(
        self,
    ) -> None:

        sorted_list=sorted(self.states, key=lambda st: st.name)

        #Creamos un diccionario que para cada estado devuelve sus transiciones
        state_dic = {}
        for tr in self.transitions:
            if tr.initial_state not in state_dic:
                state_dic[tr.initial_state] = [tr]
            else:
                state_dic[tr.initial_state].append(tr)


        num_states = len(sorted_list)

        #Creamos la matriz con todos los estados indistinguibles
        #Llenamos la matriz para la clase de equivalencia E0
        eq_clases = {}
        new_eq_clases = {}
        matrix_dis = [ [ False for i in range(num_states) ] for j in range(num_states) ]

        for i in range(num_states):
            if sorted_list[i].is_final:
                new_eq_clases[sorted_list[i]] = 0
            else:
                new_eq_clases[sorted_list[i]] = 1

            for j in range(i + 1, num_states):
                if sorted_list[i].is_final != sorted_list[j].is_final:
                    matrix_dis[i][j] = True

        it = 0
        #TODO:Asegurar si es <= o < o que
        while(it <= num_states - 2):
            #Condición de parada del algoritmo
            if(new_eq_clases == eq_clases):
                break
            eq_clases = new_eq_clases.copy()
            new_eq_clases = {}
            for i in range(num_states - 1):
                for j in range(i + 1, num_states):
                    #Si son distinguibles pasamos
                    if (matrix_dis[i][j] == True):
                        continue
                    trs_i = state_dic[sorted_list[i]]
                    trs_j = state_dic[sorted_list[j]]
                    dis = False
                    for tr_i in trs_i:
                        for tr_j in trs_j:
                            if(tr_i.symbol == tr_j.symbol):
                                if(eq_clases[tr_i.final_state] != eq_clases[tr_j.final_state]):
                                    dis = True
                                    matrix_dis[i][j] = True
                                    break
                        if(dis == True):
                            break

            #Creamos las nuevas clases de equivalencia
            num_clases = 0
            for i in range(num_states):
                if sorted_list[i] not in new_eq_clases:
                    new_eq_clases[sorted_list[i]] = num_clases
                    for j in range(i + 1, num_states):
                        if(matrix_dis[i][j] is False):
                            new_eq_clases[sorted_list[j]] = num_clases
                    num_clases += 1
            it += 1

        # Diccionario Clase equivalencia: estados
        inv_eq_clases = {}
        for k,v in new_eq_clases.items():
            inv_eq_clases[v] = inv_eq_clases.get(v,[]) + [k]

        new_states_dic = {}

        for states_list in inv_eq_clases.values():
            new_state = State(self._joint_name(states_list), is_final = states_list[0].is_final)
            for st in states_list:
                new_states_dic[st] = new_state
                if st == self.initial_state:
                    initial_state = new_state

        #TODO: puede que añada misma transicion twice?
        new_transitions = set()
        for tr in self.transitions:
            new_transitions.add(Transition(new_states_dic[tr.initial_state], tr.symbol, new_states_dic[tr.final_state]))

        return initial_state, set(new_states_dic.values()), new_transitions
