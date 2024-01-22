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

    html = '<table style="border: 1px solid black;">\n'
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
    finalDescription += "<p>Sie erhalten eine Sammlung von Datenpunkten, für die Sie die Analyse durchführen sollen.</p>"
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

        finalDescription += f'<br><img src="data:image/png;base64, {encoded_string[2:-1]}" alt="Streudiagramm" /><br><br>'

    #help description for calculating distance matrix
    if str(distanceMatrixBoolean) == "true":
        finalDescription += f"<p>Hilfe zur Distanzberechnung</p><p>So haben die {str(distanceMethod)} Methode zur Berechnung der Distanz gewaehlt. Diese wird wie folgt berechnet:</p>"
        if distanceMethod == 'manhattan':
            finalDescription += '<br><br><math xmlns="http://www.w3.org/1998/Math/MathML"><mi>d</mi><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo><mo>=</mo><munderover><mo>&#x2211;</mo><mi>i</mi><mo>=</mo><mn>1</mn><mi>n</mi></munderover><mo>|</mo><msub><mi>a</mi><mi>i</mi></msub><mo>-</mo><msub><mi>b</mi><mi>i</mi></msub><mo>|</mo></math><br><br>'
                
        elif distanceMethod == 'euclidean':
            finalDescription += '<p><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAY4AAABuCAYAAAAwN/RKAAAMPmlDQ1BJQ0MgUHJvZmlsZQAASImVVwdYU8kWnluSkEAIEEBASuhNEJESQEoILYD0biMkAUKJMRBU7MiigmtBxQI2dFVEsdPsiJ1FsffFgoKyLhbsypsU0HVf+d75vrn3v/+c+c+Zc+eWAYB2gisW56AaAOSK8iUxwf6MpOQUBqkbIAAHNGANLLm8PDErKiocQBs8/93e3YDe0K46yLT+2f9fTZMvyOMBgERBnMbP4+VCfBAAvIonluQDQJTx5lPzxTIMG9CWwAQhXijDGQpcJcNpCrxX7hMXw4a4FQAVNS5XkgGA+mXIMwp4GVBDvQ9iJxFfKAKAxoDYJzd3Mh/iVIhtoI8YYpk+M+0HnYy/aaYNaXK5GUNYMRe5qQQI88Q53On/Zzn+t+XmSAdjWMGmlikJiZHNGdbtVvbkMBlWg7hXlBYRCbEWxB+EfLk/xCglUxoSr/BHDXl5bFgzoAuxE58bEAaxIcRBopyIcCWfli4M4kAMVwg6TZjPiYNYD+KFgrzAWKXPJsnkGGUstD5dwmYp+XNciTyuLNYDaXY8S6n/OlPAUepj6oWZcYkQUyC2KBAmRECsDrFjXnZsmNJnTGEmO2LQRyKNkeVvAXGMQBTsr9DHCtIlQTFK/9LcvMH5YpsyhZwIJd6fnxkXoqgP1srjyvOHc8EuC0Ss+EEdQV5S+OBc+IKAQMXcsW6BKD5WqfNBnO8foxiLU8Q5UUp/3EyQEyzjzSB2ySuIVY7FE/LhglTo4+ni/Kg4RZ54YRY3NEqRD74MhAM2CAAMIIUtDUwGWUDY3tvQC68UPUGACyQgAwiAg5IZHJEo7xHBYywoBH9CJAB5Q+P85b0CUAD5r0Os4ugA0uW9BfIR2eApxLkgDOTAa6l8lGgoWgJ4AhnhP6JzYePBfHNgk/X/e36Q/c6wIBOuZKSDERm0QU9iIDGAGEIMItriBrgP7oWHw6MfbM44E/cYnMd3f8JTQgfhEeE6oZNwe5KwSPJTlmNBJ9QPUtYi7cda4FZQ0xX3x72hOlTGdXED4IC7wDgs3BdGdoUsW5m3rCqMn7T/NoMf7obSj+xERsnDyH5km59Hqtupuw6pyGr9Y30UuaYN1Zs91PNzfPYP1efDc9jPnthC7AB2FjuJnceOYA2AgR3HGrE27KgMD62uJ/LVNRgtRp5PNtQR/iPe4J2VVTLPqdapx+mLoi9fME32jgbsyeLpEmFGZj6DBb8IAgZHxHMcwXB2cnYBQPZ9Uby+3kTLvxuIbtt3bv4fAHgfHxgYOPydCz0OwD53+Pg3fedsmPDToQrAuSaeVFKg4HDZgQDfEjT4pOkDY2AObOB8nIEb8AJ+IBCEgkgQB5LBRJh9JlznEjAVzATzQAkoA8vAKrAObARbwA6wG+wHDeAIOAnOgIvgMrgO7sLV0wVegD7wDnxGEISEUBE6oo+YIJaIPeKMMBEfJBAJR2KQZCQVyUBEiBSZicxHypByZB2yGalB9iFNyEnkPNKB3EYeIj3Ia+QTiqFqqDZqhFqhI1EmykLD0Dh0ApqBTkEL0WJ0CboGrUZ3ofXoSfQieh3tRF+g/RjAVDFdzBRzwJgYG4vEUrB0TILNxkqxCqwaq8Oa4X2+inVivdhHnIjTcQbuAFdwCB6P8/Ap+Gx8Mb4O34HX4634Vfwh3od/I1AJhgR7gieBQ0giZBCmEkoIFYRthEOE0/BZ6iK8IxKJukRrojt8FpOJWcQZxMXE9cQ9xBPEDuJjYj+JRNIn2ZO8SZEkLimfVEJaS9pFOk66QuoifVBRVTFRcVYJUklREakUqVSo7FQ5pnJF5ZnKZ7IG2ZLsSY4k88nTyUvJW8nN5EvkLvJniibFmuJNiaNkUeZR1lDqKKcp9yhvVFVVzVQ9VKNVhapzVdeo7lU9p/pQ9aOalpqdGlttvJpUbYnadrUTarfV3lCpVCuqHzWFmk9dQq2hnqI+oH5Qp6s7qnPU+epz1CvV69WvqL+kkWmWNBZtIq2QVkE7QLtE69Uga1hpsDW4GrM1KjWaNG5q9GvSNUdpRmrmai7W3Kl5XrNbi6RlpRWoxdcq1tqidUrrMR2jm9PZdB59Pn0r/TS9S5uoba3N0c7SLtPerd2u3aejpeOik6AzTadS56hOpy6ma6XL0c3RXaq7X/eG7qdhRsNYwwTDFg2rG3Zl2Hu94Xp+egK9Ur09etf1Pukz9AP1s/WX6zfo3zfADewMog2mGmwwOG3QO1x7uNdw3vDS4fuH3zFEDe0MYwxnGG4xbDPsNzI2CjYSG601OmXUa6xr7GecZbzS+JhxjwndxMdEaLLS5LjJc4YOg8XIYaxhtDL6TA1NQ0ylpptN200/m1mbxZsVme0xu29OMWeap5uvNG8x77MwsRhrMdOi1uKOJdmSaZlpudryrOV7K2urRKsFVg1W3dZ61hzrQuta63s2VBtfmyk21TbXbIm2TNts2/W2l+1QO1e7TLtKu0v2qL2bvdB+vX3HCMIIjxGiEdUjbjqoObAcChxqHR466jqGOxY5Nji+HGkxMmXk8pFnR35zcnXKcdrqdHeU1qjQUUWjmke9drZz5jlXOl8bTR0dNHrO6MbRr1zsXQQuG1xuudJdx7oucG1x/erm7iZxq3PrcbdwT3Wvcr/J1GZGMRczz3kQPPw95ngc8fjo6eaZ77nf8y8vB69sr51e3WOsxwjGbB3z2NvMm+u92bvTh+GT6rPJp9PX1JfrW+37yM/cj++3ze8Zy5aVxdrFeunv5C/xP+T/nu3JnsU+EYAFBAeUBrQHagXGB64LfBBkFpQRVBvUF+waPCP4RAghJCxkechNjhGHx6nh9IW6h84KbQ1TC4sNWxf2KNwuXBLePBYdGzp2xdh7EZYRooiGSBDJiVwReT/KOmpK1OFoYnRUdGX005hRMTNjzsbSYyfF7ox9F+cftzTubrxNvDS+JYGWMD6hJuF9YkBieWJn0sikWUkXkw2ShcmNKaSUhJRtKf3jAsetGtc13nV8yfgbE6wnTJtwfqLBxJyJRyfRJnEnHUglpCam7kz9wo3kVnP70zhpVWl9PDZvNe8F34+/kt8j8BaUC56le6eXp3dneGesyOjJ9M2syOwVsoXrhK+yQrI2Zr3Pjszenj2Qk5izJ1clNzW3SaQlyha1TjaePG1yh9heXCLunOI5ZdWUPkmYZFsekjchrzFfG/7It0ltpL9IHxb4FFQWfJiaMPXANM1pomlt0+2mL5r+rDCo8LcZ+AzejJaZpjPnzXw4izVr82xkdtrsljnmc4rndM0NnrtjHmVe9rzfi5yKyovezk+c31xsVDy3+PEvwb/UlqiXSEpuLvBasHEhvlC4sH3R6EVrF30r5ZdeKHMqqyj7spi3+MKvo35d8+vAkvQl7Uvdlm5YRlwmWnZjue/yHeWa5YXlj1eMXVG/krGydOXbVZNWna9wqdi4mrJaurpzTfiaxrUWa5et/bIuc931Sv/KPVWGVYuq3q/nr7+ywW9D3UajjWUbP20Sbrq1OXhzfbVVdcUW4paCLU+3Jmw9+xvzt5ptBtvKtn3dLtreuSNmR2uNe03NTsOdS2vRWmltz67xuy7vDtjdWOdQt3mP7p6yvWCvdO/zfan7buwP299ygHmg7qDlwapD9EOl9Uj99Pq+hsyGzsbkxo6m0KaWZq/mQ4cdD28/Ynqk8qjO0aXHKMeKjw0cLzzef0J8ovdkxsnHLZNa7p5KOnWtNbq1/XTY6XNngs6cOss6e/yc97kj5z3PN11gXmi46Haxvs217dDvrr8fandrr7/kfqnxssfl5o4xHceu+F45eTXg6plrnGsXr0dc77gRf+PWzfE3O2/xb3Xfzrn96k7Bnc93594j3Cu9r3G/4oHhg+o/bP/Y0+nWefRhwMO2R7GP7j7mPX7xJO/Jl67ip9SnFc9MntV0O3cf6Qnqufx83POuF+IXn3tL/tT8s+qlzcuDf/n91daX1Nf1SvJq4PXiN/pvtr91edvSH9X/4F3uu8/vSz/of9jxkfnx7KfET88+T/1C+rLmq+3X5m9h3+4N5A4MiLkSrvxXAIMNTU8H4PV2AKjJANDh/owyTrH/kxui2LPKEfhPWLFHlJsbAHXw/z26F/7d3ARg71a4/YL6tPEARFEBiPMA6OjRQ21wrybfV8qMCPcBm6K+puWmgX9jij3nD3n/fAYyVRfw8/lfaIh8bGQqdDoAAACKZVhJZk1NACoAAAAIAAQBGgAFAAAAAQAAAD4BGwAFAAAAAQAAAEYBKAADAAAAAQACAACHaQAEAAAAAQAAAE4AAAAAAAAAkAAAAAEAAACQAAAAAQADkoYABwAAABIAAAB4oAIABAAAAAEAAAGOoAMABAAAAAEAAABuAAAAAEFTQ0lJAAAAU2NyZWVuc2hvdLaR2z4AAAAJcEhZcwAAFiUAABYlAUlSJPAAAAHWaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA2LjAuMCI+CiAgIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgICAgIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIj4KICAgICAgICAgPGV4aWY6UGl4ZWxZRGltZW5zaW9uPjExMDwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4zOTg8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpVc2VyQ29tbWVudD5TY3JlZW5zaG90PC9leGlmOlVzZXJDb21tZW50PgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KUc8Z3AAAABxpRE9UAAAAAgAAAAAAAAA3AAAAKAAAADcAAAA3AAAQREBPPowAABAQSURBVHgB7F0HeBXFFj6oSFFEevVRFHiCykMFVEDkCfb2EKSX0EOAEFqEkEaIIQmhhgQILZAQAgjYRUUEwY6AShMIoHQEQgdRcf7FGXaXvWXvTd5H7j3n+5Ipe2Z297+z+085c7bQmdwTV4iFEWAEGAFGgBFwE4FCTBxuIsVqjAAjwAgwAhoCTBzcEBgBRoARYARsIcDEYQsuVmYEGAFGgBFg4uA2wAgwAowAI2ALASYOW3CxMiPACDACjAATB7cBRoARYAQYAVsIMHHYgouVGQFGgBFgBJg4uA0wAowAI8AI2EKAicMWXKzMCDACjAAjwMTBbYARYAQYAUbAFgJMHLbgYmVGgBFgBBgBJg5uA4wAI8AIMAK2EGDisAUXKzMCjAAjwAgwcXAbYAQYAUaAEbCFABOHLbhYmRFgBBgBRoCJg9sAI8AIMAKMgC0EmDhswcXKjAAjwAgwAkwc3AYYAUaAEWAEbCHAxGELLlZmBBgBRoARYOLgNsAIMAKMACNgCwEmDltwsTIjwAgwAowAEwe3AUaAEWAEGAFbCDBx2IKLlRkBRoARYASYOLgNMAKMACPACNhCgInDFlyszAgwAowAI8DEwW2AEWAEGAFGwBYCTBy24GJlRoARYAQYASYObgOMACPACDACthBg4rAFFyszAowAI8AIMHFwG2AEGAFGgBGwhQAThy24WJkRYAQYAUaAiYPbACPACDACjIAtBJg43IDr7LlztGPHz7Rt+3bau3cvBfbrS2VKl3ajJNGVK1do46ZN9GCDBm7p36hKl37/Xdz7Ptq5cyft3LWLqlWrRq1fedmty7146ZKGX/0H7ndL31+VVq1eTdNnpGm3f/PNN9OizAX+CkW+3PeZs2dp9+7dog3vopw9e6hVy5biufyPR+dKmjiZvvr6a61szRo1KD4u1qN6CmohJg6LX+78hQs0OjySTubm0pkzZ+jPP/80aKUmT6WKFSsY8qwShw4fpuiYWDpy5AhNGJ9ANapXt1K7YfNWvPU2vf/hSsoVOFy+fNlwnQ8/9BCFjQw15DlKzJ47j9597336d506FBkxmooWKeJI1a/z33v/A5o1Z67CYPnSxSrOEc8QSEyaQFu3bbd8jgP79qGnWrX0qOKomLG0efMPWtlKFStSSvIUj+opqIWYOCx+ORBHVHQMnTp9io4ePWbQKCJeeu70BPESwAsTI44mjz1Kw4aEGOopCIm3332P1q79nI4eO6Y9ePpr7i9GXa1aPqnPchg/dfo0DRsRSr/9dpxKly4lSDSRSt5xh0N9fz3AxJH3v/ykKVO1kfLBQ4eu6/zMnZ1Gd5Ys6dFJmThyT1zxCDk/KbQgI5OWrXhL3S2mW6IiwlXaKjJnXjq9I166kOeefYZ69+xhpVag8tq062AYec2bM8vWy/93MWIZFRZOu3NyqFixYjQhMcGtUVuBAsnLi2Xi8BJAJ8UxvTri9VFKo0SJEjR/7myVthth4mDicNpmklNSadWnq5VOz4Du9MLzz6m0OYK5z3Xr12vZjzdrSiHBg8wqBS6de+oUBfTsra77DjFaSBfEYVcw5Tdw8BA6JHp/t9xyC8XFxtA9d99ttxqf1WfiyL+f9uNPVlHK9BnqBI80bkyhw4eqtN0IEwcTh9M207d/kGG6Km1GKpUtU8ayTPqCDMK6AAQvxMT4OEu9gpb5yapPaVrqdHXZTZs8RkNDBqu0nci58+epd99AuiCmA0Eec2bNpBK3326nCp/VZeLIv582Lj6Bvvn2O3UCdOjQsfNUmDiYOBy2Hax1dOrSTR0vXrw4Zc6fp9L6yDfffktx8YlaVqFChQgE467llb6eGzEeExtH32/cqC4NPTX02DyVdeu/oKSJk7Tide+9l2Jjoj2tyqfKMXHk38/ZqWt3Oi86LVKyhMWaN0YaTBxMHLItXRd+tmYtTZ6arPIferABjR41UqVl5LSwvOrRq49aA3j5pRepe9cu8nCBDzt07koXL17U7gOkmJ2VSYXFaMEb6T9gEMHqDBIU2I9aPvlfb6rzibJMHPnzM8LABTMHUipUqEDTp02VSY9CJg4mDocNJzYunr7bsEEdHxAUSE+2aKHSMpIwPom+/OqqTTdGJVh0gx2+L8jBg4coaFCwupUqVapQ8uSJKu1pZPuOHTRSLJZDgNXM6SlUulQpT6vziXJMHPnzM8K4BUYuUp5/7lnq1SNAJj0KmTiYOBw2nI5imgpz8VIyxDTVbYIY9LJ//wGx4HvN1LZPr5707DNP61UKdDx78RJaJP6kvPLyS9StS2eZ9CqElQusXSCORnNenaCAFWbiyJ8fTN/OcAYYZWBPkTfCxMHEoU0x7fvlF0Lvum7de7WeLyx/+g+81tMuW7YMpU1Pva6tYV0D6xtSvLENl3UglLtcz549R3Vq16Jy5cpph7G4fPDgQTom9lbUrVvXYzt0/bmcxYcOD9V22UqdpIR4qlmzhkxq15mTs4fOnTtLVatWpapiRHLTTTep484iy0VPcP4/PUFMgWHeucittzor4tPH8po40Eb27N1Lf/31F9WvX5+KFS2q4Xfi5EnNsu2UsJbDWpW7v1dBBB/7qNq276imkTG6XZqdZbiVqzjtI7TB6tWrUbmyZQ3HrRJMHH5MHJs2b6aFWdmq1ysbSKVKlTSLC/S2pWCzGza9meW1Dp3UxqLbb7uNFqRf2/lr1nWVxl4H7LBevnwFwc2JXrCI3OKJ5gbrptdHDKfGjRrq1fI0jhcO9m/g4YMULlyYFov1DQgsVFJnzNR2lWsZ//zDBsmA7l3p6Vat9NmWcZD14CHD1DFMH2AawV8lL4jjZO4pyspaRKvXrKE//vhDQYmXIszIT5w4Qeu/+FLlY73qVvG7+qrATdCo0RHq9jDSwIgDbRsdl+wlS9XzK5XQSYTVoLNRCROHHxIHdjLHvjFOEQYeKvisqVO7Nq3+bI1atJUNCWF0ZAQ9cP99+iz64cefKDJ6jMpr1LAhjQwdrtJ2Ilu2bqWx4prkInRJsaP1FbHIXlT0Eld+9DHt3bfvuury+6E339/999WjMVGRFJ+YpPz0XHdR/2S4SwL6jYUg7JSpkx1V6fP53hIHdvrPS5+viB4m4U8JlxogC7iOOS3avV7Kly9HM1Km6bN8Lg4XLsBVSkC3rtRSdAKDQ4ZongxkvjnEO2F8wjiCHyorYeLwM+LAyzAm9g3VG8MLemx0lJhmqaK1Dzjk6yisiGQvG5kY3qKnbR7Sw6QUpqVS7LjhkGUQZi3KpsVL31RZVusIessmKP4/XrLYMIWNU1KwfrNJ+OeRU3PYRV+rVi3av3+/IJJvpJoWYnSSlTHfpZEARhwYeUiZnpJMFcqXl0mPwi1bt1F4ZJRHZe0U6tq5E+G3yivxlDiwsRIdGNw3BC89jEYbNXxYXdqRo0epX/8BKo0I1uLwm/qy9AsaqPmKk/c4eWISjRH+444LMsVz/egjjYUHg4q0YcP32rSe1EPobC8WE4cfEceG7zdSbNw4RQoYkqYIh4Vm09I+gUHaGoJsRHfXrKn1PmRahgHCBBcOAKXAFYldD7ALMhfSMjE1JQU9opdefEEmVTg6IlK9GJD54gvPU4/u1/aYKMU8jPTuF2jolbVo3lybAoHlWHRkuGHXN6bY4JtLL+Fho1x6H50waTJ9vm69KubuSEUVsIiYR0oWKnmS1bF9O2rb5tU8qQuVeEIcII3QkWGaKxfUAdJIGPeG4bdBPqR9py50SXSMpIwdE0X1xDqZrwo6gR3EPUvBVHJp4dX6l19/1UYSEeFhBrc5UWNiaPMPP0p1LVy2JFvD1JApEkwcfkIc27bvoLDwCEUa2LWcKmy5rXaBDxJuMX4VvWgpnTq0pzavtpZJFerXN5BpXjhWig4i2GWO3eZSnDlDhJddrMlIyQvLEFmXVWje/IgXEkZhmDqbKsxxzbiZFyFRpyMS1J9vRtos+nDlRyorL3x7/bRlixhxRKs68yviqF14ej5PiAP3ifuVMmhAkLYWJtP6UG8liN72kkULLV+K+jIFOQ7XP3ABJAX3DKKtLj4JgGkopPWyS7hcHx5q3KflaATMxOEHxAELJbi50Pe2wsNGOvxGRrcevQzzwVZu1PGibN22nb7dafPFmDd2R3Jy9tBQ4TFWiqv9HwOCQ+jAgQOaOhq82TJE1pNXIdZ6piRfP/89MSlRe/CszmPu0XYRUzmuvtlhHnE1EGtNEWKk4o1cFovC74r5/qtL+t7U5Lxs88eb5al3ALvEseLtdyh9/gJ1kc6wMxs6OBpFq8p8IKLfXyVvB88Z3NxYWe9dEJtcMU2tl2lTJlPlypX0WVqcicMPiMNsx11PmNyOHWPdI4VlUzthKSUFnlwXLkiXSRXCpLFnb6OVVabQKy70XQl6Pd0FOektp5y58YA+TApBVpBa99yjTUe4Oo83x82bH1GX1dqL/hzmEZize5Ll3ly2nDIWXjOPrFK5MiVPueqOROr4S2iHONCJgMNI2SYwIpydNpNK3VnSEi7zKKz9a22pnfjzVL4TawIZYpo1v6ROndqE72V4I126BRieMdQVEx1J99WrZ1mtebMrlNBBM49MkM/E4ePEgekdTPPoxWoEIY+b9bHAODJ0hDyswh0/76TXR4WpNCLufnhn6ZvLKFOYTEpxtdBtvqa8nluX16EP9dMayEdPLUOYGuMFZSX4QmD7jsaNgVMnTVRGB1ZlkIdpKkxXSXFE1PK4L4d2iAO77rH7XoqrKb6Zs2bTB8KySgoWif91110yaTvUe4G2XdiNAt56KPjt+HFtlkF/KmcjMujpfaghrTc/R1ovTBw+ThzmBV5X7pTjE8cbLIRCggeKPR3N9G1Gi/8sPqGKRUm9OFpI0+tgRNO5a3eD7fjQkGBq2qSJXs0QN89je/vQGyq3SBw+fIQCBww0HHHVQ10jPvg0SXw0R4q7H7zC51KTp6XKYk4fVqXkoxF3icNqLt7Z91EwYu0set/S1Bvre1jf8EZudOIwT+PhXpMSxeZVB+a1OD5+wkTDHheMTDBCsRImDh8mDqsHDBYnmOqxEuzKxvBWDv+hs1CYlModt/oy0AUB6GX+vDkuXYR/sHIlzUybrYphsRlmq44EFiDBIUPVYWe9IKXkZWSpmD7K1E0fYZSBaTgrHOSpzDvMn2j+OAUPNJp/Sl19aLbG8vRbH/o6C2rcXeIweyt29XExsxGG3ATnDU5ox2vXrvOmCqdl4YLGyiDFaSHdQfOIzNWoHuSKNTr9pskRw4Zq5rq6alWUicOHiQOLu1jklYLpFkdu0aGj/54G0q68aGJxXE8y+O4wvj/sTGC1AUKT0qxpExoy+JprE5kvQ7MZbl489LJuR6H5GjEawqjIkVit97g7KjL7wrpLuC2ZMmmCo1O5lQ8bff20jFuFPFB6pHEjS7NXD6rSirhDHGhvWEvSv+CwyxnfSLES82gDOp06dqA2rf9npe4zeVgTNGLkfFRv/uYMOnR4V5j3bkmA/J04/gYAAP//aJT8RwAADWZJREFU7Z0HeBZFHsb/KN2TejQFpaNYAO/0BEQO1LMrvQQRaQFSiCC9pREQNIQiPfReBLvecyICKidW9ECwQILSkSJFAYWbd3123F3y5duwX5B8+/6fB3dmdnay85vyTtvPfMePHj4vYWqdunSTn376SeeuaZN/Smx0lPZbHefOnZOIjp3k9OnTOvjhhx6Ubl06a7/T8WTnrnL8+HEdPPbZUVKjenXtdzrOnz8vLdu0E1xNGz50iNxWr67ptV13ff+9xPV5xhbWIaK9tGrR3BYWSg/erXW7CPntt990slNfmCTly5fTfqcjMTlFPt+8WQff+Y87ZGD/ftqfnWP23Hny6muv6yi33HKzJMWP0P6LcXzx5f8kPjHpYh7N0TMR7dpK61Ytc/RMdpFff+NNSZ89R0dZvXK5dpsOZ97y5csnSxcvlIIFCphRbNdVL70sCxYusoVNGp8mFSteawsLJ8/X33wjAwcP1VkqUqSILF4wT/udDtR1tOVTp07pWzHRveSeJk203+lISB4pmzd/YQRXKF9eprww0RklrP35wlk4WrRua+ukIQIQg6wMnRc6Mas9OypFatWsYQ2yufs8018yMjN1WPzwoVK3Th3tdzoOHjwokb2ibcErly2RK6+80hZmegYNGSbbv/7a9BrXCWmpcl2lSrawUHq2bN0qw0Yk6CQrVawoE8eP036nY9v27TJ46HAdjLzMTp8hxa6+Wodl55g0eYq8s/ZdHaVJ48bSO9bOSN906XB2ri4fy3G0P0M4nPW0dKlSkj5jWpbvfvrMGemkOkTrYCh//vyyYuniLOOHS6BzMPLoIw9Ll6c6BczeosVLZOWq1fq+GyGgcITpjOPEyZPSsVNnXRngSFQj2VvViNZpBw4clJ7RMTaRQQeITh2GBrh///4LOuzUtPHy3vsf6OQ6PdlRmj32qPY7HRiVY3RuWnaNeNGSpbLyxVVmVONqjf/j4cOC0WapkiVtcbx6ZqTPkjff+rdO5jHV6DoHaHRnzp6VyJ5RcuzYMR1/8MABcsftf9f+YI5Rz46Rjz7+REd7pk+c3NWwofZfjGPPnr0S19c+U7uYdII9E6tGpXc3ahQsmuv7bmYczvLBDBczXadh5jhg0BD59rvvbLeqV6smz40ZbYRl7tol11xzjRRQYhJOFhUbJ3v37tVZGpmUKDfVvlH7rY4fftgtvfv01W2/gJq5Yfbw19KlrdEucFM4wlQ4Dh46ZHRq1hLPavp56uefJTbuaTl8+Ig1qrHkhAaJBth/4GDZsXOnrFqxzBbnq23bZciwP0bbdW69RRJG/OG3RVaeDzZulOdS03SwVQh0oHKsW79Bxk+cJEWLFrVNn6tUrizjnh8ryFtsXB8ppUabUyZN0I9CmFatfkm+27FTypUtK13VDCtQg9EPORw9oqIFQmpacmK83HzTTabXdh02Il62bP1Kh7Vp3Urat22j/W4cnbtFytGjR42oEMJlSxaFXUfmhgPiuBEO1AvUD9MCCUfahImyfsN7Urx4cZuwt2jeTDp2iDDEGqL90IMPSPeuXczk8vwVg5m27TvofKBOYQB4xRVX6DDTgbbfQw18MMg0bWRSgmoztU1vwCuFI0yFAx0+lqqsVqfOrZIwfJgOOnL0mBqVDZJDh35UnXBJm3iYnWBSyij57LPPJdDegnUfJdha6s6MDOnbb4D++3CkPjdGqlaposM2/vdDJS6/Lw316hEpU6ZN1/fQyDGjievbT3755RcZNTJJbqhVy7j/s/J3UHs0yLdpaDSDBvRTM4DbzaBsr0gj4oknbXEWqbXhomqN2Gr4G5OnTpM176zVwS3VvssTav8lJ4aGi3c2LVAnaN4P96sb4Vi6fIUsU/9MwwgZZWTOGlA2s+bMNUQIA497mzaRVyx7SBjYnFWdK0QD9XX61Mnyl6uuMpPL81e0n7HPp+p8FCtWTObNTtd+03FS7WdgH2T37t1GENrK0MGD5G+31TOjZHulcISpcKDUn+ra3TbaQuWIaN9OdbY15ZNPPzM2ZbExhg6rcuXr5T9vr9GV5bZ69YyN72++/VZq33ijpCQn6ntWx5Jly2X5ipU6aNbM6QGXj87++qsxGrJ27mi0PSK7qc3oc7Jm7Vr5Um3s/t7h9zc29tFBm1auXDljdI416z5xsbZlEmenYz4TbI/CjIfrpo8+ltFjxlqD5MXlS22jtcNHjsiI+ETZvWePEQ/vive//777bM+58ThnYJHdusqDD9zv5tGwjOMsQzeb4wCBmSgGNvv27VMi8ZoxYyxcuLBMGJeqRGSOUa4mMAw0sC+FpdhJau+qQoUK5q2wuL4wZaptQFOmTBmZocTRal9t2yZJI0cZgy+EFypUSDDTwDKeW6NwhLFwvL3mHWNknF1lqFWzpiEKk6dMk7Xr1l0QtVrVqjJmdErADWznXkp2G/BI3LkZ7PyD6IiHDRmkTlrVM/YasKbtNOw5YO/BauvVsgSWJ5yG9LAZio4imGV1igsd+b/uu1d2qfXwjz/5VDCi+1UJIAyiNHhg/4vufKzLLmi8i+bPdfWewfKRV++7EQ7kDQcscNAikGGmgUMUWKc3Z8zWuKgLKclJ2R78sMbPS+7V6hTZfMcpsrjYGGNguGXLVqMOW08ANqh/p0RH9bpgVh0szxSOMBYOFP68BQvlpZdfuaAeYH/hkYcfMtZ7sf6JTW5sdlut8d2NjOO7wTpdayVCo10wd7ZtlG5NEzMcHBW17g2Y9zGzQSUvW7aMEbT/wAHpGRVj3jY61Z6R3eXee5rqMNOBtd2o6FjBprnTcFyzUMGCzuAs/dionpGebizfZRlBBUJMWzR/XBrUrx8oStBwLFPhxI8pQn6fbQCYW+FAGWPJ03rUHM9jkIC60aXzU1JYCTHMeQoL9TM5IV6qVq1i3A/H/2AFYLVq81jOzcrQnnEEHsvROZllWNOytnk3p7Csz4aDO6yP45oFhL2MDRs2yL79+6W4WvO8/vrrpG7durpxmfFwLBQdJ+7f1aCB67PumHV0i+ypjz26OaaJ0y4YvZ9RJ7aw1ADRyOpbiR07dsqHmzZJiZIlpKF6p2DHXCFIJ9X7YFSF01FYsliycL6ZRddXMMvMzJCMjExjM760Gr1ihlFTHU8GQ6+WmjZBifX7RjIlSpSQOeoIr9/NrXCAE5Y7sbS4VR2fzq/2OWpUrya11aaus37g+6RP1R7ddrU8VUkd427YoL5vZnV71dJdpjoun5G5S06cOCHo4MHghhtqBfzuxW0dpHCE+YzDbUXwGm/zF19KQlKykQxmM/PmzMrx9NfrO1ifN5fEgp30sj5zqdw4Bvq02uCHYZSMtfZrrw3fD9Lccs2JcLhNk/FyhwCFg8IRspo1c9ZseePNt4z07m50l9rA7h2ytHOSEGYdOCoLw5l0jLQuJ4vp/bTeXAcjsKK5X6oiqz+fAIWDwhGyWojlg14xvY2PBZFoZHd1Suj+S3tKCF9NJ41MMX4ypEWzx6XjE3+caQ9ZRj0k9Py4NHn/g41GCq1atpAO6pQb7XcCnHHknZpA4aBwhLS2YtN3uPrJDnwwCMOpI7ffUXh9EetGKI7H9uzR3WuSIX3eOiML9pV9SP9wHkmMwpFHCkq9JoWDwpErtRU/VoeOAJbVF+u58Uenz0yXd9etN5bIcvKzH7nxLtY0MRPDR404DIA9jRh1/BE/OEmzE6Bw2Hlczj4KB4Uj1+onPnAbN36isWyU2z9OmGuZCEHCc+cvkJdfedU4Zowvly+3PZcQZDEkSVA4QoLxkiRC4aBw5GpFw08avK42zPF7QBht+9GwbPfhpo+kXZvWvmXgptytwoFvDcwf2XTzLONcWgJW4cBxevyGnJ/MF99x+KlAmde8SwAfh+L3wmAQjiLqGxza5UkAv5iN3/yCFVQf1wb6/6Fcnm/v/a0oHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBCgc3hkyBRIgARLwFQEKh6+Km5klARIgAe8EKBzeGTIFEiABEvAVAQqHr4qbmSUBEiAB7wQoHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBCgc3hkyBRIgARLwFQEKh6+Km5klARIgAe8EKBzeGTIFEiABEvAVAQqHr4qbmSUBEiAB7wQoHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBCgc3hkyBRIgARLwFQEKh6+Km5klARIgAe8EKBzeGTIFEiABEvAVAQqHr4qbmSUBEiAB7wQoHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBCgc3hkyBRIgARLwFQEKh6+Km5klARIgAe8EKBzeGTIFEiABEvAVAQqHr4qbmSUBEiAB7wQoHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBCgc3hkyBRIgARLwFQEKh6+Km5klARIgAe8EKBzeGTIFEiABEvAVAQqHr4qbmSUBEiAB7wQoHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBCgc3hkyBRIgARLwFQEKh6+Km5klARIgAe8EKBzeGTIFEiABEvAVAQqHr4qbmSUBEiAB7wQoHN4ZMgUSIAES8BUBCoevipuZJQESIAHvBP4PkQkVkiOs+AQAAAAASUVORK5CYII=" alt="Distanzmethode" /></p>'

        elif distanceMethod == 'maximum':
            finalDescription += '<p>Ermittle die größere der beiden Zahlen -> max( x , y )</p>'

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
    if str(diagramHelpBoolean) == "true":
        finalDescription += "<br><p>Vorschau des Streudiagramms:</p><br>"

        #add base64 img
        print_diagram(data)
        with open("streudiagramm.png", "rb") as image_file:
            encoded_string = str(base64.b64encode(image_file.read()))

        finalDescription += f'<br><img src="data:image/png;base64, {encoded_string[2:-1]}" alt="Streudiagramm" /><br><br>'

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

def generate_matrix_headers(numClusters, pointsPerCluster, iterationNumber):

    length = int(numClusters) * int(pointsPerCluster)
    matrixHeaders = list(string.ascii_uppercase)

    return matrixHeaders[0:(length - int(iterationNumber))]

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
    #data = np.array([[2, 3],[5, 2],[5, 3],[1, 4],[4, 5]])
        

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
            jsonDict["DigraphIterationHeader{}".format(iteration)] = generate_matrix_headers(numClusters, pointsPerCluster, iteration)
            
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

            #matrix headers
            jsonDict["DigraphIterationHeader{}".format(iteration)] = generate_matrix_headers(numClusters, pointsPerCluster, iteration)
            
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