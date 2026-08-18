import streamlit as st
import plotly.graph_objects as go

from utils import berechne_vermoegensverlauf

# Standardannahmen — Quellen im Portfolio dokumentieren!
RENDITE_ETF = 7.0
RENDITE_TAGESGELD = 2.0
INFLATION = 2.0


def render(daten):
    st.subheader("ETF vs. Tagesgeld")

    # TODO: 2-3 Sätze — was sind Opportunitätskosten?
    st.markdown("TODO: Erklärung für die Zielgruppe")

    jahre = daten["laufzeit"]

    df_etf = berechne_vermoegensverlauf(
        daten["startkapital"], daten["sparrate"], RENDITE_ETF, jahre)
    df_tag = berechne_vermoegensverlauf(
        daten["startkapital"], daten["sparrate"], RENDITE_TAGESGELD, jahre)

    eingezahlt = df_etf.iloc[-1]["Eingezahlt"]
    nominal_etf = df_etf.iloc[-1]["Vermögen"]
    nominal_tag = df_tag.iloc[-1]["Vermögen"]

    # Inflationsbereinigung: nominaler Wert / (1 + Inflation)^Jahre
    faktor = (1 + INFLATION / 100) ** jahre
    real_etf = nominal_etf / faktor
    real_tag = nominal_tag / faktor

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Nominal",
        x=["ETF (7 %)", "Tagesgeld (2 %)"],
        y=[nominal_etf, nominal_tag],
    ))
    fig.add_trace(go.Bar(
        name="Real (heutige Kaufkraft)",
        x=["ETF (7 %)", "Tagesgeld (2 %)"],
        y=[real_etf, real_tag],
    ))
    fig.add_hline(
        y=eingezahlt,
        line_dash="dash",
        annotation_text=f"Selbst eingezahlt: {eingezahlt:,.0f} €",
    )
    fig.update_layout(
        barmode="group",
        title=f"Vermögen nach {jahre} Jahren",
        yaxis_title="Euro",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.metric(
        "Opportunitätskosten (reale Differenz)",
        f"{real_etf - real_tag:,.0f} €",
    )