"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)
    #'''
    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            qf final
            empty

            --> q0
            q0 -0-> qf
            q0 -1-> empty
            qf -0-> empty
            qf -1-> empty
            empty -0-> empty
            empty -1-> empty

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''
    #'''
    def test_case2(self) -> None:
        """Test Case 2. Ejemplo 2."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3
            q4
            q5
            q6 final
            q7

            --> q0
            q0 --> q1
            q0 --> q2
            q1 -1-> q3
            q1 -1-> q5
            q2 -0-> q4
            q4 -1-> q6
            q5 --> q7
            q5 -0-> q4
            q5 -0-> q3
            q7 --> q6
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
                Symbols: 01

                q0q1q2
                q4
                q3q5q6q7 final
                q3q4
                q6 final
                empty

                --> q0q1q2
                q0q1q2 -0-> q4
                q0q1q2 -1-> q3q5q6q7
                q4 -0-> empty
                q4 -1-> q6
                q3q5q6q7 -0-> q3q4
                q3q5q6q7 -1-> empty
                q3q4 -0-> empty
                q3q4 -1-> q6
                q6 -0-> empty
                q6 -1-> empty
                empty -0-> empty
                empty -1-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''
    #'''
    def test_case3(self) -> None:
        """Test Case 3. Diapositivas p. 50 a 110"""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3 final

            --> q0
            q0 -a-> q0
            q0 -b-> q0
            q0 -a-> q1
            q1 -b-> q2
            q2 -a-> q3
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q0q1
            q0q2
            q0q1q3 final

            --> q0
            q0 -b-> q0
            q0 -a-> q0q1
            q0q1 -a-> q0q1
            q0q1 -b-> q0q2
            q0q2 -a-> q0q1q3
            q0q2 -b-> q0
            q0q1q3 -a-> q0q1
            q0q1q3 -b-> q0q2
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    #'''
    #'''
    def test_case4(self) -> None:
        """Test Case 4. Diapositivas p. 119-167."""
        automaton_str = """
        Automaton:
            Symbols: abc

            q0
            q1
            q2
            q3
            q4
            q5
            q6
            q7
            qf final

            --> q0
            q0 --> q1
            q0 --> qf
            q1 --> q2
            q1 --> q5
            q2 -a-> q3
            q3 -b-> q4
            q4 --> q7
            q5 -c-> q6
            q6 --> q7
            q7 --> q1
            q7 --> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: abc

            q0q1q2q5qf final
            q1q2q5q6q7qf final
            q3
            q1q2q4q5q7qf final
            empty

            --> q0q1q2q5qf
            q0q1q2q5qf -a-> q3
            q0q1q2q5qf -b-> empty
            q0q1q2q5qf -c-> q1q2q5q6q7qf
            q1q2q5q6q7qf -a-> q3
            q1q2q5q6q7qf -b-> empty
            q1q2q5q6q7qf -c-> q1q2q5q6q7qf
            q3 -a-> empty
            q3 -b-> q1q2q4q5q7qf
            q3 -c-> empty
            q1q2q4q5q7qf -a-> q3
            q1q2q4q5q7qf -b-> empty
            q1q2q4q5q7qf -c-> q1q2q5q6q7qf
            empty -a-> empty
            empty -b-> empty
            empty -c-> empty
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    #'''
    #'''
    def test_case5(self) -> None:
        """Test Case 5. Ejemplo 3."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            qf final

            --> q0
            q0 -0-> q0
            q0 -1-> q0
            q0 -1-> q1
            q1 -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q0q1
            q0q1qf final

            --> q0
            q0 -0-> q0
            q0 -1-> q0q1
            q0q1 -0-> q0
            q0q1 -1-> q0q1qf
            q0q1qf -0-> q0
            q0q1qf -1-> q0q1qf

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''


if __name__ == '__main__':
    unittest.main()
