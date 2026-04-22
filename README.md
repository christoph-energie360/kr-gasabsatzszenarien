# kr-gasabsatzszenarien
Codebasis für die Gasabsatzszenarien die für KE als Grundlage für die MFPL genutzt werden

Codebasis der letzten Jahre sind enthalten (Datenbasis GJ23, Datenbasis GJ24, Datenbasis GJ25)
Bspw: Im GJ26 wird die Arbeit gemacht mit dem Abschluss des letzten vollständigen Geschäftsjahr ("Datenbasis GJ25"). Diese Arbeit ist dann eine der Grundlagen für die Gasdaten des KE für die MFPL und Budgetrunde für das kommende GJ27

Die Codebasis besteht aus zwei Python-Files (main.py und functions.py).
main.py wird ausgeführt und importiert die notwendigen Funktionen aus functions.py
Die Ordnerstruktur beinhaltet die Ordner "Inputfiles" und "Outputfiles" (inkl. "Outputfiles/Plots"), die bestehen müssen um die hinterlegten Speicher- und Ladepfade zu nutzen.

Die "Inputfiles" benötigen vor allem einen Auszug der ZANLA und ZGERAUS (beide SAP), sowie eines Exports aller Anlagen mit den zugehörigen Fernwärme/Stilllegungszonen (Export in der Vergangenheit beim Datateam/Martin Lohoff angefragt).
Einzelne zusätzliche Files werden eingelesen um bspw. fehlende Informationen zu ergänzen: Aktuelle Anlagen mit bestimmt Tarifen (bspw. Tariftyp BBV), Verbrauchsannahmen zu Grossverbrauchern (bspw. ewz Hagenholz oder Spitzenlast Cluster Volketswil), Zonenpläne des Energieplans Stadt Zürich (Zonen, Fernwärme- und Stilllegungsjahre, Anlagen in Gashaltegebieten)
Im Code sind beim Einlesen der Files Kommentare hinterlegt, welche Daten eingelesen werden. Einige dieser Daten sind jährlich von Hand zu erstellen und müssen die Formatierung einhalten oder es muss das Einlesen der Files in functions.py entsprechend angepasst werden (Teils Excel, teils csv).

Für die Arbeit "Datenbasis GJ25" ist das File "geo_zanla_data_ZH_shift_2" die Datenbasis nach dem Einlesen aller relevanten Daten. Um Rechenzeit zu sparen, kann das File einmal erzeugt werden und dann für neue Runs wieder eingelesen werden (flag "new_run==True/False")

Die Abschnitte in main.py beinhalten "Daten Einlesen", "Absenkpfade berechnen" und "Modellierung"
Einlesen und Absenkpfade berechnen sollte auf einem Laptop in der grössenordnung 10-15 Minuten dauern.

Jede Modellvariante läuft anschliessend in run 3 Minuten. Für "Datenbasis GJ25" sind 3 Szenarien zu rechnen, jeweils mit gehandelten Mengen und durchgeleiteten Mengen. (Also ebenfalls rund 15-20 Minuten für die 6 Szenarien).

Die Outputfiles sind csv die in Excel eingelesen werden können. Die Form ist darauf ausgelegt in einem neuen Reiter eine Pivottabelle einzufügen und dann alle Filter einstellen zu können.
VWZ: Verwendungszweck 
Heizung, Prozess, Spitzenlast, 80%_Biogas, Gasverstromung sind alle modelliert oder gesetzt. Die restlichen VWZ sind für alle Folgejahre fortgeschrieben ohne Veränderung (Wiederverkauf, Einspeisung, Ausspeisung, ???)

DVG: Direkt versorgte Gemeinde
Ja/Nein ob die Gemeinde im Versorgungsgebiet von E360 ist oder nicht

Gemeinde: Politische Gemeinde

FW: Fernwärme
Relevant für Gebietsunterteilung. Zu Lesen als "Gasabsatz in Gemeinde x in dem Gebiet mit Fernwärme-Erschliessungsjahr y". Die Unterscheidung ist für Stilllegungsjahre und Veränderungen durch Wechsel vom Gas auf Fernwärme relevant. Für die Analyse ist die Summe pro Gemeinde relevant (daher keine unterscheidung in Pivotübersicht sinnvoll).

Grosskunde:
Unterscheidung in Grosskunde und Kleinkunde (cutoff gesetzt bei 300MWh Verbrauch pro Jahr). cutoff kann im code entsprechend anders gesetzt werden. Die Unterscheidung ist notwendig um vereinfacht eine Tarifunterscheidung oder Margenunterscheidung für die jeweiligen Gruppen zu setzen.

Jahresspalten:
Das aktuelle Jahr ist die Summe aus der ZANLA (5-Jahres-Mittel). Die folgenden Jahre ergeben sich aus den Vorjahreswerten und den jeweiligen Absenkpfaden und Stilllegungsjahren.

Idealerweise wird das Analysefile einmal sauber aufgesetzt. Anschliessend kann ein neuer Szenarienrun mit anderen Parametern ausgeführt werden und alle Auswertungen und Abbildungen können via "Daten->Alle Aktualisieren" im Excelfile direkt upgedated werden.
