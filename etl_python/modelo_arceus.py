# =======================================
# MODELO PARA DERROTAR A ARCEUS
# =======================================
# Autor: Roberto Carlos Jimenez Rodriguez
# Version: 1.0
# =======================================

import pandas as pd
import numpy as np
import os

# =======================================
# RUTA DE ARCHIVOS
# =======================================

carpeta_script = os.path.dirname(__file__)         
carpeta_proyecto = os.path.join(carpeta_script, "..") 
ruta_archivo = os.path.join(carpeta_proyecto, "datos", "pokemon_limpio.csv")

# =======================================
# FUNCIONES
# =======================================

def obtener_multiplicador(fila):
    tipo1 = fila["tipo1"]
    tipo2 = fila["tipo2"]
    if tipo1 == "Fighting" or tipo2 == "Fighting":
        return 2.0
    elif tipo1 == "Ghost" and (tipo2 == "Ninguno" or tipo2 == "Ghost"):
        return 0.0
    else:
        return 1.0

# =======================================
# CODIGO PRINCIPAL
# =======================================

# ==================================
# DFs
# ==================================

# Leer el csv limpio
df = pd.read_csv(ruta_archivo)

# Obtener la informacion de Arceus
informacion_arceus = df[df["nombre"] == "Arceus"].iloc[0]

# df de pokemon candidatos
df_candidatos = df[df["nombre"] != "Arceus"]

# ==================================
# BONIFICADORES Y PENALIZADORES
# ==================================
# tipo1 o tipo2:
# Fighting = Bonificacion x 2.0
# Ghost = Penalizacion x 0.0
# 
# velocidad:
# Bonificacion/Penalizacion = x (Velocidad_Pokemon / Velocidad_Arceus)
# ==================================

# Multiplicador de stats dependiendo del tipo
df_candidatos["mult_tipo"] = df_candidatos.apply(obtener_multiplicador, axis = 1)

# Ataque mas poderoso
df_candidatos["poder_ofensivo"] = np.maximum(df_candidatos["ataque"], df_candidatos["ataque_especial"])

# Diferencia de poder_ofensivo y la defensa de Arceus
df_candidatos["diferencial_stat"] = (df_candidatos["poder_ofensivo"] - informacion_arceus["defensa"])

# Bono multiplicador, dependiendo de la velocidad
df_candidatos["bono_velocidad"] = df_candidatos["velocidad"] / informacion_arceus["velocidad"]

# Puntaje de estadisticas 
df_candidatos["puntaje_stats"] = (df_candidatos["diferencial_stat"] * df_candidatos["bono_velocidad"])

# Puntaje final
df_candidatos["puntaje_final"] = df_candidatos["puntaje_stats"] * df_candidatos["mult_tipo"]

# ==================================
# CLASIFICACION
# ==================================
# Tanque = (Salud + Defensa + Defensa Especial) > (Ataque + Ataque Especial + Velocidad)
# Atacante = (Ataque + Ataque Especial + Velocidad) > (Salud + Defensa + Defensa Especial)
# ==================================

df_candidatos["rol"] = np.where((df_candidatos["Puntos_de_salud"] + df_candidatos["defensa"] + df_candidatos["defensa_especial"]) > (df_candidatos["ataque"] + df_candidatos["ataque_especial"] + df_candidatos["velocidad"]), "Tanque", "Atacante")

# ==================================
# SELECCION DEL EQUIPO
# ==================================
# 1 Tanque y 3 Atacantes
# ==================================

tanque = (df_candidatos[df_candidatos["rol"] == "Tanque"]).nlargest(1, "puntaje_final")
atacantes = (df_candidatos[df_candidatos["rol"] == "Atacante"]).nlargest(3, "puntaje_final")

equipo_final = pd.concat([tanque, atacantes])

# ==================================
# PROBABILIDAD DE VICTORIA
# ==================================
# Formula utilizada: Poder del equipo combinado / (Poder del equipo combinado + Poder defensivo de Arceus) × 100
# ==================================

poder_equipo = (equipo_final["poder_ofensivo"] * equipo_final["mult_tipo"] * equipo_final["bono_velocidad"]).sum()
poder_arceus = informacion_arceus["Puntos_de_salud"] + informacion_arceus["defensa"] + informacion_arceus["defensa_especial"]
probabilidad_victoria = (poder_equipo / (poder_equipo + poder_arceus)) * 100

# ==================================
# OUTPUT FINAL
# ==================================

print("Despues del analisis de los mas de 800 Pokemones, este es el equipo definitivo para vencer a Arceus:")
for indice, fila in equipo_final.iterrows():
    print(fila["nombre"])
print(f"Con una probabilidad de victoria del {probabilidad_victoria:.2f}%")