import streamlit as st
import pandas as pd
from datasets import load_dataset
import gender_guesser.detector as gender
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
dataset = load_dataset("the-french-artist/hatvp_declaration_list_archive")

# Convert the dataset to a pandas DataFrame
df = pd.DataFrame(dataset['train'])

# Count occurrences of each 'prenom'
prenom_counts = df['prenom'].value_counts().head(10)

# Initialize the gender detector
d = gender.Detector()

# Determine the gender for each 'prenom'
df['gender'] = df['prenom'].apply(lambda x: d.get_gender(x))

# Filter out 'andy', 'unknown', and 'mostly_male', 'mostly_female' to simplify the analysis
df_filtered = df[df['gender'].isin(['male', 'female'])]

# Count occurrences of each gender
gender_counts = df_filtered['gender'].value_counts()

# Streamlit app definition
st.title("Gender Equality Analysis on HATVP Data")
st.write("This app shows gendered plots to demonstrate the imbalance between genders.")

# Creating columns for side-by-side plots
col1, col2 = st.columns(2)

with col1:
    st.write("Here is the bar chart showing the top 10 'prenom' (surnames) with their number of occurrences.")
    # Plotting the horizontal bar chart for top 10 'prenom'
    fig = px.bar(prenom_counts, orientation='h', labels={'index': 'Prenom', 'value': 'Occurrences'}, title="Top 10 'Prenom'")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey')
	)
    st.plotly_chart(fig, config={'displayModeBar': False})

with col2:
    st.write("Here is the pie chart showing the gender distribution based on the 'prenom'.")
    # Plotting the pie chart for gender distribution with custom colors
    gender_color_map = {'male': 'blue', 'female': 'pink'}
    fig2 = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, title="Gender Distribution", hole=0.3)
    fig2.update_traces(marker=dict(colors=[gender_color_map[gender] for gender in gender_counts.index]))
    st.plotly_chart(fig2, config={'displayModeBar': False})
