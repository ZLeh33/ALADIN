import pandas as pd
import numpy as np
from DecisionTreeTaskFunction import *

data_path_csv = 'src/Tasks/DecisionTrees/datasets/spiel.csv' # Originaler Datensatz
generated_data_path_csv = 'src/Tasks/DecisionTrees/datasets/generated_dataset.csv' # Generierter Datensatz

data = pd.read_csv(data_path_csv)
df = pd.DataFrame(data)

# Beispiel: Lösungsbaum-Struktur von spiel.csv
# decision_tree = {'Aussicht': {'sonnig': {'Luftfeuchtigkeit': {'hoch': 'nein', 'normal': 'ja'}},
#                               'bewölkt': 'ja',
#                               'regnerisch': {'Wind': {'nein': 'ja', 'ja': 'nein'}}}}

decision_tree_original = get_decisiontree_structure(data_path_csv)

# Prüfung, ob Baumstrukur aus generierten Datensatz gleich wie Struktur des Lösungsbaums
def check_generated_tree(original_tree, generated_tree):
    original_json = json.loads(json.dumps(original_tree, sort_keys=True))
    generated_json = json.loads(json.dumps(generated_tree, sort_keys=True))
    return original_json == generated_json

# Bootstrap-Sampling-Funktion
def bootstrap_sample(data):
    sample = data.sample(n=len(data), replace=True) # samplen der Datensätze in gleicher Größe wie die original Daten
    return sample

# Funktion zum Generieren von Datenpunkten basierend auf dem Entscheidungsbaum
def generate_data_point(tree):
    current_node = tree
    while isinstance(current_node, dict):
        feature = list(current_node.keys())[0]
        values = list(current_node[feature].keys())
        selected_value = np.random.choice(values)
        current_node = current_node[feature][selected_value]
    return current_node

# Bootstrap-Sampling und Daten generieren
def sample_data():
    while True:
        num_samples = 5

        data = pd.concat([bootstrap_sample(df.apply(generate_data_point, axis=1)) for _ in range(num_samples)], ignore_index=True)

        # als JSON speichern für die Ausgabe als Tabelle
        data.to_json('src/Tasks/DecisionTrees/datasets/generated_dataset.json',orient='records',lines=True)

        # als CSV speichern für die Berechnung des Entscheidungsbaumes
        data.to_csv('src/Tasks/DecisionTrees/datasets/generated_dataset.csv', index=False)

        # Entscheidungsbaum-Struktur für den generierten Datensatz erstellen
        decision_tree_generated = get_decisiontree_structure(generated_data_path_csv)

        if check_generated_tree(decision_tree_original, decision_tree_generated):
            print("Die generierter Datensatz entspricht der Struktur des originalen Entscheidungsbaum.")
            break

sample_data()
