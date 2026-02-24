import streamlit as st
import pandas as pd
import io

st.title("The Shredder")
st.subheader("Jouw partner om moeiteloos onnodige kolommen uit grote CSV-bestanden te slopen.")

uploaded_file = st.file_uploader("Upload een CSV-bestand", type="csv")

if uploaded_file:
    # 1. Lees kolommen in (slechts de eerste rij om geheugen te sparen)
    df_sample = pd.read_csv(uploaded_file, nrows=0)
    kolommen = df_sample.columns.tolist()
    
    # Reset de pointer direct na het lezen van de kolommen
    uploaded_file.seek(0)

    keep_columns = st.multiselect("Selecteer de kolommen die je wilt behouden", kolommen)

    if keep_columns:
        if st.button("Genereer gefilterd CSV-bestand"):
            # Maak een in-memory buffer aan
            output = io.StringIO()
            
            chunksize = 100000
            
            # Voortgangsbalk toevoegen (optioneel, maar fijn voor de gebruiker)
            progress_bar = st.progress(0)
            
            # Chunkwise verwerken
            try:
                # We gebruiken een generator om door het bestand te lopen
                reader = pd.read_csv(uploaded_file, chunksize=chunksize, usecols=keep_columns)
                
                for i, chunk in enumerate(reader):
                    # Schrijf naar de buffer
                    header = (i == 0)
                    chunk.to_csv(output, index=False, header=header, mode='a' if i > 0 else 'w')
                
                # Zet de cursor van de buffer weer naar het begin
                processed_data = output.getvalue()
                
                st.success("Bestand is klaar voor download!")
                
                st.download_button(
                    label="Download gefilterd CSV-bestand",
                    data=processed_data,
                    file_name="filtered_output.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Er is iets misgegaan: {e}")
