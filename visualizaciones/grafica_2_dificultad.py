# ==========================================================
# GRÁFICA 2: Top 10 Pokémon más difíciles de capturar
# Autor: Neil (Ingeniería de Datos y Visualización)
# ==========================================================

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image
import fitz
import io
import os
import pandas as pd
import seaborn as sns

# --- Rutas Relativas ---
carpeta_script = os.path.dirname(__file__)
ruta_proyecto = os.path.join(carpeta_script, "..")
ruta_csv = os.path.join(ruta_proyecto, "datos", "pokemon_limpio.csv")
ruta_plantilla = os.path.join(ruta_proyecto, "documentacion", "Plantilla_Membrete_EuroTrainers.pdf")

# --- Datos ---
df = pd.read_csv(ruta_csv)
top_10_dif = df.sort_values(by=['Probabilidad_de_captura', 'total_base'], 
                            ascending=[True, False]).head(10)

# --- PASO 1: Construir template landscape ---
doc = fitz.open(ruta_plantilla)
page = doc[1] 
pix = page.get_pixmap(dpi=200)
portrait = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')
pw, ph = portrait.size
landscape_w, landscape_h = 2200, 1700
canvas = Image.new('RGBA', (landscape_w, landscape_h), (255, 255, 255, 255))
scale = landscape_w / pw

header = portrait.crop((0, 0, pw, 320)).resize((landscape_w, int(320 * scale)), Image.LANCZOS)
footer = portrait.crop((0, ph - 145, pw, ph)).resize((landscape_w, int(145 * scale)), Image.LANCZOS)
watermark = portrait.crop((250, 450, 1450, 1650)).resize((900, 900), Image.LANCZOS)
canvas.paste(header, (0, 0))
canvas.paste(footer, (0, landscape_h - footer.height))
canvas.paste(watermark, ((landscape_w - 900) // 2, (landscape_h - 900) // 2), watermark)

# --- PASO 2: Crear Gráfica ---
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
fig.patch.set_alpha(0)
ax.set_facecolor('none')

sns.barplot(data=top_10_dif, x='Probabilidad_de_captura', y='nombre', palette='Reds_r', ax=ax)
ax.set_title('Top 10 Pokémon con Menor Ratio de Captura Base', fontsize=14, fontweight='bold', color='#2E5090')
ax.set_xlabel('Ratio de Captura (Catch Rate)', fontsize=10, fontweight='bold')

plt.tight_layout()

# --- PASO 3: Componer y Guardar ---
buf = io.BytesIO()
fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
buf.seek(0)
graph = Image.open(buf).convert('RGBA')
graph.thumbnail((1940, 1039), Image.LANCZOS)
canvas.paste(graph, (130 + (1940 - graph.width) // 2, 444 + (1039 - graph.height) // 2), graph)

ruta_salida = os.path.join(ruta_proyecto, "visualizaciones", "grafica_2_dificultad_membrete.png")
canvas.convert('RGB').save(ruta_salida, quality=95)
print(f"Gráfica 2 generada en: {ruta_salida}")