"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser
from typing import Collection


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
            self,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language.

        """
        initial_state = State("q0", is_final=False)
        final_state = State("qf", is_final=True)
        states = set({initial_state, final_state})
        symbols: Collection[str] = []
        transitions: Collection[Transition] = []
        return FiniteAutomaton(initial_state=initial_state, states=states, symbols=symbols, transitions=transitions)

    def _create_automaton_lambda(
            self,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string.

        """
        initial_state = State("q0", is_final=True)
        states = set({initial_state})
        symbols: Collection[str] = []
        transitions: Collection[Transition] = []
        return FiniteAutomaton(initial_state=initial_state, states=states,
                                symbols=symbols, transitions=transitions)

    def _create_automaton_symbol(
            self,
            symbol: str,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept.

        Returns:
            Automaton that accepts a symbol.

        """
        initial_state = State("q0", is_final=False)
        final_state = State("qf", is_final=True)
        states = set({initial_state, final_state})
        symbols = set({symbol})
        transitions = set({Transition(initial_state, symbol, final_state)})
        return FiniteAutomaton(initial_state=initial_state, states=states,
                                symbols=symbols, transitions=transitions)

    def _create_automaton_star(
            self,
            automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed.

        Returns:
            Automaton that accepts the Kleene star.

        """
        initial_state = State("q0", is_final=False)
        final_state = State("qf", is_final=True)

        a_states = set()
        # Renombramos los viejos estados para no repetir q0 y qf
        self.state_counter = 0
        for state in automaton.states:
            self.state_counter += 1
            state.name = "q" + str(self.state_counter)
            a_states.add(state)

        # Guardamos los estados finales (que dejan de serlo)
        a_final_states = list()
        for state in automaton.states:
            if state.is_final:
                a_final_states.append(state)
                state.is_final = False

        transitions = set(automaton.transitions)
        # Lambda transition:
        transitions.add(Transition(initial_state, None, automaton.initial_state))
        transitions.add(Transition(initial_state, None, final_state))
        for state in a_final_states:
            transitions.add(Transition(state, None, automaton.initial_state))
            transitions.add(Transition(state, None, final_state))

        # Creamos el set de estados
        states = set()
        states.add(initial_state)
        for t in transitions:
            for s in (t.initial_state, t.final_state):
                if s not in states:
                    states.add(s)

        return FiniteAutomaton(initial_state=initial_state, states=states,
                            symbols=automaton.symbols, transitions=transitions)

    def _create_automaton_union(
            self,
            automaton1: FiniteAutomaton,
            automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union.
            automaton2: Second automaton of the union.

        Returns:
            Automaton that accepts the union.

        """
        initial_state = State("q0", is_final=False)
        final_state = State("qf", is_final=True)

        # Renombramos los viejos estados para no repetir
        a1_states = set()
        self.state_counter = 0
        for state in automaton1.states:
            self.state_counter += 1
            state.name = "q" + str(self.state_counter)
            a1_states.add(state)
        a2_states = set()
        for state in automaton2.states:
            self.state_counter += 1
            state.name = "q" + str(self.state_counter)
            a2_states.add(state)

        # Juntamos los simbolos en un mismo set
        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols)

        # Guardamos los estados finales (que dejan de serlo)
        pre_final_states = list()
        for state in set(a1_states).union(set(a2_states)):
            if state.is_final:
                pre_final_states.append(state)
                state.is_final = False

        transitions = set(automaton1.transitions)
        transitions.update(automaton2.transitions)
        # Lambda transition:
        transitions.add(Transition(initial_state, None, automaton1.initial_state))
        transitions.add(Transition(initial_state, None, automaton2.initial_state))
        for state in pre_final_states:
            transitions.add(Transition(state, None, final_state))

        # Creamos el set de estados
        states = set()
        states.add(initial_state)
        for t in transitions:
            for s in (t.initial_state, t.final_state):
                if s not in states:
                    states.add(s)

        return FiniteAutomaton(initial_state=initial_state, states=states,
                                symbols=symbols, transitions=transitions)

    def _create_automaton_concat(
            self,
            automaton1: FiniteAutomaton,
            automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation.
            automaton2: Second automaton of the concatenation.

        Returns:
            Automaton that accepts the concatenation.

        """
        initial_state = automaton1.initial_state

        # Renombramos los viejos estados para no repetir
        a1_states = set()
        self.state_counter = 0
        for state in automaton1.states:
            self.state_counter += 1
            state.name = "q" + str(self.state_counter)
            a1_states.add(state)
        a2_states = set()
        for state in automaton2.states:
            self.state_counter += 1
            state.name = "q" + str(self.state_counter)
            a2_states.add(state)

        # Juntamos los simbolos en un mismo set
        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols)

        # Guardamos los estados finales (que dejan de serlo)
        a1_final_states = list()
        for state in a1_states:
            if state.is_final:
                a1_final_states.append(state)
                state.is_final = False

        transitions = set(automaton1.transitions)
        transitions.update(automaton2.transitions)
        # Lambda transition:
        for state in a1_final_states:
            transitions.add(Transition(state, None, automaton2.initial_state))

        # Creamos el set de estados
        states = set()
        states.add(initial_state)
        for t in transitions:
            for s in (t.initial_state, t.final_state):
                if s not in states:
                    states.add(s)

        return FiniteAutomaton(initial_state=initial_state, states=states,
                                symbols=symbols, transitions=transitions)
