from unittest.mock import inplace

import pandas as pd
import numpy as np
import time
from scipy import stats
from matplotlib import pyplot as plt

t_0 = time.time()

#Allgemeinde Funktionen
def get_time(t_start, print_text=''):
    """Returns the runtime since the inputtime"""
    t_end = time.time()
    t_running = t_end - t_start
    time_string = (print_text + '\nProcess executed after ' + str(round(t_running, 1)) + ' seconds (i.e. '
                   + str(int(t_running/60)) + ':' + str(int(round(t_running % 60, 0))).zfill(2) + ').')
    print(time_string)


#Daten Einlesen
def zanla_data_reader(new_read=True, zuerich_jahre_shifted=False):
    if new_read:
        # Read ZANLA Export
        dtypes_zanla = {'Anlage Nummer': int, 'Anlagenart': str, 'Tariftyp': str, 'Abrechnungsklasse': int,
                        'Anlage Branche': str,
                        'Anschlussobjekt (Haus)': str, 'Gasdruckgebiet': str, 'Anschlussobjekt Strasse': str,
                        'Anschlussobjekt PLZ': float, 'Anschlussobjekt Ort': str, 'Anschlussobjekt PLZ/Ort': str,
                        'Regionalstrukturgrp.': str,
                        'Erlös Tot Jahr -1': float, 'Erlös Tot Jahr -2': float, 'Erlös Tot Jahr -3': float,
                        'Erlös Tot Jahr -4': float, 'Erlös Tot Jahr -5': float, 'Erlös Tot Jahr -6': float,
                        'Erlös Tot Jahr -7': float, 'Erlös Tot Jahr -8': float, 'Erlös Tot Jahr -9': float,
                        'Erlös Tot Jahr -10': float,
                        'Anzahl Apparate': int, 'Anzahl Apparate Objektart AH*': int, 'Leistung Nennwert': int,
                        'Apparat 1 Geräteart': str, 'Apparat 1 Bezeichnung': str, 'Apparat 1 Leistung': int,
                        'Apparat 1 Baujahr': float,
                        'Apparat 2 Geräteart': str, 'Apparat 2 Bezeichnung': str, 'Apparat 2 Leistung': int,
                        'Apparat 2 Baujahr': float,
                        'Apparat 3 Geräteart': str, 'Apparat 3 Bezeichnung': str, 'Apparat 3 Leistung': int,
                        'Apparat 3 Baujahr': float,
                        'Apparat 4 Geräteart': str, 'Apparat 4 Bezeichnung': str, 'Apparat 4 Leistung': int,
                        'Apparat 4 Baujahr': float,
                        'Apparat 5 Geräteart': str, 'Apparat 5 Bezeichnung': str, 'Apparat 5 Leistung': int,
                        'Apparat 5 Baujahr': float,
                        'Absatz Durchg. Jahr -1': float, 'Absatz Durchg. Jahr -2': float,
                        'Absatz Durchg. Jahr -3': float,
                        'Absatz Durchg. Jahr -4': float, 'Absatz Durchg. Jahr -5': float,
                        'Absatz Durchg. Jahr -6': float,
                        'Absatz Durchg. Jahr -7': float, 'Absatz Durchg. Jahr -8': float,
                        'Absatz Durchg. Jahr -9': float,
                        'Absatz Durchg. Jahr -10': float,
                        'Absatz Handel Jahr -1': float, 'Absatz Handel Jahr -2': float, 'Absatz Handel Jahr -3': float,
                        'Absatz Handel Jahr -4': float, 'Absatz Handel Jahr -5': float, 'Absatz Handel Jahr -6': float,
                        'Absatz Handel Jahr -7': float, 'Absatz Handel Jahr -8': float, 'Absatz Handel Jahr -9': float,
                        'Absatz Handel Jahr -10': float,
                        'Erlös AP Jahr -1': float, 'Erlös AP Jahr -2': float, 'Erlös AP Jahr -3': float,
                        'Erlös AP Jahr -4': float,
                        'Erlös AP Jahr -5': float, 'Erlös AP Jahr -6': float, 'Erlös AP Jahr -7': float,
                        'Erlös AP Jahr -8': float,
                        'Erlös AP Jahr -9': float, 'Erlös AP Jahr -10': float,
                        'Erlös LP Jahr -1': float, 'Erlös LP Jahr -2': float, 'Erlös LP Jahr -3': float,
                        'Erlös LP Jahr -4': float,
                        'Erlös LP Jahr -5': float, 'Erlös LP Jahr -6': float, 'Erlös LP Jahr -7': float,
                        'Erlös LP Jahr -8': float,
                        'Erlös LP Jahr -9': float, 'Erlös LP Jahr -10': float,
                        'Geschäftspartner Nummer': float, 'Geschäftspartner Name': str}
        dtypes_zanla_backup = {'Anlage Nummer': int, 'Anlagenart': str, 'Tariftyp': str, 'Abrechnungsklasse': int,
                               'Anlage Branche': str,
                               'Anschlussobjekt (Haus)': str, 'Gasdruckgebiet': str, 'Anschlussobjekt Strasse': str,
                               'Anschlussobjekt PLZ': int, 'Anschlussobjekt Ort': str, 'Anschlussobjekt PLZ/Ort': str,
                               'Regionalstrukturgrp.': str,
                               # 'Absatz Durchg. -1 (Sommer)':float, 'Absatz Durchg. -1 (Winter)':float,
                               # 'Absatz Durchg. -2 (Sommer)':float, 'Absatz Durchg. -2 (Winter)':float,
                               # 'Absatz Biogas -1':float, 'Absatz Biogas -2':float,
                               # 'Absatz CO2-Komp. -1':float, 'Absatz CO2-Komp. -2':float,
                               'Erlös Tot Jahr -1': float, 'Erlös Tot Jahr -2': float, 'Erlös Tot Jahr -3': float,
                               'Erlös Tot Jahr -4': float, 'Erlös Tot Jahr -5': float, 'Erlös Tot Jahr -6': float,
                               'Erlös Tot Jahr -7': float, 'Erlös Tot Jahr -8': float, 'Erlös Tot Jahr -9': float,
                               'Erlös Tot Jahr -10': float,
                               # 'Erlös AP Handel Jahr -1':float, 'Erlös AP Handel Jahr -2':float,
                               # 'Erlös AP Transport Jahr -1':float, 'Erlös AP Transport Jahr -2':float,
                               # 'Erlös AP Verteilung Jahr -1':float, 'Erlös AP Verteilung Jahr -2':float,
                               # 'Erlös AP Biogas Jahr -1':float, 'Erlös AP Biogas Jahr -2':float,
                               # 'Erlös AP CO2-Komp. Jahr -1':float, 'Erlös AP CO2-Komp. Jahr -2':float,
                               # 'Erlös LP Handel Jahr -1':float, 'Erlös LP Handel Jahr -2':float,
                               # 'Erlös LP Transport Jahr -1':float, 'Erlös LP Transport Jahr -2':float,
                               # 'Erlös LP Verteilung Jahr -1':float, 'Erlös LP Verteilung Jahr -2':float,
                               # 'Erlös AP Trsp Regional Jahr -1':float, 'Erlös AP Trsp Regional Jahr -2':float,
                               # 'Erlös AP Trsp Swissgas Jahr -1':float, 'Erlös AP Trsp Swissgas Jahr -2':float,
                               # 'Erlös LP Trsp Regional Jahr -1':float, 'Erlös LP Trsp Regional Jahr -2':float,
                               # 'Erlös LP Trsp Swissgas Jahr -1':float, 'Erlös LP Trsp Swissgas Jahr -2':float,
                               'Anzahl Apparate': int, 'Anzahl Apparate Objektart AH*': int, 'Leistung Nennwert': int,
                               'Apparat 1 Geräteart': str, 'Apparat 1 Bezeichnung': str, 'Apparat 1 Leistung': int,
                               'Apparat 1 Baujahr': float,
                               'Apparat 2 Geräteart': str, 'Apparat 2 Bezeichnung': str, 'Apparat 2 Leistung': int,
                               'Apparat 2 Baujahr': float,
                               'Apparat 3 Geräteart': str, 'Apparat 3 Bezeichnung': str, 'Apparat 3 Leistung': int,
                               'Apparat 3 Baujahr': float,
                               'Apparat 4 Geräteart': str, 'Apparat 4 Bezeichnung': str, 'Apparat 4 Leistung': int,
                               'Apparat 4 Baujahr': float,
                               'Apparat 5 Geräteart': str, 'Apparat 5 Bezeichnung': str, 'Apparat 5 Leistung': int,
                               'Apparat 5 Baujahr': float,
                               'Absatz Durchg. Jahr -1': float, 'Absatz Durchg. Jahr -2': float,
                               'Absatz Durchg. Jahr -3': float,
                               'Absatz Durchg. Jahr -4': float, 'Absatz Durchg. Jahr -5': float,
                               'Absatz Durchg. Jahr -6': float,
                               'Absatz Durchg. Jahr -7': float, 'Absatz Durchg. Jahr -8': float,
                               'Absatz Durchg. Jahr -9': float,
                               'Absatz Durchg. Jahr -10': float,
                               'Absatz Handel Jahr -1': float, 'Absatz Handel Jahr -2': float,
                               'Absatz Handel Jahr -3': float,
                               'Absatz Handel Jahr -4': float, 'Absatz Handel Jahr -5': float,
                               'Absatz Handel Jahr -6': float,
                               'Absatz Handel Jahr -7': float, 'Absatz Handel Jahr -8': float,
                               'Absatz Handel Jahr -9': float,
                               'Absatz Handel Jahr -10': float,
                               # 'Absatz Handel -1 (Sommer)':float, 'Absatz Handel -1 (Winter)':float,
                               # 'Absatz Handel -2 (Sommer)':float, 'Absatz Handel -2 (Winter)':float,
                               'Erlös AP Jahr -1': float, 'Erlös AP Jahr -2': float, 'Erlös AP Jahr -3': float,
                               'Erlös AP Jahr -4': float,
                               'Erlös AP Jahr -5': float, 'Erlös AP Jahr -6': float, 'Erlös AP Jahr -7': float,
                               'Erlös AP Jahr -8': float,
                               'Erlös AP Jahr -9': float, 'Erlös AP Jahr -10': float,
                               'Erlös LP Jahr -1': float, 'Erlös LP Jahr -2': float, 'Erlös LP Jahr -3': float,
                               'Erlös LP Jahr -4': float,
                               'Erlös LP Jahr -5': float, 'Erlös LP Jahr -6': float, 'Erlös LP Jahr -7': float,
                               'Erlös LP Jahr -8': float,
                               'Erlös LP Jahr -9': float, 'Erlös LP Jahr -10': float,
                               'Geschäftspartner Nummer': int, 'Geschäftspartner Name': str}
        full_zanla_df = pd.read_excel('Inputfiles/ZANLA_EXPORT_260106.xlsx', header=0,
                                      skiprows=[1],
                                      dtype=dtypes_zanla)  # skiprows resp. skipfooter to remove sum-row, (sum row from zanla)

        print('zanla_df cols & shape')
        print(full_zanla_df.columns.tolist())
        print(full_zanla_df.shape)
        print('\n')

        # Anzahl Columns reduzieren und notwendige Columns mit dtype ergänzen
        rel_cols = ['Anlage Nummer', 'Anlagenart', 'Tariftyp', 'Regionalstrukturgrp.', 'Anschlussobjekt (Haus)',
                    'Anschlussobjekt Strasse', 'Anschlussobjekt Ort', 'Anschlussobjekt PLZ/Ort', 'Leistung Nennwert',
                    'Apparat 1 Geräteart', 'Apparat 1 Baujahr', 'Apparat 1 Leistung', 'Apparat 1 Bezeichnung',
                    'Apparat 2 Geräteart', 'Apparat 2 Baujahr', 'Apparat 2 Leistung', 'Apparat 2 Bezeichnung',
                    'Apparat 3 Geräteart', 'Apparat 3 Baujahr', 'Apparat 3 Leistung', 'Apparat 3 Bezeichnung',
                    'Apparat 4 Geräteart', 'Apparat 4 Baujahr', 'Apparat 4 Leistung', 'Apparat 4 Bezeichnung',
                    'Apparat 5 Geräteart', 'Apparat 5 Baujahr', 'Apparat 5 Leistung', 'Apparat 5 Bezeichnung',
                    'Absatz Durchg. Jahr -1', 'Absatz Durchg. Jahr -2', 'Absatz Durchg. Jahr -3',
                    'Absatz Durchg. Jahr -4', 'Absatz Durchg. Jahr -5', 'Absatz Durchg. Jahr -6',
                    'Absatz Durchg. Jahr -7', 'Absatz Durchg. Jahr -8', 'Absatz Durchg. Jahr -9',
                    'Absatz Durchg. Jahr -10',
                    'Absatz Handel Jahr -1', 'Absatz Handel Jahr -2', 'Absatz Handel Jahr -3', 'Absatz Handel Jahr -4',
                    'Absatz Handel Jahr -5', 'Absatz Handel Jahr -6', 'Absatz Handel Jahr -7', 'Absatz Handel Jahr -8',
                    'Absatz Handel Jahr -9', 'Absatz Handel Jahr -10', 'Geschäftspartner Nummer']
        zanla_df = full_zanla_df[rel_cols]
        additional_cols_dict = {'VWZ': str, 'Gemeinde': str, 'DVG': str,
                                'durchschnittlicher Absatz durchgeleitet': float,
                                'durchschnittlicher Absatz gehandelt': float, 'Grosskunde': str,
                                'separat Modelliert': str, 'Apparat 1 Alter': float, 'Apparat 2 Alter': float,
                                'Apparat 3 Alter': float, 'Apparat 4 Alter': float, 'Apparat 5 Alter': float,
                                'stilllegungen': float}
        zanla_df = zanla_df.reindex(columns=zanla_df.columns.tolist() + list(additional_cols_dict.keys()))
        for col, dtype in additional_cols_dict.items():
            zanla_df[col] = zanla_df[col].astype(dtype)
        print(zanla_df.info())

        # VWZ: Verwendungszweck gemäss Anlagenart zuteilen
        anlagen_mapping = {'NHE': 'Heizung', 'AHE': 'Heizung',
                           'NBA': 'Prozess', 'ABA': 'Prozess',
                           'AUSP': 'Ausspeisung', 'EISP': 'Einspeistung',
                           'WVER': 'Wiederverkauf',
                           'WVDV': '???', 'ZVEN': '???', 'ZTRN': '???'}
        zanla_df['VWZ'] = zanla_df['Anlagenart'].map(anlagen_mapping)

        def heizungsalter_berechnen(baujahr):
            if baujahr > 1900:
                return 2026-baujahr
            else:
                return np.nan

        zanla_df['Apparat 1 Alter'] = zanla_df['Apparat 1 Baujahr'].map(heizungsalter_berechnen)
        zanla_df['Apparat 2 Alter'] = zanla_df['Apparat 2 Baujahr'].map(heizungsalter_berechnen)
        zanla_df['Apparat 3 Alter'] = zanla_df['Apparat 3 Baujahr'].map(heizungsalter_berechnen)
        zanla_df['Apparat 4 Alter'] = zanla_df['Apparat 4 Baujahr'].map(heizungsalter_berechnen)
        zanla_df['Apparat 5 Alter'] = zanla_df['Apparat 5 Baujahr'].map(heizungsalter_berechnen)

        # Gemeinde & DVG & Absatzmengen: Für die Adressen aus der ZANLA wird eine saubere Gemeindenzuordnung gemacht mit separatem File inkl. DVG-Angabe
        gemeinde_mapping = pd.read_csv('Inputfiles/Gemeinde_mapping_mit_dvg.csv', index_col=0, dtype=str, sep=';')
        gemeinde_mapping.index = gemeinde_mapping.index.str.replace('\xa0', '')
        index_list = gemeinde_mapping.index.to_list()
        i = 0
        for idx in zanla_df.index:
            if pd.isna(zanla_df.loc[idx, 'Anschlussobjekt PLZ/Ort']):
                adress_key = 'keineGemeinde'
            else:
                adress_key = zanla_df.loc[idx, 'Anschlussobjekt PLZ/Ort'].replace('\xa0', '')
            if adress_key not in gemeinde_mapping.index:
                i += 1
                print(adress_key, i)
            zanla_df.loc[idx, 'Gemeinde'] = gemeinde_mapping.loc[adress_key, 'Politische_Gemeinde']
            zanla_df.loc[idx, 'DVG'] = gemeinde_mapping.loc[adress_key, 'DVG']

            # Absatz durchgeleitet und gehandelt: Durchschnittlicher Verbrauch für jeden ZANLA-Eintrag abspeichern (für Handelsmengen und durchgeleitete Mengen)
            zanla_df.loc[idx, 'durchschnittlicher Absatz durchgeleitet'] = int(zanla_df.loc[
                                                                                   idx, ['Absatz Durchg. Jahr -1',
                                                                                         'Absatz Durchg. Jahr -2',
                                                                                         'Absatz Durchg. Jahr -3',
                                                                                         'Absatz Durchg. Jahr -4',
                                                                                         'Absatz Durchg. Jahr -5']].mean())
            zanla_df.loc[idx, 'durchschnittlicher Absatz gehandelt'] = int(zanla_df.loc[idx, ['Absatz Handel Jahr -1',
                                                                                              'Absatz Handel Jahr -2',
                                                                                              'Absatz Handel Jahr -3',
                                                                                              'Absatz Handel Jahr -4',
                                                                                              'Absatz Handel Jahr -5']].mean())
        print('zanla_df cols & shape')
        print(zanla_df.shape)
        print(zanla_df.columns.tolist())
        print('\n')

        ## --> neue Struktur prüfen mit E360-CH merger
        ## --> Verkaufsmengen und Transportmengen separat auswertbar machen

        # Grosskunde: Unterscheidung nach Handelsmenge
        def grosskunden_mapper(umsatz):
            grosskunden_identifier = 300000  # 300 MWh/a als Cutoff?
            if umsatz < grosskunden_identifier:
                return 'Kleinkunde'
            elif umsatz >= grosskunden_identifier:
                return 'Grosskunde'
            else:
                return 'Nicht zuortenbar'

        zanla_df['Grosskunde'] = zanla_df['durchschnittlicher Absatz gehandelt'].map(grosskunden_mapper)

        # separat modelliert: Ausklammern von Grosskunden für einen spezifischen Absenkpfad
        # ewz Liste (Ref Mail Christophe Wicht 31.03.2025 ergänzt mit Mails Andi Ebner 16.04.2025)
        separate_modellierung_list = [1000320, 1014166, #Regina-Kägi-Hof 13 direkt und Energie 360° Schweiz AG
                                      1021376, 1021380, 1021381, 1001199, 1011349, 1011350, # Herzogenmühle 2 direkt und Energie 360° Schweiz AG
                                      1020617, 1020619, 1021655, 1020616, 1020618, 1021657, # Josefstrasse 205 direkt und Energie 360° Schweiz AG
                                      1021383, # Enerprice Rathingen DE
                                      1021414] # Hagenholz 182C  --> ?
        zanla_df['separat Modelliert'] = 'Nein'
        separate_modellierung_index = zanla_df['Anlage Nummer'].isin(separate_modellierung_list)
        zanla_df.loc[separate_modellierung_index, 'separat Modelliert'] = 'Ja'

        zanla_df['spitzenlast_ignorieren'] = 'Nein'


        # Read Geodaten Export (Martin)
        geodaten_df = pd.read_excel('Inputfiles/CH Anschlussobjekte in Verbünde.xlsx',
                                  header=0, usecols=['aobj_id', 'energieverbund', 'status', 'quelle', 'erschliessungsjahr',
                                                     'realisierungswahrscheinlichkeit', 'gemeinde'], index_col='aobj_id')
        filling_idx = geodaten_df['energieverbund'].isna()
        geodaten_df.loc[filling_idx, 'energieverbund'] = 'placeholder_ev_' + geodaten_df.loc[filling_idx, 'gemeinde'].astype(str)
        geodaten_df.to_csv('Inputfiles/geodaten_01.csv', sep=';')


        def get_jahr_mittel(jahr):
            if isinstance(jahr, int):
                return_jahr = jahr
            elif isinstance(jahr, str) and '-' in jahr:
                start, end = map(int, jahr.split('-'))
                return_jahr =  int(round((start + end) / 2))
            elif jahr == 'Bestehend':
                return_jahr =  int(2025)    #Achtung: Alle bereits erschlossenen EV werden auf das aktuelle Jahr gesetzt. Die Absenkung der Absätze wird perspektivisch damit überbewertet. Durch den rolling Average bei den Absätzen aktuell voraussichtlich kein grosses Problem.
            elif isinstance(jahr, str):
                return_jahr =  int(jahr)
            else:
                return_jahr =  np.nan
            if return_jahr < 2025:
                return_jahr = 2025  # Alle Fernwärmejahre auf 2025 setzen (für Summe Fernwärme noch relevant (2024 fehlt in Zeilen, in Spalten ist ab 2025 okay). Umbau zu prüfen für nöchstes Jahr
            return return_jahr

        #Erschliessungsjahr Fernwärme Gemeinden (Zürich separat)
        geodaten_df['erschliessungsjahr_mittel'] = geodaten_df['erschliessungsjahr'].apply(get_jahr_mittel)
        geodaten_df['erschliessungsjahr_mittel'] = geodaten_df['erschliessungsjahr_mittel'].astype(float)
        filter_idx = geodaten_df.loc[(geodaten_df['gemeinde'] != 'Zürich') & (~geodaten_df['status'].isin([2, 4]))].index
        geodaten_df.drop(filter_idx, axis='index', inplace=True)
        geo_zanla_df = zanla_df.merge(geodaten_df[['energieverbund', 'status', 'quelle', 'erschliessungsjahr', 'realisierungswahrscheinlichkeit', 'erschliessungsjahr_mittel']], how='left', left_on='Anschlussobjekt (Haus)', right_index=True)
        update_erschliessungsjahr_dict = pd.read_excel('Inputfiles/Wärmeerschliessung_Ergänzung_Gemeinden.xlsx', header=0, index_col='energieverbund').to_dict()['Energielieferjahr']
        filter_idx = geo_zanla_df.loc[(geo_zanla_df['erschliessungsjahr_mittel'].isna()) & (geo_zanla_df['energieverbund'].isin(update_erschliessungsjahr_dict.keys()))].index
        geo_zanla_df.loc[filter_idx, 'Erschliessungsjahr'] = geo_zanla_df.loc[filter_idx, 'energieverbund'].map(update_erschliessungsjahr_dict)
        geo_zanla_df.loc[filter_idx, 'erschliessungsjahr_mittel'] = geo_zanla_df.loc[filter_idx, 'Erschliessungsjahr']

        #Stilllegungsjahre Gemeinden (Zürich separat)
        stilllegungen_data_gemeinden = pd.read_excel('Inputfiles/stilllegung_gemeinden.xlsx', header=0, index_col='gemeinde')
        fw_ausserhalb_idx = geo_zanla_df.loc[(geo_zanla_df['Gemeinde']!='Zürich') & (geo_zanla_df['DVG']=='Ja') & (geo_zanla_df['energieverbund'].notna())].index
        geo_zanla_df.loc[fw_ausserhalb_idx, 'stilllegungen'] = geo_zanla_df.loc[fw_ausserhalb_idx, 'Gemeinde'].map(stilllegungen_data_gemeinden['stilllegungsjahr_e'])
        # geo_zanla_df.loc[fw_ausserhalb_idx, 'Stilllegungsjahr'] = geo_zanla_df.loc[fw_ausserhalb_idx, 'erschliessungsjahr_mittel'] + 20 #Stilllegung auf 20 Jahre nach Energielieferung

        #Erschliessungsjahr Fernwärme & Stilllegungsjahre Zürich
        zonen_mapper_dtypes = {'stilllegungsjahr_a':float, 'stilllegungsjahr_e':float, 'Fernwärme_Lieferung':float, 'Fernwärme_ewz':float}
        zonen_data_zh = pd.read_excel('Inputfiles/Mapping_Zonen_Zuerich.xlsx', header=0, index_col='energieverbund', dtype=zonen_mapper_dtypes)
        fw_zh_idx = geo_zanla_df.loc[(geo_zanla_df['Gemeinde']=='Zürich') & (geo_zanla_df['energieverbund'].notna())].index
        lieferung_filter = geo_zanla_df.loc[fw_zh_idx, 'energieverbund'].map(zonen_data_zh['Fernwärme_Lieferung'])
        geo_zanla_df.loc[fw_zh_idx, 'erschliessungsjahr_mittel'] = np.where(lieferung_filter < 2026, lieferung_filter, lieferung_filter + zuerich_jahre_shifted)
        geo_zanla_df['erschliessungsjahr_mittel'] = geo_zanla_df['erschliessungsjahr_mittel'].replace(float(2024), float(2025))
        geo_zanla_df.loc[fw_zh_idx, 'erschliessungsjahr'] = geo_zanla_df.loc[fw_zh_idx, 'erschliessungsjahr_mittel'].astype(str)
        stilllegung_filter = geo_zanla_df.loc[fw_zh_idx, 'energieverbund'].map(zonen_data_zh['stilllegungsjahr_e'])
        geo_zanla_df.loc[fw_zh_idx, 'stilllegungen'] = np.where(stilllegung_filter < 2026, stilllegung_filter, stilllegung_filter + zuerich_jahre_shifted)

        #Selektion der Verbünde mit ewz Spitzenlast (separat modelliert)
        ewz_spitzenlast = zonen_data_zh.loc[zonen_data_zh['Fernwärme_ewz'] == 1].index.tolist()
        print(ewz_spitzenlast)
        spitzenlast_idx = geo_zanla_df.loc[geo_zanla_df['energieverbund'].isin(ewz_spitzenlast)].index
        geo_zanla_df.loc[spitzenlast_idx, 'spitzenlast_ignorieren'] = 'Ja'

        #Spitzenlast Volketswil
        volketswil_spitzenlast = geo_zanla_df.loc[geo_zanla_df['Gemeinde'].isin(['Effretikon', 'Volketswil', 'Schwerzenbach', 'Greifensee'])]['energieverbund'].dropna().unique().tolist()
        print(volketswil_spitzenlast)
        spitzenlast_idx = geo_zanla_df.loc[geo_zanla_df['energieverbund'].isin(volketswil_spitzenlast)].index
        geo_zanla_df.loc[spitzenlast_idx, 'spitzenlast_ignorieren'] = 'Ja'
        #Option

        #Gashaltegebiet G11 in Zürich
        gashaltegebiete_data_zh = pd.read_excel('Inputfiles/Stadt_Zuerich_Zone_G11_nur_Anlagen.xlsx', header=0, index_col='Anlage')
        geo_zanla_df = geo_zanla_df.merge(gashaltegebiete_data_zh, left_on='Anlage Nummer', right_index=True, how='left')

        #BBV-Tarife / 80% Biogaslösungen
        bbv_tarife = pd.read_excel('Inputfiles/BBV_Tarife_SAP.xlsx', header=0, index_col='Anlage Nummer')
        geo_zanla_df = geo_zanla_df.merge(bbv_tarife, left_on='Anlage Nummer', right_index=True, how='left')
        #print('bbv_tarife')
        #print(geo_zanla_df.columns)


        # Save csv for easy read-in later
        geo_zanla_df.index.name = 'index_name'
        geo_zanla_df.to_csv('Inputfiles/geo_zanla_data_ZH_shift_' + str(zuerich_jahre_shifted) + '.csv', sep=';')
    else:
        print('Inputfiles/geo_zanla_data_ZH_shift_' + str(zuerich_jahre_shifted) + '.csv')
        geo_zanla_df = pd.read_csv('Inputfiles/geo_zanla_data_ZH_shift_' + str(zuerich_jahre_shifted) + '.csv', sep=';', header=0)
        geo_zanla_df.set_index('index_name', inplace=True)
    return geo_zanla_df


