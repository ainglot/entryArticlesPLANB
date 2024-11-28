import streamlit as st
import sqlite3
import pandas as pd

# Function to add data to the database
def add_entry(MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords):
    conn = sqlite3.connect("inputPLAN_B.db")
    cursor = conn.cursor()

    # Inserting data with support for None values
    cursor.execute(""" 
    INSERT INTO Bibliografia 
    (MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        MitigationName or None,  # If empty string, replace with None
        Type or None,
        Subtype or None,
        ScaleOfImplementation or None,
        ImpactOnLightPollution or None,
        ImpactOnNoisePollution or None,
        CauseOfPollutionAddressed or None,
        AdditionalPollutionImpacts or None,
        Keywords or None
    ))
    conn.commit()
    conn.close()


def text_input_with_none(label, max_chars=255, key=None):
    """Creates a Streamlit text field with a default value of None."""
    value = st.text_input(label, max_chars=max_chars, key=key)
    return value if value else None

def selectbox_with_custom_input(label, options, custom_option="Other", key=None):
    """
    A function that combines a selectbox and the ability to enter a custom value.
    
    Args:
    - label (str): The label for the selectbox.
    - options (list): A list of available options in the selectbox.
    - custom_option (str): An option that allows you to enter a custom value.
    - key (str): The key for the Streamlit component.
    
    Returns:
    - str: The value selected or entered by the user.
    """
    # Adding the option to enter a custom value to the list of options
    options_with_custom = options + [custom_option]

    # Selectbox to select values from a list or "Other" option
    selected_option = st.selectbox(label, options_with_custom, key=key)

    # If "Other" is selected, a text box appears for you to enter your own value
    if selected_option == custom_option:
        custom_key = f"{key}_custom"  # Creating a unique key for each custom input
        custom_value = st.text_input(f"Please specify {label.lower()}", key=custom_key)
        return custom_value if custom_value else None

    # If something is selected from the list, we return this value
    return selected_option

# The main part of the application
st.title("Light and Noise Pollution Mitigation: Adding data to a SQLite database")

# Data entry form outside the form block
st.header("Mitigation/Prevention Measure Details")

MitigationName = text_input_with_none("Name of the mitigation activity or solution.", max_chars=255)
Type = text_input_with_none("Category (e.g., environmental, regulatory, social, planning, technological).", max_chars=255)
Subtype = text_input_with_none("Specific subcategory under the primary type.", max_chars=255)
ScaleOfImplementation = selectbox_with_custom_input("Scale of Implementation", ["Local", "National", "Global"], key="other_scale_of_implementation")
ImpactOnLightPollution = selectbox_with_custom_input("Impact on Light Pollution", ["High", "Moderate", "Minimal", "None"], key="other_impact_on_light_pollution")
ImpactOnNoisePollution = selectbox_with_custom_input("Impact on Noise Pollution", ["High", "Moderate", "Minimal", "None"], key="other_impact_on_noise_pollution")
CauseOfPollutionAddressed = text_input_with_none("Primary causes the measure targets (e.g., traffic, industry, urban lighting).", max_chars=255)
AdditionalPollutionImpacts = text_input_with_none("Secondary effects (e.g., air pollution, heat).", max_chars=255)
Keywords = text_input_with_none("Relevant keywords for categorization and indexing.")

# Submit button
if st.button("Send to base"):
    if any([MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords]):
        try:
            add_entry(MitigationName, Type, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords)
            st.success("Added notification to the base.")
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
