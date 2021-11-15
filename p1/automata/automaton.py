"""Automaton implementation."""
from typing import Collection, Optional, Tuple, Dict, List

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

    sumidero: Optional[State]

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
        """
        Return a equivalent deterministic automaton.

        Returns:
            Equivalent deterministic automaton.

        """
        new_transitions = set()

        # Creamos el estado inicial y computamos su clausura lambda
        list_reachable, final = self._complete_lambda(self.initial_state)
        new_initial_state = State(self._joint_name(list_reachable), is_final=final)

        # Creamos un diccionario {nombre nuevo estado: estados que junta}
        new_states_dic = {new_initial_state.name: list_reachable}

        new_states_list = [new_initial_state]
        i = 0
        # Mientras aparezcan nuevos estados iteramos por ellos
        while i < len(new_states_list):
            state = new_states_list[i]
            # Diccionario que guardara {simbolo: estados finales} desde el estado
            # de la iteracion actual
            trans_dic = {}
            # Para los estados que tiene el estado junto encontramos todas las transiciones
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

                # Guardamos el nuevo estado conseguido en la lista si no lo hemos
                # analizado antes y anadimos la nueva transicion
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
        """
        Dada una lista de estados calcula un nombre conjunto (en orden alfabetico)

        Returns:
            String con el nombre conjunto.

        """
        sorted_list=sorted(state_list, key=lambda st: st.name)
        joint_name = ''
        for st in sorted_list:
            joint_name += st.name
        return joint_name

    def _complete_lambda(self, state: State) -> Tuple[Collection[State], bool]:
        """
        Dado un estado calcula su clausura segun self.transitions. Ademas, ve si
        alguno de los estados alcanzados es final y lo devuelve.

        Returns:
            Tupla con una lista de estados alcanzables (clausura lambda) y un
            booleano indicando si entre ellos algun valor es final.


        """
        # Añadimos el propio estado a la clausura
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
        """
        Return a equivalent minimal automaton.

        Returns:
            Equivalent minimal automaton.

        """
        accesibles, new_transitions = self._get_accesibles(self.initial_state, self.transitions)
        initial_state, new_states, new_transitions = self._get_equivalente(accesibles, new_transitions)
        return FiniteAutomaton(initial_state=initial_state, states=new_states,
                                symbols=self.symbols, transitions=new_transitions)


    def _get_accesibles(
        self,
        initial_state: State,
        transitions: Collection[Transition]
    ) -> Tuple[Collection[State], Collection[Transition]]:
        """
        Devuelve los estados accesibles (y sus transiciones) dado un estado inicial.

        Returns:
            Tupla con una lista de los estados accesibles y una lista de las
            nuevas transiciones.

        """
        accesibles = [initial_state]
        i = 0
        # Iteramos mientras encontremos estados accesibles
        while i < len(accesibles):
            for tr in transitions:
                if tr.initial_state == accesibles[i]:
                    if tr.final_state not in accesibles:
                        accesibles.append(tr.final_state)
            i+=1

        # Guardamos las transiciones que implican a los accesibles
        new_transitions = []
        for tr in transitions:
            if tr.initial_state in accesibles and tr.final_state in accesibles:
                new_transitions.append(tr)

        return accesibles, new_transitions

    def _get_equivalente(
        self,
        states: Collection[State],
        transitions: Collection[Transition]
    ) -> Tuple[State, Collection[State], Collection[Transition]]:
        """
        Devuelve los datos necesarios para crear un automata equivalente.

        Returns:
            Tupla con estado inicial, lista de estados y lista de transiciones
            del automata equivalente.

        """
        sorted_list=sorted(states, key=lambda st: st.name)

        # Creamos un diccionario que para cada estado devuelve sus transiciones
        # (en las que son estado inicial) {estado: transiciones}
        state_dic = {}
        for tr in transitions:
            if tr.initial_state not in state_dic:
                state_dic[tr.initial_state] = [tr]
            else:
                state_dic[tr.initial_state].append(tr)

        num_states = len(sorted_list)
        # Creamos la matriz con todos los estados indistinguibles (False indistinguible, True distinguible)
        matrix_dis = [ [ False for i in range(num_states) ] for j in range(num_states) ]

        # Diccionario {estado: numero de la clase de equivalencia}
        new_eq_clases = {}
        # Llenamos la matriz para la relación de equivalencia E0 (finales vs no finales)
        for i in range(num_states):
            if sorted_list[i].is_final:
                new_eq_clases[sorted_list[i]] = 0
            else:
                new_eq_clases[sorted_list[i]] = 1
            for j in range(i + 1, num_states):
                if sorted_list[i].is_final != sorted_list[j].is_final:
                    matrix_dis[i][j] = True

        it = 0
        # Diccionario auxiliar similar a new_eq_clases {estado: numero clase equivalencia}
        eq_clases: Optional[Dict[State, int]] = {}
        while(it <= num_states - 2):
            # Condición de parada del algoritmo: si las clases de equivalencia
            # no se actualizan hemos terminado
            if(new_eq_clases == eq_clases):
                break
            eq_clases = new_eq_clases.copy()

            # Recorremos la 'submatriz triangular superior' de la matriz (es simetrica)
            for i in range(num_states - 1):
                for j in range(i + 1, num_states):
                    # Si son distinguibles pasamos
                    if (matrix_dis[i][j] == True):
                        continue

                    # Vemos las transiciones desde los dos estados que comparamos
                    trs_i = state_dic[sorted_list[i]]
                    trs_j = state_dic[sorted_list[j]]
                    dis = False
                    for tr_i in trs_i:
                        for tr_j in trs_j:
                            # Si encontramos una transicion 'distinta', son distinguibles
                            if tr_i.symbol == tr_j.symbol and eq_clases[tr_i.final_state] != eq_clases[tr_j.final_state]:
                                dis = True
                                matrix_dis[i][j] = True
                                break
                        if(dis == True):
                            break

            # Creamos las nuevas clases de equivalencia
            new_eq_clases = {}
            num_clases = 0
            for i in range(num_states):
                # Si el estado no esta en el dicionario lo anadimos como nueva clase
                if sorted_list[i] not in new_eq_clases:
                    new_eq_clases[sorted_list[i]] = num_clases
                    # Anadimos a la misma clase los estados indistinguibles
                    for j in range(i + 1, num_states):
                        if(matrix_dis[i][j] is False):
                            new_eq_clases[sorted_list[j]] = num_clases
                    num_clases += 1
            it += 1

        # Diccionario inverso {clase equivalencia: lista de estados}
        inv_eq_clases: Dict[int, List[State]] = {}
        for st, clase in new_eq_clases.items():
            inv_eq_clases[clase] = inv_eq_clases.get(clase,[]) + [st]

        # Diccionario con {estado: nuevo estado al que pertenece}
        new_states_dic = {}
        for states_list in inv_eq_clases.values():
            new_state = State(self._joint_name(states_list), is_final = states_list[0].is_final)
            for st in states_list:
                new_states_dic[st] = new_state
                if st == self.initial_state:
                    initial_state = new_state

        #Creamos el set de nuevos estados
        new_states = set(new_states_dic.values())

        # Anadimos las nuevas transiciones con los nuevos estados
        new_transitions = set()
        for list_st in inv_eq_clases.values():
            #Pues los estados de list_st son equivalentes, nos vale con ver las transiciones del primero
            st = list_st[0]
            transitions_st = state_dic[st]
            for tr in transitions_st:
                new_transitions.add(Transition(new_states_dic[tr.initial_state], tr.symbol, new_states_dic[tr.final_state]))

        return initial_state, new_states, new_transitions
