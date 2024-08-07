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
import string

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
    letter = list(string.ascii_uppercase)
    letterPosition = 0

    html = '<table style="border: 1px solid black;margin-left: auto;margin-right: auto;">\n'
    html += '<tr><th style="border: 1px solid black;"> Name Datenpunkt </th><th style="border: 1px solid black;"> Position X-Achse </th><th style="border: 1px solid black;"> Position Y-Achse </th></tr>'
    for row in array:
        html += '<tr>\n'
        html += f'<td style="border: 1px solid black; border-collapse: collapse;">{letter[letterPosition]}</td>'
        for item in row:
            html += f'<td style="border: 1px solid black; border-collapse: collapse;">{item}</td>\n'
        html += '</tr>\n'
        letterPosition += 1
    html += '</table>'
    return html

def generate_task_description(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean, data):
    finalDescription = ""

    #add the main task descripton to the variable
    finalDescription += "<p>In dieser Aufgabe sollen Sie zeigen, dass Sie die hierarchische Clusteranalyse verstanden haben und diese anwenden koennen.</p><br>"

    #add example data to description
    finalDescription += "<p>Sie erhalten eine Sammlung von Datenpunkten, für die Sie die Analyse durchführen sollen.</p><br>"
    finalDescription += array_to_html_table(data)
    finalDescription += "<br><br>"

    #add more task description
    if str(diagramHelpBoolean) == "false":
        finalDescription += "<p>Zeichnen Sie im ersten Schritt die Datenpunkte in ein Koordinatensystem als visuelle Hilfe ein, oder nutzen Sie alternativ das Streudiagramm, welches Ihnen ALADIN als Hilfestellung bietet.</p>"

    #if diagram help checkbox is checked
    if str(diagramHelpBoolean) == "true":
        finalDescription += "<br><p>Sie haben bei der Aufgabenerstellung ausgewaehlt, dass Ihnen das Streudiagramm angezeigt werden soll. Das folgende Diagramm zeigt die verteilten Datenpunkte im Koordinatensystem.</p><br>"

        #add base64 img
        #TODO
        print_diagram(data)
        with open("streudiagramm.png", "rb") as image_file:
            encoded_string = str(base64.b64encode(image_file.read()))

        finalDescription += f'<br><img style="display: block;margin-left: auto;margin-right: auto;" src="data:image/png;base64, {encoded_string[2:-1]}" alt="Streudiagramm" /><br><br>'

    #help description for calculating distance matrix
    if str(distanceMatrixBoolean) == "true":
        finalDescription += f"<p>Hilfe zur Distanzberechnung</p><p>So haben die {str(distanceMethod)} Methode zur Berechnung der Distanz gewaehlt. Diese wird wie folgt berechnet:</p>"
        if distanceMethod == 'manhattan':
            finalDescription += '<div style="text-align:center;"><br><br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>=</mo><mover><mo>=</mo><mo>^</mo></mover><mtext>&nbsp;Datenpunkt&nbsp;</mtext><mn>1</mn></math></p>'
            finalDescription += '<br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>b</mi><mo>=</mo><mover><mo>=</mo><mo>^</mo></mover><mtext>&nbsp;Datenpunkt&nbsp;</mtext><mn>2</mn></math></p>'
            finalDescription += '<br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>d</mi><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo><mo>=</mo><munderover><mo>&#x2211;</mo><mi>i</mi><mo>=</mo><mn>1</mn><mi>n</mi></munderover><mo    >|</mo><msub><mi>a</mi><mi>i</mi></msub><mo>-</mo><msub><mi>b</mi><mi>i</mi></msub><mo>|</mo></math></p><br><br></div>'
                
        elif distanceMethod == 'euclidean':
            finalDescription += '<div style="text-align:center;"><br><br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>=</mo><mover><mo>=</mo><mo>^</mo></mover><mtext>&nbsp;Datenpunkt&nbsp;</mtext><mn>1</mn></math></p>'
            finalDescription += '<br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>b</mi><mo>=</mo><mover><mo>=</mo><mo>^</mo></mover><mtext>&nbsp;Datenpunkt&nbsp;</mtext><mn>2</mn></math></p>'
            finalDescription += '<br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>d</mi><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo><mo>=</mo><mo>|</mo><mi>a</mi><mo>-</mo><mi>b</mi><mo>|</mo></math></p><br><br></div>'

        elif distanceMethod == 'maximum':
            finalDescription += '<div style="text-align:center;"><br><br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>a</mi><mo>=</mo><mover><mo>=</mo><mo>^</mo></mover><mtext>&nbsp;Datenpunkt&nbsp;</mtext><mn>1</mn></math></p>'
            finalDescription += '<br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>b</mi><mo>=</mo><mover><mo>=</mo><mo>^</mo></mover><mtext>&nbsp;Datenpunkt&nbsp;</mtext><mn>2</mn></math></p>'
            finalDescription += '<br><p><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>d</mi><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo><mo>=</mo><mrow><mo>max</mo><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo></mrow></math></p><br><br></div>'

    #help description for draw the dendrogram
    if str(dendogramBoolean) == "true":
        finalDescription += "<p>Um ein Dendrogramm aus einer Distanzmatrix zu erstellen, verwendet man zuerst einen hierarchischen Clustering-Algorithmus (wie z.B. Single-Linkage, Complete-Linkage oder Average-Linkage), um die Cluster-Hierarchie aus der Distanzmatrix zu erzeugen. Anschließend stellt man diese Hierarchie graphisch als Dendrogramm dar, wobei die Länge der Verbindungslinien die Distanzen oder Ähnlichkeiten zwischen den Clustern repräsentiert.</p>"
    

    finalDescription += "<p>Berechnen Sie nun im nächsten Schritt die einzelnen Distanzmatrizen bis zu einer 2x2 Matrix und gebe sie Ihre Lösung in den Editor ein.</p>"
    finalDescription += f"<p>Nutzen Sie für die Berechnung der Distanzen zwischen den einzelnen Datenpunkten die Berechnungsmethode {distanceMethod}</p>"

    return finalDescription

