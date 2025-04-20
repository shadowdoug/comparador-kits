import pandas as pd
import streamlit as st

# Configura o layout para tela cheia
st.set_page_config(page_title="Comparador de KITS", layout="wide")

st.title("🔬 Comparador de KITS Genéticos")

# Upload do Excel
uploaded_file = st.file_uploader("📁 Faça upload do arquivo Excel copiado do GEDmatch", type="xlsx")

if uploaded_file is not None:
    # Lê o arquivo, pulando as 41 primeiras linhas
    df = pd.read_excel(uploaded_file, skiprows=41, header=None)

    # Define o cabeçalho correto
    df.columns = [
        "Nada", "N", "KIT", "Nome", "Nada2", "Nada3", "Nada4", "Nada5",
        "Total cM", "Maior Seg", "Gen", "Nada6", "Nada7", "Nada8",
        "Lab.", "Nada9", "Nada10", "Mt-X", "Y"
    ]

    # Remove colunas que começam com "Nada"
    df = df.loc[:, ~df.columns.str.startswith("Nada")]

    # Lê os KITS de comparação
    kits_base = pd.read_excel("KITS.xlsx")
    df["KIT"] = df["KIT"].astype(str).str.strip()
    kits_base["KIT"] = kits_base["KIT"].astype(str).str.strip()

    # Junta os dados apenas onde o KIT bate
    df_merged = pd.merge(df, kits_base, on="KIT", how="inner")

    # Filtro: Total cM >= 1
    df_merged["Total cM"] = pd.to_numeric(df_merged["Total cM"], errors="coerce")
    df_merged = df_merged[df_merged["Total cM"] >= 1]

    # Substitui NaN por string vazia
    df_merged = df_merged.fillna("")

    # Estilização para altura e largura da tabela
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
            .stDataFrame {
                height: 80vh !important;
                max-height: 80vh !important;
                overflow: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Exibe a tabela
    st.write("🔍 Resultados encontrados:")
    st.dataframe(df_merged, use_container_width=True)

    # Botão para baixar resultado como CSV
    csv = df_merged.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar resultado como CSV", data=csv, file_name="resultado.csv", mime="text/csv")

else:
    st.info("👆 Faça upload do arquivo para começar.")
