import streamlit as st
import pandas as pd
import pyreadstat
import os
import datetime
import gspread
from google.oauth2.service_account import Credentials

# Initial Understanding Section
st.subheader("Initial Understanding:")
st.write("""
- There are 18 columns and 220 entries.
- There are 12 columns with object dtype and 6 columns with float64 dtype.
- There is no missing information.
- The F30 study covers 22 patients. All 22 have a unique identifier. Unique Identifier is defined by two columns: "USUBJID", "SUBJID". 
- There is only one Planned Treatment for this study.
""")

# Immune Response Section
st.subheader("Immune Response and Treatment Emergent Anti-Drug Antibodies (ADA) Status")
st.write("We have 3 parameters in this dataset that describe antibodies produced by the immune system in response to enzyme replacement therapies (ERTs) used to treat the disease.")
st.image('plots/Immune system response_plot.png', use_column_width=True)
st.image('plots/treatment.png', use_column_width=True)

st.subheader("Questions for SME (Immune and ADA Response):")
st.write("1. What is the clinical or biological significance of the relationship between the presence of different antibodies (e.g., IgG, IgE, Neutralizing Antibodies) and ADA status (Positive/Negative), and how should this relationship guide model development?")
immune_response_1 = st.text_area("Response to Immune Response Question 1", key="immune_response1_unique")  # Updated key
if immune_response_1:
    st.write(f"**Response to Question 1:** {immune_response_1}")

# Visit Duration Section
st.subheader("Visit Duration")
st.image('plots/Visiting - Duration.png', use_column_width=True)

st.subheader("Questions for SME (Visit Duration):")
st.write("1. Why are there duplicate SUBJID (Patient record) for each AVISIT (visit)? Could it be due to multiple visits or assessments for the same subject within the same AVISIT period?")
visit_duration_response_1 = st.text_area("Response to Visit Duration Question 1", key="visit_duration_response1_unique")  # Updated key
if visit_duration_response_1:
    st.write(f"**Response to Question 1:** {visit_duration_response_1}")

st.write("2. How should I treat these duplicates?")
visit_duration_response_2 = st.text_area("Response to Visit Duration Question 2", key="visit_duration_response2_unique")  # Updated key
if visit_duration_response_2:
    st.write(f"**Response to Question 2:** {visit_duration_response_2}")

# Sex and Fabry Disease Classification Section
st.subheader("SEX, Fabry Disease Classification of the patients")
st.image('plots/sex.png', use_column_width=True)
st.image('plots/Baseline.png', use_column_width=True)

st.subheader("Questions for SME (Sex, Fabry Classification):")
st.write("1. Does This Gender Imbalance Affect the Generalizability of the Results?")
sex_response_1 = st.text_area("Response to SEX, Fabry Disease Classification 1", key="sex_response1_unique")  # Updated key
if sex_response_1:
    st.write(f"**Response to Question 1:** {sex_response_1}")

st.write("2. What is the difference between Classical Vs Non-classical Fabry?")
sex_response_2 = st.text_area("Response to SEX, Fabry Disease Classification 2", key="sex_response2_unique")  # Updated key
if sex_response_2:
    st.write(f"**Response to Question 2:** {sex_response_2}")

# Google Sheets Authentication and Saving
def authenticate_gsheets():
    # Use the credentials directly from Streamlit secrets
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    
    # Authorize with Google Sheets API
    client = gspread.authorize(creds)
    
    # Open the Google Sheet (replace 'Your Spreadsheet Name' with the actual sheet name)
    sheet = client.open("sme_response_adada").sheet1
    return sheet

# Function to save responses to Google Sheets
def save_responses_to_gsheets(sheet, immune_response1, visit_duration_response1, visit_duration_response2, sex_response_1, sex_response_2):
    # Get the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare data to be inserted
    data = [current_time, immune_response1, visit_duration_response1, visit_duration_response2, sex_response_1, sex_response_2]
    
    # Insert the data into the first available row in the Google Sheet
    sheet.append_row(data)
    
    # Display success message in Streamlit
    st.success("Responses saved to Google Sheets")

# Button to save all responses
if st.button('Save All Responses to Google Sheets'):
    # Authenticate with Google Sheets API
    sheet = authenticate_gsheets()
    
    # Save the responses
    save_responses_to_gsheets(sheet, immune_response_1, visit_duration_response_1, visit_duration_response_2, sex_response_1, sex_response_2)
