import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

from automata.automaton import FiniteAutomaton
from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.utils import AutomataFormat

def _create_automata():

    description = """
    Automaton:
        Symbols: Helo

        Empty
        H
        He
        Hel
        Hell
        Hello final

        --> Empty
        Empty -H-> H
        H -e-> He
        He -l-> Hel
        Hel -l-> Hell
        Hell -o-> Hello
    """

    return AutomataFormat.read(description)

automaton = _create_automata()
evaluator = FiniteAutomatonEvaluator(automaton)
evaluator.process_string('Hello')
print(evaluator.current_states)
