# Erster Versuch (ohne delay ausgabe)
"""    
df = self.data.dropna(subset=['effective_soll', 'effective_ist']) # Entfernt Zeilen wo keine Zeit steht
#df['delay_minutes'] = (df['effective_ist'] - df['effective_soll'])# / 60 Berechnung verspaetung
df['delay_seconds'] = (df['ist_ab_von'] - df['soll_ab_von']) # Delay in secunden
df_avg_delay = df.groupby('halt_diva_von')['delay_seconds'].mean().reset_index() # Durchschnittliche Verspätung für jeden Stop
df_sorted = df_avg_delay.sort_values(by='delay_seconds', ascending=False) # Sortieren um die ersten 10 identifizieren zu können
print('Top 10 most unreliable stops:') # Ausgabe erste 10
for halt_diva_von in df_sorted['halt_diva_von'][:10]:
    print(halt_diva_von)
"""