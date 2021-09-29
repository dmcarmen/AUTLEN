"""
Alejandro Bravo de la Serna y Carmen Diez Menendez
"""

"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[a-zA-Z]+"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-5:
"""
RE1 = "[a-zA-Z0-9_]+\.py"

RE2 = "-?([1-9][0-9]*|0)?(\.[0-9]*)?"
"""
RE2 acepta la cadena - y la cadena vacia. Si no nos equivocamos en clase se dio el visto bueno.
Aun así, hemos añadido la RE2Adicional que no acepta ni - ni la cadena vacia. Eso sí, acepta 
la cadena ".", que interpretamos que es correcta y similar a escribir "0.0" (Se podría retirar 
"." sustituyendo el último * por +).
"""
RE2Adicional = "-?((([1-9][0-9]*|0)(\.[0-9]*)?)|(([1-9][0-9]*|0)?(\.[0-9]*)))"
RE3 = "[a-z]+\.[a-z]+@(estudiante\.)?uam\.es"

#RE45_AUX: cadena de caracteres que no contiene parentesis.
RE45_AUX = "[^\(\)]*"
RE4 = "((" + RE45_AUX + "\(" + RE45_AUX + "\)" + RE45_AUX + ")+)"
RE5 = "(" + RE45_AUX + "\((" + RE4 + "|" + RE45_AUX + ")\)" + RE45_AUX + ")+"
"""
Recuerda que puedes usar el fichero prueba.py para probar tus
expresiones regulares.
"""

"""
EJERCICIO 6:
Incluye a continuacion, dentro de esta cadena, tu respuesta
al ejercicio 6.

Las expresiones regulares no pueden usar recursión, una pila o un contador que no este previamente acotado 
(como no pueden los autómatas finitos) para llevar la cuenta de si los paréntesis están bien balanceados.

"""
