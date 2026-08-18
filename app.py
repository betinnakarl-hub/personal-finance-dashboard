import streamlit as st

import modul1
import modul2
import modul3

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")


def sidebar_inputs():
    st.sidebar.header("Deine Basisdaten")
    return {
        "alter": st.sidebar.number_input("Alter", 1, 100, 25),
        "nettoeinkommen": st.sidebar.number_input("Nettoeinkommen (monatlich)", 0, value=2500, step=100),
        "startkapital": st.sidebar.number_input("Startkapital", 0, value=5000, step=500),
        "sparrate": st.sidebar.number_input("Monatliche Sparrate", 0, value=200, step=50),
        "laufzeit": st.sidebar.slider("Anlagehorizont (Jahre)", 1, 50, 30),
    }


def main():
    st.title("Personal Finance Dashboard")
    st.caption("Ein interaktives Werkzeug für Studierende und Berufseinsteiger*innen")

    daten = sidebar_inputs()

    tab1, tab2, tab3 = st.tabs(["Zinseszins", "ETF vs. Tagesgeld", "Rente"])

    with tab1:
        modul1.render(daten)
    with tab2:
        modul2.render(daten)
    with tab3:
        modul3.render(daten)


if __name__ == "__main__":
    main()