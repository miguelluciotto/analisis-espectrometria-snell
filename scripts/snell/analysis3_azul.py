import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Configuración del estilo de las gráficas
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({"font.size":12, "figure.dpi": 300})

# Carga de datos
file_path = "../../data/snell/tabla3_azul.csv"
df = pd.read_csv(file_path)

# Filtrar datos RIT
df.columns = df.columns.str.strip() # Eliminar espacios en nombres de columnas
df["refractado"] = pd.to_numeric(df["refractado"], errors="coerce") # Valores vacíos RIT -> NaN

df_flt = df.dropna(subset=["refractado"]).copy() # Drop rows with Nans (remove RIT)

# Conversión a radianes
df_flt["incidente_rad"] = np.radians(df_flt["incidente"])
df_flt["refractado_rad"] = np.radians(df_flt["refractado"])

df_flt["sin_incidente"] = np.sin(df_flt["incidente_rad"])
df_flt["sin_refractado"] = np.sin(df_flt["refractado_rad"])

# Gráfica 1 - ley de reflexión
plt.figure(figsize=(10, 7))
sns.scatterplot(data = df, x = "incidente", y = "reflejado", color='b', label="Datos experimentales")

## Modelo teórico
max_ang = max(df["incidente"].max(), 70) if not df.empty else 70
x_line = np.linspace(0, max_ang, 100)
plt.plot(x_line, x_line, color='r', label=r"Modelo teórico: $\theta_1 = \theta_2$")

## RIT
plt.xlim(0, 75)
plt.axvline(42, color="purple", linestyle=":", label=r"Ángulo crítico experimental: $\theta_c \approx 42 ^\circ$")
plt.axvspan(42, 75, color="purple", alpha=0.1, label="Zona de reflexión interna total")

plt.title(
    """Comprobación experimental de la Ley de Reflexión $\\theta_1$ vs $\\theta_2$
    Interfaz Acrílico $\\rightarrow$ Aire usando el filtro azul
    """)
plt.xlabel(r"Ángulo de incidencia $\theta_1$ [$^\circ$]")
plt.ylabel(r"Ángulo de reflexión $\theta_2$ [$^\circ$]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../graphs/reflexion_plot3_azul.png", dpi=300)
plt.show()

# Gráfica 2 - Relación de ángulos de refracción
plt.figure(figsize=(10, 7))
sns.scatterplot(data = df_flt, x = "incidente", y = "refractado", color='b', label="Datos experimentales")

plt.xlim(0,50)
plt.ylim(0,90)

plt.axvline(42, color="purple", linestyle=":", label=r"Ángulo crítico experimental: $\theta_c \approx 42 ^\circ$")
plt.axvspan(42, 50, color="purple", alpha=0.1, label="Zona de reflexión interna total")

plt.title(
    """Relación $\\theta_1$ vs $\\theta_3$
    Interfaz Acrílico $\\rightarrow$ Aire usando el filtro azul
    """)
plt.xlabel(r"Ángulo de incidencia $\theta_1$ [$^\circ$]")
plt.ylabel(r"Ángulo de refracción $\theta_3$ [$^\circ$]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../graphs/refraction_plot3_azul.png", dpi=300)
plt.show()

# Mínimos cuadrados y modelado
x = df_flt["sin_incidente"]
y = df_flt["sin_refractado"]

m, b, r, p, std_err = linregress(x, y)
r2 = r ** 2

## y = mx + b
## n_acr sin(theta_1) = n_air sin(theta_3) => sin(theta_3) = n_acr sin(theta_1) => n_acr = m
n_acr = m
error = std_err # Propagación de error

print(f"Pendiente m = n_acrílico: {n_acr:.4f} +- {error:.4f}")
print(f"Ordenada al origen b: {b:.4f}")
print(f"R^2: {r2:.4f}")

## Línea de ajuste
x_fit = np.linspace(min(x), max(x), 100)
y_fit = m * x_fit + b

## Gráfica 3 - Ley de Snell con ajuste lineal
plt.figure(figsize=(10,7))
sns.scatterplot(x = x, y = y, color = 'b', label = "Datos experimentales")
plt.plot(x_fit, y_fit, color = 'r', label = (
    f"$y = {m:.4f} + {b:.4f}$\n"
    f"$R^2 = {r2:.4f}$"
    )
)

#plt.axhline(1.0, color="gray", linestyle="--", alpha=0.7, label=r"Límite de refracción: sin$\theta_3 = 1$")

plt.title(
    """Ajuste lineal para ley de Snell
    Interfaz Acrílico $\\rightarrow$ Aire usando el filtro azul
    """)
plt.xlabel(r"sin$\theta_1$")
plt.ylabel(r"sin$\theta_3$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../../graphs/fit_refraction_plot3_azul.png", dpi=300)
plt.show()
