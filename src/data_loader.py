import pandas as pd
import logging
from pathlib import Path

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Lädt eine CSV-Datei mit automatischer Erkennung von Encoding und Trennzeichen.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

    # verschiedene Encodings (häufigste zuerst)
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    separators = [',', ';', '\t', '|']

    df = None
    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=sep, dtype=str, keep_default_na=False)
                # Wenn mehr als 1 Spalte erkannt wurde, war es erfolgreich
                if len(df.columns) > 1:
                    logging.info(f"Erfolgreich geladen: Encoding={encoding}, Trennzeichen='{sep}', Zeilen={len(df)}")
                    return df
            except Exception:
                continue

    # Pandas automatisch erkennen lassen
    try:
        df = pd.read_csv(file_path, encoding='utf-8', dtype=str, keep_default_na=False)
        logging.info(f"Fallback-Geladen: {len(df)} Zeilen")
        return df
    except Exception as e:
        raise ValueError(f"Konnte CSV nicht laden. Bitte prüfen Sie das Format. Fehler: {e}")
