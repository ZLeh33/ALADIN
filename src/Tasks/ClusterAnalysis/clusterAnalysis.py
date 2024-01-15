#Clusteranalyse

import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from graphviz import Digraph
import graphviz
#from IPython.display import display
import math
import json
import sys
import os
import pathlib
import base64

#functions
def generate_clusters(n_clusters, m_points_per_cluster, rangeStart, rangeEnd):
    # Generate random cluster centers
    cluster_centers = np.random.randint(rangeStart, rangeEnd, size=(n_clusters, 2))
    noise_scale = 1

    # Generate points for each cluster
    points = []
    for center in cluster_centers:
        cluster_points = np.random.randint(-5, 5, size=(m_points_per_cluster, 2)) + center
        points.extend(cluster_points)

    # Add noise to the points
    noisy_points = points + (np.random.randint(-2, 2, size=(len(points), 2)))
    
    return np.array(noisy_points)

def is_element_in_array(cluster_array, single_point):
    for sub_array in cluster_array:
        for element in sub_array:
            if element[0] == single_point[0] and element[1] == single_point[1]:
                return True
    return False

def is_element_in_array_location(cluster_array, single_point):
    i = 0
    j = 0
    for sub_array in cluster_array:
        for element in sub_array:
            if element[0] == single_point[0] and element[1] == single_point[1]:
                #print("LOCATION")
                #print(element[0])
                #print(element[1])
                return [i, j]
            j += 1
        i += 1
    return False

def check_array_exists(arrayName):
    if 'clusters' in dir():
        return True
    else:
        return False

#todo
def manhattan_distance(point1, point2):
    return np.sum(np.abs(point1 + point2))

#ready
def euclidean_distance(array1, array2):
    return round(math.sqrt((pow((array1[0] - array2[0]), 2)) + (pow((array1[1] - array2[1]), 2))),2)

#todo
def maximum_distance(point1, point2):
    return np.max([[point1],[point2]])

def calculate_inital_abstraction_matrix(data, distance_function):
    
    # Initialize clusters with each data point as a separate cluster
    array = np.zeros((data.shape[0],data.shape[0]))
    
    for iteration_number_row in range(len(data)):
        
        for iteration_number_column in range(len(data)):
            array[iteration_number_row, iteration_number_column] = distance_function(data[iteration_number_row],data[iteration_number_column])

    return array

def single_linkage_get_indices(inital_abstraction_matrix):

    # Exclude diagonal elements and zeros
    lower_triangular = np.tril(inital_abstraction_matrix, k=-1)
    lower_triangular[lower_triangular == 0] = np.inf
    
    min_index = np.unravel_index(np.argmin(lower_triangular), lower_triangular.shape)
    
    # Adjust indices to consider the original matrix
    #adjusted_indices = (min_index[0] + 1, min_index[1])

    #print(min_index)
    return min_index

#get nearest of 2 points to get the new center of the cluster
def get_nearest_point(data, point_a, point_b, distance_function):
    #get the point that is more near the other points
    # Calculate distances for both points
    distances_to_a = [distance_function(point_a, point) for point in data]
    distances_to_b = [distance_function(point_b, point) for point in data]

    # Find the index of the nearest point for each given point for both points
    nearest_point_index_a = np.argmin(distances_to_a)
    nearest_point_index_b = np.argmin(distances_to_b)
    
    sum_distance_to_a = 0
    for distance in distances_to_a:
        sum_distance_to_a += float(distance)
    
    sum_distance_to_b = 0
    for distance in distances_to_b:
        sum_distance_to_b += float(distance)

        
    # Compare the distances
    #[[nearest_point][point_to_delete]]
    if sum_distance_to_a < sum_distance_to_b:
        nearest_point = [data[nearest_point_index_a] , data[nearest_point_index_b]]
    elif sum_distance_to_a > sum_distance_to_b:
        nearest_point = [data[nearest_point_index_b] , data[nearest_point_index_a]]
    else: #equal
        nearest_point = [data[nearest_point_index_a] , data[nearest_point_index_b]]
            
    return nearest_point

