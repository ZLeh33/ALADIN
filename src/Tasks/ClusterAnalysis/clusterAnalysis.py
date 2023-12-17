#Clusteranalyse

import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import graphviz
import math

#functions
def generate_clusters(n_clusters, m_points_per_cluster):
    # Generate random cluster centers
    cluster_centers = np.random.randint(0, 30, size=(n_clusters, 2))
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


def clusterAnalysisMain():
    #data = generate_clusters(num_clusters, points_per_cluster)
    data = np.array([[2, 3],
                         [5, 2],
                         [5, 3],
                         [1, 4],
                         [4, 5]])
    

    
    for iteration in range(data.shape[0]):
        #erste iteration
        if(iteration == 0):
            
            clusters = []
            
            #inital abstraction matrix
            print("---Inital Iteration---")
            matrix = calculate_inital_abstraction_matrix(data, euclidean_distance)
            print("Abstandsmatrix:")
            print(matrix)
            single_linkage_indices = single_linkage_get_indices(matrix)
            #print(single_linkage_indices)
            
            #get two points from given index that are the first cluster
            point_a = data[single_linkage_indices[0]]
            point_b = data[single_linkage_indices[1]]
            
            nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)
            #delete the point from the dataset, that is not nearest
            point_to_remove = nearest_point[1]
            
            #define cluster elements
            #clusters = np.array([[point_a, point_b]])
            clusters.append([point_a, point_b])
            print("Aktuelle Cluster:")
            print(clusters)
            
            #define new dataset
            new_data = np.array([point for point in data if not np.array_equal(point, point_to_remove)])
            print("Neuer Hauptdatensatz")
            print(new_data)

        #alle weiteren iterationen  
        elif(iteration > 0):
            print("")
            print("")
            print("---Next Iteration---")
            matrix = calculate_inital_abstraction_matrix(new_data, euclidean_distance)
            print("Abstandsmatrix:")
            print(matrix)
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
                print("Erweitere Cluster")
 
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
                print(clusters[arrayLocation[0]])
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
                        
                
                print("UPDATED CLUSTER:")
                print(newClusters)
                print("-------")
                
                clusters = newClusters

            #create new cluster
            else:
                print("Definiere neues Cluster")
                #define cluster elements if ist an new cluster
                #clusters = np.append(clusters,[[point_a, point_b]], axis=0)
                clusters.append([point_a, point_b])
                #print(clusters)
            
            print("Aktuelle Cluster:")
            print(clusters)
            
            nearest_point = get_nearest_point(data, point_a, point_b, euclidean_distance)
            #delete the point from the dataset, that is not nearest
            point_to_remove = nearest_point[1]
            
            #define new dataset
            new_data = np.array([point for point in new_data if not np.array_equal(point, point_to_remove)])
            print("Neuer Hauptdatensatz")
            print(new_data)
    return "HIER STEHT TEXT"
    
# Anzahl der Datenpunktansammlungen (Cluster)
num_clusters = 2
# Anzahl der Datenpunkte pro Cluster
points_per_cluster = 3
#Hauptfunktion ausfuehren
clusterAnalysisMain()
