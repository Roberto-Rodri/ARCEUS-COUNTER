import pandas as pd
import os
# 1. Carga
df = pd.read_csv(r'C:\Users\tibur\Downloads\pokemon.csv')

# 2. Normalización de Texto
df['nombre'] = df['nombre'].str.strip().str.title()
df['tipo1'] = df['tipo1'].str.capitalize()
df['tipo2'] = df['tipo2'].fillna('Ninguno').str.capitalize()
df['habilidades'] = df['habilidades'].str.replace(r"[\[\]']", "", regex=True)

# 3. Limpieza de nulos y tipos numéricos
df['Probabilidad_de_captura'] = pd.to_numeric(df['Probabilidad_de_captura'].str.extract('(\d+)')[0], errors='coerce')
df['altura_(m)'] = df['altura_(m)'].fillna(df['altura_(m)'].median())
df['peso_(kg)'] = df['peso_(kg)'].fillna(df['peso_(kg)'].median())
df['%_macho'] = df['%_macho'].fillna(-1)

# 4. Optimización de Memoria (Neil's Task)
# Estadísticas a int16
stats_cols = ['ataque', 'defensa', 'Puntos_de_salud', 'ataque_especial', 'defensa_especial', 'velocidad', 'total_base']
df[stats_cols] = df[stats_cols].astype('int16')

# Resistencias a float32
resistencia_cols = [c for c in df.columns if 'contraataque' in c]
df[resistencia_cols] = df[resistencia_cols].astype('float32')

# 5. Guardado Final

# 1. Definir el nombre de la carpeta
carpeta_destino ='ARCEUS-COUNTER/datos'

# 2. Verificar si la carpeta existe; si no, crearla
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)
    print(f"Carpeta '{carpeta_destino}' creada con éxito.")

# 3. Guardar el CSV dentro de esa carpeta
# Usamos '/' para indicar que el archivo va dentro de la carpeta
df.to_csv(f'{carpeta_destino}/pokemon_limpio.csv', index=False)

print(f"¡ETL Completada! El archivo se guardó en: {carpeta_destino}/pokemon_limpio.csv")