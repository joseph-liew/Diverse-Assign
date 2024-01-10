import sys
import os
import pandas as pd
import numpy as np
from math import log
from random import shuffle 
from collections import deque 
import time

'''
###############################################
HELPER FUNCTIONS
###############################################
'''
def csvCheck(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == ".csv"

def calculateDiversity(dataframe, subset):
    
    # initialise group_unique_count to store the unique counts of items in each column
    group_unique_count = {}
    
    row_total_count = len(dataframe)
    column_total_count = len(dataframe.columns)
    subset_unique_value_count = subset.nunique()
    total_count_N = row_total_count
    shannon_weiner_index = 0
    
    for column in range(column_total_count):
        unique_count_n = subset_unique_value_count.iloc[column]
        column_name = dataframe.columns[column]
        group_unique_count[column_name] = unique_count_n
        
    for column in range(column_total_count):
        column_name = dataframe.columns[column]
        n = group_unique_count[column_name]
        
        p_i = n / total_count_N
        shannon_weiner_index += (p_i * log(p_i))
        shannon_weiner_index = -(shannon_weiner_index)
    return shannon_weiner_index

def assigner(num_groups, num_rows, data):
    
    # Initialise the initial assignment participants distributed evenly among groups
    assignment = np.tile(np.arange(1, num_groups + 1), num_rows // num_groups + 1)[:num_rows] 
    data['assigned_group'] = assignment
    
    # Initialise variable to store total diversity 
    diversity_sum = 0
    
    # Initialise dict to store diversity for each group
    dict_diversity_store = {}
    
    for i in range(1, num_groups + 1):
        subset = data.loc[data['assigned_group'] == i]
        dict_diversity_store[i] = calculateDiversity(data, subset)
    
    for value in dict_diversity_store.values():
        diversity_sum += value
    
    initial_diversity = diversity_sum
    current_diversity = initial_diversity
    
   
    # Initialise buffer dictionary to temporarily store previous diversity of the 2 groups. (Before the 2 groups had a row swapped)
    dict_buffer_diversity_store = {}
    
    # Initialise tracking buffer to check whether a progress milestone has reached.
    buffer_progress = 0
    
    # Define the initial temperature and cooling rate for simulated annealing
    temperature = 1.0
    cooling_rate = 0.96
    
    # while temperature > 0.8:
    while temperature > 0.01:
        # Generate a random sequence of indices to pop.
        
        indices_lst = [i for i in range(num_rows)]
        shuffle(indices_lst)
        indices_lst = deque(indices_lst)
        
        # if there are odd number of rows, ignore the last row since there is no row to swap with.
        if (num_rows % 2) > 0:
            num_rows_even_capped = num_rows - 1
        else:
            num_rows_even_capped = num_rows
        
        # Iniialise a tracker. Used in 'for' loop in data.iterrows(). 
        # If index has already been swapped, this variable is used to identify the index to skip.
        previous_index = []
        
        # Group assignment, using iterrows() for iteration. Algorithm: simulated annealing
        for index, i in data.iterrows():
                       
            # If the index has already swapped, skipped swapping
            if index in previous_index: 
                continue
            
            # cap the swaps to the last even index
            elif index == num_rows_even_capped:
                break
            
            elif len(indices_lst) == 0:
                break
            
            assign_i = data.at[index, 'assigned_group']
            pointer = indices_lst[0]
            assign_j = data.at[pointer, 'assigned_group']
            
            # Compute optimisation: prevent row swapping within the same group or self-swapping
            if indices_lst[0] == index or assign_i == assign_j:
                continue
            else:    
                buffer = assign_i                     
                indices_lst.popleft()
            
                new_diversity = current_diversity - dict_diversity_store[assign_i] - dict_diversity_store[assign_j]
                
                # swap their assignments
                data.at[index, 'assigned_group'] = assign_j
                data.at[pointer, 'assigned_group'] = buffer
                
                subset_i = data.loc[data['assigned_group'] == assign_i]
                subset_j = data.loc[data['assigned_group'] == assign_j]
                
                # temporarily store current diversity values for selected two groups
                dict_buffer_diversity_store[assign_i] = dict_diversity_store[assign_i]
                dict_buffer_diversity_store[assign_j] = dict_diversity_store[assign_j]
                
                # Calculate the change in diversity
                dict_diversity_store[assign_i] = calculateDiversity(data, subset_i)
                dict_diversity_store[assign_j] = calculateDiversity(data, subset_j)
                
                new_diversity = new_diversity + dict_diversity_store[assign_i] + dict_diversity_store[assign_j]
                 
                delta_diversity = new_diversity - current_diversity
                             
                # Accept the new assignment based if there is increased diversity. 
                # There is a proability to reject this swap and make a new swap instead
                if delta_diversity > 0 or np.random.rand() < np.exp(delta_diversity / temperature):
                    current_diversity = new_diversity
                    previous_index.append(index)
                    
                else:
                    # revert the swap
                    data.at[pointer, 'assigned_group'] = data.at[index, 'assigned_group']
                    data.at[index, 'assigned_group'] = buffer
                    dict_diversity_store[assign_i] = dict_buffer_diversity_store[assign_i]
                    dict_diversity_store[assign_j] = dict_buffer_diversity_store[assign_j]
                    indices_lst.append(pointer)
                
                    # re-shuffle the indices to swap with
                    shuffle(indices_lst)
    
    
        temperature *= cooling_rate
        progress = (1 - temperature) * 100
        stepped_progress = (progress // 1) % 10
        
        if buffer_progress != round(progress) and stepped_progress  == 0:
            print(f"Progress on current solution {progress: .0f}%")
        
        buffer_progress = round(progress)
         
    return data, initial_diversity, current_diversity

# Stopwatch program. Used in estimating compute time. Credit: Mostly AI-generated
class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def elapsed_time(self):
        estimator_modifier = 1.1
        elapsed_seconds = int(self.end_time - self.start_time) * estimator_modifier
        
        return elapsed_seconds
'''
###############################################
DRIVER CODE
###############################################
'''

# Set working folder
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    base_path = sys._MEIPASS
else:
    # Running normally as a Python script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.getcwd()

# Welcome screen
print()
print("*** Diverse-Assign v.0.2.2a ***")
print()
print(" --- Need help? \n --- Do you need a sample file to demo? \n --- You can refer to the README file for more info.")
print()
print("Hi there! Please put your CSV file of the participant profiles")
print("into the same folder as this programme.")
print()      
print("When ready, please input the file name below. \n --- File name must end with \'.csv\' \n --- No space allowed in the file name. No space allowed in the file name. \n --- File name e.g.: \'sample_class_group.csv\'")

# Load data 
while True:  
    try:
        input_filename = input("\n **Input file name here (e.g. my_participants.csv)**: ")
        
        if csvCheck(input_filename):
            data = pd.read_csv(input_filename)
        else:    
            raise ValueError() 
        
    except Exception or OSError as e:
        print()
        print("\n Wrong input or file does not exist in this folder. Please re-try.")
        continue
    
    break

# Define the number of groups
print()
print("Please input the number of groups you want to split your class into.")
print(" --- The programme will evenly distribute the participants into groups. \n --- Participant will be distributed to make every group possible.")
while True:
    print()  
    try:
        num_groups = input("**Input the number of groups (numerical digit e.g. 12)**: ")
        num_groups = int(num_groups)
        num_rows = len(data)
        print()
        print(f"... there are {num_rows} of participants in your class.")
        
        if num_groups < 1:
            raise ValueError("\n Wrong input. Number has to be an integer greater than 0. Please re-try.")
        
        elif num_groups >= num_rows:
            raise ValueError("\n Wrong input. The number of groups must be smaller than the number of participants. Please re-try.")
            
    except Exception as e:
        print("\n Wrong input. Number has to be an integer greater than 0. Please re-try.")
        continue

    break

# Define the number instances or solutions to generate
print()
print("Please input the number of solutions you want to generate.")
print(" --- The programme will automatically pick solution with the highest score.")
print(" --- Caution: Greater number of solutions will increase calculation time.")
while True:
    print()  
    try:
        instance_count = input("**Input the number of solutions you want (numerical digit e.g. 10)**: ")
        instance_count = int(instance_count)
        
        if num_groups < 1:
            raise ValueError("\n Wrong input. Number has to be an integer greater than 0. Please re-try.")
            
    except Exception as e:
        print("\n Wrong input. Number has to be an integer greater than 0. Please re-try.")
        continue

    break

print()
print("The programme is assigning the groups now.")

best_solution = None
initial_diversity = None
best_diversity = None
picked_solution = 0
minutes_esitmate = None
seconds_esitmate = None

# Assign groups over indicated number of instances.
# Then, pick the solution with greatest diversity
stopwatch = Stopwatch()
for i in range(instance_count):
    solution_number = i + 1
    print()
    print(f"Working on Solution Number {solution_number} now...")
    stopwatch.start()
    if best_solution is None:
        output = assigner(num_groups, num_rows, data)
        best_solution = output[0]
        initial_diversity = output[1]
        diversity = output[2]
        best_diversity = diversity 
    else:
        output = assigner(num_groups, num_rows, data)
        initial_diversity = output[1]
        diversity = output[2]
    
    print("Progress on current solution  100%")
    print()
    print(f"Solution Number {solution_number}'s initial diversity score was {initial_diversity}")
    print(f"Solution Number {solution_number}'s final diversity score was {best_diversity}")
    stopwatch.stop()
    
    if i == 0:
        stopwatch.stop()
    if instance_count > 1:
        elapsed_clock = stopwatch.elapsed_time()
        solutions_left = instance_count - solution_number
        elapsed_clock = solutions_left * elapsed_clock
        minutes_estimate = elapsed_clock // 60
        seconds_estimate = elapsed_clock % 60

        print()
        print(f"Estimated time left to complete: {minutes_estimate:.0f} minutes {seconds_estimate:.0f} seconds")
    
    if instance_count == 1:
        picked_solution = 1
    
    elif diversity > best_diversity:
        best_diversity = diversity
        best_solution = output[0]
        picked_solution = i + 1

data = best_solution

# Solution found screen
print()
print(f"{instance_count} number of solutions completed. The best solution picked is Solution Number {picked_solution}. The best diversity score acheived was {best_diversity}")

print()
print("Group assignment is completed.")
    
# Save output to working folder
while True:
    print()
    print("Saving output... what is the file name to save to?")
    try: 
        output_filename = input("\n **Input the output save name here (e.g. done.csv)**: ")
        if csvCheck(output_filename):
            data.to_csv(f"{output_filename}")
        else:    
            raise ValueError() 
            
    except Exception as e:
        print("\n Wrong input. File name must be valid and end with \'.csv\' (e.g. done.csv)")
        print("Please re-try.")
        continue
    
    break

print()
print("The group assignment is stored into the current folder.") 
print(f"Output saved as: \n \'{output_filename}\'")
print("\n You can close this programme now. \n Goodbye!")

