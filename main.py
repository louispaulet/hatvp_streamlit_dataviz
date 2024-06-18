import streamlit as st
import pandas as pd
from datasets import load_dataset
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")


# Load the dataset
dataset = load_dataset("the-french-artist/hatvp_declaration_list_archive")

# Convert the dataset to a pandas DataFrame
df = pd.DataFrame(dataset['train'])

# Count occurrences of each 'prenom'
prenom_counts = df['prenom'].value_counts().head(10)

def get_gender(civility):
    if civility == 'Mme':
        return 'female'
    return 'male'

# Determine the gender for each 'prenom'
#df['gender'] = df['prenom'].apply(lambda x: d.get_gender(x))
df['gender'] = df['civilite'].apply(lambda x: get_gender(x))

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
    st.header("Top Surnames")
    st.write("Here is the bar chart showing the top 10 'prenom' (surnames) with their number of occurrences.")
    # Plotting the horizontal bar chart for top 10 'prenom'
    fig = px.bar(prenom_counts, orientation='h', labels={'index': 'Prenom', 'value': 'Occurrences'}, title="Top 10 'Prenom' (surnames)")
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey')
    )
    st.plotly_chart(fig, config={'displayModeBar': False})

with col2:
    st.header("Total gender ratio")
    st.write("Here is the pie chart showing the gender distribution based on the 'prenom'.")
    # Plotting the pie chart for gender distribution with custom colors
    gender_color_map = {'male': 'blue', 'female': 'pink'}
    fig2 = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, title="Gender Distribution", hole=0.3)
    fig2.update_traces(marker=dict(colors=[gender_color_map[gender] for gender in gender_counts.index]))
    st.plotly_chart(fig2, config={'displayModeBar': False})

col1, col2 = st.columns(2)

with col1:
    st.header('Mandate type')
    st.write('We show that the gender ratio is different for each mandate type.')
    # Button to switch between normalized and count bar plot
    plot_type = st.radio("Choose plot type for 'type_mandat' with gender distribution:", ("Normalized 100%", "Count"))

    # Prepare the data for the split bar plot and order by female counts
    type_mandat_gender_counts = df_filtered.groupby(['type_mandat', 'gender']).size().reset_index(name='counts')

    # Pivot the table to get counts of males and females side by side for sorting
    pivot_table = type_mandat_gender_counts.pivot(index='type_mandat', columns='gender', values='counts').fillna(0)

    if plot_type == "Normalized 100%":
        # Normalize the counts
        pivot_table['total'] = pivot_table['male'] + pivot_table['female']
        pivot_table['male'] = pivot_table['male'] / pivot_table['total'] * 100
        pivot_table['female'] = pivot_table['female'] / pivot_table['total'] * 100
        # Sort by female percentage
        pivot_table = pivot_table.sort_values(by='female', ascending=False).reset_index()
    else:
        pivot_table = pivot_table.sort_values(by='female', ascending=False).reset_index()

    # Melt the table back to long form
    ordered_type_mandat_gender_counts = pivot_table.melt(id_vars='type_mandat', value_vars=['female', 'male'], var_name='gender', value_name='counts')

    # Plotting the split bar plot ordered by female counts
    yaxis_title = 'Percentage' if plot_type == "Normalized 100%" else 'Count'
    fig3 = px.bar(ordered_type_mandat_gender_counts, x='type_mandat', y='counts', color='gender',
                  labels={'type_mandat': 'Type of Mandate', 'counts': yaxis_title, 'gender': 'Gender'},
                  title="Distribution of males and females for each type of mandate",
                  color_discrete_map=gender_color_map)

    fig3.update_layout(
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey')
    )

    st.plotly_chart(fig3, config={'displayModeBar': False})