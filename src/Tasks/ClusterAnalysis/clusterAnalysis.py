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


def clusterAnalysisMain(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod):
    
    numClusters = int(sys.argv[2])
    pointsPerCluster = int(sys.argv[1])
    nodeRangeStart = int(sys.argv[9])
    nodeRangeEnd = int(sys.argv[10])
    diagramHelpBoolean = sys.argv[4]
    dendogramBoolean = sys.argv[5]
    linkageMethod = sys.argv[8]
    distanceMatrixBoolean = sys.argv[6]
    data = generate_clusters(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd)
    
    #taskDescription = generate_task_description(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod, diagramHelpBoolean, dendogramBoolean, distanceMatrixBoolean)
    #TODO: atrribute richtig machen aus Fronted -> destrukturieren
    #aufgabenbeschreibung generieren

    distanceMethod = sys.argv[7]

    #data = np.array([[2, 3],
    #                     [5, 2],
    #                     [5, 3],
    #                     [1, 4],
    #                     [4, 5]])
    
    
    #createScatterDiagram(data)
    jsonDict = {}
    
    jsonDict["Dendogram"] = createDendogramDotLanguage(data, distanceMethod)
        
    
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
            print("DIGRAPH - Abstandsmatrix")
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
            
            print("")
            print("")
            print("---Next Iteration---")
            
            
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

    print(jsonDict)
    jsonDict["iterations"] = iteration
    with open("data.json", "w+",  encoding="utf8") as f:
        json.dump(jsonDict, f)

    return json.dumps(jsonDict)
    
# Anzahl der Datenpunktansammlungen (Cluster)
#numClusters = int(sys.argv[1])
#pointsPerCluster = int(sys.argv[2])
#nodeRangeStart = int(sys.argv[3])
#nodeRangeEnd = int(sys.argv[4])
#distanceMethod = int(sys.argv[5])
#linkageMethod = int(sys.argv[6])

numClusters = 2
pointsPerCluster = 3
nodeRangeStart = 0
nodeRangeEnd = 25
distanceMethod = 'euclidean'
linkageMethod = 'single'
#Hauptfunktion ausfuehren
clusterAnalysisMain(numClusters, pointsPerCluster, nodeRangeStart, nodeRangeEnd, distanceMethod, linkageMethod)


#TODO
#Eingabevalidierung!!!