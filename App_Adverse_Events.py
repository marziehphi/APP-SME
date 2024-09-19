import streamlit as st
import pandas as pd
import pyreadstat
import os
import datetime
import gspread
from google.oauth2.service_account import Credentials

# Display the initial understanding 
st.subheader("Initial Understanding:")
st.write("""
- There are 50 columns and 146 entries.
- There are missing informations for the columns: AESTTM , LOCAN , AETMCATN, TRTSPTM , TRTSTTM, TRTIFEDT  
- The F30 study covers 21 patients. All 21 have a unique identifier. Unique Identifier is defined by two columns: "USUBJID", "SUBJID". 
- There is only one Planned Treatment for this study.
""")

st.subheader("Questions for SME (Discrepancies):")
    
# Question 1 for immune response
st.write("1.How should we handle discrepancies in number of records across datasets during model development?")
st.write("""- The columns SUBJID, SEX, TEADA, and FDCLA exhibit different distributions between the two datasets (Anti-Drug vs. Adverse Events).""")
patient_response1 = st.text_area("Response to Discrepancies Question 1", key="patient_response1")
if patient_response1:
    st.write(f"**Response to Question 1:** {patient_response1}")

# Timestamp Information Section
st.subheader("Questions for SME (timestamps information):")
st.write("""- From a dataset we could observe there are 8 columns that describe the timestamp.""")

data = {
    "timestamp_column_name": ["SCRDT","TRTSDTM", "TRTSDT", "AESTDT", "AESTTM", "TRTIFEDT", "TRTSTTM", "TRTSPTM"],
    "Number_unique_values": [17, 21, 16, 111, 37, 77, 56, 59]
}

# Convert to DataFrame and display it
timestamp_df = pd.DataFrame(data)
st.write("### Timestamp Columns Information")
st.dataframe(timestamp_df)

st.subheader("Questions for SME (Timestamp column clarification):")
st.write("1.Could you explain what information each column is capturing, and whether it makes sense that the count of unique values differs based on the existence of timestamps?")
time_response1 = st.text_area("Response to Timestamp column clarification Question 1", key="time_response1")
if time_response1:
    st.write(f"**Response to Question 1:** {time_response1}")

# Clarification Section
st.subheader("clarification")
st.image('plots/PREAEFL.png', use_column_width=True)
st.image('plots/TEAEFL.png', use_column_width=True)

st.subheader("Questions for SME (clarification):")
st.write("1. Could you clarify what these columns represent? It seems they are capturing different aspects of the same data.")
st.write("""2. There are two columns please let us know if it is important in the process of development or we could ignore it?
- AESEQ
- ASTDTF""")
clear_response1 = st.text_area("Response to clarification Question 1", key="clear_response1")
if clear_response1:
    st.write(f"**Response to Question 1:** {clear_response1}")

clear_response2 = st.text_area("Response to clarification Question 2", key="clear_response2")
if clear_response2:
    st.write(f"**Response to Question 2:** {clear_response2}")

# Textual Information Section
st.subheader("Textual Information")
st.subheader("Questions for SME (Textual Feature):")
st.write("""
1. Could you clarify what these columns represent?
- AEBODSYS
- AEDECOD
- AETERM
- AETMCAT1
- AETMDESC       
""")
st.write("""
2. In your opinion, which of this information is most important to include during the process?
We have columns that represent Patient Status during these adverse events such as:
- AEOUT
- AEACN
- FCE
""")
st.write("""
3. We have three columns that categorize the stages of adverse events. Could you explain the differences between them?
- AETOXGRC
- AESEV
- AEREL
""")

text_response1 = st.text_area("Response to Textual Feature Question 1", key="text_response1")
if text_response1:
    st.write(f"**Response to Question 1:** {text_response1}")
    
text_response2 = st.text_area("Response to Textual Feature Question 2", key="text_response2")
if text_response2:
    st.write(f"**Response to Question 2:** {text_response2}")
    
text_response3 = st.text_area("Response to Textual Feature Question 3", key="text_response3")
if text_response3:
    st.write(f"**Response to Question 3:** {text_response3}")

# Function to save responses to Google Sheets
def authenticate_gsheets():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open("sme_response_adae").sheet1
    return sheet

def save_responses_to_gsheets(sheet, patient_response1, time_response1, clear_response1, clear_response2, text_response1, text_response2, text_response3):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare data to insert
    data = [
        current_time, patient_response1, time_response1, clear_response1, clear_response2,
        text_response1, text_response2, text_response3
    ]
    
    # Insert the data into the first available row in the Google Sheet
    sheet.append_row(data)
    
    st.success("Responses saved to Google Sheets")

# Button to save all responses
if st.button('Save All Responses to Google Sheets'):
    sheet = authenticate_gsheets()
    save_responses_to_gsheets(sheet, patient_response1, time_response1, clear_response1, clear_response2, text_response1, text_response2, text_response3)
