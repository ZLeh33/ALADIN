import sys
import ast
import json
import re
import pandas as pd
import numpy as np

nodes_list = []
edges_list = []

# Berechnung der Entropie
def entropy(labels):
    unique_labels, label_counts = np.unique(labels, return_counts=True)
    probabilities = label_counts / label_counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    entropy = round(entropy, 5)
    return entropy if entropy > 0.0 else -entropy

# Berechnung des Informationsgewinns
def information_gain(data, feature, target):
    total_entropy = entropy(data[target])
    weighted_entropy = 0

    unique_values = data[feature].unique()
    gain_info = {'entropies': {}, 'infogain': {}}

    for value in unique_values:
        subset = data[data[feature] == value]
        subset_entropy = entropy(subset[target])

        weight = len(subset) / len(data)
        weighted_entropy += weight * subset_entropy

        # Entropie der Ausprägung speichern
        gain_info['entropies'][f"{feature} = {value}"] = subset_entropy

    # Informationsgewinn des Attributs speichern
    information_gain = round(total_entropy - weighted_entropy, 5)
    gain_info['infogain'][feature] = information_gain
    return gain_info

# Bestes Merkmal auswählen
def choose_best_feature(data, features, target):
    best_feature_list = []
    best_feature = None
    max_info_gain = -1
    best_feature_info = {"entropies": {}, "infogain": {}}

    for feature in features:
        feature_info = information_gain(data, feature, target)

        if feature_info["infogain"][feature] > max_info_gain:
            max_info_gain = feature_info["infogain"][feature]
            best_feature = feature
            best_feature_info = feature_info
            best_feature_list = [(best_feature, best_feature_info)]
        elif feature_info["infogain"][feature] == max_info_gain:
            best_feature = feature
            best_feature_info = feature_info
            best_feature_list.append((best_feature, best_feature_info))

    return best_feature_list

# Überprüfen, ob mehrere Lösungen vorhanden sind
def check_multiple_solutions(best_feature, solutions, level):
    for tuple in solutions:
        if level == tuple[1] and best_feature == tuple[2]:
            return True
            break

# Hauptfunktion: Lösungsbaum berechnen
def build_decision_tree(data, features, target, level, solutions):
    if len(data[target].unique()) == 1:
        return data[target].iloc[0]
    if len(features) == 0:
        return data[target].mode().iloc[0]

    best_feature = None
    best_feature_info = None
    option_selected = False

    best_feature_list = choose_best_feature(data, features, target)

    # Wenn Mehrfachlösungen vorhanden sind
    if len(best_feature_list) > 1:
        for index, tupel in enumerate(best_feature_list):
            best_feature = tupel[0]
            best_feature_info = tupel[1]

            option_selected = check_multiple_solutions(best_feature, solutions, level)
            if option_selected:
                break
    else:
        for tupel in best_feature_list:
            best_feature = tupel[0]
            best_feature_info = tupel[1]
            option_selected = True

    tree = {best_feature: best_feature_info}
    unique_values = data[best_feature].unique()
    for value in unique_values:
        subset = data[data[best_feature] == value]
        sub_features = features.drop(best_feature)
        tree[best_feature][value] = build_decision_tree(subset, sub_features, target, level+2, solutions)
    return tree

# Struktur des Entscheidungsbaums abstrahieren
def decisiontree_structure(tree):
    new_tree = {}
    for key, value in tree.items():
        if key != 'entropies' and key != 'infogain':
            if isinstance(value, dict):
                new_value = decisiontree_structure(value)
                if new_value:
                    new_tree[key] = new_value
            else:
                new_tree[key] = value
    return new_tree

# Gesamtliste aller Werte (Knoten und Kanten) des Lösungsbaums erstellen
def build_decision_tree_list(tree, level=0, tree_list=None, counter=0, parent_counter=None):
    if tree_list is None:
        tree_list = []

    node_type = 'node' if level % 2 == 0 else 'edge'

    for key, value in tree.items():
        tree_list.append((counter, level, key, node_type, parent_counter))
        counter += 1

        if isinstance(value, dict):
            counter = build_decision_tree_list(value, level + 1, tree_list, counter, parent_counter=counter - 1)
        elif node_type == 'edge':
            tree_list.append((counter, level + 1, value, 'node', counter - 1))
            counter += 1

    return counter

