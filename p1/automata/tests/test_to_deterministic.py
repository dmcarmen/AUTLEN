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


    def test_case1(self) -> None:
        """Test Case 1. Comprobamos que el caso solo con lambda y sin símbolos
        funciona correctamente."""
        automaton_str = """
        Automaton:
            Symbols:

            q0
            qf final

            --> q0
            q0 --> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols:

            qf final

            --> qf
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self) -> None:
        """Test Case 2. Comprobamos en un caso simple que a los estados que
        no tienen asignada una transición para cada símbolo se le aniade
        correctamente una que va a un sumidero."""
        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3
            q4 final

            --> q0
            q0 -a-> q1
            q1 -b-> q2
            q2 -a-> q3
            q3 -b-> q4
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1
            q2
            q3
            q4 final
            sumidero

            --> q0
            q0 -a-> q1
            q0 -b-> sumidero
            q1 -b-> q2
            q1 -a-> sumidero
            q2 -a-> q3
            q2 -b-> sumidero
            q3 -b-> q4
            q3 -a-> sumidero
            q4 -a-> sumidero
            q4 -b-> sumidero
            sumidero -a-> sumidero
            sumidero -b-> sumidero
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self) -> None:
        """Test Case 3. Ejemplo genérico (sin transiciones lambda sólo AFN -> AFD)
        para probar que se añaden estados nuevos y las transiciones
        correspondientes. Extraído de los apuntes de clase, diapositivas p. 50 a 110"""
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

    def test_case4(self) -> None:
        """Test Case 4. Ejemplo completo (con transiciones lambda AFN-lambda -> AFD)
        para probar que se añaden estados nuevos, las transiciones correspondientes
        y se calculan correctamente las clausuras.
        Extraído de los apuntes de clase, diapositivas p. 119 a 167"""

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

    def test_case5(self) -> None:
        """Test Case 5. Generamos estados interconectados exclusivamente por
        transiciones lambda y comprobamos que se unen en un solo estado correctamente.

        """
        automaton_str = """
        Automaton:
            Symbols:ab

            q0
            q1
            q2
            q3
            q4
            qf final

            --> q0
            q0 -a-> q1
            q0 -b-> q0
            q1 --> q2
            q2 --> q3
            q3 --> q4
            q4 --> q1
            q4 -a-> qf
            q4 -b-> q0
            qf -a-> qf
            qf -b-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols:ab

            q0
            q1q2q3q4
            qf final

            --> q0
            q0 -a-> q1q2q3q4
            q0 -b-> q0
            q1q2q3q4 -a-> qf
            q1q2q3q4 -b-> q0
            qf -a-> qf
            qf -b-> qf
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case6(self) -> None:
        """Test Case 6. Given with the code. Basic example that cretaes empty
        state and creates transitions to that state.

        """

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

    def test_case7(self) -> None:
        """Test Case 7. Ejemplo 1:
        AF que reconoce un número decimal con signo opcional."""
        automaton_str = """
        Automaton:
            Symbols: 0123456789+-.

            q0
            q1
            q2
            q3
            q4
            q5 final

            --> q0
            q0 -+-> q1
            q0 ---> q1
            q0 --> q1
            q1 -0-> q1
            q1 -1-> q1
            q1 -2-> q1
            q1 -3-> q1
            q1 -4-> q1
            q1 -5-> q1
            q1 -6-> q1
            q1 -7-> q1
            q1 -8-> q1
            q1 -9-> q1
            q1 -0-> q4
            q1 -1-> q4
            q1 -2-> q4
            q1 -3-> q4
            q1 -4-> q4
            q1 -5-> q4
            q1 -6-> q4
            q1 -7-> q4
            q1 -8-> q4
            q1 -9-> q4
            q1 -.-> q2
            q2 -0-> q3
            q2 -1-> q3
            q2 -2-> q3
            q2 -3-> q3
            q2 -4-> q3
            q2 -5-> q3
            q2 -6-> q3
            q2 -7-> q3
            q2 -8-> q3
            q2 -9-> q3
            q4 -.-> q3
            q3 -0-> q3
            q3 -1-> q3
            q3 -2-> q3
            q3 -3-> q3
            q3 -4-> q3
            q3 -5-> q3
            q3 -6-> q3
            q3 -7-> q3
            q3 -8-> q3
            q3 -9-> q3
            q3 --> q5
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
            Symbols: 0123456789+-.

            q0q1
            q1
            q1q4
            q2
            q2q3q5 final
            q3q5 final
            empty

            --> q0q1
            q0q1 -+-> q1
            q0q1 ---> q1
            q0q1 -.-> q2
            q0q1 -0-> q1q4
            q0q1 -1-> q1q4
            q0q1 -2-> q1q4
            q0q1 -3-> q1q4
            q0q1 -4-> q1q4
            q0q1 -5-> q1q4
            q0q1 -6-> q1q4
            q0q1 -7-> q1q4
            q0q1 -8-> q1q4
            q0q1 -9-> q1q4
            q1 -0-> q1q4
            q1 -1-> q1q4
            q1 -2-> q1q4
            q1 -3-> q1q4
            q1 -4-> q1q4
            q1 -5-> q1q4
            q1 -6-> q1q4
            q1 -7-> q1q4
            q1 -8-> q1q4
            q1 -9-> q1q4
            q1 -.-> q2
            q1 -+-> empty
            q1 ---> empty
            q1q4 -.-> q2q3q5
            q1q4 -0-> q1q4
            q1q4 -1-> q1q4
            q1q4 -2-> q1q4
            q1q4 -3-> q1q4
            q1q4 -4-> q1q4
            q1q4 -5-> q1q4
            q1q4 -6-> q1q4
            q1q4 -7-> q1q4
            q1q4 -8-> q1q4
            q1q4 -9-> q1q4
            q1q4 -+-> empty
            q1q4 ---> empty
            q2q3q5 -0-> q3q5
            q2q3q5 -1-> q3q5
            q2q3q5 -2-> q3q5
            q2q3q5 -3-> q3q5
            q2q3q5 -4-> q3q5
            q2q3q5 -5-> q3q5
            q2q3q5 -6-> q3q5
            q2q3q5 -7-> q3q5
            q2q3q5 -8-> q3q5
            q2q3q5 -9-> q3q5
            q2q3q5 -+-> empty
            q2q3q5 ---> empty
            q2q3q5 -.-> empty

            q2 -0-> q3q5
            q2 -1-> q3q5
            q2 -2-> q3q5
            q2 -3-> q3q5
            q2 -4-> q3q5
            q2 -5-> q3q5
            q2 -6-> q3q5
            q2 -7-> q3q5
            q2 -8-> q3q5
            q2 -9-> q3q5
            q2 -+-> empty
            q2 ---> empty
            q2 -.-> empty
            q3q5 -0-> q3q5
            q3q5 -1-> q3q5
            q3q5 -2-> q3q5
            q3q5 -3-> q3q5
            q3q5 -4-> q3q5
            q3q5 -5-> q3q5
            q3q5 -6-> q3q5
            q3q5 -7-> q3q5
            q3q5 -8-> q3q5
            q3q5 -9-> q3q5
            q3q5 -+-> empty
            q3q5 ---> empty
            q3q5 -.-> empty
            empty -0-> empty
            empty -1-> empty
            empty -2-> empty
            empty -3-> empty
            empty -4-> empty
            empty -5-> empty
            empty -6-> empty
            empty -7-> empty
            empty -8-> empty
            empty -9-> empty
            empty -+-> empty
            empty ---> empty
            empty -.-> empty

        """
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


    def test_case8(self) -> None:
        """Test Case 7. Ejemplo 2:
        AF que reconoce las cadenas
        “1”, “01”, y “101”, artificiosamente ampliado con transiciones lambda.
        """
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

    def test_case9(self) -> None:
        """Test Case 9. Ejemplo 3:
        AF que reconoce las cadenas acabadas en “11”. El AFD resultante mantiene
        el número de estados.
        """
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

if __name__ == '__main__':
    unittest.main()
