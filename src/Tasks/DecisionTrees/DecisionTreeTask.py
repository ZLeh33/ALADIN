import sys
import ast
import json
import pandas as pd
import numpy as np
from DecisionTreeTaskFunction import *

# generierten Datensatz für die Berechnung verwenden
data_path_csv = 'src/Tasks/DecisionTrees/datasets/generated_dataset.csv'
dataframe = pd.read_csv(data_path_csv)

# Merkmale, Zielmerkmal und Klassen abstrahieren
attributes = dataframe.columns[:-1]
target_attribute = dataframe.columns[-1]
classes = dataframe[target_attribute].unique()

# Funktion für den Beginn der Aufgabe - Lösungsbaum berechnen und Überprüfung des eingegebenen Entscheidungsbaums
def start_decisiontree_task(received_nodes, received_edges, classes):
    dt = build_decision_tree(dataframe, attributes, target_attribute, 0, received_nodes)

    decision_tree_structure_dict = decisiontree_structure(dt)
    entropy_infogain_dict = extract_entropy_and_infogain(dt)

    tree_list = []
    build_decision_tree_list(decision_tree_structure_dict, tree_list=tree_list)
    tree_list = add_parent_label(tree_list)
    tree_list = add_child_node(tree_list)

    nodes_list = [item for item in tree_list if item[3] == 'node']
    edges_list = [item for item in tree_list if item[3] == 'edge']

    edges_list = add_entropy(edges_list, entropy_infogain_dict)
    nodes_list = add_infogain(nodes_list, entropy_infogain_dict)

    # Werte des Lösungsbaum in zwei Listen aufgeteilt, für die Überprüfung des eingegebnen Baums (seperate Listen für Knoten und Kante)
    solutions_nodes, solutions_edges = prepare_lists(nodes_list, edges_list)

    # Überprüfung des eingegebenen Entscheidungsbaums
    results_nodes, results_edges = validateGraph(solutions_nodes, solutions_edges, received_nodes, received_edges, classes)

    correctNodesCount = 0
    correctEdgesCount = 0

    # Überprüfung, ob Entscheidungsbaum vollständig gelöst
    for r in results_nodes:
        if r['result'] == True:
            correctNodesCount += 1

    for r in results_edges:
        if r['result'] == True:
            correctEdgesCount += 1

    if(len(solutions_nodes) == correctNodesCount and len(solutions_edges) == correctEdgesCount and len(solutions_nodes) == len(received_nodes) and len(solutions_edges) == len(received_edges)):
        result = { 'nodes': results_nodes, 'edges': results_edges, 'finished': True, 'entropies': entropy_infogain_dict }
    else:
        result = { 'nodes': results_nodes, 'edges': results_edges, 'finished': False, 'entropies': entropy_infogain_dict }

    return (json.dumps(result))


# Erhalt der Nodes- und Edges-Liste aus WrapperValidateDecisionTree.ts
received_nodes_list, received_edges_list = sys.argv[1], sys.argv[2] if len(sys.argv) <= 3 else (None, None)

modified_nodes_list_1 = ast.literal_eval(received_nodes_list)
modified_nodes_list_2 = [tuple(inner) for inner in modified_nodes_list_1] # Inhalt der Liste als Tupel umwandeln
current_nodes_list = [(x[0], x[1], 0 if x[2] is None else x[2], x[3], x[4]) for x in modified_nodes_list_2] # Wert in Tupel prüfen, ob 3. Element None ist (Wurzelknoten) → mit 0 ersetzen

modified_nodes_list = ast.literal_eval(received_edges_list)
current_edges_list = [tuple(inner) for inner in modified_nodes_list]

print(start_decisiontree_task(current_nodes_list, current_edges_list, classes))
