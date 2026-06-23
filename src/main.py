import argparse
import logging
from pathlib import Path
from data_loader import load_csv
from data_cleaner import clean_data
from duplicate_detector import detect_duplicates, remove_duplicates
from analyzer import generate_report
from plotter import create_plots

def main():
    parser = argparse.ArgumentParser(description="Kundendaten bereinigen und analysieren")
    parser.add_argument("input", help="Pfad zur Eingabe-CSV")
    parser.add_argument("--output", default="./data/processed", help="Ausgabeverzeichnis")
    parser.add_argument("--log", default="INFO", help="Log-Level (DEBUG, INFO, WARNING)")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper()),
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    """Laden"""
    df = load_csv(args.input)
    logging.info(f"{len(df)} Zeilen geladen.")

    """Bereinigung"""
    df_clean = clean_data(df)
    
    """Duplikate erkennen & entfernen"""
    duplicates = detect_duplicates(df_clean)
    logging.info(f"{len(duplicates)} Duplikate gefunden.")
    df_final = remove_duplicates(df_clean)
    
    """Bericht & Diagramme"""
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    generate_report(df_final, duplicates, out_dir / "report.txt")
    create_plots(df_final, out_dir)
    
    """Bereinigt die CSV speichern"""
    df_final.to_csv(out_dir / "cleaned_customers.csv", index=False)
    logging.info(f"Fertig. Ergebnisse in {out_dir}")

if __name__ == "__main__":
    main()