# Entropie und Informationsgewinn abstrahieren
def extract_entropy_and_infogain(tree, result_dict=None, count_dict=None, level=None):
    if result_dict is None:
        result_dict = {'entropies': {}, 'infogain': {}}
    if count_dict is None:
        count_dict = {}

    if level is None:
        level = 0

    if 'entropies' in tree:
        for key, value in tree['entropies'].items():
            count_dict_key = f"{key}_count"
            if count_dict_key not in count_dict:
                count_dict[count_dict_key] = 1
            else:
                count_dict[count_dict_key] += 1

            modified_key = f"{key}{count_dict[count_dict_key]}"
            result_dict['entropies'][modified_key] = {'value': value, 'level': level}

    if 'infogain' in tree:
        for key, value in tree['infogain'].items():
            count_dict_key = f"{key}_count"
            if count_dict_key not in count_dict:
                count_dict[count_dict_key] = 1
            else:
                count_dict[count_dict_key] += 1

            modified_key = f"{key}{count_dict[count_dict_key]}"
            result_dict['infogain'][modified_key] = {'value': value, 'level': level-1}

    for key, value in tree.items():
        if isinstance(value, dict):
            extract_entropy_and_infogain(value, result_dict, count_dict, level + 1)

    return result_dict

# Entropie-Werte der Kantenliste hinzufügen
def add_entropy(edges_list, entropy_dict):
    new_edges_list = []
    attribute_counts = {}
    for index, edge in enumerate(edges_list):
        attribute = f'{edge[5]} = {edge[2]}'
        count = attribute_counts.get(attribute, 1)

        while True:
            key = f'{attribute}{count}'

            if key in entropy_dict['entropies'] and edge[1] == entropy_dict['entropies'][key]['level']:
                value = entropy_dict['entropies'][key]['value']
                new_edges_list.append(edge + (value,))
                count += 1
            else:
                break

            attribute_counts[attribute] = count
    return new_edges_list

# Informationsgewinn-Werte der Knotenliste hinzufügen
def add_infogain(nodes_list, infogain_dict):
    new_nodes_list = []
    attribute_counts = {}

    for index, node in enumerate(nodes_list):
        attribute = node[2]
        count = attribute_counts.get(attribute, 1)

        key = f'{attribute}{count}'

        if key in infogain_dict['infogain'] and node[1] == infogain_dict['infogain'][key]['level']:
            value = infogain_dict['infogain'][key]['value']
            new_nodes_list.append(node + (value,))
            count += 1
        else:
            value = 0
            new_nodes_list.append(node + (value,))

        attribute_counts[attribute] = count

    return new_nodes_list

# Bezeichnung des Übergeordeneten Objekts dem Knoten bzw. der Kante hinzufügen
def add_parent_label(tree_list):
    new_tree_list = []

    # NODES
    for item in tree_list:
        for i in tree_list:
            if item[3] == 'node' and item[4] == i[0]:
                new_tree_list.append(item + (i[2],))
                break
            elif item[3] == 'node' and item[4] is None:
                new_tree_list.append(item + ('None',))
                break

    # EDGES
    for item in tree_list:
        for i in tree_list:
            if item[3] == 'edge' and item[4] == i[0]:
                new_tree_list.append(item + (i[2],))
                break

    return new_tree_list

# Bezeichnung und Ebene des Zielknoten der Kante hinzufügen
def add_child_node(tree_list):
    # NODE(ID, LEVEL, LABEL, TYPE, PARENTID, PARENTLABEL)
    nodes_list = [item for item in tree_list if item[3] == 'node']

    result = []
    for item in tree_list:
        if item[3] == 'edge':
            for i in tree_list:
                if i[3] == 'node' and item[0] == i[4]:
                    child_id = i[0]
                    child_label = i[2]
                    result.append(item + (child_id, child_label))

    result = result + nodes_list
    return result

