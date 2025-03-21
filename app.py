import streamlit as st
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from supabase import create_client, Client
from datetime import datetime

def init_supabase_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def add_entry(MitigationName, TypeM, Subtype, ScaleOfImplementation, ImpactOnLightPollution, ImpactOnNoisePollution,
              CauseOfPollutionAddressed, AdditionalPollutionImpacts, Keywords, AlignmentWithLandUsePlanning,
              IntegrationIntoEcologicalNetworks, Feasibility, RelevantRegulations, RegulatoryChallenges,
              StakeholderAlignment, CommunityEngagementLevel, BehavioralChangePotential, SocioeconomicBenefits,
              TechnologicalSolutionUsed, AutomationPotential, InnovativeAspects, DataDrivenTools, ImpactOnBiodiversity,
              ResilienceToClimateChange, PotentialAdverseEffects, CoBenefits, CostRange, Timeframe, AssessmentMethod,
              ValidationIndicators):

    # Konfiguracja klienta Supabase
    supabase_url = "https://rxrsynefraehciczistw.supabase.co"  # Wstaw swój URL
    supabase_anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4cnN5bmVmcmFlaGNpY3ppc3R3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI4NTkzODcsImV4cCI6MjA0ODQzNTM4N30.SJ-fggQEkBI4Pbza1J_V68HQVjElrfhPE320rb6tc4Y"   # Wstaw swój klucz anon
    supabase = create_client(supabase_url, supabase_anon_key)

    # Dane do wstawienia
    data = {
        "mitigationname": MitigationName,
        "typem": TypeM,
        "subtype": Subtype,
        "scaleofimplementation": ScaleOfImplementation,
        "impactonlightpollution": ImpactOnLightPollution,
        "impactonnoisepollution": ImpactOnNoisePollution,
        "causeofpollutionaddressed": CauseOfPollutionAddressed,
        "additionalpollutionimpacts": AdditionalPollutionImpacts,
        "keywords": Keywords,
        "alignmentwithlanduseplanning": AlignmentWithLandUsePlanning,
        "integrationintoecologicalnetworks": IntegrationIntoEcologicalNetworks,
        "feasibility": Feasibility,
        "relevantregulations": RelevantRegulations,
        "regulatorychallenges": RegulatoryChallenges,
        "stakeholderalignment": StakeholderAlignment,
        "communityengagementlevel": CommunityEngagementLevel,
        "behavioralchangepotential": BehavioralChangePotential,
        "socioeconomicbenefits": SocioeconomicBenefits,
        "technologicalsolutionused": TechnologicalSolutionUsed,
        "automationpotential": AutomationPotential,
        "innovativeaspects": InnovativeAspects,
        "datadriventools": DataDrivenTools,
        "impactonbiodiversity": ImpactOnBiodiversity,
        "resiliencetoclimatechange": ResilienceToClimateChange,
        "potentialadverseeffects": PotentialAdverseEffects,
        "cobenefits": CoBenefits,
        "costrange": CostRange,
        "timeframe": Timeframe,
        "assessmentmethod": AssessmentMethod,
        "validationindicators": ValidationIndicators,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Insert data into Mitigation table
    try:
        response = supabase.table("mitigation").insert([data]).execute()
        if response.data:  # Success code for data insertion
            st.success("Data added successfully!")
        elif response.error_message:  # If an error has occurred
            print(f"Data insertion error: {response.error_message}")
        else:
            st.error(f"Failed to insert data: {response.json()}")
    except Exception as e:
        st.error(f"Error: {e}")

# Function to establish a connection to Supabase PostgreSQL
def get_connection():
    # Tworzymy URL połączenia dla SQLAlchemy
    db_url = f"postgresql://{st.secrets['database']['user']}:{st.secrets['database']['password']}@{st.secrets['database']['host']}:{st.secrets['database']['port']}/{st.secrets['database']['database']}"
    
    # Tworzymy obiekt engine z SQLAlchemy
    engine = create_engine(db_url)
    
    return engine


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
st.title("Light and Noise Pollution Mitigation: Adding Data to PostgreSQL Database")

# 1. Data entry form outside the form block
st.header("1. Mitigation/Prevention Measure Details")

MitigationName = text_input_with_none("Name of the mitigation activity or solution.", max_chars=255)
TypeM = text_input_with_none("Category (e.g., environmental, regulatory, social, planning, technological).", max_chars=1500) # Lista rozwijalna; opcja wyboru kilku; brak - do wyboru
Subtype = text_input_with_none("Specific subcategory under the primary type.", max_chars=1500) # Wpisany tekst
ScaleOfImplementation = selectbox_with_custom_input("Scale of Implementation", ["Local", "National", "Global", "None"], key="other_scale_of_implementation")
ImpactOnLightPollution = selectbox_with_custom_input("Impact on Light Pollution", ["High", "Moderate", "Minimal", "None"], key="other_impact_on_light_pollution")
ImpactOnNoisePollution = selectbox_with_custom_input("Impact on Noise Pollution", ["High", "Moderate", "Minimal", "None"], key="other_impact_on_noise_pollution")
CauseOfPollutionAddressed = text_input_with_none("Primary causes the measure targets (e.g., traffic, industry, urban lighting).", max_chars=5000) # Wpisanie tekstu
AdditionalPollutionImpacts = text_input_with_none("Secondary effects (e.g., air pollution, heat).", max_chars=5000) # Wpisanie tekstu
Keywords = text_input_with_none("Relevant keywords for categorization and indexing.", max_chars=5000) # Lista słów kluczowych; wybór więcej niż jednego (sklejenie do jednego pola za pomocą separatora średnika)

# 2. Additional section: Planning and Design Considerations
st.header("2. Planning and Design Considerations")

AlignmentWithLandUsePlanning = text_input_with_none("Alignment with Land Use Planning.", max_chars=10000) # ?
IntegrationIntoEcologicalNetworks = text_input_with_none("Integration into Ecological Networks.", max_chars=10000) # 
Feasibility = text_input_with_none("Feasibility.", max_chars=10000)

# 3. Additional section: Regulatory and Compliance
st.header("3. Regulatory and Compliance")

RelevantRegulations = text_input_with_none("Applicable legal frameworks and guidelines (e.g., EU Directive 2002/49/WE).", max_chars=10000)
RegulatoryChallenges = text_input_with_none("Potential obstacles in legal or policy implementation.", max_chars=10000)
StakeholderAlignment = text_input_with_none("Alignment with community, governmental, or business interests.", max_chars=10000)

# 4. Additional section: Social and Behavioural Aspects
st.header("4. Social and Behavioural Aspects")

CommunityEngagementLevel = text_input_with_none("Requirement for public awareness campaigns or participation.", max_chars=10000)
BehavioralChangePotential = text_input_with_none("Likelihood of inducing long-term behavioral changes.", max_chars=10000)
SocioeconomicBenefits = text_input_with_none("Additional benefits for the community, such as improved health or aesthetics.", max_chars=10000)

# 5. Additional section: Technological Implementation
st.header("5. Technological Implementation")

TechnologicalSolutionUsed = text_input_with_none("Specific technology (e.g., dimming systems, noise barriers).", max_chars=10000)
AutomationPotential = text_input_with_none("Degree of automation and real-time adaptability.", max_chars=10000)
InnovativeAspects = text_input_with_none("New technologies or improvements introduced.", max_chars=10000)
DataDrivenTools = text_input_with_none("Use of GIS mapping, real-time monitoring, or predictive modelling.", max_chars=10000)

# 6. Additional section: Environmental Impact and Co-Benefits
st.header("6. Environmental Impact and Co-Benefits")

ImpactOnBiodiversity = text_input_with_none("Expected improvements in habitat quality or connectivity.", max_chars=10000)
ResilienceToClimateChange = text_input_with_none("Contribution to climate adaptation or mitigation.", max_chars=10000)
PotentialAdverseEffects = text_input_with_none("Negative impacts, if any, on local ecosystems.", max_chars=10000)
CoBenefits = text_input_with_none("Additional benefits like carbon sequestration, aesthetic improvements.", max_chars=10000)

# 7. Additional section: Cost, Implementation, and Validation
st.header("7. Cost, Implementation, and Validation")

CostRange = text_input_with_none("Estimated cost for local, national, or global implementation.", max_chars=10000)
Timeframe = text_input_with_none("Approximate time required for implementation.", max_chars=10000)
AssessmentMethod = text_input_with_none("Methodology to measure success (e.g., EIA, noise mapping, biodiversity surveys).", max_chars=10000)
ValidationIndicators = text_input_with_none("Key performance indicators to assess effectiveness.", max_chars=10000)


# Submit button
if st.button("Send to base"):
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
    try:
        with get_connection().connect() as conn:
            df = pd.read_sql_query("SELECT * FROM Mitigation", conn)
            st.dataframe(df)  # Dynamiczny widok tabeli
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")



