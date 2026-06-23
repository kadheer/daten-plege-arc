import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

def generate_report(df: pd.DataFrame, duplicates: pd.DataFrame, output_path: Path) -> None:
    """
    einen umfassenden Analysebericht als Textdatei.
    """
    logging.info(f"Generiere Bericht: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("KUNDENDATEN-ANALYSEBERICHT\n")
        f.write(f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        """Grundübersicht"""
        f.write("1. BASIS-STATISTIK\n")
        f.write("-" * 40 + "\n")
        f.write(f"Gesamtanzahl Datensätze (nach Bereinigung): {len(df)}\n")
        f.write(f"Anzahl Spalten: {len(df.columns)}\n")
        f.write(f"Spaltennamen: {', '.join(df.columns)}\n\n")

        """Fehlende Werte"""
        f.write("2. FEHLENDE WERTE (pro Spalte)\n")
        f.write("-" * 40 + "\n")
        missing = df.isna().sum()
        if missing.sum() > 0:
            for col, count in missing.items():
                if count > 0:
                    f.write(f"  {col}: {count} fehlend ({count/len(df)*100:.1f}%)\n")
        else:
            f.write("  Keine fehlenden Werte vorhanden.\n")
        f.write("\n")

        """Duplikate"""
        f.write("3. DUPLIKAT-ERKENNUNG\n")
        f.write("-" * 40 + "\n")
        if len(duplicates) > 0:
            f.write(f"Anzahl gefundener Duplikat-Datensätze: {len(duplicates)}\n")
            f.write("Beispiele (erste 5):\n")
            f.write(duplicates.head(5).to_string(index=False))
            f.write("\n\n")
        else:
            f.write("Keine Duplikate gefunden.\n\n")

        """Deskriptive Statistik (nur numerische Spalten)"""
        f.write("4. DESKRIPTIVE STATISTIK (numerisch)\n")
        f.write("-" * 40 + "\n")
        num_cols = df.select_dtypes(include=['number']).columns
        if len(num_cols) > 0:
            f.write(df[num_cols].describe().to_string())
        else:
            f.write("Keine numerischen Spalten vorhanden.\n")
        f.write("\n\n")

        """Kategorische Verteilungen (Top-Werte)"""
        f.write("5. TOP-KATEGORIEN\n")
        f.write("-" * 40 + "\n")
        for col in ['category', 'state']:
            if col in df.columns:
                f.write(f"\n{col.upper()} (Top 5):\n")
                counts = df[col].value_counts().head(5)
                for val, cnt in counts.items():
                    f.write(f"  {val}: {cnt} ({cnt/len(df)*100:.1f}%)\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("ENDE DES BERICHTES\n")

    logging.info("Bericht erfolgreich erstellt.")
