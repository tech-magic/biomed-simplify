import streamlit as st
import plotly.graph_objects as go

def plot_disease_links(summary_data):
    labels = ["Gene/Drug", "Disease A", "Disease B", "Population X"]
    sources = [0, 0, 0]
    targets = [1, 2, 3]
    values = [5, 3, 2]

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels),
        link=dict(source=sources, target=targets, value=values))])
    st.plotly_chart(fig)