# Liste mit Lösungswerten des Lösungsentscheidungsbaum vorbereiten für die Überprüfung
def prepare_lists(nodes_list, edges_list):
    # NODE (KEY, LEVEL, LABEL, PARENTID, PARENTLABEL, INFOGAIN)
    solutions_nodes = [(node[0], node[1], re.sub(r"(\s)+", "_", node[2]).strip(), node[4], re.sub(r"(\s)+", "_",node[5]).strip(), node[6]) for node in nodes_list]
    # EDGE (KEY, LEVEL, LABEL, PARENTID, PARENTLABEL, CHILDID, CHILDLABEL, ENTROPY)
    solutions_edges = [(edge[0], edge[1], re.sub(r"(\s)+", "_", edge[2]).strip(), edge[4], re.sub(r"(\s)+", "_", edge[5]).strip(), edge[6], re.sub(r"(\s)+", "_", edge[7]).strip(), edge[8]) for edge in edges_list]
    return solutions_nodes, solutions_edges

# Validierung der übergebenen Werte des erstellen Entscheidungsbaum mit den berechneten Lösungswerten
def validateGraph(solution_nodes_list, solution_edges_list, received_nodes_list, received_edges_list, classes):
    # SOLUTIONS_NODES (ID, LEVEL, LABEL, PARENTID, PARENTEDGELABEL, INFOGAIN)
    # RECEIVED_NODES (KEY, LEVEL, LABEL, PARENTEDGELABEL, INFOGAIN)

    # SOLUTIONS_EDGES (ID, LEVEL, LABEL, PARENTID, PARENTNODELABEL, CHILDID, CHILDNODELABEL, ENTROPY)
    # RECEIVED_EDGES (KEY, LEVEL, LABEL, PARENTKEY, PARENTNODELABEL, CHILDKEY, CHILDNODELABEL, ENTROPY)

    results_nodes = []
    results_edges = []

    # 1. PRÜFUNG - EDGES
    for received_edge in received_edges_list:
        result = False
        for solution_edge in solution_edges_list:
            if (received_edge[1] == solution_edge[1] and # (LEVEL == LEVEL)
                received_edge[2] == solution_edge[2] and # (LABEL == LABEL)
                received_edge[4] == solution_edge[4] and # (PARENTNODELABEL == PARENTNODELABEL)
                received_edge[6] == solution_edge[6] and # (CHILDNODELABEL == CHILDNODELABEL)
                received_edge[7] == solution_edge[7]     # (ENTROPY == ENTROPY)
            ):
                result = True
                break

        results_edges.append({'key': received_edge[0], 'result': result})

    # 2. PRÜFUNG - NODES
    for received_node in received_nodes_list:
        result = False
        for solution_node in solution_nodes_list:
           # WURZELKNOTEN PRÜFEN
            if (received_node[0] == '1' and                 # (KEY == 1)
                received_node[2] == solution_node[1] and    # (LEVEL == LEVEL)
                received_node[1] == solution_node[2] and    # (LABEL == LABEL)
                received_node[3] == 'None' and              # (PARENTEDGELABEL == 'NONE')
                received_node[4] == solution_node[5]):      # (INFOGAIN == INFOGAIN)
                result = True
                break

            elif (received_node[1] == solution_node[1] and # (LEVEL == LEVEL)
                  received_node[2] == solution_node[2] and # (LABEL == LABEL)
                  received_node[3] == solution_node[4] and # (PARENTEDGELABEL == PARENTEDGELABEL)
                  received_node[4] == solution_node[5]):   # (INFOGAIN == INFOGAIN)
                result = True
                break

            elif (received_node[2] in classes):  # (LABEL IN CLASSES['ja', 'nein'])
                for solution_edge in solution_edges_list:
                    if (received_node[2] == solution_edge[6] and
                        received_node[3] == solution_edge[2] and
                        received_node[4] == 'decision'):
                        result = True
                        break

        results_nodes.append({'key': received_node[0], 'result': result})
    return results_nodes, results_edges

# Struktur des Entscheidungsbaums erhalten (Funktion für die Datengenerierung)
def get_decisiontree_structure(data_path_csv):
    dataframe = pd.read_csv(data_path_csv)
    received_nodes = []

    target_attribute = dataframe.columns[-1]
    classes = dataframe[target_attribute].unique()
    attributes = dataframe.columns[:-1]

    dt = build_decision_tree(dataframe, attributes, target_attribute, 0, received_nodes)
    dt_struct = decisiontree_structure(dt)

    return dt_struct