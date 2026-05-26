import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from scipy.signal import find_peaks

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({"font.size": 12, "figure.dpi": 300})

file_path = "../../data/espectrometria/P-laser-He_Ne-rojo-001.txt"

# Limpieza de datos
start_idx = None
with open(file_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "===START===" in line:
        start_idx = i + 1
        break

df = pd.read_csv(
    file_path, 
    skiprows=start_idx, 
    sep=r"\s+", 
    names=["wavelength_nm", "intensity"], 
    engine="python"
)

df["wavelength_nm"] = pd.to_numeric(df["wavelength_nm"], errors="coerce") 
df["intensity"] = pd.to_numeric(df["intensity"], errors="coerce") 
df = df.dropna()

print(df.head())
print(df.columns)
print(df.dtypes)
print(df.shape)
print(df.tail())

# Normalización de la intensidad
df["intensity_norm"] = df["intensity"]/df["intensity"].max()

x = df["wavelength_nm"].values
y = df["intensity_norm"].values
picos, propiedades = find_peaks(y, height=0.2, prominence=0.1)

print("Picos de emisión:")
for i in picos:
    print(f"Longitud de onda: {x[i]:.4f} nm | Intensidad: {y[i]:.4f}")

# Gráfica del espectro de emisión
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="wavelength_nm", y="intensity_norm", label="Espectro de emisión experimental")
plt.fill_between(x, y, alpha=0.1)

## Marcar picos de emisión
plt.plot(x[picos], y[picos], "x", color='r', markersize=8, label="Picos de emisión")

## Labels de los picos
for i in picos:
    plt.text(x[i], y[i] + 0.05, f"{x[i]:.2f} nm", horizontalalignment="center", fontsize=9, color="darkred")

plt.title(
    """Perfil de emisión espectral normalizado
    Láser He-Ne rojo
    """
)
plt.xlabel(r"Longitud de onda $\lambda$ [nm]")
plt.ylabel("Intensidad [u.a.]")

plt.ylim(0, 1.15)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("../../graphs/laser_He-Ne.png")
plt.show()
