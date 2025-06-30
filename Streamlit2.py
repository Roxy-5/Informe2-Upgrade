import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Configuración de la página
st.set_page_config(
    page_title="Análisis Airbnb - Rocío Ramírez",
    page_icon="🏠",
    layout="wide"
)

# Función para cargar datos con caché
@st.cache_data
def load_calendar_data(usecols=None):
    """Cargar datos del calendario con caché para mejor rendimiento"""
    file_path = "calendar.csv"
    if not os.path.exists(file_path):
        file_path = "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/calendar.csv"
    return pd.read_csv(file_path, usecols=usecols, on_bad_lines='skip')

@st.cache_data
def load_listings_data(usecols=None):
    """Cargar datos de listings con caché para mejor rendimiento"""
    file_path = "listings.csv"
    if not os.path.exists(file_path):
        file_path = "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv"
    return pd.read_csv(file_path, usecols=usecols, on_bad_lines='skip')

st.title("Mi segundo informe para Upgrade")
st.image("https://raw.githubusercontent.com/Roxy-5/Informe1/main/images.jpg", use_container_width=True)
st.title("Cómo usar")
st.write("1. Clona este repositorio.")
st.write("2. Instale las dependencias necesarias.")
st.write("3. Ejecuta el proyecto.")
st.title("Autor")
st.write("Rocío Ramírez")
st.title("Proceso llevado a cabo para la limpieza y corrección:")
st.write("Se cargan los archivos CSV usando pd.read_csv() para on_bad_lines='skip' ignorar filas problemáticas.")
st.write("Se visualizan las primeras y últimas filas con df.head() y df.tail().")
st.write("Se revisa la estructura y tipos de datos con df.info(), df.dtypes, y df.describe().")
st.write("Se cuentan filas y columnas (df.shape).")
st.write("Se buscan duplicados con df.duplicated().sum().")
st.write("Se identifican columnas con valores nulos (df.isna().any(), df.isna().sum()).")
st.write("Se identifican columnas completamente nulas y se eliminan si es necesario.")
st.write("Se identifican columnas constantes (nunique() == 1) y de baja variabilidad (nunique() < 5).")
st.write("Se eliminan columnas irrelevantes, constantes, completamente nulas o con baja variabilidad.")
st.write("Se eliminan columnas específicas que no aportan valor al análisis (por ejemplo, ID, URL, descripciones, etc.).")
st.write("Se convierte la columna 'date' a tipo fecha (datetime).")
st.write("Se convierte la columna 'available' a tipo category.")
st.write("Se limpia la columna 'price' eliminando símbolos y convirtiéndola a float.")
st.write("Se rellenan valores nulos en columnas relevantes con ceros (fillna(0)), por ejemplo en 'host_name' y 'reviews_per_month'.")
st.write("Se eliminan filas donde el precio es menor o igual a cero (df = df.loc[df['price'] > 0]).")
st.write("Se revisa el DataFrame resultante con df.info(), df.describe(), y se comprueba que no quedan valores nulos importantes.")
st.write("Se revisa la forma final del DataFrame (df.shape).")
st.write("Se crean nuevas columnas si es necesario (por ejemplo, 'month').")
st.write("Se agrupan y resumen datos para análisis exploratorio y visualización.")

st.subheader("¿Qué se corrige en este proceso? :")
st.write("Errores de lectura (filas corruptas).")
st.write("Tipos de datos incorrectos (fechas, precios, categorías).")
st.write("Columnas innecesarias o problemáticas (constantes, nulas, irrelevantes).")
st.write("Valores nulos (relleno o eliminación).")
st.write("Registros no válidos (precios negativos o cero).")
st.write("Duplicados.")
st.write("Preparación para análisis (columnas nuevas, agrupaciones).")

st.title("Respuestas a las preguntas del cliente:")
st.subheader("1. ¿Cómo varían los precios promedio por vecindario a lo largo del tiempo?")

# Cargar solo las columnas necesarias usando las funciones optimizadas
try:
    calendar = load_calendar_data(usecols=['listing_id', 'date', 'price'])
    listings = load_listings_data(usecols=['id', 'neighbourhood_cleansed'])
except Exception as e:
    st.error(f"Error cargando los datos: {e}")
    st.stop()
