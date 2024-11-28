import streamlit as st
import sqlite3
import pandas as pd

# Function to add data to the database
def add_entry(MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords):
    conn = sqlite3.connect("inputPLAN_B.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Bibliografia (MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords))
    conn.commit()
    conn.close()

# The main part of the application
st.title("Bibliography: Adding data to a SQLite database")

# Data entry form
with st.form("entry_form"):
    st.header("Add new publication")

    MitigationName = st.text_input("Name of the mitigation activity or solution.", max_chars=255)
    Type = st.text_input("Category (e.g., environmental, regulatory, social, planning, technological).", max_chars=255)
    Subtype = st.text_input("Specific subcategory under the primary type.", max_chars=255)
    ScaleOfImplementation = st.selectbox("Scale of Implementation", ["Local", "National", "Global"])
    ImpactOnLightPollution = st.selectbox("Impact on Light Pollution", ["High", "Moderate", "Minimal", "None"])
    ImpactOnNoisePollution = st.selectbox("Impact on Noise Pollution", ["High", "Moderate", "Minimal", "None"])
    CauseOfPollutionAddressed = st.text_input("Primary causes the measure targets (e.g., traffic, industry, urban lighting).", max_chars=255)
    AdditionalPollutionImpacts = st.text_input("Secondary effects (e.g., air pollution, heat).", max_chars=255)
    Keywords = st.text_input("Relevant keywords for categorization and indexing.")

    # Button to submit form
    submitted = st.form_submit_button("Add publication")

    if submitted:
        if MitigationName and Type and Subtype and ScaleOfImplementation and ImpactOnLightPollution and ImpactOnNoisePollution and CauseOfPollutionAddressed and AdditionalPollutionImpacts and Keywords:
            try:
                add_entry(MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords)
                st.success("The publication has been successfully added to the database.")
            except Exception as e:
                st.error(f"An error occurred while adding data: {e}")
        else:
            st.warning("Please fill in all fields of the form.")

# Podgląd zawartości bazy danych
if st.checkbox("Show database contents"):
    conn = sqlite3.connect("inputPLAN_B.db")
    df = pd.read_sql_query("SELECT * FROM Bibliografia", conn)
    conn.close()
    st.write(df)