def createScatterDiagram(data):
    # Streudiagramm zeichnen
    # Extract x and y coordinates
    x = data[:, 0]
    y = data[:, 1]

    # Generate random colors
    colors = np.random.rand(len(x), 3)

    # Create scatter plot with random colors
    plt.scatter(x, y, marker='o', color=colors)

    # Add labels and title
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.title('Streudiagram')

    # #display the plot
    plt.show()

def createDigraph(distanceMatrix, points, iterationNumber):
    #transform matrix
    
    #print(distanceMatrix)

    points = points.astype(str)
    distanceMatrix = distanceMatrix.astype(str)
    pointsY = np.array([[' - '.join(row)] for row in points])  
    pointsX = np.array([[' - '.join(row)] for row in points]) 
    #pointsX = np.insert(pointsX, 0, 'Iteration {}'.format(iterationNumber), axis=0)
    pointsX = np.insert(pointsX, 0, str(iterationNumber), axis=0)

    # Concatenate arr1 and arr2 vertically
    distanceMatrix = np.concatenate((pointsY, distanceMatrix), axis=1)
    
    Array2d = np.array([np.concatenate(pointsX.T)])
    distanceMatrixNew = np.append(Array2d, distanceMatrix, axis=0)
    
    # Create a Digraph object
    dot = Digraph(comment='Distance Matrix')

    # Create a single table for the entire matrix
    table_label = f'<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
    for i in range(distanceMatrixNew.shape[0]):
        table_label += '<TR>'
        for j in range(distanceMatrixNew.shape[1]):
            table_label += f'<TD>{distanceMatrixNew[i, j]}</TD>'
        table_label += '</TR>'
    table_label += '</TABLE>>'

    # Add a single node to the graph with the entire table as label
    dot.node('table', label=table_label, shape='plaintext')
                
    # Save the graph as a PNG file
    #dot.render('directed_graph', format='png', cleanup=True)
    
    #display(dot)
    
    return str(dot)



# Helper function to recursively add nodes and edges to the graph
def add_nodes_edges(dot, node_id, Z, dendrogram_data):
        if node_id < len(Z):
            # Internal node
            child1, child2 = Z[node_id, 0], Z[node_id, 1]
            dot.node(f'node_{node_id}', label=str(Z[node_id, 2]))
            add_nodes_edges(dot, int(child1), Z, dendrogram_data)
            add_nodes_edges(dot, int(child2), Z, dendrogram_data)
            dot.edge(f'node_{node_id}', f'node_{int(child1)}')
            dot.edge(f'node_{node_id}', f'node_{int(child2)}')
        else:
            # Leaf node
            leaf_index = node_id - len(Z)
            dot.node(f'leaf_{leaf_index}', label=str(dendrogram_data['ivl'][leaf_index]))


def createDendogramDotLanguage(data, distanceMethod):
    
    if distanceMethod == 'manhattan':
        linkage_data = linkage(data, method='single', metric='cityblock')

    elif distanceMethod == 'euclidean':
        linkage_data = linkage(data, method='single', metric='euclidean')

    elif distanceMethod == 'maximum':
        linkage_data = linkage(data, method='single', metric='maximum')

    else:
        return ''
        
    #dendrogram(linkage_data)
    
    #print(linkage_data)

    #plt.show()
    
    # Create a dendrogram
    dendrogram_data = dendrogram(linkage_data, no_plot=True)

    # Create a Graphviz graph
    dot = graphviz.Digraph(comment='Dendrogram')

    # Add nodes and edges to the graph
    add_nodes_edges(dot, len(linkage_data) * 2 - 2, linkage_data, dendrogram_data)
    #display(dot)
    
    return str(dot)

def array_to_html_table(array):
    html = '<table style="border: 1px solid black;">\n'
    html += '<tr><th style="border: 1px solid black;>Position X-Achse</th><th style="border: 1px solid black;>Position Y-Achse</th></tr>'
    for row in array:
        html += '<tr>\n'
        for item in row:
            html += f'<td style="border: 1px solid black;  border-collapse: collapse;">{item}</td>\n'
        html += '</tr>\n'
    html += '</table>'
    return html

