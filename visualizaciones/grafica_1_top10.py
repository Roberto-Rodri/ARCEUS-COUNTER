# =======================================
# GRÁFICA 1: Top 10 Mejores Pokémon
# Agrupados por Tipo
# =======================================
# Autor: Neil (Visualizaciones)
# Base: Código de referencia por Rupert
# =======================================

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image
from matplotlib.patches import Patch
import fitz
import io
import os
import pandas as pd
import numpy as np

# =======================================
# RUTA DE ARCHIVOS
# =======================================

carpeta_script = os.path.dirname(__file__)
carpeta_proyecto = os.path.join(carpeta_script, "..")
ruta_csv = os.path.join(carpeta_proyecto, "datos", "pokemon_limpio.csv")
ruta_plantilla = os.path.join(carpeta_proyecto, "documentacion", "Plantilla_Membrete_EuroTrainers.pdf")

# =======================================
# DATOS
# =======================================

df = pd.read_csv(ruta_csv)

# Top 10 por total_base
top10 = df.nlargest(10, 'total_base')[['nombre', 'tipo1', 'tipo2', 'total_base']].reset_index(drop=True)

# Paleta de colores por tipo (basada en identidad corporativa)
colores_tipo = {
    'Dragon':  '#2E5090',
    'Psychic': '#9B59B6',
    'Water':   '#3498DB',
    'Ground':  '#C8962E',
    'Normal':  '#95A5A6',
    'Rock':    '#8B7355',
    'Steel':   '#7F8C8D',
}

# ==========================================
# PASO 1: Construir template landscape
# ==========================================

doc = fitz.open(ruta_plantilla)
page = doc[1]  # Página 2 (header + footer + watermark)
pix = page.get_pixmap(dpi=200)
portrait = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')
pw, ph = portrait.size  # 1700 x 2200 a 200dpi

# Canvas landscape: 2200x1700 (tamaño carta horizontal a 200dpi)
landscape_w, landscape_h = 2200, 1700
canvas = Image.new('RGBA', (landscape_w, landscape_h), (255, 255, 255, 255))

# Factor de escala
scale = landscape_w / pw

# Header
header_strip = portrait.crop((0, 0, pw, 320))
new_header_h = int(320 * scale)
header_scaled = header_strip.resize((landscape_w, new_header_h), Image.LANCZOS)
canvas.paste(header_scaled, (0, 0))

# Footer
footer_strip = portrait.crop((0, ph - 145, pw, ph))
new_footer_h = int(145 * scale)
footer_scaled = footer_strip.resize((landscape_w, new_footer_h), Image.LANCZOS)
canvas.paste(footer_scaled, (0, landscape_h - new_footer_h))

# Watermark
watermark_area = portrait.crop((250, 450, 1450, 1650))
watermark_resized = watermark_area.resize((900, 900), Image.LANCZOS)
wm_x = (landscape_w - 900) // 2
wm_y = (landscape_h - 900) // 2
canvas.paste(watermark_resized, (wm_x, wm_y), watermark_resized)

# ==========================================
# PASO 2: Crear Gráfica 1
# ==========================================

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
fig.patch.set_alpha(0)
ax.set_facecolor('none')

# Ordenar de menor a mayor para que el mejor quede arriba visualmente
top10_sorted = top10.sort_values('total_base', ascending=True)
colores_sorted = [colores_tipo.get(t, '#2E5090') for t in top10_sorted['tipo1']]

# Barras horizontales
bars = ax.barh(
    top10_sorted['nombre'],
    top10_sorted['total_base'],
    color=colores_sorted,
    edgecolor='#1a1a1a',
    linewidth=0.5,
    height=0.7
)

# Etiquetas de valor al final de cada barra
for bar, val in zip(bars, top10_sorted['total_base']):
    ax.text(
        bar.get_width() + 3,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va='center', fontsize=8, fontweight='bold', color='#333333'
    )

# Títulos y formato
ax.set_xlabel('Total Base de Estadísticas', fontsize=10, fontweight='bold', color='#333333')
ax.set_title(
    'Top 10 Pokémon con Mayor Total Base — Agrupados por Tipo',
    fontsize=12, fontweight='bold', color='#2E5090', pad=15
)
ax.set_xlim(0, max(top10['total_base']) * 1.08)

# Limpiar bordes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Leyenda de tipos
tipos_presentes = top10_sorted['tipo1'].unique()
legend_elements = [
    Patch(facecolor=colores_tipo.get(t, '#2E5090'), edgecolor='#1a1a1a',
          linewidth=0.5, label=t)
    for t in sorted(tipos_presentes)
]
ax.legend(
    handles=legend_elements, title='Tipo Primario',
    loc='lower right', fontsize=7, title_fontsize=8, framealpha=0.9
)

plt.tight_layout()

# ==========================================
# PASO 3: Guardar gráfica en memoria
# ==========================================

buf = io.BytesIO()
fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
buf.seek(0)
graph = Image.open(buf).convert('RGBA')
plt.close()

# ==========================================
# PASO 4: Redimensionar y centrar
# ==========================================

usable_x, usable_y = 130, new_header_h + 30
usable_w = landscape_w - 260
usable_h = landscape_h - new_header_h - new_footer_h - 60

graph_ratio = graph.width / graph.height
usable_ratio = usable_w / usable_h

if graph_ratio > usable_ratio:
    new_w = usable_w
    new_h = int(usable_w / graph_ratio)
else:
    new_h = usable_h
    new_w = int(usable_h * graph_ratio)

graph_resized = graph.resize((new_w, new_h), Image.LANCZOS)
paste_x = usable_x + (usable_w - new_w) // 2
paste_y = usable_y + (usable_h - new_h) // 2

# ==========================================
# PASO 5: Componer y guardar
# ==========================================

canvas.paste(graph_resized, (paste_x, paste_y), graph_resized)
final = canvas.convert('RGB')

ruta_salida = os.path.join(carpeta_proyecto, "visualizaciones", "grafica_1_top10_membrete.png")
final.save(ruta_salida, quality=95)

print("Gráfica 1 generada exitosamente!")
print(f"Guardada en: {ruta_salida}")