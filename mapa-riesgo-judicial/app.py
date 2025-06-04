import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mapa de Riesgo Judicial", layout="wide")

st.title("⚖️ Mapa de Riesgo - Rama Judicial")
st.markdown("""
📄 **Instrucciones:** Sube un archivo Excel con tres columnas:
- `Riesgo`
- `Probabilidad` (Baja, Media, Alta)
- `Impacto` (Bajo, Medio, Alto)

Ejemplo:
| Riesgo | Probabilidad | Impacto |
|--------|--------------|---------|
| Corrupción interna | Alta probabilidad | Alto impacto |
""")

# Subida del archivo
archivo = st.file_uploader("📂 Carga tu archivo Excel", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)

        st.success("✅ Archivo cargado correctamente")
        st.markdown("Vista previa del archivo:")
        st.dataframe(df)

        # Validación de columnas necesarias
        columnas_esperadas = {"Riesgo", "Probabilidad", "Impacto"}
        if not columnas_esperadas.issubset(set(df.columns)):
            st.error("❌ El archivo debe tener las columnas: Riesgo, Probabilidad, Impacto")
        else:
            # Pesos para cálculo de puntajes
            pesos = {
                "Bajo impacto": 1,
                "Medio impacto": 2,
                "Alto impacto": 3,
                "Baja probabilidad": 1,
                "Media probabilidad": 2,
                "Alta probabilidad": 3
            }

            puntaje_total = 0
            asignaciones = []

            for _, row in df.iterrows():
                riesgo = row["Riesgo"]
                probabilidad = row["Probabilidad"]
                impacto = row["Impacto"]
                puntaje = pesos.get(probabilidad, 0) * pesos.get(impacto, 0)
                puntaje_total += puntaje
                asignaciones.append({
                    "⚠️ Riesgo": riesgo,
                    "📈 Probabilidad": probabilidad,
                    "📉 Impacto": impacto,
                    "🎯 Puntaje": puntaje
                })

            df_resultado = pd.DataFrame(asignaciones)
            st.markdown("---")
            st.subheader("📊 Resultado del Mapa de Riesgo")
            st.dataframe(df_resultado)
            st.success(f"🏁 **Puntaje total del mapa de riesgos:** {puntaje_total}")

            # Descargar el resultado como Excel
            st.download_button(
                label="📥 Descargar resultados en Excel",
                data=df_resultado.to_excel(index=False, engine='openpyxl'),
                file_name="resultado_mapa_riesgo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👈 Esperando que subas un archivo Excel válido...")
