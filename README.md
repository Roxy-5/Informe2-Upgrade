![](https://github.com/Roxy-5/Informe1/blob/main/images.jpg)

🛸 Informe2

Análisis de datos de la tabla.

🌍 Cómo usar

1. Clona este repositorio.
2. Instala las dependencias necesarias.
3. Ejecuta el proyecto.

🪐 Autor

Rocío Ramírez

🌌 Proceso llevado a cabo para la limpieza y corrección: 
- Se cargan los archivos CSV usando `pd.read_csv()` con `on_bad_lines='skip'` para ignorar filas problemáticas.
- Se visualizan las primeras y últimas filas con `df.head()` y `df.tail()`.
- Se revisa la estructura y tipos de datos con `df.info()`, `df.dtypes`, y `df.describe()`.
- Se cuentan filas y columnas (`df.shape`).
- Se buscan duplicados con `df.duplicated().sum()`.
- Se identifican columnas con valores nulos (`df.isna().any()`, `df.isna().sum()`).
- Se identifican columnas completamente nulas y se eliminan si es necesario.
- Se identifican columnas constantes (`nunique() == 1`) y de baja variabilidad (`nunique() < 5`).
- Se eliminan columnas irrelevantes, constantes, completamente nulas o con baja variabilidad.
- Se eliminan columnas específicas que no aportan valor al análisis (por ejemplo, IDs, URLs, descripciones, etc.).
- Se convierte la columna `'date'` a tipo fecha (`datetime`).
- Se convierte la columna `'available'` a tipo `category`.
- Se limpia la columna `'price'` eliminando símbolos y convirtiéndola a `float`.
- Se rellenan valores nulos en columnas relevantes con ceros (`fillna(0)`), por ejemplo en `'host_name'` y `'reviews_per_month'`.
- Se eliminan filas donde el precio es menor o igual a cero (`df = df.loc[df['price'] > 0]`).
- Se revisa el DataFrame resultante con `df.info()`, `df.describe()`, y se comprueba que no queden valores nulos importantes.
- Se revisa la forma final del DataFrame (`df.shape`).
- Se crean nuevas columnas si es necesario (por ejemplo, `'month'`).
- Se agrupan y resumen datos para análisis exploratorio y visualización.
- **¿Qué se corrige en este proceso?**:
  - **Errores de lectura** (filas corruptas).
  - **Tipos de datos incorrectos** (fechas, precios, categorías).
  - **Columnas innecesarias o problemáticas** (constantes, nulas, irrelevantes).
  - **Valores nulos** (relleno o eliminación).
  - **Registros no válidos** (precios negativos o cero).
  - **Duplicados**.
  - **Preparación para análisis** (columnas nuevas, agrupaciones).

🚀 Respuestas a las preguntas del cliente:

1. ¿Cómo varían los precios promedio por vecindario a lo largo del tiempo?
2. ¿Qué listados tienen la mayor disponibilidad y cómo se relaciona esto con su precio?
3. ¿Existen patrones de precios en función de las características de los listados (número de habitaciones, tipo de propiedad, etc.)?
4. ¿Qué vecindarios tienen los listados con las mejores reseñas (si hay una columna de puntuación)?
5. ¿Cómo se distribuyen los precios por vecindario y tipo de propiedad?
6. ¿Qué listados tienen la mayor cantidad de reseñas y cómo se relaciona esto con su precio?
7. ¿Existen listados con muchas reseñas pero precios bajos o altos? ¿Qué podría significar esto?
8. ¿Cómo afecta la disponibilidad de un listado (en el calendario) a la cantidad de reseñas que recibe?
9. ¿Existen patrones entre los precios, la disponibilidad y la cantidad de reseñas?

🌋 Hallazgos


🧭 Recomendaciones estratégicas



