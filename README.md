# EuroTrainers - Proyecto: Enciclopedia Pokémon

## Descripción del Proyecto
Este repositorio contiene el desarrollo integral de una base de datos optimizada y un sistema de análisis estadístico para la "Enciclopedia Pokémon". El proyecto abarca desde la extracción, limpieza y normalización de datos en bruto (Pipeline ETL), hasta la implementación de una base de datos relacional y el desarrollo de visualizaciones analíticas complejas para la toma de decisiones.

## Equipo de Trabajo y Roles
* **Roberto Carlos Jimenez Rodriguez (Administrador):** Ingeniería de Datos, Arquitectura SQL y Modelado Matemático.
* **Rolando Garcia Reyes (Colaborador):** Arquitectura de Base de Datos (Modelo ER) e Identidad Corporativa.
* **Neil Guadalupe Flores Escobedo (Colaborador):** Ingeniería de Datos (ETL), Enriquecimiento de Datos y Visualización Analítica.

## Tecnologías Utilizadas
* **Lenguajes:** Python, SQL.
* **Librerías:** Pandas, Numpy, ggplot2/Matplotlib.
* **Gestor de Base de Datos:** MySQL.

## Estructura del Repositorio
* `/datos`: Archivo CSV inicial en bruto y recopilación de fuentes de datos externas.
* `/scripts_bd`: Scripts SQL (DDL y DML) para la creación, relación y llenado de la base de datos.
* `/etl_python`: Scripts de limpieza, normalización de datos y el Algoritmo de Puntuación Estratégica.
* `/visualizaciones`: Código fuente de las gráficas analíticas e imágenes finales exportadas.
* `/documentacion`: Diagramas Entidad-Relación (ER), esquemas conceptuales y documentos corporativos administrativos.

## Metodología Destacada: Análisis Estratégico (Batalla Legendaria)
Para determinar el equipo óptimo capaz de derrotar al Pokémon Legendario (Arceus), este proyecto descarta el uso de modelos predictivos de caja negra en favor de un **Algoritmo de Puntuación Ponderada** determinista y transparente. El modelo evalúa:
1. Multiplicadores matemáticos de ventaja y desventaja de tipo.
2. Diferenciales de estadísticas base (ej. Ataque del retador vs. Defensa de Arceus).
3. Probabilidad estadística de victoria basada en el rendimiento combinado del equipo.

## Instrucciones de Despliegue
1. Ejecutar los scripts ubicados en `/etl_python` para limpiar y preparar los datos del archivo inicial.
2. Importar y ejecutar los archivos de `/scripts_bd` en un servidor MySQL local para estructurar la base de datos e insertar la información.
3. Ejecutar los scripts de `/visualizaciones` (previamente conectados a las credenciales locales de MySQL) para generar el análisis gráfico.