# -*- coding: utf-8 -*-
"""
Created On : Sat Nov 20 22:10:42 2021
Last Modified : Thur Nov 25 2021
Course : MSBD5002 
Assignment : Assignment 04 


"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import random

def points_within_eps(mainpoint, full_list_points, epsilon):
    """ Return the list of points that are within the epsilon range 
        Distance determined using Euclidean Distance Formula""" 
    points_neighbourhood = []
    for point in full_list_points:
        distance = math.sqrt(math.pow((mainpoint[0]-point[0]), 2) +
                    math.pow((mainpoint[1]-point[1]), 2))
        if distance <= epsilon:
            points_neighbourhood.append(point)
    return points_neighbourhood 


def plot_cluster(cluster_data_dict_input, epsilon_input, minpoint_input, remaining_points_input):
    """ Function to Plot the Clusters for every Parameter"""
    colors_list = ['b','g','r','c','y','m']
    ### Plots each Clusters in Unique Colors
    for cluster_num in range(0, len(cluster_data_dict_input)):
        cluster_data_list = cluster_data_dict[cluster_num+1]
        datapoints_y = [ x[1] for x in cluster_data_list]
        datapoints_x = [ x[0] for x in cluster_data_list]
        plt.plot(datapoints_x, datapoints_y, '.',
                 color = colors_list[cluster_num])
        plt.title("Parameter Combo (Epsilon {} & Min Point {})".format(epsilon_input,minpoint_input))
    ### Plot the Outliers (the points that are not part of a Cluster)
    data_r_y =  [ x[1] for x in remaining_points_input]
    data_r_x =  [ x[0] for x in remaining_points_input]
    plt.plot(data_r_x, data_r_y, 'o',
             color = 'k')
    plt.show()


### Data Processing
# Extract the dataset from txt file
dataset_df = pd.read_csv("DBSCAN_Points.txt" , sep="\n", header=None)
dataset_list = dataset_df[0].tolist()
dataset_str_list = [ x.split(" ") for x in dataset_list]
dataset_float_list = []
# Convert the string data into float data
for coordinate in dataset_str_list:
    dataset_float_list.append([float(coordinate[0]), float(coordinate[1])])

# Remove duplicate points
dataset_list = []
for coordinate in dataset_float_list:
    if coordinate not in dataset_list:
        dataset_list.append(coordinate)


#### Start the DBSCAN 
epsilon_list = [3,2.5,2,2 ]
minpoints_list = [5,20,20,15]

# Variables below is to record the results of each Parameter combination and to print the results at the end
final_results_number_cluster = []
final_results_number_outliers = []
final_results_eps_val = []
final_results_minpoints_val = []

### DBSCAN Algorithm for every Parameter Combination
for index in range(0, len(epsilon_list)):
    eps_val = epsilon_list[index] # Current Epsilon Value
    minpoints_val = minpoints_list[index] # Current MinPoints Value
    cluster_data_dict = {} # Store the Coordinates for each Cluster that was found, into a dictionary
    cluster_number = 0 # Set the current cluster number to 0
    
    # This variable is meant to be modifiable for each iteration
    # After every group of Points (Coordinates) is found as part of a Cluster
    # The Points (Coordinates) will be removed from the "points_list" variable
    # The remaining Points (Coordinates) will be the Outlier for the current Parameter Combination
    points_list = dataset_list.copy()

    
    # The "number_previous_cluster" variable is to keep track of the number of clusters from the previous iteration
    # This is meant to be used in a comparison to break the While Loop
    # The moment there is no change in the number of clusters found for an iteration 
    # E.g. number_current_cluster == number_previous_cluster 
    # The While Loop will end
    number_previous_cluster = 0 
    cluster_flag = True # Set to True until all the possible Clusters are found 
    while cluster_flag:
        random.seed(1234) ## < === Uncomment to not fix the random seed
        # random.seed(4321) 
        # random.seed(100) 
        ### Select a random point from points unconsidered so far 
        # - "points_list" variable is modified everytime a Cluster is found
        random_start_point = random.choice(points_list) 

        ### This is the First neighbouring points to kickstart the cascading collection of neighbouring points
        points_in_neighbourhood = points_within_eps(random_start_point, dataset_list, eps_val) 

        # This variable is meant to stop the While Loop the moment there are no new neighbouring points to be found
        # - the While Loop to be checked by this variable is the "While cluster_flag=True" (Outer Loop)
        length_previous_cluster = 0 
        
        ### If number of neighbouring points for the random starting point from "random_start_point" exceeds the minimum points value
        # - Start looking for points that are density-reachable
        if len(points_in_neighbourhood) >= minpoints_val:
            cluster_number += 1 
            print(""" {} Cluster was found """.format(cluster_number))
            
            
            ########################################
            ### The Inner While Loop is to find all the Density-Reachable Points
            # - Based on the initial set of points found from "points_in_neighbourhood" variable
            # - the Inner While Loop will end after there are no more Density-Reachable Points
            current_neighbourhood_points = points_in_neighbourhood.copy() # make a copy of the original variable
            cluster_points_list = [] # Collects all the possible points that are part of this Cluster  (density-reachable)
            density_reachable_flag = True
            while density_reachable_flag:
                ### Add the neighbouring points into the cluster_points_list if it is not included already
                # - At the end of the While Loop, this variable will output all of the points that is part of this Cluster
                for point in current_neighbourhood_points:
                    if point not in cluster_points_list:
                        cluster_points_list.append(point)
                
                ### This section is to check if the cluster_points_list is being updated at each loop
                # - If there are new neighbouring points discovered, the length of the cluster_points_list will increase at each loop
                # - If there are no more new neighbouring points, the Inner While Loop is ended
                length_current_cluster = len(cluster_points_list)
                if length_current_cluster == length_previous_cluster:
                    # if the cluster_points_list stops being updated
                    # end the while loop, because it is most likely all the possible neighbouring points has been exhausted
                    density_reachable_flag = False
                else:
                    # otherwise, proceed
                    length_previous_cluster = length_current_cluster        
                
                ### Find new neighbouring points with the current list of neighbouring points that are density-reachable
                newpoints_collected = []
                for inner_start_point in current_neighbourhood_points:
                    new_points_in_neighbourhood = points_within_eps(mainpoint = inner_start_point, 
                                                                      full_list_points = dataset_list, 
                                                                      epsilon = eps_val)
                    if len(new_points_in_neighbourhood) >= minpoints_val:
                        # append only if the number of points in the neighbourhood exceed the minimum point value
                        newpoints_collected += new_points_in_neighbourhood
                    else:
                        pass

                ### remove duplicate points from the list of new neighbouring points ("newpoints_collected")
                sorted_newpoints_collected = []
                for i in newpoints_collected:
                    if i not in sorted_newpoints_collected:
                        sorted_newpoints_collected.append(i)

                ### Make the new neighbouring points as part of the current neighbourhood points to be added into "cluster_points_list" variable
                # - All density-reachable points found are added to be part of this cluster
                current_neighbourhood_points = sorted_newpoints_collected
            ########################################
            
            
            ### After the end of the Inner While Loop (Density-Reachable Points)
            # - All the points that were found are part of a Cluster
            # - Store the list of points of the Current Cluster into the Cluster Data Dictionary
            cluster_data_dict[cluster_number] = cluster_points_list


        ### This section is to check if new clusters was found and updated to the cluster_data_dict variable
        # - If no new clusters are found, the While Loop is ended
        # - Otherwise the While Loop continues until no new clusters can be found
        number_current_cluster = len(cluster_data_dict)
        if number_current_cluster == number_previous_cluster:
            # end the while loop, because it is most likely all the possible neighbouring points has been exhausted
            cluster_flag = False
        else:
            # otherwise, proceed
            number_previous_cluster = number_current_cluster   
            ### Remove points already in a Cluster
            # - points are removed from "points_list" variable
            # - remaining points are either used to find the next cluster or considered an outlier point
            intermediate_cluster_points_list = cluster_points_list
            for points_check in dataset_list:
                if points_check in intermediate_cluster_points_list:
                    points_list.remove(points_check)

    

    ### This Section is to plot the Clusters and Outliers at the current Parameter Combination
    remaining_points = points_list.copy()
    plot_cluster(cluster_data_dict, eps_val, minpoints_val,remaining_points)
    
    ### This Section is to store the Number of Clusters and Outliers information at the current Parameter Combination
    number_of_clusters = len(cluster_data_dict)
    number_of_outliers = len(remaining_points)
    # The information are stored in the following variables to be printed as a DataFrame at the end of the Parameter Iteration
    final_results_number_cluster.append(number_of_clusters)
    final_results_number_outliers.append(number_of_outliers)
    final_results_eps_val.append(eps_val)
    final_results_minpoints_val.append(minpoints_val)


#### Print a Summary of the Final Results 
print("""
      Summary of Results from the DBSCAN 
      """)
final_results_data = {"Epsilon":final_results_eps_val, 
                      "MinPoints":final_results_minpoints_val,
                      "No. Cluster":final_results_number_cluster,
                      "No. Outliers":final_results_number_outliers}
final_results_df = pd.DataFrame(final_results_data)
final_results_df.set_index(['Epsilon'], inplace = True)
print(final_results_df)



    