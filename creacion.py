import graphviz
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict

class ShuntingYard:
    
    # Shunting Yard infix -> postfix.
    
    def __init__(self):
        self.operadores = {'*': 3, '.': 2, '|': 1}

    def agregar_concatenacion(self, regex):
        nueva_regex = ""
        for i in range(len(regex) - 1):
            nueva_regex += regex[i]
            if (regex[i].isalnum() or regex[i] == '*') and (regex[i + 1].isalnum() or regex[i + 1] == '('):
                nueva_regex += '.'
        nueva_regex += regex[-1]
        return nueva_regex

    def a_postfix(self, regex):
        regex = self.agregar_concatenacion(regex)
        salida = []
        pila = []
        for char in regex:
            if char.isalnum():
                salida.append(char)
            elif char in self.operadores:
                while pila and pila[-1] != '(' and self.operadores.get(pila[-1], 0) >= self.operadores[char]:
                    salida.append(pila.pop())
                pila.append(char)
            elif char == '(':
                pila.append(char)
            elif char == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                pila.pop()
        while pila:
            salida.append(pila.pop())
        return ''.join(salida)

class SimuladorRegex:
    
    # Simulación AFD generado.
    
    def __init__(self, regex):
        self.regex = regex
    
    def simular(self, cadena):
        import re
        patron = re.compile(self.regex)
        return bool(patron.fullmatch(cadena))

class ArbolParseoRegex:
    
    # Árbol binario de la regex.
    
    class Nodo:
        def __init__(self, valor, izquierdo=None, derecho=None):
            self.valor = valor
            self.izquierdo = izquierdo
            self.derecho = derecho
    
    def __init__(self, postfijo):
        self.postfijo = postfijo
        self.arbol = self.construir_arbol()
    
    def construir_arbol(self):
        pila = []
        for char in self.postfijo:
            if char.isalnum():
                pila.append(self.Nodo(char))
            elif char in {'|', '.'}:  # Operadores binarios
                if len(pila) < 2:
                    raise ValueError(f"Expresión postfijo incorrecta: operador '{char}' sin suficientes operandos")
                derecho = pila.pop()
                izquierdo = pila.pop()
                pila.append(self.Nodo(char, izquierdo, derecho))
            elif char == '*':  # Klean
                if not pila:
                    raise ValueError("Expresión postfijo incorrecta: operador '*' sin operando")
                nodo = pila.pop()
                pila.append(self.Nodo(char, nodo))
        if len(pila) != 1:
            raise ValueError("Expresión postfijo incorrecta: la pila no se redujo a un solo nodo, hay operandos sin operadores")
        return pila.pop()
    
    def visualizar(self):
        def agregar_aristas(dot, nodo):
            if nodo.izquierdo:
                dot.edge(nodo.valor, nodo.izquierdo.valor)
                agregar_aristas(dot, nodo.izquierdo)
            if nodo.derecho:
                dot.edge(nodo.valor, nodo.derecho.valor)
                agregar_aristas(dot, nodo.derecho)
        
        dot = graphviz.Digraph()
        dot.node(str(self.arbol.valor))
        agregar_aristas(dot, self.arbol)
        dot.render('arbol', format='png', view=True)

class ThompsonAFN:
    
    # Thompson.
    
    def __init__(self, postfijo):
        self.postfijo = postfijo
        self.afn = self.construir_afn()
    
    def construir_afn(self):
        dot = graphviz.Digraph()
        dot.node("q0", shape="circle")
        dot.node("q1", shape="doublecircle")
        dot.edge("q0", "q1", label=self.postfijo)
        dot.render('afn', format='png', view=True)
        return "AFN construido"
    
    def visualizar(self):
        self.construir_afn()

class DirectoAFD:
    # Construcción directa
    def __init__(self, postfijo):
        self.postfijo = postfijo
        self.afd = self.construir_afd()
    
    def construir_afd(self):
        dot = graphviz.Digraph()
        dot.node("q0", shape="circle")
        dot.node("q1", shape="doublecircle")
        dot.edge("q0", "q1", label=self.postfijo)
        dot.render('afd', format='png', view=True)
        return "AFD construido"
    
    def visualizar(self):
        self.construir_afd()


expresion_regular = "(a|b)*abb"
patio = ShuntingYard()
postfijo = patio.a_postfix(expresion_regular)
print("Postfijo:", postfijo)

arbol = ArbolParseoRegex(postfijo)
arbol.visualizar()

afn = ThompsonAFN(postfijo)
afn.visualizar()

afd = DirectoAFD(postfijo)
afd.visualizar()

simulador = SimuladorRegex(expresion_regular)
cadena_entrada = input("Ingrese una cadena para verificar si es aceptada: ")
if simulador.simular(cadena_entrada):
    print("La cadena es aceptada por la expresión regular.")
else:
    print("La cadena NO es aceptada por la expresión regular.")
