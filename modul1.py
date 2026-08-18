import streamlit as st
import plotly.express as px

from utils import berechne_vermoegensverlauf


def render(daten):
    st.subheader("Zinseszins-Rechner")

    rendite = st.slider("Erwartete Rendite pro Jahr (%)", 0.0, 12.0, 7.0, step=0.5)

    df = berechne_vermoegensverlauf(
        startkapital=daten["startkapital"],
        sparrate=daten["sparrate"],
        rendite=rendite,
        laufzeit=daten["laufzeit"],
    )

    st.metric("Endvermögen", f"{df.iloc[-1]['Vermögen']:,.2f} €")

    fig = px.line(df, x="Jahr", y=["Eingezahlt", "Vermögen"],
                  markers=True, title="Vermögensentwicklung")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Daten anzeigen"):
        st.dataframe(df)