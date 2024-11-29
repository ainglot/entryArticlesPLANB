import streamlit as st
import psycopg2
import pandas as pd

# Function to add data to the database
def add_entry(MitigationName, TypeM, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution,
              CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords, AlignmentWithLandUsePlanning,
              IntegrationIntoEcologicalNetworks, Feasibility, RelevantRegulations, RegulatoryChallenges,
              StakeholderAlignment, CommunityEngagementLevel, BehavioralChangePotential, SocioeconomicBenefits,
              TechnologicalSolutionUsed, AutomationPotential, InnovativeAspects, DataDrivenTools, ImpactOnBiodiversity,
              ResilienceToClimateChange, PotentialAdverseEffects, CoBenefits, CostRange, Timeframe, AssessmentMethod,
              ValidationIndicators):

    # Połącz się z bazą danych Supabase
    conn = get_connection()
    cursor = conn.cursor()

    # Wstaw dane do tabeli Mitigation
    cursor.execute("""
    INSERT INTO Mitigation (
        MitigationName, TypeM, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution,
        CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords, AlignmentWithLandUsePlanning,
        IntegrationIntoEcologicalNetworks, Feasibility, RelevantRegulations, RegulatoryChallenges,
        StakeholderAlignment, CommunityEngagementLevel, BehavioralChangePotential, SocioeconomicBenefits,
        TechnologicalSolutionUsed, AutomationPotential, InnovativeAspects, DataDrivenTools, ImpactOnBiodiversity,
        ResilienceToClimateChange, PotentialAdverseEffects, CoBenefits, CostRange, Timeframe, AssessmentMethod,
        ValidationIndicators
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        MitigationName, TypeM, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution,
        CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords, AlignmentWithLandUsePlanning,
        IntegrationIntoEcologicalNetworks, Feasibility, RelevantRegulations, RegulatoryChallenges,
        StakeholderAlignment, CommunityEngagementLevel, BehavioralChangePotential, SocioeconomicBenefits,
        TechnologicalSolutionUsed, AutomationPotential, InnovativeAspects, DataDrivenTools, ImpactOnBiodiversity,
        ResilienceToClimateChange, PotentialAdverseEffects, CoBenefits, CostRange, Timeframe, AssessmentMethod,
        ValidationIndicators
    ))

    conn.commit()
    cursor.close()
    conn.close()
    st.success("Data added successfully to Supabase!")


# Function to establish a connection to Supabase PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )


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

# 1. Data entry form outside the form block
st.header("1. Mitigation/Prevention Measure Details")

MitigationName = text_input_with_none("Name of the mitigation activity or solution.", max_chars=255)
TypeM = text_input_with_none("Category (e.g., environmental, regulatory, social, planning, technological).", max_chars=255)
Subtype = text_input_with_none("Specific subcategory under the primary type.", max_chars=255)
ScaleOfImplementation = selectbox_with_custom_input("Scale of Implementation", ["Local", "National", "Global"], key="other_scale_of_implementation")
ImpactOnLightPollution = selectbox_with_custom_input("Impact on Light Pollution", ["High", "Moderate", "Minimal", "None"], key="other_impact_on_light_pollution")
ImpactOnNoisePollution = selectbox_with_custom_input("Impact on Noise Pollution", ["High", "Moderate", "Minimal", "None"], key="other_impact_on_noise_pollution")
CauseOfPollutionAddressed = text_input_with_none("Primary causes the measure targets (e.g., traffic, industry, urban lighting).", max_chars=255)
AdditionalPollutionImpacts = text_input_with_none("Secondary effects (e.g., air pollution, heat).", max_chars=255)
Keywords = text_input_with_none("Relevant keywords for categorization and indexing.")

# 2. Additional section: Planning and Design Considerations
st.header("2. Planning and Design Considerations")

AlignmentWithLandUsePlanning = text_input_with_none("Alignment with Land Use Planning.")
IntegrationIntoEcologicalNetworks = text_input_with_none("Integration into Ecological Networks.")
Feasibility = text_input_with_none("Feasibility.")

# 3. Additional section: Regulatory and Compliance
st.header("3. Regulatory and Compliance")

RelevantRegulations = text_input_with_none("Applicable legal frameworks and guidelines (e.g., EU Directive 2002/49/WE).")
RegulatoryChallenges = text_input_with_none("Potential obstacles in legal or policy implementation.")
StakeholderAlignment = text_input_with_none("Alignment with community, governmental, or business interests.")

# 4. Additional section: Social and Behavioural Aspects
st.header("4. Social and Behavioural Aspects")

CommunityEngagementLevel = text_input_with_none("Requirement for public awareness campaigns or participation.")
BehavioralChangePotential = text_input_with_none("Likelihood of inducing long-term behavioral changes.")
SocioeconomicBenefits = text_input_with_none("Additional benefits for the community, such as improved health or aesthetics.")

# 5. Additional section: Technological Implementation
st.header("5. Technological Implementation")

TechnologicalSolutionUsed = text_input_with_none("Specific technology (e.g., dimming systems, noise barriers).")
AutomationPotential = text_input_with_none("Degree of automation and real-time adaptability.")
InnovativeAspects = text_input_with_none("New technologies or improvements introduced.")
DataDrivenTools = text_input_with_none("Use of GIS mapping, real-time monitoring, or predictive modelling.")

# 6. Additional section: Environmental Impact and Co-Benefits
st.header("6. Environmental Impact and Co-Benefits")

ImpactOnBiodiversity = text_input_with_none("Expected improvements in habitat quality or connectivity.")
ResilienceToClimateChange = text_input_with_none("Contribution to climate adaptation or mitigation.")
PotentialAdverseEffects = text_input_with_none("Negative impacts, if any, on local ecosystems.")
CoBenefits = text_input_with_none("Additional benefits like carbon sequestration, aesthetic improvements.")

# 7. Additional section: Cost, Implementation, and Validation
st.header("7. Cost, Implementation, and Validation")

CostRange = text_input_with_none("Estimated cost for local, national, or global implementation.")
Timeframe = text_input_with_none("Approximate time required for implementation.")
AssessmentMethod = text_input_with_none("Methodology to measure success (e.g., EIA, noise mapping, biodiversity surveys).")
ValidationIndicators = text_input_with_none("Key performance indicators to assess effectiveness.")


# Submit button
if st.button("Send to base"):
    # if any([MitigationName, TypeM, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution, CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords]):
    if any([MitigationName , 	TypeM , 	Subtype , 	ScaleOfImplementation , 	ImpactOnLightPollution , 	ImpactOnNoisePollution , 	CauseOfPollutionAddressed , 	AdditionalPollutionImpacts , 	Keywords , 	AlignmentWithLandUsePlanning , 	IntegrationIntoEcologicalNetworks , 	Feasibility , 	RelevantRegulations , 	RegulatoryChallenges , 	StakeholderAlignment , 	CommunityEngagementLevel , 	BehavioralChangePotential , 	SocioeconomicBenefits , 	TechnologicalSolutionUsed , 	AutomationPotential , 	InnovativeAspects , 	DataDrivenTools , 	ImpactOnBiodiversity , 	ResilienceToClimateChange , 	PotentialAdverseEffects , 	CoBenefits , 	CostRange , 	Timeframe , 	AssessmentMethod , 	ValidationIndicators]):
        try:
            add_entry(MitigationName , 	TypeM , 	Subtype , 	ScaleOfImplementation , 	ImpactOnLightPollution , 	ImpactOnNoisePollution , 	CauseOfPollutionAddressed , 	AdditionalPollutionImpacts , 	Keywords , 	AlignmentWithLandUsePlanning , 	IntegrationIntoEcologicalNetworks , 	Feasibility , 	RelevantRegulations , 	RegulatoryChallenges , 	StakeholderAlignment , 	CommunityEngagementLevel , 	BehavioralChangePotential , 	SocioeconomicBenefits , 	TechnologicalSolutionUsed , 	AutomationPotential , 	InnovativeAspects , 	DataDrivenTools , 	ImpactOnBiodiversity , 	ResilienceToClimateChange , 	PotentialAdverseEffects , 	CoBenefits , 	CostRange , 	Timeframe , 	AssessmentMethod , 	ValidationIndicators)
            st.success("Added notification to the base.")
        except Exception as e:
            st.error(f"An error occurred while adding data: {e}")
    else:
        st.warning("Please fill in at least one field of the form.")

# Preview the contents of the database
if st.checkbox("Show database contents"):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM Mitigation", conn)
    conn.close()
    st.write(df)

