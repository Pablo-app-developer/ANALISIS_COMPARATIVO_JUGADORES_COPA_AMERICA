import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cargar el archivo CSV
file_path = r'C:\Users\SAMSUNG\Documents\DATOS PARA GRAFICAS\FUTBOLEROS\international-copa-america-players-2024-to-2024-stats.csv'  # Asegúrate de tener el archivo CSV en la ruta correcta
df = pd.read_csv(file_path)

# Reemplazar USMNT por USA en Current Club
df['Current Club'] = df['Current Club'].replace('USMNT', 'USA')

# Obtener listas únicas de países
current_club_countries = sorted(df['Current Club'].unique())
all_countries = sorted(set(df['Current Club'].unique()) | set(df['nationality'].unique()))

# Crear una tabla comparativa
comparative_table = pd.DataFrame(0, index=all_countries, columns=current_club_countries)

# Llenar la tabla comparativa
for _, row in df.iterrows():
    comparative_table.loc[row['nationality'], row['Current Club']] += 1

# Totalizar filas y columnas
comparative_table['Total'] = comparative_table.sum(axis=1)
comparative_table.loc['Total'] = comparative_table.sum()

# Separar los países adicionales de nationality
additional_countries = [country for country in all_countries if country not in current_club_countries]

# Configurar el tamaño del gráfico y estilo
fig = plt.figure(figsize=(24, 30))
sns.set(style="whitegrid", font_scale=1.5)

# Función para crear heatmap con títulos horizontales y celdas ajustadas
def create_heatmap(data, ax, cmap):
    # Crear una máscara para los totales
    mask = np.zeros_like(data, dtype=bool)
    mask[:, -1] = True
    mask[-1, :] = True

    # Crear el heatmap
    sns.heatmap(data, annot=True, fmt="d", cmap=cmap, cbar=False, linewidths=.5, 
                ax=ax, linecolor='black', linestyle=':', square=False, 
                annot_kws={'size': 20}, mask=mask)
    
    # Añadir los totales sin color de fondo
    for i in range(len(data.index)):
        ax.text(len(data.columns) - 0.5, i + 0.5, data.iloc[i, -1], 
                ha="center", va="center", fontweight="bold")
    for j in range(len(data.columns) - 1):
        ax.text(j + 0.5, len(data.index) - 0.5, data.iloc[-1, j], 
                ha="center", va="center", fontweight="bold")

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='y', labelrotation=0, labelsize=20)
    ax.tick_params(axis='x', labelsize=20)
    ax.set_xlabel(ax.get_xlabel(), fontsize=17)
    ax.set_ylabel(ax.get_ylabel(), fontsize=17)
    
    # Ajustar el tamaño de las celdas
    plt.setp(ax.get_yticklabels(), ha="right")
    ax.set_ylim(len(data), 0)

# Crear un heatmap para la tabla comparativa principal
ax_main = fig.add_subplot(211)
create_heatmap(comparative_table.loc[current_club_countries + ['Total']], ax_main, "Blues")
ax_main.set_xlabel("País representado")
ax_main.set_ylabel("Nacionalidad")

# Añadir una sección adicional para los países extra de nationality
if additional_countries:
    additional_table = comparative_table.loc[additional_countries].copy()
    additional_table['Total'] = additional_table.sum(axis=1)
    additional_table.loc['Total'] = additional_table.sum()

    ax_additional = fig.add_subplot(212)
    create_heatmap(additional_table.loc[additional_countries + ['Total']], ax_additional, "Greens")
    ax_additional.set_xlabel("País representado")
    ax_additional.set_ylabel("Países adicionales\n(solo nacionalidad)")
    ax_additional.set_ylim(len(additional_table), 0)

    # Asegurar que ambas tablas tengan el mismo ancho de columnas y filas
    ax_additional.set_xticks(ax_main.get_xticks())
    ax_additional.set_xticklabels(ax_main.get_xticklabels())
    ax_additional.set_xlim(ax_main.get_xlim())
    ax_additional.set_ylim(ax_main.get_ylim())

# Ajustar la posición del título y los subtítulos
fig.suptitle("Tabla Comparativa: Nacionalidad vs. País Representado en Copa América 2024", 
             fontsize=25, y=0.98)

# Ajustar el diseño
plt.tight_layout()
plt.subplots_adjust(top=0.96, hspace=0.2)

# Guardar el gráfico como un archivo PNG
output_path = r'C:\Users\SAMSUNG\Documents\DATOS PARA GRAFICAS\FUTBOLEROS\comparative_table_copa_america_2024.svg'
plt.savefig(output_path, format='svg', bbox_inches='tight', dpi=300)

# Mostrar la ruta del archivo guardado
print(f'Archivo SVG guardado en: {output_path}')
