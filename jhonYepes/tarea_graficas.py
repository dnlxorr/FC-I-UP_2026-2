import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carga de datos y asignación de variables
# Asegúrate de que el archivo CSV se llame exactamente así y esté en tu carpeta
df = pd.read_csv('Heterogeneous_Data .csv', low_memory=False)

# 2. Limpieza de datos
# Descartamos valores vacíos y tomamos una muestra de 500 para que la PC no sufra renderizando
df_repos = df.dropna(subset=['stars', 'forks', 'watchers']).head(500)

estrellas = df_repos['stars']
bifurcaciones = df_repos['forks']
observadores = df_repos['watchers']

# 3. Creación del lienzo principal con 4 subdivisiones
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Análisis Visual del Dataset de GitHub', fontsize=16, fontweight='bold')

# Gráfica en 2D (Líneas)
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(range(len(estrellas[:50])), estrellas[:50], color='#1f77b4', linewidth=2)
ax1.set_title('Gráfica en 2D: Top 50 Repositorios')
ax1.set_xlabel('Índice del Repositorio')
ax1.set_ylabel('Cantidad de Estrellas')

# Gráfica de Dispersión
ax2 = fig.add_subplot(2, 2, 2)
sns.scatterplot(x=bifurcaciones, y=estrellas, ax=ax2, color='#2ca02c', alpha=0.6)
ax2.set_title('Dispersión: Forks vs Estrellas')
ax2.set_xlabel('Forks')
ax2.set_ylabel('Estrellas')

# Gráfica de Densidad
ax3 = fig.add_subplot(2, 2, 3)
sns.kdeplot(x=estrellas, ax=ax3, color='#9467bd', fill=True)
ax3.set_title('Densidad: Distribución de Estrellas')
ax3.set_xlabel('Estrellas')
ax3.set_ylabel('Densidad')

# Gráfica en 3D
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
ax4.scatter(estrellas, bifurcaciones, observadores, color='#d62728', alpha=0.7)
ax4.set_title('3D: Estrellas, Forks y Watchers')
ax4.set_xlabel('Estrellas')
ax4.set_ylabel('Forks')
ax4.set_zlabel('Watchers')

# Ajustamos los márgenes y mostramos la ventana en pantalla
plt.tight_layout()
plt.show()
#cambio
