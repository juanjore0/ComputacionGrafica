import numpy as np
import matplotlib.pyplot as plt
from function import *

x = np.linspace(-2, 2, 400)

# Definir el número de términos para todas las aproximaciones
n_terms = 10  # Cambia este valor según lo que desees

# Funciones reales de NumPy
y_exp = np.exp(x)
y_sin = np.sin(x)
y_cos = np.cos(x)
y_ln1p = np.log1p(x[x>-1])  # restringido a x>-1
y_arctan = np.arctan(x)

# Aproximaciones con el mismo número de términos
y_exp_taylor = [taylor_exp(val, n_terms) for val in x]
y_sin_taylor = [taylor_sin(val, n_terms) for val in x]
y_cos_taylor = [taylor_cos(val, n_terms) for val in x]
y_ln1p_taylor = [taylor_ln1p(val, n_terms) for val in x[x>-1]]
y_arctan_taylor = [taylor_arctan(val, n_terms) for val in x]

# Crear subplots
fig, axs = plt.subplots(3, 2, figsize=(12, 10))

# e^x
axs[0,0].plot(x, y_exp, label="exp(x)")
axs[0,0].plot(x, y_exp_taylor, "--", label=f"Taylor exp ({n_terms} términos)")
axs[0,0].set_title("Aproximación e^x")
axs[0,0].legend()

# sin(x)
axs[0,1].plot(x, y_sin, label="sin(x)")
axs[0,1].plot(x, y_sin_taylor, "--", label=f"Taylor sin ({n_terms} términos)")
axs[0,1].set_title("Aproximación sin(x)")
axs[0,1].legend()

# cos(x)
axs[1,0].plot(x, y_cos, label="cos(x)")
axs[1,0].plot(x, y_cos_taylor, "--", label=f"Taylor cos ({n_terms} términos)")
axs[1,0].set_title("Aproximación cos(x)")
axs[1,0].legend()

# ln(1+x)
axs[1,1].plot(x[x>-1], y_ln1p, label="ln(1+x)")
axs[1,1].plot(x[x>-1], y_ln1p_taylor, "--", label=f"Taylor ln(1+x) ({n_terms} términos)")
axs[1,1].set_title("Aproximación ln(1+x)")
axs[1,1].legend()

# arctan(x)
axs[2,0].plot(x, y_arctan, label="arctan(x)")
axs[2,0].plot(x, y_arctan_taylor, "--", label=f"Taylor arctan ({n_terms} términos)")
axs[2,0].set_title("Aproximación arctan(x)")
axs[2,0].legend()

# Ajustar layout
plt.tight_layout()
plt.show()
