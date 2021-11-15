# Práctica 1: autómatas finitos

Alejandro Bravo de la Serna y Carmen Díez Menéndez.

Para correr el proyecto:

1. `pip3 install mypy`
2. Desde *p1/*: `mypy --strict --strict-equality automata/` y `export PYTHONPATH=$PYTHONPATH:.`
3. Desde *p1/*: `python3 automata/tests/test_evaluator.py`, `python3 automata/tests/test_re_parser.py`, `python3 automata/tests/test_to_deterministic.py` y `python3 automata/tests/test_to_minimized.py`
`

En la carpeta *Images/* incluimos fotos de los autómatas de los tests (los originales y los transformados). En los tests hemos añadido además los ejemplos de prueba que se daban en las prácticas (pero no incluimos las fotos, pues están en las diapositivas de Moodle).

En el algoritmo para pasar un autómata a determinista hemos seguido el algoritmo propuesto en las clases teóricas y en las diapositivas de las prácticas. Al seguir este algoritmo se llega a que todos los estados inalcanzables son eliminados (pues empezamos a iterar desde q0 en adelante, y no podemos llegar a estos estados). Lo hemos considerado correcto porque, a pesar de no estar los inalcanzables, son autómatas equivalentes pues reconocen el mismo lenguaje.
