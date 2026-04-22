import pandas as pd
import numpy as np
import time
from matplotlib import pyplot as plt
from functions import *

t_0 = time.time()

#Szenario-Variablen (operativ)
new_run = True
#Szenario-Variablen (inhaltlich)
zuerich_jahre_shifted = 2 #Änderungen mindestens einmal mit new_run=True laufen lassen

# Daten einlesen
# Zanla lesen und mit Geodaten verbinden
zanla = zanla_data_reader(new_read=new_run, zuerich_jahre_shifted=zuerich_jahre_shifted)
print('zanla eingelesen')
# Gerätedaten lesen
zgeraus = zgeraus_data_reader(new_read=True, remove_lebensdauer_under=2)
print('zgeraus eingelesen')

# Analysen ohne direkten Modelleinfluss
# Plots zu Gerätedaten und Verteilung
lebensdauer_analysis(zgeraus_data=zgeraus) #Plots für die ZGRAUS Gerätedaten

# Modellbasis
# Absenkpfad Heizungen modellieren/einlesen
absenkpfade_frame = absenkpfad_generation(zanla_data=zanla, zgeraus_data=zgeraus, simulations=1000, plot=True, new_read=new_run, fitted=True, lifetime_extension=2)
print('Absenkpfad Modus +2 Jahre abgeschlossen')
heizung_absenkpfad = absenkpfade_frame.loc['alle_gebiete_%']

# Absenkpfad Prozesse (linear halbiert, auf 2/3 und gleichbleibend)
jahres_range = list(range(2025, 2051))
prozess_ansenkpfad = pd.DataFrame(index=[100, 67, 33], columns=jahres_range, dtype=float)
for limit in prozess_ansenkpfad.index:
    prozess_ansenkpfad.loc[limit, 2025] = 1.0
    prozess_ansenkpfad.loc[limit, 2050] = limit / 100
prozess_ansenkpfad.interpolate(axis=1, inplace=True)

print('Modellierung gestartet')
get_time(t_0)

for absatz_option in ['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt']:
    calculate_scenario(zanla_data=zanla, absatz_option=absatz_option,
                       modell_varianten_name='Referenz',
                       set_absenkpfad=heizung_absenkpfad, set_prozesspfad=prozess_ansenkpfad.loc[67],
                       halterate_heizungen_80_bis_2030= 0.1, halterate_heizungen_80_post_2030=0.2,
                       save_appendix='')
    print('szenario Referenz abgeschlossen', absatz_option)
    get_time(t_0)

for absatz_option in ['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt']:
    calculate_scenario(zanla_data=zanla, absatz_option=absatz_option,
                       modell_varianten_name='verschärft',
                       set_absenkpfad=heizung_absenkpfad, set_prozesspfad=prozess_ansenkpfad.loc[33],
                       halterate_heizungen_80_bis_2030= 0.1, halterate_heizungen_80_post_2030=0.0,
                       save_appendix='')
    print('szenario verschärft abgeschlossen', absatz_option)
    get_time(t_0)

for absatz_option in ['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt']:
    calculate_scenario(zanla_data=zanla, absatz_option=absatz_option,
                       modell_varianten_name='gelockert',
                       set_absenkpfad=heizung_absenkpfad, set_prozesspfad=prozess_ansenkpfad.loc[100],
                       halterate_heizungen_80_bis_2030= 0.1, halterate_heizungen_80_post_2030=0.5,
                       save_appendix='')
    print('szenario gelockert abgeschlossen', absatz_option)
    get_time(t_0)

get_time(t_0)