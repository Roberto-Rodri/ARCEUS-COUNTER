# ==========================================================
# GRÁFICA 4: Tablero de 6 Radares (Integrantes + Equipo + Arceus)
# Autor: Neil (Ingeniería de Datos y Visualización)
# ==========================================================

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image
import fitz # PyMuPDF
import io
import os
import numpy as np
import pandas as pd

# --- Configuración de Rutas ---
carpeta_script = os.path.dirname(__file__)
ruta_proyecto = os.path.join(carpeta_script, "..")
ruta_plantilla = os.path.join(ruta_proyecto, "documentacion", "Plantilla_Membrete_EuroTrainers.pdf")

# --- Datos del PDF y Algoritmo ---
categorias = ['PS', 'Ataque', 'Defensa', 'At. Esp', 'Def. Esp', 'Velocidad']
et_blue = '#2E5090'
et_gold = '#C8962E'

sujetos = [
    {'n': '1. Mewtwo (Atacante)', 's': [106, 110, 90, 194, 90, 140], 'c': '#9B59B6'}, # Púrpura
    {'n': '2. Tyranitar (Tanque)', 's': [100, 134, 110, 95, 100, 61], 'c': '#27AE60'}, # Verde
    {'n': '3. Gallade (Lucha)', 's': [68, 165, 65, 65, 115, 80], 'c': '#2980B9'},    # Azul
    {'n': '4. Heracross (Lucha)', 's': [80, 185, 75, 40, 95, 85], 'c': '#C0392B'},   # Rojo
    {'n': 'EQUIPO COMPLETO', 's': [106, 185, 110, 194, 120, 140], 'c': et_blue},    # Azul ET (Pico)
    {'n': 'ARCEUS (RIVAL)', 's': [120, 120, 120, 120, 120, 120], 'c': et_gold}      # Dorado
]

# --- PASO 1: Template Landscape ---
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

# --- PASO 2: Crear Cuadrícula 2x3 ---
angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
angulos += angulos[:1]

fig, axs = plt.subplots(2, 3, figsize=(10, 6), subplot_kw=dict(polar=True), dpi=200)
fig.patch.set_alpha(0)
ax_flat = axs.flatten()

for i, ax in enumerate(ax_flat):
    data = sujetos[i]
    stats = data['s'] + data['s'][:1]
    
    # Estilo de Radar
    ax.set_facecolor('none')
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 200)
    
    # Dibujar Arceus como sombra de referencia (excepto en el propio Arceus)
    if data['n'] != 'ARCEUS (RIVAL)':
        ref = sujetos[5]['s'] + sujetos[5]['s'][:1]
        ax.plot(angulos, ref, color=et_gold, linewidth=1, linestyle='--', alpha=0.4)
        
    # Dibujar Sujeto
    ax.plot(angulos, stats, color=data['c'], linewidth=2)
    ax.fill(angulos, stats, color=data['c'], alpha=0.3)
    
    # Etiquetas
    ax.set_thetagrids(np.degrees(angulos[:-1]), categorias, color=et_blue, fontsize=7, fontweight='bold')
    ax.set_title(data['n'], fontsize=9, fontweight='bold', color=data['c'], pad=15)
    ax.set_rgrids([100, 200], labels=[], alpha=0) # Limpiar radios internos

plt.suptitle("COMPARATIVA INDIVIDUAL Y DE EQUIPO VS ARCEUS", 
             size=14, color=et_blue, y=1.02, fontweight='bold')
plt.tight_layout()

# --- PASO 3: Componer y Guardar ---
buf = io.BytesIO()
fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
buf.seek(0)
graph = Image.open(buf).convert('RGBA')
graph.thumbnail((1940, 1039), Image.LANCZOS)
canvas.paste(graph, (130 + (1940 - graph.width) // 2, 444 + (1039 - graph.height) // 2), graph)

ruta_salida = os.path.join(ruta_proyecto, "visualizaciones", "grafica_4_tablero_6_membrete.png")
canvas.convert('RGB').save(ruta_salida, quality=95)
print(f"✅ Tablero de 6 radares generado en: {ruta_salida}")