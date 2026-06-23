import pandas as pd
import logging
import re

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    eine umfassende Datenbereinigung durch.
    """
    logging.info("Starte Datenbereinigung...")
    df = df.copy()

    """Spaltennamen bereinigen (Leerzeichen, Groß-/Kleinschreibung, Sonderzeichen)"""
    df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', col.strip().lower()) for col in df.columns]
    logging.info(f"Spalten umbenannt in: {list(df.columns)}")

    """Führende/nachfolgende Leerzeichen in ALLEN Textspalten entfernen"""
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        """Leere Strings durch NaN ersetzen (für spätere Behandlung)"""
        df[col] = df[col].replace('', pd.NA)

    """Spezifische Spalten-Typkonvertierungen (falls vorhanden)"""
    """Alter: Konvertiere zu Integer, falls möglich"""
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        # Fehlende Alter durch Median ersetzen (robust)
        if df['age'].isna().any():
            median_age = df['age'].median()
            df['age'].fillna(median_age, inplace=True)
            logging.info(f"Fehlende Alter durch Median ({median_age}) ersetzt.")
        df['age'] = df['age'].astype('Int64')  # nullable Integer

    """E-Mail-Adressen standardisieren (Kleinbuchstaben)"""
    if 'email' in df.columns:
        df['email'] = df['email'].astype(str).str.lower().str.strip()
        # Ungültige E-Mails (ohne @) als NaN markieren
        df.loc[~df['email'].str.contains('@', na=False), 'email'] = pd.NA

    """Fehlende Werte in Kategorie/Region durch "Unbekannt" ersetzen (für Diagramme)"""
    for col in ['category', 'state']:
        if col in df.columns:
            df[col] = df[col].fillna('Unbekannt')

    logging.info("Bereinigung abgeschlossen.")
    return df
