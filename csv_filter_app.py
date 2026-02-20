import streamlit as st
import pandas as pd
import tempfile
import os

st.title("The Shredder")
st.subheader("Jouw partner om moeiteloos onnodige kolommen uit grote CSV-bestanden te slopen.")


# Upload CSV-bestand
uploaded_file = st.file_uploader("Upload een CSV-bestand", type="csv")

# Verwerk bestand als het is geüpload
if uploaded_file:
    # Lees een klein stukje van het bestand in om kolommen te tonen
    df_sample = pd.read_csv(uploaded_file, nrows=1000)
    kolommen = df_sample.columns.tolist()

    # Kolommen selecteren
    keep_columns = st.multiselect("Selecteer de kolommen die je wilt behouden", kolommen)

    if keep_columns:
        if st.button("Genereer gefilterd CSV-bestand"):
            chunksize = 100000

            # Tijdelijk bestand aanmaken
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                output_file = tmp.name

            # Heropen het bestand (we moeten opnieuw beginnen bij begin)
            uploaded_file.seek(0)

            # Chunkwise verwerken
            with pd.read_csv(uploaded_file, chunksize=chunksize) as reader:
                for i, chunk in enumerate(reader):
                    chunk = chunk[keep_columns]
                    mode = 'w' if i == 0 else 'a'
                    header = i == 0
                    chunk.to_csv(output_file, mode=mode, index=False, header=header)

            # Laat download knop zien
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download gefilterd CSV-bestand",
                    data=f,
                    file_name="filtered_output.csv",
                    mime="text/csv"
                )

            # Opruimen na download
            os.remove(output_file)

