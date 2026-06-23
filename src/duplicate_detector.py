import pandas as pd

def detect_duplicates(df, subset=['email', 'name', 'postal_code']):
    """
    Findet semantische Duplikate anhand der angegebenen Spalten.
    Gibt einen DataFrame mit den Duplikat-Gruppen zurück.
    """
    """Exakte Duplikate"""
    exact_dups = df[df.duplicated(subset=subset, keep=False)]
    """Zusätzlich: E-Mail-Duplikate (auch wenn Name abweicht)"""
    email_dups = df[df.duplicated(subset=['email'], keep=False)]
    """Kombinieren"""
    all_dups = pd.concat([exact_dups, email_dups]).drop_duplicates()
    return all_dups

def remove_duplicates(df, subset=['email']):
    """Behält den ersten Eintrag pro E-Mail (kann angepasst werden)."""
    return df.drop_duplicates(subset=subset, keep='first')
