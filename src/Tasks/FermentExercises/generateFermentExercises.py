
import json
from view import plot_visualisieren
from excel_export import export_to_excel

from nebenrechnungen import Berechnung_der_Sauerstoffloeslichkeit
from nebenrechnungen import Berechnung_des_kla_Wertes
from nebenrechnungen import parameter

from berechnungen import berechnung_der_Tabelle1
from berechnungen import berechnung_der_Tabelle2
from berechnungen import berechnung_der_Tabelle3
from berechnungen import berechnung
from feedback_schaetzung import feedback_schatzung

from interne_daten.data_importieren import data_importieren_von_json

from Input.json_Input import JsonInput





import json
from view import plot_visualisieren
from excel_export import export_to_excel

from nebenrechnungen import Berechnung_der_Sauerstoffloeslichkeit
from nebenrechnungen import Berechnung_des_kla_Wertes
from nebenrechnungen import parameter

from berechnungen import berechnung_der_Tabelle1
from berechnungen import berechnung_der_Tabelle2
from berechnungen import berechnung_der_Tabelle3
from berechnungen import berechnung
from feedback_schaetzung import feedback_schatzung

from interne_daten.data_importieren import data_importieren_von_json

from Input.json_Input import JsonInput

def generateFermentExercises():
    # Modelle aus modelle.json laden
    modelleOb = JsonInput('modelle.json')
    modelleOb.ladeJson()
    modelle  = modelleOb.get_data()

    # Zum Test im Meeting
    m = modelleOb.get_Value()

    # Input aus input.json laden
    eingabeOb = JsonInput('input.json')
    eingabeOb.ladeJson()
    eingabe = eingabeOb.get_Value()

    # Berechnungen durchführen
    Sauerstoffoeslichkeit_array = Berechnung_der_Sauerstoffloeslichkeit(eingabe[1], eingabe[9], eingabe[3])
    kla_werte = Berechnung_des_kla_Wertes(Sauerstoffoeslichkeit_array, modelle, eingabe[4], eingabe[0], eingabe[5], eingabe[1])
    parameter_werte = parameter(Sauerstoffoeslichkeit_array, kla_werte, modelle, eingabe[1], eingabe[0])
    const_array = berechnung_der_Tabelle1(parameter_werte, eingabe[0], modelle, eingabe[5], eingabe[7], eingabe[1])
    t_ranges_array = berechnung_der_Tabelle2(eingabe[2], eingabe[1])
    param_array = berechnung_der_Tabelle3(const_array, eingabe[10], eingabe[6], eingabe[8], eingabe[11], eingabe[1])

    # Berechnung ausführen
    ergebnis = berechnung(t_ranges_array, param_array, const_array, eingabe[1])
    c_ox_sat, y_combined, t_combined, cum_feeding = ergebnis

    # Eingaben für Phasen abfragen
    print("Bitte geben Sie die Feed-Werte für die 4 Phasen ein (Werte von 0 bis 5):")
    
    phasen = {}
    for i in range(4):  # Für Phase_0 bis Phase_3
        phase_input = input(f"Phase_{i}: ")
        while not phase_input.isdigit() or not (0 <= int(phase_input) <= 5):
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl zwischen 0 und 5 ein.")
            phase_input = input(f"Phase_{i}: ")
        phasen[f"Phase_{i}"] = int(phase_input)

    # Ergebnisse in JSON-Datei speichern
    with open("src/Tasks/FermentExercises/phasen_eingaben.json", "w") as json_file:
        json.dump(phasen, json_file, indent=4)
    
    print("Eingaben für die Phasen wurden erfolgreich in 'phasen_eingaben.json' gespeichert.")
    
     # Feedback Schätzung ausführen
    feedback_schatzung()
    
if __name__ == "__main__":
    generateFermentExercises()

    # Export Ergebnis in Excel-Datei (optional)
    # export_to_excel("model_result.xlsx", t_combined, y_combined, cum_feeding)

    # Feedback Schätzung (optional)
    # lösung = feed_s1  # Hier die tatsächliche Lösung setzen
    # feedback_schatzung(lösung)

    # Darstellung ausgeben (optional)
    # plot_visualisieren(c_ox_sat, y_combined, t_combined, cum_feeding)
