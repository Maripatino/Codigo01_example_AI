import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
st.set_page_config(
    page_title="EDA - Datos Climáticos",
    layout="wide"
)

st.title("🌦️ Análisis Exploratorio de Datos Climáticos")
st.write("Aplicación desarrollada con Streamlit.")

# -----------------------------
# CREAR DATOS SINTÉTICOS
# -----------------------------

st.sidebar.header("Configuración")

n = st.sidebar.slider(
    "Cantidad de registros",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

np.random.seed(42)

fechas = pd.date_range("2025-01-01", periods=n)

temperatura = np.random.normal(25, 5, n)
humedad = np.random.randint(40, 100, n)
viento = np.random.uniform(0, 40, n)
lluvia = np.random.uniform(0, 100, n)

estados = np.random.choice(
    ["Soleado", "Nublado", "Lluvioso"],
    size=n,
    p=[0.5, 0.3, 0.2]
)

df = pd.DataFrame({
    "Fecha": fechas,
    "Temperatura": temperatura,
    "Humedad": humedad,
    "Velocidad_Viento": viento,
    "Precipitacion": lluvia,
    "Estado_Clima": estados
})

# -----------------------------
# MOSTRAR DATOS
# -----------------------------

st.header("Datos Sintéticos")

st.dataframe(df.head(20))

# -----------------------------
# FILTRO
# -----------------------------

st.sidebar.subheader("Filtro")

estado = st.sidebar.multiselect(
    "Estado del clima",
    options=df["Estado_Clima"].unique(),
    default=df["Estado_Clima"].unique()
)

df_filtrado = df[df["Estado_Clima"].isin(estado)]

st.write("Registros filtrados:", len(df_filtrado))

# -----------------------------
# EDA CUALITATIVO
# -----------------------------

st.header("1. Variables Cualitativas")

st.write(df_filtrado["Estado_Clima"].value_counts())

fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(
    data=df_filtrado,
    x="Estado_Clima",
    ax=ax
)
ax.set_title("Frecuencia del Estado del Clima")
st.pyplot(fig)

# -----------------------------
# EDA CUANTITATIVO
# -----------------------------

st.header("2. Variables Cuantitativas")

st.write(df_filtrado.describe())

# -----------------------------
# MATRIZ DE CORRELACIÓN
# -----------------------------

st.header("3. Correlación")

fig, ax = plt.subplots(figsize=(7,5))

corr = df_filtrado.select_dtypes(include=np.number).corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# -----------------------------
# HISTOGRAMA
# -----------------------------

st.header("4. Histogramas")

variable = st.selectbox(
    "Seleccione una variable",
    [
        "Temperatura",
        "Humedad",
        "Velocidad_Viento",
        "Precipitacion"
    ]
)

fig, ax = plt.subplots(figsize=(7,4))

sns.histplot(
    df_filtrado[variable],
    kde=True,
    ax=ax
)

ax.set_title(f"Distribución de {variable}")

st.pyplot(fig)

# -----------------------------
# BOXPLOT
# -----------------------------

st.header("5. Boxplot")

fig, ax = plt.subplots(figsize=(7,4))

sns.boxplot(
    data=df_filtrado,
    x="Estado_Clima",
    y="Temperatura",
    ax=ax
)

st.pyplot(fig)

# -----------------------------
# SCATTER
# -----------------------------

st.header("6. Relación entre Variables")

fig, ax = plt.subplots(figsize=(7,5))

sns.scatterplot(
    data=df_filtrado,
    x="Temperatura",
    y="Humedad",
    hue="Estado_Clima",
    ax=ax
)

st.pyplot(fig)

# -----------------------------
# CONCLUSIONES
# -----------------------------

st.header("Conclusiones")

st.markdown("""
- Se generaron datos sintéticos del clima.
- Se realizó análisis descriptivo de variables cuantitativas.
- Se analizó la variable cualitativa Estado del Clima.
- Se muestran histogramas, boxplots, scatterplots y mapa de calor.
- El usuario puede interactuar modificando la cantidad de datos y filtrando el estado del clima.
""")
