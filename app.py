import streamlit as st
import sqlite3
import pandas as pd

# Function to add data to the database
def add_entry(data):
    conn = sqlite3.connect("inputPLAN_B.db")
    cursor = conn.cursor()

    # Insert data with None values for empty fields
    cursor.execute("""
    INSERT INTO Bibliografia 
    (MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords, AlignmentWithLandUsePlanning, IntegrationIntoEcologicalNetworks, Feasibility) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    
    conn.commit()
    conn.close()

def text_input_with_none(label, max_chars=255, key=None):
    """Creates a Streamlit text field with a default value of None."""
    value = st.text_input(label, max_chars=max_chars, key=key)
    return value if value else None

def selectbox_with_custom_input(label, options, custom_option="Other", key=None):
    """Combines a selectbox with the ability to enter a custom value."""
    options_with_custom = options + [custom_option]
    selected_option = st.selectbox(label, options_with_custom, key=key)
    if selected_option == custom_option:
        custom_value = st.text_input(f"Please specify {label.lower()}", key=f"{key}_custom")
        return custom_value if custom_value else None
    return selected_option

# The main part of the application
st.title("Light and Noise Pollution Mitigation: Data Entry Application")

# Tabs for different forms
tab1, tab2 = st.tabs(["Mitigation/Prevention Measure", "Planning and Design Considerations"])

# Tab 1: Mitigation/Prevention Measure
with tab1:
    st.header("Mitigation/Prevention Measure Details")
    with st.form("entry_form1"):
        MitigationName = text_input_with_none("Name of the mitigation activity or solution.")
        Type = text_input_with_none("Category (e.g., environmental, regulatory, social, planning, technological).")
        Subtype = text_input_with_none("Specific subcategory under the primary type.")
        ScaleOfImplementation = selectbox_with_custom_input("Scale of Implementation", ["Local", "National", "Global"])
        ImpactOnLightPollution = selectbox_with_custom_input("Impact on Light Pollution", ["High", "Moderate", "Minimal", "None"])
        ImpactOnNoisePollution = selectbox_with_custom_input("Impact on Noise Pollution", ["High", "Moderate", "Minimal", "None"])
        CauseOfPollutionAddressed = text_input_with_none("Primary causes the measure targets.")
        AdditionalPollutionImpacts = text_input_with_none("Secondary effects (e.g., air pollution, heat).")
        Keywords = text_input_with_none("Relevant keywords for categorization and indexing.")

        submitted1 = st.form_submit_button("Send Mitigation Data to Base")

        if submitted1:
            data = (MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords, None, None, None)
            if any(data[:9]):  # Check if at least one required field is filled
                try:
                    add_entry(data)
                    st.success("Mitigation data added to the database.")
                except Exception as e:
                    st.error(f"An error occurred while adding data: {e}")
            else:
                st.warning("Please fill in at least one field of the form.")

# Tab 2: Planning and Design Considerations
with tab2:
    st.header("Planning and Design Considerations")
    with st.form("entry_form2"):
        AlignmentWithLandUsePlanning = text_input_with_none("Alignment with Land Use Planning.")
        IntegrationIntoEcologicalNetworks = text_input_with_none("Integration into Ecological Networks.")
        Feasibility = text_input_with_none("Feasibility.")

        submitted2 = st.form_submit_button("Send Planning Data to Base")

        if submitted2:
            data = (None, None, None, None, None, None, None, None, None, AlignmentWithLandUsePlanning, IntegrationIntoEcologicalNetworks, Feasibility)
            if any(data[9:]):  # Check if at least one required field is filled
                try:
                    add_entry(data)
                    st.success("Planning data added to the database.")
                except Exception as e:
                    st.error(f"An error occurred while adding data: {e}")
            else:
                st.warning("Please fill in at least one field of the form.")

# Preview the contents of the database
if st.checkbox("Show database contents"):
    conn = sqlite3.connect("inputPLAN_B.db")
    df = pd.read_sql_query("SELECT * FROM Bibliografia", conn)
    conn.close()
    st.write(df)