def generate_task_description(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean, data):
    finalDescription = ""

    #add the main task descripton to the variable
    finalDescription += "<p>In dieser Aufgabe sollen Sie zeigen, dass Sie die hierarchische Clusteranalyse verstanden haben und diese anwenden koennen.</p><br>"

    #add example data to description
    finalDescription += "<p>Sie erhalten eine Sammlung von Datenpunkten, für die Sie die Aufgabe durchführen sollen.</p>"
    totalPoints = int(pointsPerCluster) * int(numClusters)
    finalDescription += f"<p>Sie besteht aus {numClusters} zentrierten Clustern mit jeweils {pointsPerCluster} Datenpunkten. In Summe haben Sie somit {totalPoints} Datenpunkte gegeben.</p><br>"
    finalDescription += array_to_html_table(data)
    finalDescription += "<br><br>"

    #add more task description
    finalDescription += "<p>Zeichnen Sie im ersten Schritt die Datenpunkte in ein Koordinatensystem als visuelle Hilfe ein.</p>"

    #if diagram help checkbox is checked
    if str(diagramHelpBoolean) == "true":
        finalDescription += "<br><p>Sie haben bei der Aufgabenerstellung ausgewaehlt, dass Ihnen das Streudiagramm angezeigt werden soll. Das folgende Diaramm zeigt die verteilten Punkte im Koordinatensystem.</p><br>"

        #add base64 img
        #TODO
        print_diagram(data)
        with open("streudiagramm.png", "rb") as image_file:
            encoded_string = str(base64.b64encode(image_file.read()))

        finalDescription += f'<br><img src="data:image/png;base64, {encoded_string[2:-1]}" alt="Streudiagramm" /><br><br>'

    #help description for calculating distance matrix
    if str(distanceMatrixBoolean) == "true":
        finalDescription += f"<p>Hilfe zur Distanzberechnung</p><p>So haben die {str(distanceMethod)} Methode zur Berechnung der Distanz gewaehlt. Diese wird wie folgt berechnet:</p>"
        if distanceMethod == 'manhattan':
            finalDescription += '<p><img src="data:image/png;base64,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" alt="Distanzmethode" /></p>'
                
        elif distanceMethod == 'euclidean':
            finalDescription += '<p><img src="data:image/png;base64,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" alt="Distanzmethode" /></p>'

        elif distanceMethod == 'maximum':
            finalDescription += '<p>Ermittle die größere der beiden Zahlen -> max( x , y )</p>'

    #help description for draw the dendrogram
    if str(dendogramBoolean) == "true":
        finalDescription += "<p>Um ein Dendrogramm aus einer Distanzmatrix zu erstellen, verwendet man zuerst einen hierarchischen Clustering-Algorithmus (wie z.B. Single-Linkage, Complete-Linkage oder Average-Linkage), um die Cluster-Hierarchie aus der Distanzmatrix zu erzeugen. Anschließend stellt man diese Hierarchie graphisch als Dendrogramm dar, wobei die Länge der Verbindungslinien die Distanzen oder Ähnlichkeiten zwischen den Clustern repräsentiert.</p>"
    

    finalDescription += "Berechnen Sie nun im nächsten Schritt die einzelnen Distanzmatrizen bis zu einer 2x2 Matrix und gebe sie Ihre Loesung in den Editor ein."
    finalDescription += f"Nutzen Sie für die Berechnung der Distanzen zwischen den einzelnen Datenpunkten die Berechnungmethode {distanceMethod}"

    return finalDescription

def print_diagram(data):
    # Streudiagramm zeichnen
    # Extracting X and Y coordinates from the data
    x = [point[0] for point in data]
    y = [point[1] for point in data]

    # Creating the plot
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'o')  # 'o' creates a scatter plot
    plt.title('Streudiagramm')
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')

    # Display the plot
    #plt.show()
    plt.savefig('streudiagramm.png')

