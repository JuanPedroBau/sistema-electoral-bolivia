import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
from PIL import Image

# ----------------------
# 🔽 Aquí comienza tu sistema electoral
# ----------------------
def run_app():
    st.sidebar.success(f"Sesión iniciada como: {st.session_state.get('usuario', 'desconocido')}")

    st.title("🗳️ Sistema de Análisis Electoral - Bolivia")

    @st.cache_data
    def obtener_hojas():
        xls = pd.ExcelFile("data/analisis_electoral.xlsx")
        return xls.sheet_names

    @st.cache_data
    def cargar_hoja(nombre_hoja):
        return pd.read_excel("data/analisis_electoral.xlsx", sheet_name=nombre_hoja)

    hojas = obtener_hojas()
    hoja_seleccionada = st.selectbox("📁 Selecciona una hoja:", hojas)

    df = cargar_hoja(hoja_seleccionada)
    df.columns = df.columns.astype(str).str.strip().str.upper()

    st.subheader("👀 Vista previa de los datos")
    st.dataframe(df.head(10))

    # Detección automática de tipo de hoja
    is_resumen = "RESUMEN" in hoja_seleccionada.upper()
    is_por_departamento = "PORDEPARTAMENTO" in hoja_seleccionada.upper()
    is_general = "ELECCIONESGENERALES" in hoja_seleccionada.upper()

    st.markdown("---")
    st.subheader("📊 Análisis interactivo")

    if is_general:
        st.info("📋 Análisis por municipio / mesa")

        if "DEPARTAMENTO" in df.columns:
            departamento = st.selectbox("Departamento:", df['DEPARTAMENTO'].dropna().unique())
            df = df[df["DEPARTAMENTO"] == departamento]
        else:
            departamento = "Sin filtro"

        if "MUNICIPIO" in df.columns:
            municipio = st.selectbox("Municipio:", df['MUNICIPIO'].dropna().unique())
            df = df[df["MUNICIPIO"] == municipio]
        else:
            municipio = "Sin filtro"

        if "CIRCUNSCRIPCION" in df.columns:
            circunscripcion = st.selectbox("Circunscripción:", df['CIRCUNSCRIPCION'].dropna().unique())
            df = df[df["CIRCUNSCRIPCION"] == circunscripcion]
        else:
            circunscripcion = "Sin filtro"

        if "RECINTO" in df.columns:
            recinto = st.selectbox("Recinto:", df['RECINTO'].dropna().unique())
            df = df[df["RECINTO"] == recinto]
        else:
            recinto = "Sin filtro"

        excluir = ["VOTOS_BLANCOS", "VOTOS_NULOS", "VOTOS_VALIDOS", "VOTOS_EMITIDOS", "VOTOS_INSCRITOS"]
        columnas_partido = [
            col for col in df.columns
            if col.startswith("VOTOS_") and not any(exc in col.upper() for exc in excluir)
        ]

        df_suma = df[columnas_partido].sum().reset_index()
        df_suma.columns = ["PARTIDO", "VOTOS"]
        df_suma["PARTIDO"] = df_suma["PARTIDO"].str.replace("VOTOS_", "")

        fig = px.pie(df_suma, names="PARTIDO", values="VOTOS", title=f"Distribución de votos - {municipio}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_suma)

        # Exportar a PDF
        if st.button("📄 Exportar análisis a PDF"):
            img_buffer = io.BytesIO()
            fig.write_image(img_buffer, format="png")
            img_buffer.seek(0)

            # Crear gráfico con matplotlib
            fig_mpl, ax = plt.subplots(figsize=(6, 6))
            colors = plt.get_cmap('tab20')(range(len(df_suma)))
            ax.pie(df_suma["VOTOS"], labels=df_suma["PARTIDO"], autopct='%1.1f%%', startangle=90, colors=colors)
            ax.set_title(f"Distribución de votos - {municipio}", fontsize=12)
            plt.tight_layout()
            fig_mpl.savefig("grafico_temp.png")

            # Generar PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, f"Análisis Electoral - {municipio}", ln=True, align='C')
            pdf.set_font("Arial", "", 12)
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"Departamento: {departamento}\nMunicipio: {municipio}\nCircunscripción: {circunscripcion}\nRecinto: {recinto}")
            pdf.ln(5)

            pdf.set_font("Arial", "", 10)
            for _, row in df_suma.iterrows():
                votos = f"{int(row['VOTOS']):,}".replace(",", ".")
                pdf.cell(0, 8, f"{row['PARTIDO']}: {votos} votos", ln=True)

            pdf.ln(5)
            pdf.image("grafico_temp.png", x=30, w=100)
            pdf.output("analisis_exportado.pdf")

            st.success("✅ PDF generado: analisis_exportado.pdf")
            with open("analisis_exportado.pdf", "rb") as f:
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=f,
                    file_name="analisis_exportado.pdf",
                    mime="application/pdf"
                )

    elif is_resumen:
        st.info("📘 Análisis histórico comparativo nacional")
        partidos = st.multiselect("Selecciona partidos:", df['PARTIDO'].dropna().unique(), default=df['PARTIDO'].dropna().unique())
        tipo_valor = st.radio("Tipo de valor a graficar:", ["VOTOS", "PORCENTAJE"])
        df_filtrado = df[df['PARTIDO'].isin(partidos)].copy()
        df_filtrado.set_index('PARTIDO', inplace=True)
        columnas = [col for col in df_filtrado.columns if tipo_valor in col]
        fig = px.line(df_filtrado[columnas].T, title=f"Evolución histórica ({tipo_valor.lower()})")
        st.plotly_chart(fig, use_container_width=True)

    elif is_por_departamento:
        st.info("📍 Análisis por departamento")
        departamento = st.selectbox("Departamento:", df['DEPARTAMENTO'].dropna().unique())
        df_depto = df[df['DEPARTAMENTO'] == departamento]
        columnas_partido = [col for col in df.columns if col.startswith("VOTOS_") and col != 'VOTOS_VALIDOS']
        df_melt = df_depto.melt(id_vars="DEPARTAMENTO", value_vars=columnas_partido, var_name="PARTIDO", value_name="VOTOS")
        df_melt["PARTIDO"] = df_melt["PARTIDO"].str.replace("VOTOS_", "")
        fig = px.bar(df_melt, x="PARTIDO", y="VOTOS", color="PARTIDO", title=f"Votos por partido - {departamento}")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ Esta hoja no está clasificada como resumen, por departamento o general.")
