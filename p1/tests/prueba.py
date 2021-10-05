import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

from automata.automaton import FiniteAutomaton
from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.utils import AutomataFormat

def _create_automata():

    description = """
    Automaton:
        Symbols:

        1
        2
        3
        4 final

        --> 1
        1 --> 2
        2 --> 3
        3 --> 4
    """

    return AutomataFormat.read(description)

automaton = _create_automata()
evaluator = FiniteAutomatonEvaluator(automaton)
evaluator.process_string('')
print(evaluator.current_states)
