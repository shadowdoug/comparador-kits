import pandas as pd
import streamlit as st

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha seu arquivo Excel do GEDmatch", type="xlsx")

if uploaded_file is not None:
    # Lê o arquivo, pula as 41 primeiras linhas
    df = pd.read_excel(uploaded_file, skiprows=41, header=None)

    # Define o cabeçalho
    df.columns = [
        "Nada", "N", "KIT", "Nome", "Nada2", "Nada3", "Nada4", "Nada5",
        "Total cM", "Maior Seg", "Gen", "Nada6", "Nada7", "Nada8",
        "Lab.", "Nada9", "Nada10", "Mt-X", "Y"
    ]

    # Remove colunas com prefixo 'Nada'
    df = df.loc[:, ~df.columns.str.startswith("Nada")]

    # Carrega o comparativo
    kits_base = pd.read_excel("KITS.xlsx")
    df["KIT"] = df["KIT"].astype(str).str.strip()
    kits_base["KIT"] = kits_base["KIT"].astype(str).str.strip()

    # Faz a junção apenas dos kits que existem nos dois
    df_merged = pd.merge(df, kits_base, on="KIT", how="inner")

    # Filtro de Total cM >= 1
    df_merged["Total cM"] = pd.to_numeric(df_merged["Total cM"], errors="coerce")
    df_merged = df_merged[df_merged["Total cM"] >= 1]

    # Remove NaN
    df_merged = df_merged.fillna("")

    # Exibe tabela
    st.write("🔍 Resultados encontrados:")
    st.dataframe(df_merged)

    # Permite baixar CSV
    csv = df_merged.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar resultado como CSV", data=csv, file_name="resultado.csv", mime="text/csv")