def zgeraus_data_reader(new_read=True, remove_lebensdauer_under=0):
    if new_read:
        zgeraus_data = pd.read_excel('Inputfiles/ZGRAUS_EXPORT.XLSX', header=0, parse_dates=['Einbaudatum', 'Ausbaudatum'], index_col='Anlage', dtype={'Hausnummer':str, 'Sernr (Zähler)': str})
        zgeraus_data['Adresse'] = zgeraus_data['Ort'] + ' ' + zgeraus_data['Strasse Hausnummer']
        zgeraus_data['Status'] = ''
        unique_platz = list(sorted(zgeraus_data['Technischer Platz'].unique().tolist()))

        category_dict = {'erste aktive Heizung': 0,
                         'ersetzte und aktive Heizung': 0,
                         'inaktive letzte Heizung': 0}
        tot_platz_zahl = len(unique_platz)
        j = 0
        k = 0

        for platz in unique_platz:
            sub_frame = zgeraus_data.loc[zgeraus_data['Technischer Platz'] == platz]
            number_entries = sub_frame.shape[0]
            active_heaters = sub_frame.loc[sub_frame['Ausbaudatum'].isnull()].shape[0]
            decommissioned_heaters = sub_frame.loc[sub_frame['Ausbaudatum'] > pd.Timestamp('2000-01-01')].shape[0]

            if active_heaters > 0 and decommissioned_heaters == 0:
                category_dict['erste aktive Heizung'] += 1
                zgeraus_data.loc[sub_frame.index, 'Status'] = 'erste aktive Heizung'
            elif active_heaters == 0 and decommissioned_heaters > 0:
                category_dict['inaktive letzte Heizung'] += 1
                zgeraus_data.loc[sub_frame.index, 'Status'] = 'inaktive letzte Heizung'
            elif active_heaters > 0 and decommissioned_heaters > 0:
                category_dict['ersetzte und aktive Heizung'] += 1
                zgeraus_data.loc[sub_frame.index, 'Status'] = 'ersetzte und aktive Heizung'
                # Unterscheidungen und detailbetrachtungen ggf. nötig. --> Leistung ausgebaut mit Leistung eingebaut vergleichen?
            j += 1
            k += 1
            if k == 1000:
                print(j, j / tot_platz_zahl)
                k = 0

        print(zgeraus_data['Status'].value_counts())

        print(category_dict)

        zgeraus_data['Heizungsalter bei Ausbau'] = zgeraus_data['Ausbaudatum'].sub(zgeraus_data['Einbaudatum']).dt.days / 365
        zgeraus_data = zgeraus_data.loc[zgeraus_data['Heizungsalter bei Ausbau'] > remove_lebensdauer_under]

        # Filter frühe Ausbaujahre, die mit Einbaujahr 1987 eine Verzerrung drin haben (frühe Jahre haben im Schnitt niedrigere Ausbaudaten)
        zgeraus_data_cleaned = zgeraus_data.loc[(zgeraus_data['Ausbaudatum'] > pd.Timestamp('2015-12-31')) & (zgeraus_data['Einbaudatum'] > pd.Timestamp('1987-12-31'))]   # Einbauten nicht gefiltert. Bei stärkerer Nutzung von Einbaudaten aufpassen
        zgeraus_data_cleaned.to_csv('Inputfiles/ZGRAUS_EXPORT_v2.csv', sep=';')

    else:
        zgeraus_data_cleaned = pd.read_csv('Inputfiles/ZGRAUS_EXPORT_v2.csv', sep=';', header=0, index_col=0, parse_dates=['Einbaudatum', 'Ausbaudatum'], dtype={'Hausnummer':str, 'Sernr (Zähler)': str})

    return zgeraus_data_cleaned

