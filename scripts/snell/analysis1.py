import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Configuración del estilo de las gráficas
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({"font.size":12, "figure.dpi": 300})

# Carga de datos y limpieza
file_path = "../../data/snell/tabla1.csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()
df["refractado"] = pd.to_numeric(df["refractado"], errors="coerce")
df = df.dropna(subset=["refractado"]).copy()

# Conversión a radianes
df["incidente_rad"] = np.radians(df["incidente"])
df["refractado_rad"] = np.radians(df["refractado"])

df["sin_incidente"] = np.sin(df["incidente_rad"])
df["sin_refractado"] = np.sin(df["refractado_rad"])

# Gráfica 1 - Ley de reflexión
plt.figure(figsize=(10, 7))
sns.scatterplot(data = df, x = "incidente", y = "reflejado", color='b', label="Datos experimentales")

## Modelo teórico
max_ang = max(df["incidente"].max(), 70) if not df.empty else 70
x_line = np.linspace(0, max_ang, 100)
plt.plot(x_line, x_line, color='r', label=r"Modelo teórico: $\theta_1 = \theta_2$")
#plt.plot(df["incidente"], df["reflejado"], color='r', label=r"Pendiente $m = 1$")

plt.title(
    """Comprobación de Ley de Reflexión $\\theta_1$ vs $\\theta_2$
    Interfaz Aire $\\rightarrow$ Acrílico
    """)
#plt.title(r"Comprobación de Ley de reflexión $\theta_1$ vs $\theta_2$\nInterfaz Aire $\rightarrow$ Acrílico")
plt.xlabel(r"Ángulo de incidencia $\theta_1$ [$^\circ$]")
plt.ylabel(r"Ángulo de reflexión $\theta_2$ [$^\circ$]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../graphs/reflexion_plot1.png")
plt.show()

# Gráfica 2 - Relación de ángulos de refracción
plt.figure(figsize=(10, 7))
sns.scatterplot(data=df, x="incidente", y="refractado", color='b', label="Datos experimentales")

plt.title(
    """Relación $\\theta_1$ vs $\\theta_3$
    Interfaz Aire $\\rightarrow$ Acrílico
    """)
plt.xlabel(r"Ángulo de incidencia $\theta_1$ [$^\circ$]")
plt.ylabel(r"Ángulo de refracción $\theta_3$ [$^\circ$]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../graphs/refraction_plot1.png")
plt.show()

# Mínimos cuadrados
x = df["sin_incidente"]
y = df["sin_refractado"]

m, b, r, p, std_err = linregress(x, y)
r2 = r**2

## y = mx + b
## n_aire sin(theta_1) = n_acrilico sin(theta_3) => sin(theta_3) = (1/n_acrilico) sin(theta_1) => m = 1/n_acrilico
n_acr = 1 / m
error = (1 / m**2) * std_err # Propagación de error

print(f"Pendiente m: {m:.4f} +- {std_err:.4f}")
print(f"Ordenada al origen b: {b:.4f}")
print(f"R^2: {r2:.4f}")
print(f"n_acrilico experimental: {n_acr:.4f} +- {error:.4f}")

# Línea de ajuste
x_fit = np.linspace(min(x), max(x), 100)
y_fit = m * x_fit + b

# Gráfica de Ley de Snell con ajuste lineal
plt.figure(figsize=(10,7))
sns.scatterplot(x = x, y = y, color = 'b' , label = "Datos experimentales")

plt.plot(x_fit, y_fit, color = 'r', label = (
    f"y = {m:.4f}x + {b:.4f}\n"
    f"$R^2 = {r2:.4f}$"
))

plt.title(
    """Ajuste lineal para Ley de Snell
    Interfaz Aire $\\rightarrow$ Acrílico
    """)
plt.xlabel(r"sin$\theta_1$")
plt.ylabel(r"sin$\theta_3$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../graphs/fit_refraction_plot1.png")
plt.show()
