"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        '''
        print(automaton)
        print()
        print(transformed)
        print()
        print(expected)
        '''
        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

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

    def test_case2(self) -> None:
        """Test Case 2."""
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
            empty

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
                q3q5q6q7
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

if __name__ == '__main__':
    unittest.main()