def generate_task_description_preview(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean, data):
    finalDescription = ""

    #add the main task descripton to the variable
    finalDescription += "<p>Vorschau der Datentabelle:</p><br>"

    finalDescription += array_to_html_table(data)
    finalDescription += "<br><br>"

    #if diagram help checkbox is checked
    finalDescription += "<br><p>Vorschau des Streudiagramms:</p><br>"

    #add base64 img
    print_diagram(data)
    with open("streudiagramm.png", "rb") as image_file:
        encoded_string = str(base64.b64encode(image_file.read()))

    finalDescription += f'<br><img style="display: block;margin-left: auto;margin-right: auto;" src="data:image/png;base64, {encoded_string[2:-1]}" alt="Streudiagramm" /><br><br>'

    return finalDescription


def print_diagram(data):
    # Streudiagramm zeichnen
    # Extracting X and Y coordinates from the data
    
    x = [point[0] for point in data]
    y = [point[1] for point in data]

    length = len(x)
    matrixHeaders = list(string.ascii_uppercase)

    n = matrixHeaders[0:length]

    # Erstellen des Plots
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y)  # Verwendung von scatter() anstelle von plot()

    # Hinzufügen von Beschriftungen an jedem Punkt
    for i, label in enumerate(n):
        plt.text(x[i], y[i], n[i], fontsize=12)

    plt.title('Streudiagramm')
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')

    # Display the plot
    #plt.show()
    plt.savefig('streudiagramm.png')

def generate_matrix_headers(data, iterationNumber):
    x = [point[0] for point in data]
    length = len(x)
    matrixHeaders = list(string.ascii_uppercase)
    
    return matrixHeaders[0:(length)] #- int(iterationNumber))]

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
    
    #Testdata
    data = np.array([[2, 3],[5, 2],[5, 3],[1, 4],[4, 5]])
        

    #print(data)

    taskDescription = generate_task_description(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean, data)

    taskDescriptionPreview = generate_task_description_preview(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean, data)
    #TODO: atrribute richtig machen aus Fronted -> destrukturieren
    #aufgabenbeschreibung generieren

    
    
    #createScatterDiagram(data)
    jsonDict = {}
    #jsonDict["Dendogram"] = createDendogramDotLanguage(data, distanceMethod)
    jsonDict["taskDescription"] = taskDescription
    jsonDict["taskDescriptionPreview"] = taskDescriptionPreview
    

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

            #matrix headers
            jsonDict["DigraphIterationHeader{}".format(iteration)] = generate_matrix_headers(data, iteration)
            
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
            
            #matrix headers
            jsonDict["DigraphIterationHeader{}".format(iteration)] = generate_matrix_headers(new_data, iteration)

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


#algo überarbeiten zur generierung der einzelnen punkte für dei clusteranalyse
#leute sollen verstehen was diese aufgabe soll -> "wir wollen hierarchsiche clusteranalyse üben oder in der prüfung abfragen"