import json
import numpy as np

from nebenrechnungen import Berechnung_der_Sauerstoffloeslichkeit
from nebenrechnungen import Berechnung_des_kla_Wertes
from nebenrechnungen import parameter

from berechnungen import berechnung_der_Tabelle1
from berechnungen import berechnung_der_Tabelle2
from berechnungen import berechnung_der_Tabelle3
from berechnungen import berechnung

from interne_daten.data_importieren import data_importieren_von_json

from Input.json_Input import JsonInput

# Example data for the variables
#c_ox_sat = 0.21  # Example value for oxygen saturation concentration
#t_combined = np.linspace(0, 10, 100)  # Example time data
#y_combined = np.random.rand(5, 100)  # Example concentration data with 5 different concentrations over time
#cum_feeding = np.cumsum(np.random.rand(100))  # Example cumulative feeding data

#c_ox_sat = None  # Oxygen saturation concentration
#t_combined = None  # Time data
#y_combined = None  # Concentration data
#cum_feeding = None  # Cumulative feeding data


 #Modelle aus modelle.jsom laden
modelleOb = JsonInput('modelle.json')
modelleOb.ladeJson()
modelle  = modelleOb.get_data()
    
 #Zum Test im Meeting
m = modelleOb.get_Value()
print(m)
#modelle = data_importieren_von_json('Modelle.json')
    
#Input aus input.json laden
eingabeOb   =  JsonInput('input.json')
eingabeOb.ladeJson()
eingabe = eingabeOb.get_Value()
print(eingabe)


Sauerstoffoeslichkeit_array=Berechnung_der_Sauerstoffloeslichkeit(eingabe[1],eingabe[9],eingabe[3])
    
    
kla_werte=Berechnung_des_kla_Wertes(Sauerstoffoeslichkeit_array,modelle,eingabe[4],eingabe[0],eingabe[5],eingabe[1])
    
    
parameter_werte=parameter(Sauerstoffoeslichkeit_array,kla_werte,modelle,eingabe[1],eingabe[0])
    
    
const_array=berechnung_der_Tabelle1(parameter_werte,eingabe[0],modelle,eingabe[5],eingabe[7],eingabe[1])
    
    
t_ranges_array= berechnung_der_Tabelle2(eingabe[2],eingabe[1])
    
    
param_array=berechnung_der_Tabelle3(const_array,eingabe[10],eingabe[6],eingabe[8],eingabe[11],eingabe[1])
    
    
#Berechnung_ausführen
ergebnis = berechnung(t_ranges_array, param_array, const_array,eingabe[1])
c_ox_sat, y_combined, t_combined, cum_feeding = ergebnis

def generateFermentationDataMain():
    
    
    
    
    data = {
        "labels":  t_combined.tolist(), #["0","5","10","15","20","25","30","35","40","45","50"]
        "datasets": [
            {
                "label": "c_{x}",
                "data": y_combined[0, :].tolist(),
                "borderColor": "#008080",
                "backgroundColor": "#008080",
                "tension": 0.1
            },
            {
                "label": "c_{S1}",
                "data": y_combined[1, :].tolist(),
                "borderColor": "#FF6347",
                "backgroundColor": "#FF6347",
                "tension": 0.1
            },
            {
                "label": "c_{P}",
                "data": y_combined[3, :].tolist(),
                "borderColor": "#FF69B4",
                "backgroundColor": "#FF69B4",
                "tension": 0.1
            },
            {
                "label": "c_{O2}",
                "data": (y_combined[4, :] / c_ox_sat * 100).tolist(),
                "borderColor": "#FF69B4",
                "backgroundColor": "#FF69B4",
                "tension": 0.1
            },
            {
                "label": "c_{S2}",
                "data": y_combined[2, :].tolist(),
                "borderColor": "#4169E1",
                "backgroundColor": "#4169E1",
                "tension": 0.1
            },
            {
                "label": "cum Feed",
                "data": cum_feeding.tolist(),
                "borderColor": "#FFD700",
                "backgroundColor": "#FFD700",
                "tension": 0.1
            }
        ]
    }
    return data

with open('./src/Tasks/Ferment/data.json', 'w') as output:
    json.dump(generateFermentationDataMain(), output)

# Beispiel für die Verwendung der Funktion
fermentationData = generateFermentationDataMain()
print(fermentationData)
