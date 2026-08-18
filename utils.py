import pandas as pd


def berechne_vermoegensverlauf(startkapital, sparrate, rendite, laufzeit):
    """Vermögensentwicklung eines monatlichen Sparplans.
    rendite: jährliche Rendite in Prozent (z.B. 7 für 7%)
    """
    monatszins = rendite / 100 / 12
    kapital = startkapital
    daten = []

    for monat in range(laufzeit * 12 + 1):
        if monat % 12 == 0:
            eingezahlt = startkapital + sparrate * monat
            daten.append({
                "Jahr": monat // 12,
                "Eingezahlt": eingezahlt,
                "Zinsertrag": kapital - eingezahlt,
                "Vermögen": kapital,
            })
        kapital += sparrate
        kapital *= (1 + monatszins)

    return pd.DataFrame(daten)