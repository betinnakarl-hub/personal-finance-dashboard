import streamlit as st
import plotly.graph_objects as go

from utils import berechne_vermoegensverlauf

# Standardannahmen — im Portfolio begründen und mit Quellen belegen!
RENTENNIVEAU = 0.48      # gesetzliche Rente, Anteil vom Nettoeinkommen
BEDARFSQUOTE = 0.80      # Bedarf im Alter, Anteil vom Nettoeinkommen
BAV_SPARQUOTE = 0.04     # Anteil des Nettoeinkommens für bAV
BAV_RENDITE = 3.0        # konservative Verzinsung der bAV (%)
PRIVAT_RENDITE = 7.0     # Rendite der privaten Vorsorge (%)
LEBENSERWARTUNG = 85     # Annahme für die Entnahmedauer


def render(daten):
    st.subheader("Renten-Simulator")

    # TODO: Drei-Säulen-Modell in 2-3 Sätzen erklären
    st.markdown("TODO: Erklärung für die Zielgruppe")

    rentenalter = st.slider("Gewünschtes Renteneintrittsalter", 60, 70, 67)

    jahre_bis_rente = rentenalter - daten["alter"]
    if jahre_bis_rente <= 0:
        st.warning("Das Renteneintrittsalter muss über dem aktuellen Alter liegen.")
        return

    entnahme_monate = (LEBENSERWARTUNG - rentenalter) * 12
    netto = daten["nettoeinkommen"]

    bedarf = netto * BEDARFSQUOTE
    saeule_1 = netto * RENTENNIVEAU

    kapital_bav = berechne_vermoegensverlauf(
        0, netto * BAV_SPARQUOTE, BAV_RENDITE, jahre_bis_rente
    ).iloc[-1]["Vermögen"]
    saeule_2 = kapital_bav / entnahme_monate

    kapital_privat = berechne_vermoegensverlauf(
        daten["startkapital"], daten["sparrate"], PRIVAT_RENDITE, jahre_bis_rente
    ).iloc[-1]["Vermögen"]
    saeule_3 = kapital_privat / entnahme_monate

    luecke = max(0, bedarf - (saeule_1 + saeule_2 + saeule_3))

    fig = go.Figure()
    for name, wert, farbe in [
        ("Gesetzliche Rente", saeule_1, "#1f77b4"),
        ("Betriebliche Vorsorge", saeule_2, "#2ca02c"),
        ("Private Vorsorge", saeule_3, "#ff7f0e"),
        ("Rentenlücke", luecke, "#d62728"),
    ]:
        fig.add_trace(go.Bar(
            name=name, x=["Bedarf im Alter"], y=[wert],
            marker_color=farbe,
        ))
    fig.update_layout(
        barmode="stack",
        title=f"Monatlicher Bedarf: {bedarf:,.0f} €",
        yaxis_title="Euro pro Monat",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.metric("Monatliche Rentenlücke", f"{luecke:,.0f} €")

    st.warning(
        "Stark vereinfachte Modellrechnung, keine Finanzberatung."
    )