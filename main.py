import streamlit as st
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt

# Load the dataset
dataset = load_dataset("the-french-artist/hatvp_declaration_list_archive")

# Convert the dataset to a pandas DataFrame
df = pd.DataFrame(dataset['train'])

# Count occurrences of each 'prenom'
prenom_counts = df['prenom'].value_counts().head(10)

# Streamlit app definition
st.title("Top 10 'Prenom' in the Dataset")

st.write("This app displays the top 10 'prenom' with the number of occurrences.")

# Plotting the bar chart
fig, ax = plt.subplots()
prenom_counts.plot(kind='bar', ax=ax)
ax.set_xlabel('Prenom')
ax.set_ylabel('Occurrences')
ax.set_title("Top 10 'Prenom'")

st.pyplot(fig)