#Analyse
def lebensdauer_analysis(zgeraus_data):
    options_dict = {'ganzes_gebiet': zgeraus_data,
                    'St_ZH': zgeraus_data.loc[zgeraus_data['Ort'] == 'Zürich'].copy(),
                    'ausserhalb': zgeraus_data.loc[zgeraus_data['Ort'] != 'Zürich'].copy()}
    leistungs_dict = {'alle_Leistungen': range(0, 100000),
                      'kleine_Leistungen': range(0, 31),
                      'mittlere_Leistungen': range(31, 101),
                      'grosse_Leistungen': range(101, 100000)}
    export_frame = pd.DataFrame(index=['alle_Leistungen_Anzahl', 'alle_Leistungen_Durchschnitt',
                                       'kleine_Leistungen_Anzahl', 'kleine_Leistungen_Durchschnitt',
                                       'mittlere_Leistungen_Anzahl', 'mittlere_Leistungen_Durchschnitt',
                                       'grosse_Leistungen_Anzahl', 'grosse_Leistungen_Durchschnitt'],
                                columns=['ganzes_gebiet_total', 'St_ZH_total', 'ausserhalb_total',
                                         'ganzes_gebiet_ersatz', 'St_ZH_ersatz', 'ausserhalb_ersatz',
                                         'ganzes_gebiet_ausbau', 'St_ZH_ausbau', 'ausserhalb_ausbau'])

    # Berechnungen & Plots zu Heizungsaltern und Absenkpfaden
    def print_plots(einbau, ausbau, heizungsalter, save_name_prefix, title_prefix):
        y_lim = 400
        bins_range = []
        for year in range(2015, 2027):
            bins_range.append(pd.to_datetime(str(year) + '-01-01'))
            bins_range.append(pd.to_datetime(str(year) + '-04-01'))
            bins_range.append(pd.to_datetime(str(year) + '-07-01'))
            bins_range.append(pd.to_datetime(str(year) + '-10-01'))

        bins_range_heizungsalter = [x for x in range(int(max(heizungsalter['total'])) + 1)]

        stat_dict = {'total':
                         {'len': len(heizungsalter['total']),
                          'mean': heizungsalter['total'].mean().round(1),
                          'median': heizungsalter['total'].median()},
                     'ersetzte und aktive Heizung':
                         {'len': len(heizungsalter['ersetzte und aktive Heizung']),
                          'mean': heizungsalter['ersetzte und aktive Heizung'].mean().round(1),
                          'median': heizungsalter['ersetzte und aktive Heizung'].median()},
                     'inaktive letzte Heizung':
                         {'len': len(heizungsalter['inaktive letzte Heizung']),
                          'mean': heizungsalter['inaktive letzte Heizung'].mean().round(1),
                          'median': heizungsalter['inaktive letzte Heizung'].median()}}
        suptitle_dict = {'total': 'Total (' + str(stat_dict['total']['len']) + ')\nmean: ' + str(
            stat_dict['total']['mean']) + ', median: ' + str(stat_dict['total']['median']),
                         'ersetzte und aktive Heizung': 'Total (' + str(
                             stat_dict['ersetzte und aktive Heizung']['len']) + ')\nmean: ' + str(
                             stat_dict['ersetzte und aktive Heizung']['mean']) + ', median: ' + str(
                             stat_dict['ersetzte und aktive Heizung']['median']),
                         'inaktive letzte Heizung': 'Total (' + str(
                             stat_dict['inaktive letzte Heizung']['len']) + ')\nmean: ' + str(
                             stat_dict['inaktive letzte Heizung']['mean']) + ', median: ' + str(
                             stat_dict['inaktive letzte Heizung']['median'])}

        fig, axs = plt.subplots(3, figsize=(16, 16), dpi=300)
        axs[0].hist(ausbau['total'], bins=bins_range)
        axs[1].hist(ausbau['ersetzte und aktive Heizung'], bins=bins_range)
        axs[2].hist(ausbau['inaktive letzte Heizung'], bins=bins_range)
        axs[0].set_xlim([pd.to_datetime('2015-01-01'), pd.to_datetime('2027-01-01')])
        axs[1].set_xlim([pd.to_datetime('2015-01-01'), pd.to_datetime('2027-01-01')])
        axs[2].set_xlim([pd.to_datetime('2015-01-01'), pd.to_datetime('2027-01-01')])
        axs[0].set_ylim([0, y_lim])
        axs[1].set_ylim([0, y_lim])
        axs[2].set_ylim([0, y_lim])
        axs[0].title.set_text('Total')
        axs[1].title.set_text('Heizungsersatz')
        axs[2].title.set_text('keine neue Heizung')
        fig.suptitle(str(title_prefix) + 'Ausbaudatum')
        fig.tight_layout()
        fig.savefig('Outputfiles/Plots/' + save_name_prefix + 'Ausbaudaten.png')
        plt.close()

        fig, axs = plt.subplots(3, figsize=(16, 16), dpi=300)
        axs[0].hist(einbau['total'], bins=bins_range)
        axs[1].hist(einbau['ersetzte und aktive Heizung'], bins=bins_range)
        axs[2].hist(einbau['inaktive letzte Heizung'], bins=bins_range)
        axs[0].set_xlim([pd.to_datetime('2015-01-01'), pd.to_datetime('2027-01-01')])
        axs[1].set_xlim([pd.to_datetime('2015-01-01'), pd.to_datetime('2027-01-01')])
        axs[2].set_xlim([pd.to_datetime('2015-01-01'), pd.to_datetime('2027-01-01')])
        axs[0].set_ylim([0, y_lim])
        axs[1].set_ylim([0, y_lim])
        axs[2].set_ylim([0, y_lim])
        axs[0].title.set_text('Total')
        axs[1].title.set_text('Heizungsersatz')
        axs[2].title.set_text('keine neue Heizung')
        fig.suptitle(str(title_prefix) + 'Einbaudatum')
        fig.tight_layout()
        fig.savefig('Outputfiles/Plots/' + save_name_prefix + 'Einbaudatum.png')
        plt.close()

        fig, axs = plt.subplots(3, figsize=(16, 16), dpi=300)
        axs[0].hist(heizungsalter['total'], bins=bins_range_heizungsalter)
        axs[1].hist(heizungsalter['ersetzte und aktive Heizung'], bins=bins_range_heizungsalter)
        axs[2].hist(heizungsalter['inaktive letzte Heizung'], bins=bins_range_heizungsalter)
        axs[0].set_ylim([0, 1250])
        axs[1].set_ylim([0, 1250])
        axs[2].set_ylim([0, 1250])
        axs[0].title.set_text('Total')
        axs[1].title.set_text('Heizungsersatz')
        axs[2].title.set_text('keine neue Heizung')
        fig.suptitle(str(title_prefix) + 'Lebensdauer der Heizung bei Ausbau')
        fig.tight_layout()
        fig.savefig('Outputfiles/Plots/' + save_name_prefix + 'Heizungsalter.png')
        plt.close()

        fig, axs = plt.subplots(1, 3, figsize=(16, 16), dpi=300)
        axs[0].boxplot(heizungsalter['total'], notch=True, whis=(5, 95), showmeans=True)
        axs[1].boxplot(heizungsalter['ersetzte und aktive Heizung'], notch=True, whis=(5, 95), showmeans=True)
        axs[2].boxplot(heizungsalter['inaktive letzte Heizung'], notch=True, whis=(5, 95), showmeans=True)
        axs[0].set_ylim([0, 40])
        axs[1].set_ylim([0, 40])
        axs[2].set_ylim([0, 40])
        axs[0].title.set_text(suptitle_dict['total'])
        axs[1].title.set_text(suptitle_dict['ersetzte und aktive Heizung'])
        axs[2].title.set_text(suptitle_dict['inaktive letzte Heizung'])
        fig.suptitle(str(title_prefix) + 'Lebensdauer der Heizung bei Ausbau')
        fig.tight_layout()
        fig.savefig('Outputfiles/Plots/' + save_name_prefix + 'Heizungsalter_Boxplot.png')
        plt.close()


        distributions = dict(keys=['total', 'ersetzte und aktive Heizung', 'inaktive letzte Heizung'])
        x = np.linspace(0, 38, 100)
        for option in ['total', 'ersetzte und aktive Heizung', 'inaktive letzte Heizung']:
            ausbaudaten = heizungsalter[option].round(0)
            mu, std = stats.norm.fit(ausbaudaten)
            distributions[option] = {'fit': stats.norm.pdf(x, mu, std), 'factors': round(mu, 1)}

        fig, axs = plt.subplots(3, figsize=(16, 16), dpi=300)
        x = np.linspace(0, 38, 100)
        axs[0].hist(heizungsalter['total'], bins=bins_range_heizungsalter, density=True)
        axs[0].plot(x, distributions['total']['fit'], 'k')
        axs[1].hist(heizungsalter['ersetzte und aktive Heizung'], bins=bins_range_heizungsalter, density=True)
        axs[1].plot(x, distributions['ersetzte und aktive Heizung']['fit'], 'k')
        axs[2].hist(heizungsalter['inaktive letzte Heizung'], bins=bins_range_heizungsalter, density=True)
        axs[2].plot(x, distributions['inaktive letzte Heizung']['fit'], 'k')
        axs[0].title.set_text('Total, Mittelwert: ' + str(distributions['total']['factors']))
        axs[1].title.set_text('Heizungsersatz, Mittelwert: ' + str(distributions['ersetzte und aktive Heizung']['factors']))
        axs[2].title.set_text('keine neue Heizung, Mittelwert: ' + str(distributions['inaktive letzte Heizung']['factors']))
        fig.suptitle(str(title_prefix) + 'Lebensdauer der Heizung bei Ausbau und gefittete Verteilung')
        fig.tight_layout()
        fig.savefig('Outputfiles/Plots/' + save_name_prefix + 'Heizungsalter_fitted.png')
        plt.close()


    for option in options_dict.keys():
        for leistungsklasse in leistungs_dict.keys():
            data_frame = options_dict[option].loc[options_dict[option]['Nennleistung'].isin(leistungs_dict[leistungsklasse])].copy()
            ausbau_frame = data_frame.loc[data_frame['Ausbaudatum'].notna()].copy()
            ausbau_frame['Heizungsalter bei Ausbau'] = ausbau_frame['Ausbaudatum'].sub(
                ausbau_frame['Einbaudatum']).dt.days / 365
            ausbau_frame['Heizungsalter bei Ausbau'] = ausbau_frame['Heizungsalter bei Ausbau'].round(0)
            heizungsalter = {'total': ausbau_frame['Heizungsalter bei Ausbau'],
                             'ersetzte und aktive Heizung':
                                 ausbau_frame.loc[ausbau_frame['Status'] == 'ersetzte und aktive Heizung'][
                                     'Heizungsalter bei Ausbau'],
                             'inaktive letzte Heizung':
                                 ausbau_frame.loc[ausbau_frame['Status'] == 'inaktive letzte Heizung'][
                                     'Heizungsalter bei Ausbau']}
            ausbau = {'total': ausbau_frame['Ausbaudatum'],
                      'ersetzte und aktive Heizung':
                          ausbau_frame.loc[ausbau_frame['Status'] == 'ersetzte und aktive Heizung']['Ausbaudatum'],
                      'inaktive letzte Heizung': ausbau_frame.loc[ausbau_frame['Status'] == 'inaktive letzte Heizung'][
                          'Ausbaudatum']}
            einbau = {'total': data_frame['Einbaudatum'],
                      'ersetzte und aktive Heizung':
                          data_frame.loc[data_frame['Status'] == 'ersetzte und aktive Heizung']['Einbaudatum'],
                      'inaktive letzte Heizung': data_frame.loc[data_frame['Status'] == 'inaktive letzte Heizung'][
                          'Einbaudatum']}
            print_plots(einbau=einbau, ausbau=ausbau, heizungsalter=heizungsalter,
                        save_name_prefix=str(option) + '_' + str(leistungsklasse) + '_',
                        title_prefix=str(option) + '_' + str(leistungsklasse) + '_')
            export_frame.loc[leistungsklasse + '_Anzahl', option + '_total'] = len(heizungsalter['total'])
            export_frame.loc[leistungsklasse + '_Durchschnitt', option + '_total'] = heizungsalter[
                'total'].mean().round(1)
            export_frame.loc[leistungsklasse + '_Anzahl', option + '_ersatz'] = len(
                heizungsalter['ersetzte und aktive Heizung'])
            export_frame.loc[leistungsklasse + '_Durchschnitt', option + '_ersatz'] = heizungsalter[
                'ersetzte und aktive Heizung'].mean().round(1)
            export_frame.loc[leistungsklasse + '_Anzahl', option + '_ausbau'] = len(
                heizungsalter['inaktive letzte Heizung'])
            export_frame.loc[leistungsklasse + '_Durchschnitt', option + '_ausbau'] = heizungsalter[
                'inaktive letzte Heizung'].mean().round(1)

    export_frame.to_csv('Outputfiles/Lebensdauern_nach_Gruppe.csv', sep=';')

