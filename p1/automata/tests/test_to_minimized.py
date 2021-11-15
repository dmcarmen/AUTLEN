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
        transformed = automaton.to_minimized()

        '''
        print()
        print(automaton)
        print(write_dot(automaton))
        print()
        print(transformed)
        print(write_dot(transformed))
        print()
        print(expected)
        print(write_dot(expected))
        print()
        print()
        '''

        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )


        self.assertTrue(equiv_map is not None)
    #'''
    def test_case1(self) -> None:
        """Test Case 1. Comprobamos que el autómata que acepta el lenguaje vacio
        lo minimiza correctamente, retirando el estado final."""
        automaton_str = """
        Automaton:
            Symbols:

            q0
            qf final

            --> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols:

            q0

            --> q0
        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''

    #'''
    def test_case2(self) -> None:
        """Test Case 2. Comprobamos un caso simple en el que tenemos
         estados equivalentes. """

        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3 final
            q4 final
            sumidero

            --> q0
            q0 -a-> q1
            q0 -b-> q2
            q1 -a-> q3
            q2 -a-> q4
            q1 -b-> sumidero
            q2 -b-> sumidero
            q3 -a-> sumidero
            q3 -b-> sumidero
            q4 -a-> sumidero
            q4 -b-> sumidero
            sumidero -a-> sumidero
            sumidero -b-> sumidero
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1q2
            q3q4 final
            sumidero

            --> q0
            q0 -a-> q1q2
            q0 -b-> q1q2
            q1q2 -a-> q3q4
            q1q2 -b-> sumidero
            q3q4 -a-> sumidero
            q3q4 -b-> sumidero
            sumidero -a-> sumidero
            sumidero -b-> sumidero
        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''

    #'''
    def test_case3(self) -> None:
        """Test Case 3. Comprobamos un caso en el que desde
        los estados de q1 a q4 no se podrá llegar al único estado final, qf,
        y por tanto deberían ser equivalentes.

        """
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3
            q4
            qf final

            --> q0
            q0 -a-> qf
            q0 -b-> q1
            q1 -a-> q3
            q1 -b-> q4
            q2 -a-> q2
            q2 -b-> q3
            q3 -a-> q4
            q3 -b-> q2
            q4 -a-> q1
            q4 -b-> q3
            qf -a-> qf
            qf -b-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1q2q3q4
            qf final

            --> q0
            q0 -b-> q1q2q3q4
            q0 -a-> qf
            q1q2q3q4 -a-> q1q2q3q4
            q1q2q3q4 -b-> q1q2q3q4
            qf -a-> qf
            qf -b-> qf
        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''

    def test_case4(self) -> None:
        """Test Case 4. Comprobamos un caso en el que hay varios
        estados conectados entre ellos a los que no se puede acceder.

        """
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3
            q4
            qf final

            --> q0
            q0 -a-> q1
            q0 -b-> q0
            q1 -a-> qf
            q1 -b-> qf
            q2 -a-> q3
            q2 -b-> q4
            q3 -a-> q2
            q3 -b-> q4
            q4 -a-> q1
            q4 -b-> qf
            qf -a-> qf
            qf -b-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            qf final

            --> q0
            q0 -a-> q1
            q0 -b-> q0
            q1 -a-> qf
            q1 -b-> qf
            qf -a-> qf
            qf -b-> qf
        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


    #'''
    def test_case5(self) -> None:
        """Test Case 5. Diapositivas ejemplo, to minimize."""
        automaton_str = """
        Automaton:
            Symbols: 01

            A
            B
            C final
            D
            E
            F
            G
            H

            --> A
            A -0-> B
            A -1-> F
            B -0-> G
            B -1-> C
            C -0-> A
            C -1-> C
            D -0-> C
            D -1-> G
            E -0-> H
            E -1-> F
            F -0-> C
            F -1-> G
            G -0-> G
            G -1-> E
            H -0-> G
            H -1-> C
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            AE
            BH
            C final
            F
            G

            --> AE
            AE -0-> BH
            AE -1-> F
            BH -0-> G
            BH -1-> C
            C -0-> AE
            C -1-> C
            F -0-> C
            F -1-> G
            G -0-> G
            G -1-> AE

        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    ##'''

    #'''
    def test_case6(self) -> None:
        """Test Case 6. Casos de prueba 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0 final
            q1
            q2 final
            q3
            q4 final
            q5


            --> q0
            q0 -0-> q1
            q0 -1-> q1
            q1 -0-> q2
            q1 -1-> q2
            q2 -0-> q3
            q2 -1-> q3
            q3 -0-> q4
            q3 -1-> q4
            q4 -0-> q5
            q4 -1-> q5
            q5 -0-> q0
            q5 -1-> q0

        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 01

            q0q2q4 final
            q1q3q5


            --> q0q2q4
            q0q2q4 -0-> q1q3q5
            q0q2q4 -1-> q1q3q5
            q1q3q5 -0-> q0q2q4
            q1q3q5 -1-> q0q2q4

        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''
    #'''
    def test_case7(self) -> None:
        """Test Case 7. Casos de prueba 2, to minimize."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1 final
            q2
            q3 final
            q4


            --> q0
            q0 -a-> q1
            q0 -b-> q3
            q1 -a-> q2
            q1 -b-> q1
            q2 -a-> q1
            q2 -b-> q2
            q3 -a-> q4
            q3 -b-> q3
            q4 -a-> q3
            q4 -b-> q4

        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1q3 final
            q2q4


            --> q0
            q0 -a-> q1q3
            q0 -b-> q1q3
            q1q3 -a-> q2q4
            q1q3 -b-> q1q3
            q2q4 -a-> q1q3
            q2q4 -b-> q2q4

        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''
    #'''
    def test_case8(self) -> None:
        """Test Case 8. Casos de prueba 3, to minimize."""
        automaton_str = """
        Automaton:
            Symbols: abc

            A final
            B final
            C final
            D final
            E


            --> A
            A -a-> B
            A -b-> C
            A -c-> B
            B -a-> B
            B -b-> C
            B -c-> B
            C -a-> B
            C -b-> D
            C -c-> B
            D -a-> E
            D -b-> E
            D -c-> E
            E -a-> E
            E -b-> E
            E -c-> E

        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: abc

            AB final
            C final
            D final
            E

            --> AB
            AB -a-> AB
            AB -b-> C
            AB -c-> AB
            C -a-> AB
            C -b-> D
            C -c-> AB
            D -a-> E
            D -b-> E
            D -c-> E
            E -a-> E
            E -b-> E
            E -c-> E

        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
    #'''

if __name__ == '__main__':
    unittest.main()
