import matplotlib.pyplot as plt
import pandas as pd

def create_plots(df, output_dir):
    plt.style.use('seaborn-v0_8-darkgrid')
    
    """1. Altersverteilung"""
    if 'age' in df.columns:
        plt.figure(figsize=(8,5))
        df['age'].hist(bins=20, edgecolor='black')
        plt.title('Altersverteilung der Kunden')
        plt.xlabel('Alter')
        plt.ylabel('Anzahl')
        plt.savefig(output_dir / 'age_distribution.png', dpi=150)
        plt.close()
    
    """2. Kategorie-Balken"""
    if 'category' in df.columns:
        counts = df['category'].value_counts()
        plt.figure(figsize=(10,6))
        counts.plot(kind='bar', color='skyblue')
        plt.title('Kunden nach Kategorie')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_dir / 'category_bar.png', dpi=150)
        plt.close()
    
    """3. Region (z.B. Bundesland)"""
    if 'state' in df.columns:
        plt.figure(figsize=(8,8))
        df['state'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Regionale Verteilung')
        plt.ylabel('')
        plt.savefig(output_dir / 'region_pie.png', dpi=150)
        plt.close()