#Modellierung
def absenkpfad_generation(zanla_data, zgeraus_data, simulations = 1000, plot=False, new_read=True, fitted=False, lifetime_extension=0):

    #Subfuntion um eine simulierte Restlebensdauer für eine Heizung zu bekommen
    def simulate_ausbau(alter, probability_distribution):
        # Returns die simulierte Restlebensdauer der Geräte
        if alter >= 37:
            return 1
        else:
            if alter < 0:
                specific_probability = probability_distribution[0]
            else:
                specific_probability = probability_distribution[alter]
            lebensdauer = int(np.random.choice(specific_probability.index, 1, p=specific_probability.values)[0])
            return lebensdauer - alter

    #Subfunction um eine Absenkpfad zu modellieren (Mittels simulate_ausbau für die einzelnen Heizungen)
    def absenkpfad_simulieren(heizungsdaten, ausbaudaten, simulations=1000, jahre=30, fitted=True, lifetime_extension=0, plot=True, save_name=''):
        # Lebensdauer Wahrscheinlichkeit (propability_set) aus Ausbaudaten erzeugen
        probability_set = {}
        if fitted:
            mu, std = stats.norm.fit(ausbaudaten)
            mu += lifetime_extension
            distribution = stats.norm.pdf(range(38), mu, std).tolist()

            for jahr in range(38):  # Ausbaudaten nur bis 37 Jahre alter im System
                probability = distribution[jahr:]
                norm_faktor = sum(distribution[jahr:])
                probability_set[jahr] = pd.Series(index=range(jahr, 38), data=[x / norm_faktor for x in probability])

        else:
            for jahr in range(38):  # Ausbaudaten nur bis 37 Jahre alter im System
                probability = ausbaudaten.loc[ausbaudaten > jahr]
                probability_set[jahr] = probability.value_counts(normalize=True).sort_index()

        # Frame für Absenkpfad aufsetzen
        simulated_results = pd.DataFrame(index=range(simulations), columns=range(jahre))
        for idx in simulated_results.index:
            heizungsdaten['Restlebensdauer_simuliert'] = heizungsdaten['Apparat 1 Alter'].apply(lambda x: simulate_ausbau(x, probability_distribution=probability_set))
            simulated_yearly_gas_usage = pd.Series(index=simulated_results.columns)
            for jahr in simulated_results.columns:
                simulated_yearly_gas_usage.loc[jahr] = \
                heizungsdaten.loc[heizungsdaten['Restlebensdauer_simuliert'] > jahr]['durchschnittlicher Absatz gehandelt'].sum()
            simulated_results.loc[idx, :] = simulated_yearly_gas_usage
        absenkpfad = simulated_results.mean()

        if plot:
            fig, ax = plt.subplots(1, figsize=(16, 16), dpi=300)
            for i in range(simulations):
                ax.plot(range(jahre), simulated_results.loc[i].values)
            ax.plot(range(jahre), absenkpfad.values, color='k', linestyle='dashed')
            # ax.title.set_text('')
            fig.suptitle(str(save_name) + ' Modellierter Absenkpfad mit ' + str(
                simulations) + ' Simulationen und Lebensdauer + ' + str(lifetime_extension))
            fig.tight_layout()
            plt.savefig('Outputfiles/Plots/Absenkpfad_' + save_name + '.png')
            plt.close()

        return absenkpfad

    if new_read:
        t_start = time.time()
        ausbaudaten = zgeraus_data['Heizungsalter bei Ausbau'].round(0)
        heizungsdaten = zanla_data.loc[zanla_data['Apparat 1 Alter'].notna()].dropna(subset=['Apparat 1 Alter'])
        data_zuerich = heizungsdaten.loc[heizungsdaten['Anschlussobjekt Ort']=='Zürich'].copy()
        data_wareme_zuerich = data_zuerich.loc[data_zuerich['VWZ']=='Heizung'].copy()
        absenkpfad_zuerich = absenkpfad_simulieren(data_wareme_zuerich, ausbaudaten, simulations=simulations, fitted=fitted, lifetime_extension=lifetime_extension, plot=plot, save_name='Stadt_Zürich')
        get_time(t_start, print_text='Absenkpfad_ZH done')
        data_ausserhalb = heizungsdaten.loc[heizungsdaten['Anschlussobjekt Ort']!='Zürich'].copy()
        data_wareme_ausserhalb = data_ausserhalb.loc[data_ausserhalb['VWZ']=='Heizung'].copy()
        absenkpfad_ausserhalb = absenkpfad_simulieren(data_wareme_ausserhalb, ausbaudaten, simulations=simulations, fitted=fitted, lifetime_extension=lifetime_extension, plot=plot, save_name='Ausserhalb')
        get_time(t_start, print_text='Absenkpfad_ausserhalb done')
        data_alle_gebiete = heizungsdaten.loc[heizungsdaten['VWZ']=='Heizung'].copy()
        absenkpfad_alle_gebiete = absenkpfad_simulieren(data_alle_gebiete, ausbaudaten, simulations=simulations, fitted=fitted, lifetime_extension=lifetime_extension, plot=plot, save_name='Alle_Gebiete')
        get_time(t_start, print_text='Absenkpfad_alle_gebiete done')

        if plot:
            fig, ax = plt.subplots(1, figsize=(16, 16), dpi=300)
            ax.plot(range(len(absenkpfad_zuerich.index)), absenkpfad_zuerich.values, color='b', linestyle='dashed')
            ax.plot(range(len(absenkpfad_ausserhalb.index)), absenkpfad_ausserhalb.values, color='r', linestyle='dotted')
            ax.plot(range(len(absenkpfad_alle_gebiete.index)), absenkpfad_alle_gebiete.values, color='k')
            # ax.title.set_text('')
            fig.tight_layout()
            fig.savefig('Outputfiles/Plots/Vergleich_Absenkpfade_' + str(simulations) + '_simulations_lifetime_plus_' + str(lifetime_extension) + '.png')
            plt.close()

        export_frame = pd.DataFrame(columns=range(30))
        export_frame.loc['alle_gebiete', :] = absenkpfad_alle_gebiete
        export_frame.loc['Stadt_Zürich', :] = absenkpfad_zuerich
        export_frame.loc['Ausserhalb', :] = absenkpfad_ausserhalb

        jahres_range = list(range(2022, 2052))
        export_frame.columns = jahres_range
        for gebiet in export_frame.index:
            export_frame.loc[gebiet + '_%'] = export_frame.loc[gebiet] / export_frame.loc[gebiet, 2025]

        export_frame.to_csv('Outputfiles/Absenkpfade_modelliert_' + str(simulations) + '_simulations_lifetime_plus_' + str(lifetime_extension) + '.csv', sep=';')
        return export_frame
    else:
        return_frame = pd.read_csv('Outputfiles/Absenkpfade_modelliert_' + str(simulations) + '_simulations_lifetime_plus_' + str(lifetime_extension) + '.csv', sep=';', header=0, index_col=0)
        return_frame.columns = return_frame.columns.astype(int)
        return return_frame


