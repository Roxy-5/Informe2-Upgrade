![](https://github.com/Roxy-5/Informe1/blob/main/images.jpg)

🛸 ### Informe2

Análisis de datos de la tabla.

🌍 **Cómo usar**

1. Clona este repositorio.
2. Instala las dependencias necesarias.
3. Ejecuta el proyecto.

🪐 **Autor**

Rocío Ramírez

🌌 **Proceso llevado a cabo para la limpieza y corrección:** 
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
  - Errores de lectura (filas corruptas).
  - Tipos de datos incorrectos (fechas, precios, categorías).
  - Columnas innecesarias o problemáticas (constantes, nulas, irrelevantes).
  - Valores nulos (relleno o eliminación).
  - Registros no válidos (precios negativos o cero).
  - Duplicados.
  - Preparación para análisis (columnas nuevas, agrupaciones).

🚀 **Respuestas a las preguntas del cliente:**

1. ¿Cómo varían los precios promedio por vecindario a lo largo del tiempo? ![image](https://github.com/user-attachments/assets/69dca9c4-4971-4e39-ae02-a140cadb03f9) 
2. ¿Qué listados tienen la mayor disponibilidad y cómo se relaciona esto con su precio? ![image](https://github.com/user-attachments/assets/01d22ac9-4bb8-4910-a522-c2157495e0c2) No hay relación clara.
3. ¿Existen patrones de precios en función de las características de los listados (tipo de habitaciones, tipo de propiedad, etc.)? ![image](https://github.com/user-attachments/assets/263e3ae0-60b5-4f12-ab50-e6c4f20594e4) ![image](https://github.com/user-attachments/assets/c8507327-0a00-4951-a172-48cf844efc6b)
4. ¿Qué vecindarios tienen los listados con las mejores reseñas (si hay una columna de puntuación)?:
Au-Haidhausen
Pasing-Obermenzing    
Sendling-Westpark         
Schwanthalerhöhe          
Schwabing-West             
Untergiesing-Harlaching   
Tudering-Riem              
Allach-Untermenzing       
Altstadt-Lehel            
Bogenhausen
5. ¿Qué vecindarios son los más baratos?:
Ramersdorf-Perlach            
Aubing-Lochhausen-Langwied 
Hadern                     
Tudering-Riem               
Allach-Untermenzing        
Milbertshofen-Am Hart       
Moosach                       
Pasing-Obermenzing           
Obergiesing                
Untergiesing-Harlaching 
6. ¿Qué listados tienen la mayor cantidad de reseñas y cómo se relaciona esto con su precio? ![image](https://github.com/user-attachments/assets/3c2d60bc-8acf-4fb8-af35-21f86785e477) Los de precio moderado.
7. ¿Existen listados con muchas reseñas pero precios bajos o altos? ¿Qué podría significar esto?: A que los huéspedes prefieren alojamientos accesibles, con buena ubicación, calidad-precio y mejor experiencia del usuario. La popularidad no depende solo del precio.
8. ¿Cómo afecta la disponibilidad de un listado (en el calendario) a la cantidad de reseñas que recibe? ![image](https://github.com/user-attachments/assets/bf260c6e-45b6-4d61-910e-d4b337bc24d2) No afecta prácticamente nada porque la correlación es muy débil (0.09). Que un anuncio esté disponible muchos días al año no garantiza que reciba más reseñas.
9. ¿Cómo varía la disponibilidad a lo largo del año? ![image](https://github.com/user-attachments/assets/cb346c8f-f286-417a-b82f-f4bf4a118c90)
10. ¿Los anfitriones con más anuncios tienen mejores reseñas? ![image](https://github.com/user-attachments/assets/a4c71678-b0da-4aa8-8d13-42a0ca01cfb7) No, tener muchos anuncios no garantiza mejores reseñas y la puntuación promedio suele ser alta (cerca de 5) para la mayoría de anfitriones sin importar cuántos anuncios tienen.

🌋 **Hallazgos**

- La mayoría de los precios de los anuncios están concentrados en valores bajos, pero existen algunos anuncios con precios mucho más altos (outliers).
- No hay una relación clara entre la cantidad de días disponibles de un anuncio y su precio promedio. La correlación es baja, lo que indica que los anuncios más caros no necesariamente están más (o menos) disponibles.
- El precio promedio varía entre vecindarios y a lo largo del tiempo. Algunos barrios mantienen precios más altos de forma constante, mientras que otros presentan más variabilidad.
- Los anuncios de tipo "entire home/apt" suelen tener precios más altos que los de "private room" o "shared room".
- A mayor número de habitaciones, el precio tiende a ser más alto, aunque hay dispersión.
- No existe una relación fuerte entre el número de reseñas y el precio del anuncio. Los anuncios con muchas reseñas pueden tener precios altos o bajos.
- La correlación entre la disponibilidad de un anuncio y el número de reseñas es baja (~0.09), lo que indica que no hay una relación directa entre cuántos días está disponible un anuncio y cuántas reseñas recibe.
- La proporción de días disponibles varía según el mes, mostrando cierta estacionalidad. Hay meses con mayor ocupación y otros con mayor disponibilidad.
- Algunos vecindarios tienen puntuaciones promedio de reseñas más altas, lo que puede indicar mejor calidad percibida por los huéspedes.
- No se observa una tendencia clara: los anfitriones con más anuncios no necesariamente tienen mejores puntuaciones promedio de reseñas.

🧭 **Recomendaciones estratégicas**

### 1. Ajuste Dinámico de Precios
El análisis muestra que los precios varían significativamente entre vecindarios y a lo largo del tiempo. Se recomienda implementar una estrategia de precios dinámica, ajustando tarifas según la demanda estacional y la competencia local para maximizar ingresos y ocupación.

### 2. Promociones en Temporada Baja
La disponibilidad presenta estacionalidad, con meses de mayor y menor ocupación. Para reducir la vacancia en meses de baja demanda, es recomendable ofrecer descuentos, promociones o estancias mínimas flexibles, incentivando así las reservas en esos periodos.

### 3. Diversificación de la Oferta
Los alojamientos completos tienen precios más altos, pero existe demanda para habitaciones privadas y compartidas. Diversificar el tipo de alojamiento permite captar distintos segmentos de clientes y aumentar la tasa de ocupación global.

### 4. Enfoque en la Experiencia del Huésped
La puntuación de reseñas es alta en la mayoría de los anuncios, independientemente del número de propiedades gestionadas por el anfitrión. Mantener altos estándares de calidad, atención personalizada y respuestas rápidas es clave para sostener y mejorar la reputación.

### 5. Potenciar Anuncios con Buen Historial
Los anuncios con muchas reseñas generan mayor confianza. Es recomendable destacarlos en las estrategias de marketing y aprovechar su reputación para atraer nuevos huéspedes.

### 6. Monitoreo Continuo de la Competencia
Dada la variabilidad de precios y ocupación por zona y temporada, es fundamental realizar un seguimiento periódico del mercado y ajustar la estrategia en función de los cambios detectados.

### 7. Gestión Profesional para Anfitriones Multipropiedad
No se observa una relación directa entre el número de anuncios y la calidad de las reseñas. Los anfitriones con muchas propiedades deben apoyarse en herramientas de gestión y procesos estandarizados para asegurar una experiencia homogénea y de calidad en todos sus anuncios.




