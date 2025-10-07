import numpy as np
import matplotlib.pyplot as plt
import math

# Aproximacion de funciones con series de taylor

def taylor_exp(x, n_terms):
    """
    Aproxima la función exponencial e^x usando la serie de Taylor.

    Args:
        x (float): Valor en el que se evalúa la función.
        n_terms (int): Número de términos de la serie de Taylor a usar.

    Returns:
        float: Aproximación del valor de e^x.
    """
    result = 0
    for n in range(n_terms):
        result += (x**n) / math.factorial(n)
    return result


def taylor_sin(x, n_terms):
    """
    Aproxima la función seno sin(x) usando la serie de Taylor.

    Args:
        x (float): Valor en radianes en el que se evalúa la función.
        n_terms (int): Número de términos de la serie de Taylor a usar.

    Returns:
        float: Aproximación del valor de sin(x).
    """
    result = 0
    for n in range(n_terms):
        result += ((-1)**n * x**(2*n + 1)) / math.factorial(2*n + 1)
    return result


def taylor_cos(x, n_terms):
    """
    Aproxima la función coseno cos(x) usando la serie de Taylor.

    Args:
        x (float): Valor en radianes en el que se evalúa la función.
        n_terms (int): Número de términos de la serie de Taylor a usar.

    Returns:
        float: Aproximación del valor de cos(x).
    """
    result = 0
    for n in range(n_terms):
        result += ((-1)**n * x**(2*n)) / math.factorial(2*n)
    return result


def taylor_ln1p(x, n_terms):
    """
    Aproxima la función logarítmica natural ln(1+x) usando la serie de Taylor.

    Nota:
        La serie solo converge para |x| < 1.

    Args:
        x (float): Valor en el que se evalúa la función (con |x| < 1).
        n_terms (int): Número de términos de la serie de Taylor a usar.

    Returns:
        float: Aproximación del valor de ln(1+x).
    """
    result = 0
    for n in range(1, n_terms+1):
        result += ((-1)**(n+1)) * (x**n) / n
    return result


def taylor_arctan(x, n_terms):
    """
    Aproxima la función arco tangente arctan(x) usando la serie de Taylor.

    Nota:
        La serie solo converge para |x| < 1.

    Args:
        x (float): Valor en el que se evalúa la función (con |x| < 1).
        n_terms (int): Número de términos de la serie de Taylor a usar.

    Returns:
        float: Aproximación del valor de arctan(x).
    """
    result = 0
    for n in range(n_terms):
        result += ((-1)**n) * (x**(2*n + 1)) / (2*n + 1)
    return result
