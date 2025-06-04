import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mapa de Riesgos por Rol", layout="wide")

# Datos base por rol
riesgos_data = {
    "🟦 Observador": [
        ("Intervención indebida en el proceso auditado", 3, 4),
        ("Incumplimiento de la confidencialidad", 2, 5),
        ("Falta de comprensión del propósito de la observación", 3, 3)
    ],
    "🟩 Auditor": [
        ("Juicio sesgado o poco objetivo", 3, 5),
        ("Falta de competencia técnica frente a normas específicas", 4, 4),
        ("Hallazgos mal documentados o ambiguos", 3, 4)
    ],
    "🟨 Coordinador de Auditoría": [
        ("Asignación de auditores sin competencia adecuada", 3, 5),
        ("Mala planificación del alcance de auditorías", 4, 4),
        ("Falta de seguimiento a acciones correctivas", 2, 5)
    ]
}

# Clasificación de niveles
def categorizar_riesgo(nivel):
    if nivel <= 6:
        return "✅ Bajo"
    elif nivel <= 9:
        return "🟡 Moderado"
    elif nivel <= 12:
        return "🟠 Alto"
    elif nivel <= 15:
        return "🔶 Muy alto"
    else:
        return "🔴 Crítico"

# Título principal
st.title("⚖️ Mapa de Riesgos por Rol")

puntaje_total = 0

# Mostrar tabla por cada rol
for rol, riesgos in riesgos_data.items():
    st.subheader(rol)
    riesgos_calculados = []
    for nombre, prob, impacto in riesgos:
        nivel = prob * impacto
        categoria = categorizar_riesgo(nivel)
        puntaje_total += nivel
        riesgos_calculados.append([nombre, prob, impacto, nivel, categoria])
    df = pd.DataFrame(riesgos_calculados, columns=["Riesgo", "📈 Probabilidad", "📉 Impacto", "🎯 Nivel", "🔍 Clasificación"])
    st.dataframe(df)

# Mostrar puntaje final
st.markdown("### 🧮 Puntaje Total de Riesgo")
st.info(f"Tu puntaje acumulado es: **{puntaje_total}**")

if puntaje_total >= 100:
    st.success("🎉 ¡Ganaste! Riesgo crítico identificado correctamente.")
else:
    st.warning("🧐 Sigue evaluando. Aún puedes identificar riesgos mayores.")

# Crear mapa de calor
st.markdown("---")
st.subheader("🔥 Mapa de Calor - Matriz de Riesgo")

matriz = []
for impacto in range(5, 0, -1):
    fila = []
    for prob in range(1, 6):
        nivel = prob * impacto
        emoji = categorizar_riesgo(nivel).split()[0]
        fila.append(f"{nivel} {emoji}")
    matriz.append(fila)

df_matriz = pd.DataFrame(matriz, index=[f"{i} (Impacto)" for i in range(5, 0, -1)],
                         columns=[f"{j} (Probabilidad)" for j in range(1, 6)])

st.dataframe(df_matriz, height=350)

        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("👈 Esperando que subas un archivo Excel válido...")