#def clusterAnalysisMain(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod):
def clusterAnalysisMain():
    
    #get data from CLI
    numClusters = int(sys.argv[2])
    pointsPerCluster = int(sys.argv[1])
    nodeRangeStart = int(sys.argv[9])
    nodeRangeEnd = int(sys.argv[10])
    diagramHelpBoolean = sys.argv[4]
    dendogramBoolean = sys.argv[5]
    distanceMethod = sys.argv[7]
    linkageMethod = sys.argv[8]
    distanceMatrixBoolean = sys.argv[6]

    #generate data for a task for the student
    data = generate_clusters(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd)
    
    print(data)

    taskDescription = generate_task_description(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean, data)
    #TODO: atrribute richtig machen aus Fronted -> destrukturieren
    #aufgabenbeschreibung generieren

    #Testdata
    #data = np.array([[2, 3],
    #                     [5, 2],
    #                     [5, 3],
    #                     [1, 4],
    #                     [4, 5]])
    
    
    #createScatterDiagram(data)
    jsonDict = {}
    #jsonDict["Dendogram"] = createDendogramDotLanguage(data, distanceMethod)
    jsonDict["taskDescription"] = taskDescription
    

    for iteration in range(data.shape[0]):
        #erste iteration
        if(iteration == 0):
            
            clusters = []
            
            #inital abstraction matrix
            print("---Inital Iteration---")
            #get distance method
            if distanceMethod == 'manhattan':
                matrix = calculate_inital_abstraction_matrix(data, manhattan_distance)

            elif distanceMethod == 'euclidean':
                matrix = calculate_inital_abstraction_matrix(data, euclidean_distance)

            elif distanceMethod == 'maximum':
                matrix = calculate_inital_abstraction_matrix(data, maximum_distance)

            else:
                break
            
            #matrix = calculate_inital_abstraction_matrix(data, euclidean_distance)
            single_linkage_indices = single_linkage_get_indices(matrix)
            #print(single_linkage_indices)
            
            #get two points from given index that are the first cluster
            point_a = data[single_linkage_indices[0]]
            point_b = data[single_linkage_indices[1]]
            
            
            if distanceMethod == 'manhattan':
                nearest_point = get_nearest_point(data, point_a, point_b, manhattan_distance)

            elif distanceMethod == 'euclidean':
                nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)

            elif distanceMethod == 'maximum':
                nearest_point = get_nearest_point(data, point_a, point_b, maximum_distance)

            else:
                break
                
            #nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)
            #delete the point from the dataset, that is not nearest
            point_to_remove = nearest_point[1]
            
            
            #create Digraph
            #TODO -> oberste Zeile noch hinzufügen
            #print("DIGRAPH - Abstandsmatrix")
            jsonDict["DigraphIteration{}".format(iteration)] = matrix.tolist() #createDigraph(matrix, data, iteration)
            
            #define cluster elements
            #clusters = np.array([[point_a, point_b]])
            clusters.append([point_a, point_b])
            #print("Aktuelle Cluster:")
            #print(clusters)
            
            #define new dataset
            new_data = np.array([point for point in data if not np.array_equal(point, point_to_remove)])
            #print("Neuer Hauptdatensatz")
            #print(new_data)

        #alle weiteren iterationen  
        elif(iteration > 0):
            
            if len(new_data) == 1:
                continue
            
            #print("")
            #print("")
            #print("---Next Iteration---")
            
            
            if distanceMethod == 'manhattan':
                matrix = calculate_inital_abstraction_matrix(new_data, manhattan_distance)
                
            elif distanceMethod == 'euclidean':
                matrix = calculate_inital_abstraction_matrix(new_data, euclidean_distance)

            elif distanceMethod == 'maximum':
                matrix = calculate_inital_abstraction_matrix(new_data, maximum_distance)

            else:
                break
            #matrix = calculate_inital_abstraction_matrix(new_data, euclidean_distance)

            #get the two points with the new minimum distance
            single_linkage_indices = single_linkage_get_indices(matrix)
                
            #get two points from given index that are the new cluster
            point_a = new_data[single_linkage_indices[0]]
            point_b = new_data[single_linkage_indices[1]]
            
            #nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)
            #delete the point from the dataset, that is not nearest
            #point_to_remove = nearest_point[1]
            
            #add point to current cluster
            if is_element_in_array(clusters, point_a) or is_element_in_array(clusters, point_b):
                #print("Erweitere Cluster")
 
                #get element number of the cluster and append point to the current cluster
                if is_element_in_array(clusters, point_a):
                    arrayLocation = is_element_in_array_location(clusters, point_a)
                    pointToAppend = point_b
                elif is_element_in_array(clusters, point_b):
                    arrayLocation = is_element_in_array_location(clusters, point_b)
                    pointToAppend = point_a
                    
                #print(arrayLocation)
                
                #append pointToAppend to cluster:
                #clusters = np.insert(clusters, arrayLocation[0], pointToAppend, axis=arrayLocation[1])
                #print(clusters[arrayLocation[0]])
                #clusters[arrayLocation[0], arrayLocation[1]]
                
                #newClusters1 = clusters[arrayLocation[0]]
                #print(clusters[arrayLocation[0]])
                pointsToAppend = np.vstack([clusters[arrayLocation[0]], pointToAppend])
                
                newClusters = []
                
                newClusters.append(pointsToAppend)

                #newClusters = np.append(clusters[arrayLocation[0]], [pointToAppend], axis=0)
                #newClusters = np.array([[point_a, point_b]])
                clusterCounter = 0
                
                for cluster in clusters:
                    if clusterCounter == arrayLocation[0]:
                        clusterCounter += 1
                        
                    else:
                        #newClusters = np.concatenate([newClusters, [cluster]])  #dimensions are not valid! -> was anderes einfallen lassen!! #letztes puzzelstück -> wie den bums richtig zusammenfügen???!!!
                        newClusters.append(cluster)
                        clusterCounter += 1
                        
                
                #print("UPDATED CLUSTER:")
                #print(newClusters)
                print("-------")
                
                clusters = newClusters

            #create new cluster
            else:
                #print("Definiere neues Cluster")
                #define cluster elements if ist an new cluster
                #clusters = np.append(clusters,[[point_a, point_b]], axis=0)
                clusters.append([point_a, point_b])
                #print(clusters)
            
            #print("Aktuelle Cluster:")
            #print(clusters)
            
            print("DIGRAPH - Abstandsmatrix")
            #createDigraph(matrix, new_data, iteration)
            jsonDict["DigraphIteration{}".format(iteration)] = matrix.tolist() #createDigraph(matrix, new_data, iteration)

            
            if distanceMethod == 'manhattan':
                nearest_point = get_nearest_point(data, point_a, point_b, manhattan_distance)
                
            elif distanceMethod == 'euclidean':
                nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)

            elif distanceMethod == 'maximum':
                nearest_point = get_nearest_point(data, point_a, point_b, maximum_distance)

            else:
                break
                
            #nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)
            #delete the point from the dataset, that is not nearest
            point_to_remove = nearest_point[1]
            

            
            #define new dataset
            new_data = np.array([point for point in new_data if not np.array_equal(point, point_to_remove)])
            #print("Neuer Hauptdatensatz")
            #print(jsonDict)

    #print(jsonDict)
    #jsonDict["taskDescription"] = 
    jsonDict["iterations"] = iteration
    with open(f"{pathlib.Path(__file__).parent.resolve()}/data.json", "w+",  encoding="utf8") as f:
        json.dump(jsonDict, f)

    return json.dumps(jsonDict)
    
# Anzahl der Datenpunktansammlungen (Cluster)
#numClusters = int(sys.argv[1])
#pointsPerCluster = int(sys.argv[2])
#nodeRangeStart = int(sys.argv[3])
#nodeRangeEnd = int(sys.argv[4])
#distanceMethod = int(sys.argv[5])
#linkageMethod = int(sys.argv[6])

#numClusters = 2
#pointsPerCluster = 3
#nodeRangeStart = 0
#nodeRangeEnd = 25
#distanceMethod = 'euclidean'
#linkageMethod = 'single'
#Hauptfunktion ausfuehren
#clusterAnalysisMain(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod)

#EXECUTE
clusterAnalysisMain()


#TODO
#Eingabevalidierung!!!