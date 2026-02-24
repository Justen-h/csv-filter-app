import streamlit as st
import pandas as pd
import io

st.title("The Shredder")
st.subheader("Jouw partner om moeiteloos onnodige kolommen uit grote CSV-bestanden te slopen.")

uploaded_file = st.file_uploader("Upload een CSV-bestand", type="csv")

if uploaded_file:
    # Check bestandsgrootte (bijv. max 500MB)
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    if file_size_mb > 500:
        st.error(f"Bestand is te groot ({file_size_mb:.1f} MB). De limiet is ongeveer 600 MB op deze server.")
    else:
        # ALLES hieronder moet ingesprongen zijn (onder de 'else')
        
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
                
                # Zorg dat we bij het begin van het geüploade bestand beginnen
                uploaded_file.seek(0)
                
                try:
                    # Gebruik usecols om alleen de nodige data in het geheugen te laden
                    reader = pd.read_csv(uploaded_file, chunksize=chunksize, usecols=keep_columns)
                    
                    for i, chunk in enumerate(reader):
                        header = (i == 0)
                        chunk.to_csv(output, index=False, header=header, mode='a' if i > 0 else 'w')
                    
                    processed_data = output.getvalue()
                    
                    st.success("Bestand is klaar voor download!")
                    
                    st.download_button(
                        label="Download gefilterd CSV-bestand",
                        data=processed_data,
                        file_name="filtered_output.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Er is iets misgegaan tijdens het verwerken: {e}")