# Limpiar y convertir tipos
calendar['price'] = calendar['price'].astype(str).str.replace(r'[^\d.]', '', regex=True).astype(float)
calendar['date'] = pd.to_datetime(calendar['date'], errors='coerce')
# Unir los datasets
df = pd.merge(calendar, listings, left_on='listing_id', right_on='id', how='left')
# Agrupar por vecindario y fecha, y calcular el precio promedio
precios_por_vecindario = df.groupby(['neighbourhood_cleansed', 'date'])['price'].mean().reset_index()
# Selecciona algunos vecindarios para graficar
vecindarios = precios_por_vecindario['neighbourhood_cleansed'].unique()[:5]
fig, ax = plt.subplots(figsize=(14, 7))
for barrio in vecindarios:
    datos_barrio = precios_por_vecindario[precios_por_vecindario['neighbourhood_cleansed'] == barrio]
    ax.plot(datos_barrio['date'], datos_barrio['price'], label=barrio)
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio promedio')
ax.set_title('Evolución del precio promedio por vecindario')
ax.legend()
plt.tight_layout()
# Mostrar el gráfico en Streamlit
st.pyplot(fig)

st.subheader("2. ¿Qué listados tienen la mayor disponibilidad y cómo se relaciona esto con su precio?")
# 1. Cargar el calendar solo con las columnas necesarias
calendar = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/calendar.csv",
    usecols=['listing_id', 'available', 'price'],
    on_bad_lines='skip'
)
# 2. Limpiar y convertir tipos
calendar['price'] = calendar['price'].astype(str).str.replace(r'[^\d.]', '', regex=True).astype(float)
# 3. Calcular disponibilidad total y precio promedio por anuncio
disponibilidad = calendar.groupby('listing_id')['available'].apply(lambda x: (x == 't').sum())
precio_promedio = calendar.groupby('listing_id')['price'].mean()
# 4. Unir ambos resultados en un DataFrame
df_disp_precio = pd.DataFrame({
    'disponibilidad': disponibilidad,
    'precio_promedio': precio_promedio
}).reset_index()
# 5. Eliminar outliers de precio_promedio usando IQR
Q1 = df_disp_precio['precio_promedio'].quantile(0.25)
Q3 = df_disp_precio['precio_promedio'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
df_disp_precio = df_disp_precio[
    (df_disp_precio['precio_promedio'] >= limite_inferior) &
    (df_disp_precio['precio_promedio'] <= limite_superior)
]
# 6. Mostrar los anuncios con mayor disponibilidad
st.write("Top 10 anuncios con mayor disponibilidad")
st.dataframe(df_disp_precio.sort_values('disponibilidad', ascending=False).head(10))

# 7. Relación entre disponibilidad y precio promedio (gráfico)
fig, ax = plt.subplots(figsize=(12,7))
sns.kdeplot(
    x=df_disp_precio['disponibilidad'],
    y=df_disp_precio['precio_promedio'],
    fill=True, cmap='viridis', thresh=0.05, ax=ax
)
ax.set_xlabel('Días disponibles')
ax.set_ylabel('Precio promedio')
ax.set_title('Densidad KDE de disponibilidad y precio promedio')
st.pyplot(fig)
st.write("Hay muchos anuncios con diferentes combinaciones de días disponibles y precios promedio.")

with st.expander("PowerBI"):
    st.subheader("Dashboard PowerBI")
    st.write("Puedes ver el dashboard interactivo en PowerBI haciendo clic en el botón de abajo:")
    
    # Crear un botón más llamativo con HTML y CSS
    st.markdown("""
    <style>
    .powerbi-button {
        display: inline-block;
        background-color: #F2C811;
        color: #323130;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin: 10px 0;
        border: 2px solid #F2C811;
        transition: all 0.3s ease;
    }
    .powerbi-button:hover {
        background-color: #323130;
        color: #F2C811;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.subheader("3. ¿Existen patrones de precios en función de las características de los listados (tipo de habitaciones, tipo de propiedad, etc.)?")
# Cargar solo las columnas relevantes
listings = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv",
    usecols=['id', 'room_type', 'property_type', 'bedrooms', 'beds', 'price'],
    on_bad_lines='skip'
)
# Limpiar el precio y manejar vacíos
listings['price'] = (
    listings['price']
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .replace('', np.nan)
    .astype(float)
)
# Eliminar nulos en columnas clave
listings = listings.dropna(subset=['price', 'room_type', 'property_type', 'bedrooms', 'beds'])
# Quitar outliers de price, bedrooms y beds usando IQR
for col in ['price', 'bedrooms', 'beds']:
    Q1 = listings[col].quantile(0.25)
    Q3 = listings[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    listings = listings[(listings[col] >= limite_inferior) & (listings[col] <= limite_superior)]
# Boxplot: precio según tipo de habitación
fig1, ax1 = plt.subplots(figsize=(10,6))
sns.boxplot(x='room_type', y='price', data=listings, ax=ax1)
ax1.set_title('Precio según tipo de habitación')
st.pyplot(fig1)
# Relación entre número de habitaciones y precio
fig2, ax2 = plt.subplots(figsize=(8,6))
sns.scatterplot(x='bedrooms', y='price', data=listings, alpha=0.5, ax=ax2)
ax2.set_title('Precio vs. número de habitaciones')
st.pyplot(fig2)
st.subheader("4. ¿Qué vecindarios tienen los listados con las mejores reseñas?")
# Cargar solo las columnas necesarias
listings = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv",
    usecols=['neighbourhood_cleansed', 'review_scores_rating'],
    on_bad_lines='skip'
)
# Eliminar nulos en la puntuación
listings = listings.dropna(subset=['review_scores_rating'])
# Calcular el promedio de puntuación por vecindario
mejores_vecindarios = listings.groupby('neighbourhood_cleansed')['review_scores_rating'].mean().sort_values(ascending=False)
# Mostrar los 10 mejores en Streamlit
st.write("Top 10 vecindarios mejor valorados")
st.dataframe(mejores_vecindarios.head(10).reset_index())

st.subheader("5. ¿Qué vecindarios son los más baratos?")
# Cargar solo las columnas necesarias
listings = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv",
    usecols=['neighbourhood_cleansed', 'price'],
    on_bad_lines='skip'
)
# Limpiar el precio
listings['price'] = (
    listings['price']
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .replace('', np.nan)  # Cambiado a np.nan
    .astype(float)
)
# Eliminar nulos
listings = listings.dropna(subset=['price'])
# Calcular el precio promedio por vecindario
vecindarios_baratos = listings.groupby('neighbourhood_cleansed')['price'].mean().sort_values().head(10)
st.write("Top 10 vecindarios más baratos (precio promedio)")
st.dataframe(vecindarios_baratos.reset_index())

st.subheader("6. ¿Qué listados tienen la mayor cantidad de reseñas y cómo se relaciona esto con su precio?")
# Cargar las columnas necesarias
listings = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv",
    usecols=['id', 'number_of_reviews', 'price'],
    on_bad_lines='skip'
)
# Limpiar el precio
listings['price'] = (
    listings['price']
    .astype(str)
    .str.replace(r'[^\d.]', '', regex=True)
    .replace('', np.nan)
    .astype(float)
)
# Eliminar nulos
listings = listings.dropna(subset=['price', 'number_of_reviews'])
# Quitar outliers de price y number_of_reviews usando IQR
for col in ['price', 'number_of_reviews']:
    Q1 = listings[col].quantile(0.25)
    Q3 = listings[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    listings = listings[(listings[col] >= limite_inferior) & (listings[col] <= limite_superior)]
# Top 10 listados con más reseñas
top_reviews = listings.sort_values('number_of_reviews', ascending=False).head(10)
st.write("Top 10 listados con más reseñas")
st.dataframe(top_reviews[['id', 'number_of_reviews', 'price']])
# Relación entre cantidad de reseñas y precio (gráfico)
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x='number_of_reviews', y='price', data=listings, alpha=0.5, ax=ax)
ax.set_xlabel('Número de reseñas')
ax.set_ylabel('Precio')
ax.set_title('Relación entre número de reseñas y precio')
st.pyplot(fig)
st.write("Los de precio moderado.")

st.subheader("7. ¿Existen listados con muchas reseñas pero precios bajos o altos? ¿Qué podría significar esto?")
st.write("A que los huéspedes prefieran alojamientos accesibles, con buena ubicación, calidad-precio y mejor experiencia del usuario. La popularidad no depende solo del precio.")

st.subheader("8. ¿Cómo afecta la disponibilidad de un listado (en el calendario) a la cantidad de reseñas que recibe?")
# 1. Cargar y procesar la disponibilidad
calendar = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/calendar.csv",
    usecols=['listing_id', 'available'],
    on_bad_lines='skip'
)
# Calcular días disponibles por anuncio
disponibilidad = calendar.groupby('listing_id')['available'].apply(lambda x: (x == 't').sum()).reset_index()
disponibilidad.rename(columns={'available': 'dias_disponibles'}, inplace=True)
# 2. Cargar las reseñas por anuncio
listings = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv",
    usecols=['id', 'number_of_reviews'],
    on_bad_lines='skip'
)
listings.rename(columns={'id': 'listing_id'}, inplace=True)
# 3. Unir ambos DataFrames
df = pd.merge(disponibilidad, listings, on='listing_id')
# Quitar outliers de dias_disponibles y number_of_reviews usando IQR
for col in ['dias_disponibles', 'number_of_reviews']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    df = df[(df[col] >= limite_inferior) & (df[col] <= limite_superior)]
# 4. Gráfico de dispersión tipo hexbin
fig, ax = plt.subplots(figsize=(10,6))
hb = ax.hexbin(df['dias_disponibles'], df['number_of_reviews'], gridsize=30, cmap='viridis', mincnt=1)
cb = fig.colorbar(hb, ax=ax)
cb.set_label('Cantidad de anuncios')
ax.set_xlabel('Días disponibles al año')
ax.set_ylabel('Número de reseñas')
ax.set_title('Hexbin: Densidad de disponibilidad vs. número de reseñas')
st.pyplot(fig)
# 5. Correlación
correlacion = df['dias_disponibles'].corr(df['number_of_reviews'])
st.write(f"Correlación entre disponibilidad y número de reseñas: {correlacion:.2f}")
st.write("No afecta prácticamente nada porque la evaluación es muy débil (0.09). Que un anuncio esté disponible muchos días al año no garantiza que reciba más reseñas.")

st.subheader("9. ¿Cómo varía la disponibilidad a lo largo del año?")
# Cargar los datos necesarios
calendar = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/calendar.csv",
    usecols=['date', 'available'],
    on_bad_lines='skip'
)
calendar['date'] = pd.to_datetime(calendar['date'], errors='coerce')
# Crear columna de mes
calendar['month'] = calendar['date'].dt.month
# Calcular la disponibilidad media por mes
disponibilidad_mensual = calendar.groupby('month')['available'].apply(lambda x: (x == 't').mean())
# Graficar
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(disponibilidad_mensual.index, disponibilidad_mensual.values, marker='o')
ax.set_xticks(range(1,13))
ax.set_xticklabels(['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'])
ax.set_xlabel('Mes')
ax.set_ylabel('Proporción de días disponibles')
ax.set_title('Disponibilidad promedio por mes')
ax.grid(True)
st.pyplot(fig)

st.subheader("10. ¿Los anfitriones con más anuncios tienen mejores reseñas?")
# Cargar los datos necesarios
listings = pd.read_csv(
    "C:/Users/Rocio/Desktop/ROCÍO/Todo_rocío/Curso_Data_Analyst/Codes/temario/temario/Informe2-Upgrade/listings.csv",
    usecols=['host_id', 'id', 'review_scores_rating'],
    on_bad_lines='skip'
)
# Eliminar nulos en la puntuación
listings = listings.dropna(subset=['review_scores_rating'])
# Número de anuncios por anfitrión
anuncios_por_host = listings.groupby('host_id')['id'].count().reset_index(name='num_anuncios')
# Promedio de puntuación por anfitrión
rating_por_host = listings.groupby('host_id')['review_scores_rating'].mean().reset_index(name='rating_promedio')
# Unir ambos DataFrames
df_host = pd.merge(anuncios_por_host, rating_por_host, on='host_id')
# Quitar outliers de num_anuncios y rating_promedio usando IQR
for col in ['num_anuncios', 'rating_promedio']:
    Q1 = df_host[col].quantile(0.25)
    Q3 = df_host[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    df_host = df_host[(df_host[col] >= limite_inferior) & (df_host[col] <= limite_superior)]
# Gráfico de dispersión
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(df_host['num_anuncios'], df_host['rating_promedio'], alpha=0.5)
ax.set_xlabel('Número de anuncios por anfitrión')
ax.set_ylabel('Puntuación promedio de reseñas')
ax.set_title('¿Los anfitriones con más anuncios tienen mejores reseñas?')
ax.grid(True)
st.pyplot(fig)
st.write("No, tener muchos anuncios no garantiza mejores reseñas y la puntuación promedio suele ser alta (cerca de 5) para la mayoría de los anfitriones sin importar cuántos anuncios tengan.")

st.markdown(
        '<a href="https://app.powerbi.com/links/kvgg5F4oNt?ctid=8aebddb6-3418-43a1-a255-b964186ecc64&pbi_source=linkShare" class="powerbi-button" target="_blank">🚀 Ver Dashboard PowerBI</a>',
        unsafe_allow_html=True
    )

st.title("Hallazgos")
st.markdown("""
- La mayoría de los precios de los anuncios están concentrados en valores bajos, pero existen algunos anuncios con precios mucho más altos (valores atípicos)
- No hay una relación clara entre la cantidad de días disponibles de un anuncio y su precio promedio. La calificación es baja, lo que indica que los anuncios más caros no necesariamente están más (o menos) disponibles.
- El precio promedio varía entre vecindarios y a lo largo del tiempo. Algunos barrios mantienen precios más altos de forma constante, mientras que otros presentan más variabilidad.
- Los anuncios de tipo 'casa/apto entero' suelen tener precios más altos que los de 'habitación privada' o 'habitación compartida'.
- A mayor número de habitaciones, el precio tiende a ser más alto, aunque hay dispersión.")
- No existe una relación fuerte entre el número de reseñas y el precio del anuncio. Los anuncios con muchas reseñas pueden tener precios altos o bajos.
- La calificación entre la disponibilidad de un anuncio y el número de reseñas es baja (~0.09), lo que indica que no hay una relación directa entre cuántos días está disponible un anuncio y cuántas reseñas recibe.
- La proporción de días disponibles varía según el mes, mostrando cierta estacionalidad. Hay meses con mayor ocupación y otros con mayor disponibilidad.
- Algunos vecindarios tienen calificación promedio de reseñas más altas, lo que puede indicar mejor calidad percibida por los huéspedes.
- No se observa una tendencia clara: los anfitriones con más anuncios no necesariamente tienen mejores calificaciones promedio de reseñas.
""")

st.title("Recomendaciones estratégicas")
st.subheader("1. Ajuste Dinámico de Precios:")
st.write("El análisis muestra que los precios varían significativamente entre vecindarios y a lo largo del tiempo. Se recomienda implementar una estrategia de precios dinámica, ajustando tarifas según la demanda estacional y la competencia local para maximizar ingresos y ocupación.")
st.subheader("2. Promociones en Temporada Baja:")
st.write("La disponibilidad presenta estacionalidad, con meses de mayor y menor ocupación. Para reducir la vacancia en meses de baja demanda, es recomendable ofrecer descuentos, promociones o estancias mínimas flexibles, incentivando así las reservas en esos periodos.")
st.subheader("3. Diversificación de la Oferta:")
st.write("Los alojamientos completos tienen precios más altos, pero existe demanda de habitaciones privadas y compartidas. Diversificar el tipo de alojamiento permite captar distintos segmentos de clientes y aumentar la tasa de ocupación global.")
st.subheader("4. Enfoque en la Experiencia del Huésped:")
st.write("La puntuación de reseñas es alta en la mayoría de los anuncios, independientemente del número de propiedades gestionadas por el anfitrión. Mantener altos estándares de calidad, atención, personalizada y respuestas rápidas es clave para sostener y mejorar la reputación.")
st.subheader("5. Potenciar Anuncios con Buen Historial:")
st.write("Los anuncios con muchas reseñas generan mayor confianza. Es recomendable destacarlos en las estrategias de marketing y aprovechar su reputación para atraer nuevos huéspedes.")
st.subheader("6. Monitoreo Continuo de la Competencia:")
st.write("Dada la variabilidad de precios y ocupación por zona y temporada, es fundamental realizar un seguimiento periódico del mercado y ajustar la estrategia en función de los cambios detectados.")
st.subheader("7. Gestión Profesional para Anfitriones Multipropiedad:")
st.write("No se observa una relación directa entre el número de anuncios y la calidad de las reseñas. Los anfitriones con muchas propiedades deben apoyarse en herramientas de gestión y procesos estandarizados para asegurar una experiencia homogénea y de calidad en todos sus anuncios.")