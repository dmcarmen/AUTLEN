"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
        initial_state = State("q0", is_final = False)
        final_state = State("qf", is_final = True)
        states = set({initial_state, final_state})
        symbols = None
        transitions = None
        return FiniteAutomaton(initial_state = initial_state, states = states, symbols = symbols, transitions = transitions)

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
        initial_state = State("q0", is_final = True)
        states = set({initial_state})
        symbols = None
        transitions = None
        return FiniteAutomaton(initial_state = initial_state, states = states, symbols = symbols, transitions = transitions)

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        initial_state = State("q0", is_final = False)
        final_state = State("qf", is_final = True)
        states = set({initial_state, final_state})
        symbols = set({symbol})
        transitions = set({Transition(initial_state, symbol, final_state)})
        return FiniteAutomaton(initial_state = initial_state, states = states, symbols = symbols, transitions = transitions)

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        initial_state = State("q0", is_final = False)
        final_state = State("qf", is_final = True)

        a_states = set()
        self.state_counter = 0
        for state in automaton.states:
            self.state_counter += 1
            state.name = "q" + str(self.state_counter)
            a_states.add(state)

        symbols = set(automaton.symbols)

        a_final_states = list()
        for state in automaton.states:
            if(state.is_final):
                a_final_states.append(state)
                state.is_final = False

        transitions = set(automaton.transitions)
        #Lambda transition:
        transitions.add(Transition(initial_state, None, automaton.initial_state))
        transitions.add(Transition(initial_state, None, final_state))
        for state in a_final_states:
            transitions.add(Transition(state, None, automaton.initial_state))
            transitions.add(Transition(state, None, final_state))

        states = set(a_states)
        states.update({initial_state, final_state})

        return FiniteAutomaton(initial_state = initial_state, states = states, symbols = symbols, transitions = transitions)

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        initial_state = State("q0", is_final = False)
        final_state = State("qf", is_final = True)
        a1_states = automaton1.states
        a2_states = automaton2.states

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

        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols)

        pre_final_states = list()
        for state in set(a1_states).union(set(a2_states)):
            if(state.is_final):
                pre_final_states.append(state)
                state.is_final = False

        transitions = set(automaton1.transitions)
        transitions.update(automaton2.transitions)
        #Lambda transition:
        transitions.add(Transition(initial_state, None, automaton1.initial_state))
        transitions.add(Transition(initial_state, None, automaton2.initial_state))
        for state in pre_final_states:
            transitions.add(Transition(state, None, final_state))

        states = set(a1_states)
        states.update(a2_states)
        states.update({initial_state, final_state})

        return FiniteAutomaton(initial_state = initial_state, states = states, symbols = symbols, transitions = transitions)

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        initial_state = automaton1.initial_state

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

        symbols = set(automaton1.symbols)
        symbols.update(automaton2.symbols)

        a1_final_states = list()
        for state in a1_states:
            if(state.is_final):
                a1_final_states.append(state)
                state.is_final = False

        transitions = set(automaton1.transitions)
        transitions.update(automaton2.transitions)
        #Lambda transition:
        for state in a1_final_states:
            transitions.add(Transition(state, None, automaton2.initial_state))

        states = set(a1_states)
        states.update(a2_states)

        return FiniteAutomaton(initial_state = initial_state, states = states, symbols = symbols, transitions = transitions)