def calculate_scenario(zanla_data, absatz_option, modell_varianten_name, set_absenkpfad, set_prozesspfad, halterate_heizungen_80_bis_2030, halterate_heizungen_80_post_2030, save_appendix=''):

    def absatz_modellieren(initial_sum, total_heizungen, vwz, fw, absenkpfad_heizung, absenkpfad_prozess, halterate_heizungen_80_bis_2030, halterate_heizungen_80_post_2030, stilllegung=2100):
        jahres_range = list(range(2025, 2051))

        def calc_heizung_jahreswert(initial_sum, vorjahreswert_biogas, jahresrueckgang, jahr, fw, stilllegung, absenkpfad_heizung_jahr, halterate_heizungen_80_bis_2030, halterate_heizungen_80_post_2030):
            if jahr >= stilllegung:
                jahreswert = 0
            else:
                if fw in ['keine_fernwärme', 'fernwärme_ohne_lieferdatum']:
                    jahreswert = initial_sum * absenkpfad_heizung_jahr
                elif fw  == '80%_Biogas':
                    if jahr == 2025:
                        jahreswert = initial_sum
                    elif jahr <= 2030:
                        jahreswert = vorjahreswert_biogas + jahresrueckgang * halterate_heizungen_80_bis_2030
                    else:
                        jahreswert = vorjahreswert_biogas + jahresrueckgang * halterate_heizungen_80_post_2030
                elif jahr < int(fw):
                    jahreswert = initial_sum * absenkpfad_heizung_jahr
                elif jahr < int(fw) + 5: #erstes Anschlussfenster vorbei, Gasnachfrage gesenkt
                    jahreswert = initial_sum * absenkpfad_heizung_jahr * 0.44
                else:   #nach zweitem Anschlussfenster, Gasnachfrage weiter gesenkt
                    jahreswert = initial_sum * absenkpfad_heizung_jahr * 0.3
            return jahreswert

        return_series = pd.Series(index=jahres_range)
        if vwz == 'Prozess':
            for jahr in jahres_range:
                return_series[jahr] = initial_sum * absenkpfad_prozess[jahr]
        if vwz == 'Wiederverkauf':
            for jahr in jahres_range:
                return_series[jahr] = initial_sum  # keine Absenkung angenommen (erster Wurf)
        if vwz in ['Einspeisung', 'Ausspeisung', '???']:
            for jahr in jahres_range:
                return_series[jahr] = initial_sum  # keine Absenkung angenommen (erster Wurf)
        if vwz == 'Heizung':
            for jahr in jahres_range:
                jahresrueckgang = total_heizungen * (absenkpfad_heizung[jahr-1] - absenkpfad_heizung[jahr])
                if jahr == 2025:
                    vorjahreswert_biogas = 0
                else:
                    vorjahreswert_biogas = return_series[jahr-1]
                return_series[jahr] = calc_heizung_jahreswert(initial_sum=initial_sum, vorjahreswert_biogas=vorjahreswert_biogas, jahresrueckgang=jahresrueckgang, jahr=jahr, fw=fw, stilllegung=stilllegung, absenkpfad_heizung_jahr=absenkpfad_heizung[jahr],
                                                          halterate_heizungen_80_bis_2030= halterate_heizungen_80_bis_2030, halterate_heizungen_80_post_2030= halterate_heizungen_80_post_2030)
        if vwz == 'Spitzenlast':
            if fw in ['keine_fernwärme', 'fernwärme_ohne_lieferdatum', '80%_Biogas']:
                for jahr in jahres_range:
                    return_series[jahr] = 0
            else:
                if fw <= 2025:
                    final_fw_energy = initial_sum * 1.17 * absenkpfad_heizung[2025]  # Annahme: 70% der Gaskunden und 60/40 Ölkunden wechseln zum Verbund, FW-Lieferung im Zweifelsfall auf 2025 gesetzt
                else:
                    final_fw_energy = initial_sum * 1.17 * absenkpfad_heizung[fw]  # Annahme: 70% der Gaskunden und 60/40 Ölkunden wechseln zum Verbund
                for jahr in jahres_range:
                    if jahr < fw:
                        return_series[jahr] = 0  # Absenkung analog Fade-Out vor fw-Lieferung
                    elif jahr < fw + 5:
                        return_series[jahr] = final_fw_energy * 0.08  # Absenkung nach Endausbau (5 Jahre nach FW-Lieferung) + Spitzenlast
                    else:
                        return_series[jahr] = final_fw_energy * 0.1  # Absenkung zwischen FW-Lieferung und Endausbau + Spitzenlast des bisherigen Ausbaus
        return return_series

    unique_gemeinden = zanla_data['Gemeinde'].unique().tolist()
    fw_jahre = range(2025, 2051)
    modeling_range = list(range(2025, 2051))
    area_mapping = ['keine_fernwärme', 'fernwärme_ohne_lieferdatum', '80%_Biogas'] + list(fw_jahre) #80% Biogas neu --> Über Tarif die Startwerte setzen nach Gemeinde
    resultframe = pd.DataFrame(columns=['Gemeinde', 'DVG', 'VWZ', 'FW', 'Grosskunde'] + modeling_range)


    i = 0 # laufender Index

    # ewz Fernwärme separat modelliert
    separate_modellierung_verbrauchsdaten_ewz = pd.read_excel('Inputfiles/SEPARATE_MODELLIERUNG_ewz_Fernwärme.xlsx', header=0, index_col=0) #wie letztes Jahr, aber konstant -50 GWh (In Absprache mit Christophe Wicht gesetzt)
    resultframe.loc[i, 'VWZ'] = 'Spitzenlast'
    resultframe.loc[i, 'FW'] = 'ewz_modellierung'
    resultframe.loc[i, 'Gemeinde'] = 'Zürich'
    resultframe.loc[i, 'Grosskunde'] = 'Spitzenlast'  # Annahme Spitzenlast ist immer Grosskunde
    resultframe.loc[i, 'DVG'] = 'Ja'
    ewz_spitzenlast = separate_modellierung_verbrauchsdaten_ewz.loc['Summe', modeling_range] * 1000000
    if modell_varianten_name == 'Referenz':
        pass
    elif modell_varianten_name == 'verschärft':
        for year in modeling_range:
            if year <= 2030:
                ewz_spitzenlast[year] -= 0
            elif year <= 2040:
                ewz_spitzenlast[year] -= 50000000
            else:
                ewz_spitzenlast[year] -= 100000000
    elif modell_varianten_name == 'gelockert':
        for year in modeling_range:
            if year <= 2035:
                ewz_spitzenlast[year] -= 0
            else:
                ewz_spitzenlast[year] -= 50000000
    else:
        print('error')
    resultframe.loc[i, modeling_range] = ewz_spitzenlast.values
    i+=1

    # Volketswil Fernwärme separat modelliert (Volketswil und Gemeinden explizit ausnehmen)
    separate_modellierung_verbrauchsdaten_volketswil = pd.read_excel('Inputfiles/SEPARATE_MODELLIERUNG_Cluster_Volketswil_Fernwärme.xlsx' ,header=0, index_col=0) #wie letztes Jahr, aber konstant -50 GWh (In Absprache mit Christophe Wicht gesetzt)
    resultframe.loc[i, 'VWZ'] = 'Spitzenlast'
    resultframe.loc[i, 'FW'] = 'volketswil_modellierung'
    resultframe.loc[i, 'Gemeinde'] = 'Volketswil'
    resultframe.loc[i, 'Grosskunde'] = 'Spitzenlast'  # Annahme Spitzenlast ist immer Grosskunde
    resultframe.loc[i, 'DVG'] = 'Ja'
    resultframe.loc[i, modeling_range] = separate_modellierung_verbrauchsdaten_volketswil.loc['Summe', modeling_range].values
    i+=1

    # Gashaltegebiete
    gemeinden_mit_gashaltegebiet = zanla_data.loc[zanla_data['Gashaltegebiet'].notna(), 'Gemeinde'].unique().tolist()
    for gemeinde in gemeinden_mit_gashaltegebiet:
        for kundenkategorie in ['Kleinkunde', 'Grosskunde']:
            gashalte_initial_sum = zanla_data.loc[(zanla_data['VWZ'] == 'Heizung') & (zanla_data['Gemeinde'] == gemeinde) & (zanla_data['Gashaltegebiet'].notna()) & (zanla_data['Grosskunde'] == kundenkategorie)][absatz_option].sum()
            #gashalte_initial_sum = zanla_data.loc[(zanla_data['VWZ'] == 'Heizung') & (zanla_data['Gemeinde'] == gemeinde) & (zanla_data['Gashaltegebiet'].notna()) & (zanla_data['Grosskunde'] == kundenkategorie)][absatz_option].count()
            resultframe.loc[i, 'VWZ'] = 'Heizung'
            resultframe.loc[i, 'FW'] = 'Gashaltegebiet_regulär'
            resultframe.loc[i, 'Gemeinde'] = gemeinde
            resultframe.loc[i, 'Grosskunde'] = kundenkategorie
            resultframe.loc[i, 'DVG'] = 'Ja'
            resultframe.loc[i, modeling_range] = set_absenkpfad * gashalte_initial_sum
            i+=1
            resultframe.loc[i, 'VWZ'] = 'Heizung'
            resultframe.loc[i, 'FW'] = 'Gashaltegebiet_80%_Biogas'
            resultframe.loc[i, 'Gemeinde'] = gemeinde
            resultframe.loc[i, 'Grosskunde'] = kundenkategorie
            resultframe.loc[i, 'DVG'] = 'Ja'
            resultframe.loc[i, modeling_range] = set_absenkpfad.apply(lambda x: (1-x)) * gashalte_initial_sum * 0.8 #Wechsel auf Biogas in Gashaltegebiet
            i+=1


    resultframe.loc[i, 'VWZ'] = 'Gasverstromung'
    resultframe.loc[i, 'FW'] = 'nicht betrachtet'
    resultframe.loc[i, 'Gemeinde'] = 'Netzgebiet Ganeos'
    resultframe.loc[i, 'Grosskunde'] = 'Gasverstromung'  # Annahme Spitzenlast ist immer Grosskunde
    resultframe.loc[i, 'DVG'] = 'Ja'
    verstromungs_series = pd.Series(index=modeling_range)
    if modell_varianten_name == 'gelockert':
        for year in modeling_range:
            if year <= 2035:
                verstromungs_series[year] = 0
            elif year <= 2045:
                verstromungs_series[year] = 100000000
            else:
                verstromungs_series[year] = 200000000
    else:
        verstromungs_series.loc[modeling_range] = 0
    resultframe.loc[i, modeling_range] = verstromungs_series
    i+=1

    for gemeinde in unique_gemeinden:
        gemeinde_frame = zanla_data.loc[(zanla_data['Gemeinde'] == gemeinde) & (zanla_data['separat Modelliert'] == 'Nein')] # Separat modellierte Verbräuche entfernen
        dvg = gemeinde_frame['DVG'].mode()[0]
        for vwz in ['Prozess', 'Wiederverkauf', 'Einspeisung', 'Ausspeisung', '???', 'Heizung', 'Spitzenlast']:
            gemeinde_vwz_frame = gemeinde_frame.loc[gemeinde_frame['VWZ'] == vwz]
            for kundenkategorie in ['Kleinkunde', 'Grosskunde']:
                gemeinde_vwz_kunde_frame = gemeinde_vwz_frame.loc[gemeinde_vwz_frame['Grosskunde'] == kundenkategorie]
                if vwz in ['Prozess', 'Wiederverkauf', 'Einspeisung', 'Ausspeisung', '???']:
                    resultframe.loc[i, 'VWZ'] = vwz
                    resultframe.loc[i, 'FW'] = 'nicht betrachtet'
                    resultframe.loc[i, 'Gemeinde'] = gemeinde
                    resultframe.loc[i, 'Grosskunde'] = kundenkategorie
                    resultframe.loc[i, 'DVG'] = dvg
                    initial_sum = gemeinde_vwz_kunde_frame[absatz_option].sum() # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                    #initial_sum = gemeinde_vwz_kunde_frame[absatz_option].count() # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                    projected_series = absatz_modellieren(initial_sum= initial_sum,
                                                          vwz= vwz,
                                                          fw= resultframe.loc[i, 'FW'],
                                                          total_heizungen= 0, #nur für 80% Biogas benötigt
                                                          absenkpfad_heizung= set_absenkpfad,
                                                          absenkpfad_prozess= set_prozesspfad,
                                                          halterate_heizungen_80_bis_2030= halterate_heizungen_80_bis_2030,
                                                          halterate_heizungen_80_post_2030= halterate_heizungen_80_post_2030)
                    resultframe.loc[i, modeling_range] = projected_series.values
                    i += 1
                elif vwz == 'Heizung':
                    for jahr in area_mapping:
                        total_heizungen = 0
                        if jahr == 'keine_fernwärme':
                            gemeinde_vwz_kunde_jahr_frame = gemeinde_vwz_kunde_frame.loc[(pd.isna(gemeinde_vwz_kunde_frame['energieverbund'])) & (pd.isna(gemeinde_vwz_kunde_frame['Gashaltegebiet']))]
                        elif jahr == 'fernwärme_ohne_lieferdatum':
                            gemeinde_vwz_kunde_jahr_frame = gemeinde_vwz_kunde_frame.loc[(pd.notna(gemeinde_vwz_kunde_frame['energieverbund']) & (pd.isna(gemeinde_vwz_kunde_frame['erschliessungsjahr_mittel']))) & (pd.isna(gemeinde_vwz_kunde_frame['Gashaltegebiet']))]
                        elif jahr == '80%_Biogas':
                            gemeinde_vwz_kunde_jahr_frame = gemeinde_vwz_kunde_frame.loc[gemeinde_vwz_kunde_frame['Biogastarif']=='BBV']
                            total_heizungen = gemeinde_vwz_kunde_frame.loc[gemeinde_vwz_kunde_frame['stilllegungen'].isna(), absatz_option].sum()  # total_heizungen ohne Effekte FW und Stilllegungen
                        else:
                            gemeinde_vwz_kunde_jahr_frame = gemeinde_vwz_kunde_frame.loc[gemeinde_vwz_kunde_frame['erschliessungsjahr_mittel'] == jahr]

                        #Stilllegungsjahre setzen
                        if len(gemeinde_vwz_kunde_jahr_frame['stilllegungen'].unique().tolist()) == 0:
                            stilllegungsjahr = 2100
                            resultframe.loc[i, 'VWZ'] = vwz
                            resultframe.loc[i, 'FW'] = jahr
                            resultframe.loc[i, 'Gemeinde'] = gemeinde
                            resultframe.loc[i, 'Grosskunde'] = kundenkategorie
                            resultframe.loc[i, 'DVG'] = dvg
                            initial_sum = gemeinde_vwz_kunde_jahr_frame[absatz_option].sum()  # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                            #initial_sum = gemeinde_vwz_kunde_jahr_frame[absatz_option].count()  # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                            projected_series = absatz_modellieren(initial_sum=initial_sum,
                                                                  vwz=vwz,
                                                                  fw=resultframe.loc[i, 'FW'],
                                                                  total_heizungen=total_heizungen,
                                                                  absenkpfad_heizung=set_absenkpfad,
                                                                  absenkpfad_prozess=set_prozesspfad,
                                                                  halterate_heizungen_80_bis_2030=halterate_heizungen_80_bis_2030,
                                                                  halterate_heizungen_80_post_2030=halterate_heizungen_80_post_2030,
                                                                  stilllegung=stilllegungsjahr)
                            resultframe.loc[i, modeling_range] = projected_series.values
                            i += 1
                        elif len(gemeinde_vwz_kunde_jahr_frame['stilllegungen'].unique().tolist()) == 1:
                            stilllegungsjahr = gemeinde_vwz_kunde_jahr_frame['stilllegungen'].unique().tolist()[0]
                            if pd.isna(stilllegungsjahr):
                                stilllegungsjahr = 2100
                            resultframe.loc[i, 'VWZ'] = vwz
                            resultframe.loc[i, 'FW'] = jahr
                            resultframe.loc[i, 'Gemeinde'] = gemeinde
                            resultframe.loc[i, 'Grosskunde'] = kundenkategorie
                            resultframe.loc[i, 'DVG'] = dvg
                            initial_sum = gemeinde_vwz_kunde_jahr_frame[absatz_option].sum()  # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                            #initial_sum = gemeinde_vwz_kunde_jahr_frame[absatz_option].count()  # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                            projected_series = absatz_modellieren(initial_sum=initial_sum,
                                                                  vwz=vwz,
                                                                  fw=resultframe.loc[i, 'FW'],
                                                                  total_heizungen=total_heizungen,
                                                                  absenkpfad_heizung=set_absenkpfad,
                                                                  absenkpfad_prozess=set_prozesspfad,
                                                                  halterate_heizungen_80_bis_2030=halterate_heizungen_80_bis_2030,
                                                                  halterate_heizungen_80_post_2030=halterate_heizungen_80_post_2030,
                                                                  stilllegung=stilllegungsjahr)
                            resultframe.loc[i, modeling_range] = projected_series.values
                            i += 1
                        elif len(gemeinde_vwz_kunde_jahr_frame['stilllegungen'].unique().tolist()) > 1:
                            for specific_stilllegungsjahr in gemeinde_vwz_kunde_jahr_frame['stilllegungen'].unique().tolist():
                                if pd.isna(specific_stilllegungsjahr):
                                    subframe = gemeinde_vwz_kunde_jahr_frame.loc[gemeinde_vwz_kunde_jahr_frame['stilllegungen'].isna()]
                                else:
                                    subframe = gemeinde_vwz_kunde_jahr_frame.loc[gemeinde_vwz_kunde_jahr_frame['stilllegungen']==specific_stilllegungsjahr]

                                resultframe.loc[i, 'VWZ'] = vwz
                                resultframe.loc[i, 'FW'] = jahr
                                resultframe.loc[i, 'Gemeinde'] = gemeinde
                                resultframe.loc[i, 'Grosskunde'] = kundenkategorie
                                resultframe.loc[i, 'DVG'] = dvg
                                initial_sum = subframe[absatz_option].sum()  # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                                #initial_sum = subframe[absatz_option].count()  # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])

                                if pd.isna(specific_stilllegungsjahr):
                                    stilllegungsjahr = 2100
                                else:
                                    stilllegungsjahr = specific_stilllegungsjahr

                                #einfacher filter um in Stilllegungsgebieten, keine 80% Biogaslösungen fortzuschreiben
                                if stilllegungsjahr < 2050:
                                    total_heizungen = 0

                                projected_series = absatz_modellieren(initial_sum=initial_sum,
                                                                      vwz=vwz,
                                                                      fw=resultframe.loc[i, 'FW'],
                                                                      total_heizungen=total_heizungen,
                                                                      absenkpfad_heizung=set_absenkpfad,
                                                                      absenkpfad_prozess=set_prozesspfad,
                                                                      halterate_heizungen_80_bis_2030=halterate_heizungen_80_bis_2030,
                                                                      halterate_heizungen_80_post_2030=halterate_heizungen_80_post_2030,
                                                                      stilllegung=stilllegungsjahr)
                                resultframe.loc[i, modeling_range] = projected_series.values
                                i += 1
                        else:
                            print('error')
                elif vwz == 'Spitzenlast':
                    if kundenkategorie == 'Kleinkunde':
                        pass    # Spitzenlast nur einmal berechnen, daher skip Kleinkunde und rechen über Grosskunde
                    else:
                        gemeinde_spitzenlast_frame = gemeinde_frame.loc[(gemeinde_frame['VWZ'] == 'Heizung') & (gemeinde_frame['spitzenlast_ignorieren'] == 'Nein') & (pd.isna(gemeinde_frame['Gashaltegebiet']))]
                        for jahr in area_mapping:
                            gemeinde_spitzenlast_jahr_frame = gemeinde_spitzenlast_frame.loc[gemeinde_spitzenlast_frame['erschliessungsjahr_mittel']==jahr]
                            resultframe.loc[i, 'VWZ'] = vwz
                            resultframe.loc[i, 'FW'] = jahr
                            resultframe.loc[i, 'Gemeinde'] = gemeinde
                            resultframe.loc[i, 'Grosskunde'] = 'Spitzenlast'
                            resultframe.loc[i, 'DVG'] = dvg
                            initial_sum = gemeinde_spitzenlast_jahr_frame[absatz_option].sum() # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                            #initial_sum = gemeinde_spitzenlast_jahr_frame[absatz_option].count() # Handel oder Durchgeleitet (['durchschnittlicher Absatz durchgeleitet', 'durchschnittlicher Absatz gehandelt'])
                            projected_series = absatz_modellieren(initial_sum= initial_sum,
                                                                  vwz= vwz,
                                                                  fw= resultframe.loc[i, 'FW'],
                                                                  total_heizungen= 0, #nur für 80% Biogas benötigt
                                                                  absenkpfad_heizung= set_absenkpfad,
                                                                  absenkpfad_prozess= set_prozesspfad,
                                                                  halterate_heizungen_80_bis_2030= halterate_heizungen_80_bis_2030,
                                                                  halterate_heizungen_80_post_2030= halterate_heizungen_80_post_2030)
                            resultframe.loc[i, modeling_range] = projected_series.values
                            i += 1
                else:
                    print('error')
                    
    if save_appendix == '':
        resultframe.to_csv('Outputfiles/Pivot_' + absatz_option + '_Prozess_'+ modell_varianten_name + '_Prozess_' + str(int(set_prozesspfad.name)) + '_Biogas_2030_' + str(int(halterate_heizungen_80_post_2030*100)) + '.csv')
    else:
        resultframe.to_csv('Outputfiles/Pivot_' + modell_varianten_name + '_Prozess_' + str(int(set_prozesspfad.name)) + '_Biogas_2030_' + str(int(halterate_heizungen_80_post_2030*100)) + '_' + save_appendix + '.csv')