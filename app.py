import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(page_title="Institutional Mapping Tool", layout="wide")
st.title("US APEC-RISE Institutional Mapping Tool")

# Upload or load data
uploaded_file = st.file_uploader("Upload your Institutional Mapping CSV", type="csv")

import os

if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif os.path.exists("sample_institutional_mapping.csv"):
    df = pd.read_csv("sample_institutional_mapping.csv")
    st.success("Loaded sample dataset.")
else:
    st.warning("Please upload a CSV file to begin.")
    st.stop()
)
else:
    st.markdown("Or use the [sample CSV](sandbox:/mnt/data/sample_institutional_mapping.csv)")
    df = pd.read_csv("sample_institutional_mapping.csv")

# Filter
economies = ["All"] + sorted(df["Economy"].unique())
selected_economy = st.selectbox("Filter by Economy", options=economies)

if selected_economy != "All":
    df = df[df["Economy"] == selected_economy]

# Build graph
G = nx.Graph()
for _, row in df.iterrows():
    G.add_node(row["Institution"], title=row["Role"], size=row["Influence Score"] * 10)
    if pd.notna(row["Linkages"]):
        for target in row["Linkages"].split(','):
            G.add_edge(row["Institution"], target.strip())

# Create Pyvis network graph
net = Network(height="600px", width="100%", bgcolor="#f8f9fa", font_color="black")
net.from_nx(G)
net.repulsion(node_distance=200, spring_length=200)
net.save_graph("graph.html")

# Display the graph
with open("graph.html", "r", encoding="utf-8") as f:
    html = f.read()
components.html(html, height=650, scrolling=True)

# Show raw data
with st.expander("View Data Table"):
    st.dataframe(df)
