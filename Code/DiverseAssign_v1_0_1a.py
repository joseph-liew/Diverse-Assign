#%% Reference package versions used in compiled app

"""
Reference package versions: 

pyinstaller 6.3.0
python 3.11.7    
numpy 1.26.3 
pandas 2.2.0 (pandas 2.03 for Win x86)
openblas 0.3.23
"""

#%% Packages

import sys
import os
from pandas import read_csv, DataFrame
from numpy import tile, arange, exp
from math import log, ceil, comb
from random import shuffle, uniform
from collections import deque 
from time import perf_counter, sleep

#%% Code version

'''
###############################################
DiverseAssign v.1.0.1a

A VERSION. THIS IS THE PRODUCTION VERSION FOR: 
    - USE AS PYTHON SCRIPT
    - SOURCE CODE FOR EXECUTABLE

###############################################
'''

#%% Helper functions

'''
###############################################
HELPER FUNCTIONS
###############################################
'''

#%% csvCheck() function. Check whether file is CSV

def csvCheck(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == ".csv"

#%% weightModfier() function. 
# Goal: generates weights to balance the influence of each column on the 
# grand sum diversity.
#
# Weights will scale the column Shannon-Weiner Index in proportion of the 
# Aggregate Diversity Score (ADS).
#
# Weights will scale to the max proportion.
#
# However, it is unclear if this is the actual effect. Needs further study.
#
# This is because the sum of the Shannon-Weiner Index 
# is not the same as that of the whole population.
#
# Maximising the Shannon-Weiner Index in a group means 
# minimising the dominance of any category within a feature in that group.
# It is a small sample size, sensitive to dominance.
# In contrast, the population is a larger than a sample. 
# It is much less sensitive to dominance.

### FOR FUTURE USE. NOT USED IN DIVERSEASSIGN.v.1.0.1

def weightModfier(data):
    # Obtain Shannon-Weiner Index for each column.
    obtain = calculateDiversity(data, return_shannon_weiner_index = True)
    ads, swi_dict = obtain[0], obtain[1]
        
    # largest proportion of swi in each column of the dataset ADS
    max_proportion = max(swi_dict.values()) / ads
  
    # Initialise dict to calculate and store weight for each column
    weight_column_dict = {}
    for column, swi in swi_dict.items():
        if swi == 0: 
            weight_column_dict[column] = 0
        else:
            weight = max_proportion / (swi_dict[column] / ads)
            weight_column_dict[column] = weight
            
    return weight_column_dict

#%% calculateDiversity() function. To calculate a diversity of a dataset.
# Weights balance the influence of all columns on the Aggregate Diversity Score (ADS)

def calculateDiversity(data, **kwargs):
    return_shannon_weiner_index = kwargs.get('return_shannon_weiner_index', False)
    weight_modifier_dict = kwargs.get('weight_modifier_dict', None)
    shannonEntropyFormula = lambda p_i: -p_i * log(p_i)
    # If return_shannon_weiner_index is True, 
    # store and return the Shannon Weiner Index of each column
    if return_shannon_weiner_index is True:
        return_swi_flag = True
        
        # Intialise dict to store Shannon Weiner Index of each column
        swi_dict = {}
        
    else:
        return_swi_flag = False
    
    # If weight modifiers are present, retrieve the dataset weights.
    if weight_modifier_dict is None:
        weight_modifier_dict = {}
    else:
        weight_modifier_dict = weight_modifier_dict
    
    column_lst = data.columns
    row_total_count = len(data)
    total_count_N = row_total_count

    # Calculate Aggregate Diversity Score (ads) of dataset.
    ads = 0
    
    for column in column_lst:
        column_attribute_count = data.groupby(column).size()
        column_attribute_len =  len(column_attribute_count)
        
        shannon_weiner_index = 0   
        # shorten Shannon-Weiner Index calculation for columns which have all unique rows
        if column_attribute_len == row_total_count:
            p_i = 1 / total_count_N
            h = shannonEntropyFormula(p_i)
            h = h  * row_total_count
            shannon_weiner_index += h
            
        elif column_attribute_len != row_total_count:
            # shorten Shannon-Weiner Index calculation for homogenous column 
            if column_attribute_len == 1:
                shannon_weiner_index = 0
            # calculate Shannon-Weiner Index for non-homogenous column 
            else:
                for attribute_row in range(column_attribute_len):
                    attribute_count_n = column_attribute_count.iloc[attribute_row]
                    p_i = attribute_count_n / total_count_N
                    h = shannonEntropyFormula(p_i)
                    shannon_weiner_index += h
                
        shannon_weiner_index = shannon_weiner_index * weight_modifier_dict.get(column, 1)
                
        if return_swi_flag is True:
            swi_dict[column] = shannon_weiner_index
        
        ads += shannon_weiner_index
    
    if return_swi_flag is True:
        return ads, swi_dict
        
    else:
        return ads
    
#%% Function determines number of instances to run.
# Heuristic used to determine number of instances 
# Heuristic is based on the simulated annealing cooling rate
# and a target annealing probability 
# based on a reasonable minimum delta diversity to be detected.

def heuristicEstimator(num_rows, num_groups, num_cols, **kwargs):
    cooling_schedule = kwargs.get('cooling_schedule', 0.95)
    exhaust_count = comb(num_rows, num_rows // num_groups)
    
    # Standard parameter obtained from experiments.
    # Standard parameter has 5 groups and 6 columns or features
    # Standard parameter is the scale of known sensitivity response to known ADS
    standard_ads_size = 5 * 6
    
    # Scale of data's ADS
    data_ads_size = num_groups * num_cols
    
    # Relative scale of data's ADS to defined paramater
    relative_ads_size = data_ads_size / standard_ads_size
    
    # Scaling delta diversity sensitivity to relative scale
    given_delta_diversity = -0.001 / (relative_ads_size)
    
    # Target annealing probability at the final simulated annealing iteration
    target_probability = 0.03 
    
    # Heuristic to determine number of instances
    power_value = log(target_probability)
    target_temperature = given_delta_diversity / power_value
    instance_count = log(target_temperature, cooling_schedule)
    instance_count = ceil(instance_count) # see below note
    ## The number of instances and target temperature will autoscale with: 
    ## - target probability
    ## - relative ADS scale
    ## - target delta diversity sensitivity
    ## The instances count refers to the number of iterations for simulated annealing 
    ## deteremined by the temperature which depends on the target annealing probability
    ## Standard parameter is the desired ratio of delta diversity to grand sum ADS
    ## Cooling schedule is fixed at 0.95
    ## Why scaling: grand sum ADS scales and delta diveristy scales with num_group and num_cols.
    ## Hence, scaling is required for constant sentivity performance. 
    
    # Exhaust_count: Number of assignment combinations if explored exhaustivel
    # Below is for rare situaitons when the exhaustive number is smaller than the simulated annealing
    # In this situation, heuristic will prefer using the exhaustive number of iterations.
    if instance_count > exhaust_count:
        instance_count = exhaust_count
    
    return exhaust_count, instance_count
    
#%% heuristicDominanceDetector() function is a heuristic to relax 
### the no-homogenous-feature-in-any-group constraint.
### Heuristic will enable relax if an element in the feature is too dominant
### hence impossible to split the groups without seeing a homogenous feature
### If too dominant, returns check_homogen_flag = FALSE

def heuristicDominanceDetector(data, num_groups):
    
    dominanceHeursitic = lambda row_total_count, attribute_count_n, num_groups: \
        ((row_total_count - attribute_count_n) // num_groups) <= 0
    
    data = data.copy(deep=True)
    column_lst = data.columns
    row_total_count = len(data)
    
    dominant_flag = False
    while dominant_flag == False:
        
        for column in column_lst:
            column_attribute_count = data.groupby(column).size()
            column_attribute_len = len(column_attribute_count)
    
            # Skips columns which have all unique rows
            if column_attribute_len != row_total_count:
            
                for attribute_row in range(column_attribute_len):   
                    attribute_count_n = column_attribute_count.iloc[attribute_row]
                    
                    # Dominance heuristic
                    if dominanceHeursitic(row_total_count, 
                                          attribute_count_n, 
                                          num_groups):
                        dominant_flag = True
                        break
                if dominant_flag == True:
                    break
            if dominant_flag == True:
                break           
        break
    
    if dominant_flag == True:
        check_homogen_flag = False
        return check_homogen_flag 
    else:
        check_homogen_flag = True
        return check_homogen_flag

#%% assigner() function to assign and swap groups

def assigner(num_groups, num_rows, data, shuffle_flag, **kwargs):
    weight_modifier_dict = kwargs.get('weight_modifier_dict', None)
    carried_over_homogen_result = kwargs.get('carried_over_homogen_result', None)
    algorithm = kwargs.get('algorithm', 'TwoHill')
    temperature = kwargs.get('temperature', 1.0)
    mode = kwargs.get('mode', None)
    
    #%% Algorithm settings
    algo_dict = {'TwoHill': (True, True, False),
                 'SimAnneal': (True, True, False),
                 'RandomRestart': (False, True, False)
                }

    simulated_annealing_flag = algo_dict[algorithm][0]
    homogen_flag = algo_dict[algorithm][1]
    randomise_flag = algo_dict[algorithm][2]
    
    # If weight modifiers are present, modify the weights of that feature.
    if weight_modifier_dict is None:
        None
    else:
        weight_modifier_dict
    
    #%% Load data
    
    data = data.copy(deep=True) 
    
    #%% Initialise variables and load them
    
    # Detect homogenity
    if homogen_flag == True:
        # Check whether there is a result loaded carried over from previous instance
        if carried_over_homogen_result is not None:
            check_homogen_flag = carried_over_homogen_result
            
        # Else no result from previous instance
        # Check whether to relax no-homogenous-columns in any group 
        # if no relax, check_homogen_flag = TRUE
        else:
            check_homogen_flag = heuristicDominanceDetector(data, num_groups)
        
            # If above TRUE, check whether there 
            # are no homogenous columns in the entire dataset
            if check_homogen_flag == False:
        
                if 1 in list(data.nunique()):
                    check_homogen_flag = False

                else:
                    check_homogen_flag = True
    
    # Instead, don't check
    elif homogen_flag == False:
        check_homogen_flag = False
        
    # Generate sequence of groups.
    # Used to tell programme which rows to swap groups to increase diversity
    # Each element in sequence represents a index in data.iterrows()
    grouping_lst = arange(1, num_groups + 1)
    
    # If shuffle_flag == TRUE: Initialise the initial assignment with sequential grouping
    if shuffle_flag == True:
        assignment = tile(grouping_lst, num_rows // num_groups + 1)[:num_rows] 
        data['assigned_group'] = assignment
    
    # Hidden Else: start off the initial assignment from the given assignment from previous solution
    
    # Initialise dict to store diversity for each group
    dict_diversity_store = {}
    for i in grouping_lst:
        subset = data.loc[data['assigned_group'] == i]
        dict_diversity_store[i] = calculateDiversity(subset, 
                                                     weight_modifier_dict = weight_modifier_dict)

    initial_diversity = 0
    for value in dict_diversity_store.values():
        initial_diversity += value
    
    
    # If shuffle_flag == TRUE: 
    # Shuffle the initial assignment to start exploring 
    # new local search space (or 'tree')
    if shuffle_flag == True:
        shuffled_grouping_lst = grouping_lst
        shuffle(shuffled_grouping_lst)
        assignment = tile(shuffled_grouping_lst, num_rows // num_groups + 1)[:num_rows] 
        data['assigned_group'] = assignment
        if randomise_flag == False and check_homogen_flag == True:
            # Identify homogenous features in groups before swap
            # If homogenous, reshuffle, to get a non-homogenous features in groups
            while True: 
                escape_flag = True
                for i in range(1, num_groups + 1):
                    subset = data.loc[data['assigned_group'] == i]
                    subset = subset.drop(columns='assigned_group')
                    if 1 in list(subset.nunique()):    
                        shuffle(assignment)
                        data['assigned_group'] = assignment
                        escape_flag = False
                        break
                if escape_flag == False:
                    continue
                else:
                    break
        
    #%% Unclosed AC3 algorithm: Initialise variables for this algorithm

    # Constraint for Unclosed AC3 algorithm: No homogenous column in entire dataset 
    # Detects whether data has a homogenous column
    # If there is a 
    ### For pseudo-random only algorithm, homogen_flag == False
    ### Assume there is a column homogenous throughout dataset
    ### Hence bypass the "no homogoenous column constraint" check
    ### Effectively turns off constraint propagation.
        
    # Initialise a set tracker, using set. Used in 'for' loop in data.iterrows(). 
    # If index has already been swapped, this variable is used to identify the index to skip.
    previous_index = set()
    
    # Initialise a dict: create hashmap to track visited neighbour solution 
    visited_nodes = {}
    
    # Initialise a dict: create hashmap to track whether a potential swap 
    # has looped back to having any column in either groups homogenous
    homogen_nodes = {}
    
    # Generate a random sequence of indices to pop. 
    target_lst = [i for i in range(num_rows)]
    shuffle(target_lst)
        
    # Use deque() for the sequence to pop.   
    target_lst = deque(target_lst)
 
    # Deque size
    target_lst_size = len(target_lst)   
    
    # Make a back-up of current data with its assignments
    backup_group_col = data['assigned_group'].copy(deep=True)
    
    #%% Unclosed AC3 algorithm
    ## Note: Regardless whether constraints are in place, this algorithm will
    ##       drive the swapping of group assignments
    
    while True:
        # Group assignment, using iterrows() for iteration. 
        # This 'for' loop drives the swaps. 
        # If check_homogen_flag == True, constraint is propagated
        
        # Initialise restart flag. Used with homogenous features detected in a group
        restart_flag = False
        
        for index, i in data.iterrows():
            
            # 'assign_i' is the index iterrows()
            assign_i = data.at[index, 'assigned_group']
            subset_i = data.loc[data['assigned_group'] == assign_i].copy(deep=True)
            
            # Create index iterrows() as key in visited_nodes hashmap
            # Tracks index target_lst visited by index iterrows()
            visited_nodes[index] = set()
            
            #%% Constraint propagation.
            
            # Create index iterrows() as key in homogen_nodes hashmap
            # Tracks index target_lst visited by index iterrows() that
            # resulted in homogenous rows
            homogen_nodes[index] = set()
                
            
            #%% Swap
            
            # This 'while' loop drives the swapping and constraint propagation
            while target_lst_size > 1:

                # Begin restart, because restart flag detected
                if restart_flag == True:
                    break
                
                # Update deque size
                target_lst_size = len(target_lst)
                
                # pointer is the index target_lst to swap with index iterrows()
                pointer = target_lst.popleft()
                
                # If the index target_lst has already swapped, skip swapping
                if index in previous_index: 
                    
                    # Exit 'while' loop driving swap at this index iterrows()
                    break
                
                # If the deque pointer has already been visited, stop swapping
                # Because this means we have cycled through the deque and couldn't make a swap
                visited_check = visited_nodes.get(index, None)
                
                if visited_check is not None: 
                    if pointer in visited_check:
                        
                        # Exit 'while' loop driving swap at this index iterrows()
                        break
                    else:
                        # Move pointer to end of deque
                        target_lst.append(pointer)
                        visited_nodes[index].add(pointer)
        
                # 'assign_j' is the index target_lst
                assign_j = data.at[pointer, 'assigned_group']
                
                # Prevent self-swapping or row swapping within the same group 
                # Then move the pointer's value to the end of the deque
                # Then re-try using the first element in the deque as the new pointer
                if pointer == index or assign_i == assign_j:
                    previous_index.add(index)
                    previous_index.add(pointer)
                    
                    # Move pointer to end of deque
                    target_lst.append(pointer)
                    visited_nodes[index].add(pointer)
                    
                    # Re-try 'while' loop driving swap at this index iterrows()
                    # Try to find another swap
                    continue
    
                else:    
                    # take snapshots of assignment and group-level diversity before swap
                    snapshot_i = assign_i.copy()
                    snapshot_j = assign_j.copy()

                    
                    # Snapshot previous diversity of the 2 groups. 
                    # (Before the 2 groups had a row swapped)
                    subset_j = data.loc[data['assigned_group'] == assign_j].copy(deep=True)
                    
                    snapshot_diversity_i = calculateDiversity(subset_i, 
                                                              weight_modifier_dict = weight_modifier_dict)
                    snapshot_diversity_j = calculateDiversity(subset_j, 
                                                              weight_modifier_dict = weight_modifier_dict)
                    
                    # Swap group assignments
                    data.at[index, 'assigned_group'] = snapshot_j
                    data.at[pointer, 'assigned_group'] = snapshot_i     
                    subset_i = data.loc[data['assigned_group'] == assign_i].copy(deep=True)
                    subset_j = data.loc[data['assigned_group'] == assign_j].copy(deep=True)
    
                    # Prevent groups with homogenous columns from forming
                    # (if dataset has no homogenous columns).
                    # If dataset has no homogenous columns
                    # and 
                    # if dataset makes any column in either groups 
                    # to be homogenous
                    # re-try another swap.
                    ### check_homogen_flag == False will effectively turns off 
                    ### constraint propagation 
                    
                    #%% Constraint propagation.
                    # If the deque pointer has looped back to 
                    # creating homogenous columns, stop swapping.
                    # Because this means all of the remaining elements of the deque
                    # will create homogenous columns for this index iterrows()
                    homogen_check = homogen_nodes.get(index, None)
                                
                    if homogen_check is not None: 
                        if pointer in homogen_check:
                            
                            # Homogenous features detected in a group. Begin restart process
                            # Revert all assginments to backup and restart assignments
                            data['assigned_group'] = backup_group_col
                            target_lst = [i for i in range(num_rows)]
                            shuffle(target_lst)
                            target_lst = deque(target_lst)
                            restart_flag = True
                            continue
                    
                    if check_homogen_flag == True:
                                                
                        # Identify homogenous columns after swaps
                        homogen_check_1 = list(subset_i.drop(columns = 'assigned_group').nunique())
                        homogen_check_2 = list(subset_j.drop(columns = 'assigned_group').nunique())
                        if 1 in homogen_check_1 or 1 in homogen_check_2:

                            # revert the swap to snapshots
                            data.at[index, 'assigned_group'] = snapshot_i
                            data.at[pointer, 'assigned_group'] = snapshot_j
                            
                            # Move pointer to end of deque
                            target_lst.append(pointer)
                            homogen_nodes[index].add(pointer)

                            # Re-try 'while' loop driving swap at this index iterrows()
                            # Try to find another swap
                            continue
                    
                    elif check_homogen_flag == False:
                        pass # do nothing
                    
                    #%% Proceeding on with the swap
                    
                    # Calculate the change in diversity
                    pair_snapshot_diversity = snapshot_diversity_i + snapshot_diversity_j 
                    
                    dict_diversity_store[assign_i] = calculateDiversity(subset_i, 
                                                                        weight_modifier_dict = weight_modifier_dict)
                    dict_diversity_store[assign_j] = calculateDiversity(subset_j, 
                                                                        weight_modifier_dict = weight_modifier_dict)
                    pair_swapped_diversity = dict_diversity_store[assign_i] + dict_diversity_store[assign_j]
                    
                    delta_diversity = pair_swapped_diversity - pair_snapshot_diversity                    
                        
                    #%% Simulated annealing 
                    
                    # Based on probability, explore alternative solutions
                    # Probability to
                    # reject the swap (ignore pointer swap target)
                    # or 
                    # accept the swap 
                    if delta_diversity > 0:
                        if simulated_annealing_flag == True:
                            probability = uniform(0,1)
                            threshold = exp(-delta_diversity / temperature)
                                        
                            # Probability to reject swap
                            if probability < threshold:
                                
                                # revert the swap to snapshots
                                data.at[index, 'assigned_group'] = snapshot_i
                                data.at[pointer, 'assigned_group'] = snapshot_j
                                dict_diversity_store[assign_i] = snapshot_diversity_i
                                dict_diversity_store[assign_j] = snapshot_diversity_j
                                
                                # Move pointer to end of deque
                                target_lst.append(pointer)

                                # Exit 'while' loop driving swap at this index iterrows()
                                break
                            
                            # Probability to accept swap
                            else:
                                
                                # accept swap 
                                previous_index.add(index)
                                previous_index.add(pointer)
                                
                                # Exit 'while' loop driving swap at this index iterrows()
                                break
                            
                        #%% Don't use simulated annealing if delta_diversity > 0
                        # If simulated annealing disabled, always swap if increased diversity
                        
                        else: 
                            
                            # accept swap 
                            previous_index.add(index)
                            previous_index.add(pointer)
                            
                            # Exit 'while' loop driving swap at this index iterrows()
                            break
                        
                    #%% Else, given delta_diversity <= 0
                    
                    else:
                        # revert the swap to snapshots
                        data.at[index, 'assigned_group'] = snapshot_i
                        data.at[pointer, 'assigned_group'] = snapshot_j
                        dict_diversity_store[assign_i] = snapshot_diversity_i
                        dict_diversity_store[assign_j] = snapshot_diversity_j
                        
                        # Move pointer to end of deque
                        target_lst.append(pointer)
                        visited_nodes[index].add(pointer)
                        
                        #%% Use simulated annealing
                        # If swapping index and pointer decreased diversity 
                        # then based on probability
                        # try finding another solution leading to increased diversity
                        # or 
                        # reject the swap 
                        
                        if simulated_annealing_flag == True:
                            probability = uniform(0,1)
                            if delta_diversity < 0:
                                threshold = exp(delta_diversity / temperature)
                                # Probability to re-try finding a swap
                                if probability < threshold:  
                                    continue
                            # reject swapping
                            # Exit 'while' loop driving swap at this index iterrows()
                                else:
                                    break
                            # ln(exp (0)) is always probability == 0
                            elif delta_diversity == 0:
                                # reject swapping
                                # Exit 'while' loop driving swap at this index iterrows()
                                break    
                            
                        #%% Don't use simulated annealing if delta_diversity <= 0
                        # If simulated annealing disabled, 
                        # always reject if decreased or same diversity
                        else:
                            # since simulated annealing disabled, reject swapping
                            
                            # Exit 'while' loop driving swap at this index iterrows()
                            break    
        
        # Homogenous features detected in a group. Passing restart flag to restart    
        if restart_flag == True:
            continue
      
        # Break from restart loop
        else: 
            break
        
    #%% Calculate grand final diversity 
    
    final_diversity = 0
    dict_diversity_store = {}
    for group_number in grouping_lst:
        subset = data.loc[data['assigned_group'] == group_number]
        dict_diversity_store[group_number] = calculateDiversity(subset, 
                                                                weight_modifier_dict = weight_modifier_dict)
    
    for value in dict_diversity_store.values():
        final_diversity += value
    
    return data, initial_diversity, final_diversity, check_homogen_flag

#%% Function to iterate assignments over specified instance counts

def iterator(writerMethod, mega_num, instance_count, num_groups, num_rows, data, **kwargs):
    # Note: writerMethod is a placeholder for additional coding in MegaTester versioon
    weight_modifier_dict = kwargs.get('weight_modifier_dict', None)
    cooling_schedule = kwargs.get('cooling_schedule', 0.95)
    algorithm = kwargs.get('algorithm', 'TwoHill')
    force_plateau_action_flag = kwargs.get('force_plateau_action_flag', None)
    verbosity = kwargs.get('verbosity', 2)
    mode = kwargs.get('mode', None)
    
    #%% Algorithm settings
    
    algo_dict = {'TwoHill': (False, True, True),
                 'SimAnneal': (False, True, True),
                 'RandomRestart': (False, True, True)
                 }
                 
    randomise_flag = algo_dict[algorithm][0]
    carry_over_flag = algo_dict[algorithm][1]
    plateau_action_flag = algo_dict[algorithm][2]
    
    # User specification to ovewrite plateau capping
    if force_plateau_action_flag == True:
        plateau_action_flag = True
    elif force_plateau_action_flag == False:
        plateau_action_flag = False

    # If weight modifiers are present, modify the weights of that feature.
    if weight_modifier_dict is None:
        None
    else:
        weight_modifier_dict    

    #%% Print opening message of iterator() function
    
    print()
    print("Work progress:")
    print()
    
    #%% Load data
    data = data.copy(deep=True) 
    
    #%% Initialise variables to store outputs from assignments
    
    better_solution = None
    best_solution = None
    current_solution = None
    baseline_initial_diversity = None
    initial_diversity = None
    final_diversity = None
    better_diversity = None
    best_diversity = None
    cache_final_diversity_deque = deque([0])
    shuffle_flag = False
    picked_solution = 0
    elapsed = 0
    
    #%% Initialise deque to support plateau detection
    cache_final_diversity_deque = [0]
    cache_final_diversity_deque = deque(cache_final_diversity_deque)
    
    #%% Initialise TESTER use only flags for reporting
    group_homogen_flag = None
    best_diversity_flag = None
    
    #%% Initialise signals
    plateau_detected_signal = None
    
    #%% Intialise settings to control number of instances
    ### and for temperature for simulated annealing 
    ### Note: for all algorithms, the number instances is controlled by 
    ###       a common math function of temperature.
    ###       Whether there is any simulated annealing in any algorithm, 
    ###       that is separately controlled by the 'threshold' in the assigner() function.
    
    # Initialise the cooling schedule for simulated annealing
    cooling_schedule = cooling_schedule    
    # Define the initial temperature for simulated annealing
    temperature = 1.0     
    # Target temperature
    target = cooling_schedule ** instance_count
    # Initialise the progress tracker variable for reporting to screen
    cache_progress = 0
    # Initialise the solution number tracker
    solution_number = 0

    #%% Run assignment until target instances
    
    while temperature > target:        
        solution_number  += 1    
        
        #%% Start stopwatch
        
        if solution_number == 1:
            stopwatch = Stopwatch()
            stopwatch.start()
            
        #%% Update temperature
        
        # Update temperature
        temperature = temperature * cooling_schedule

        #%% Update progress reporting, synced to temperature

        # Set progress print interval based on verbosity setting
        if verbosity == 2:
            print()
            print(f"Working on Solution Number {solution_number:,} of {instance_count:,} now...")
            
            # Print the progress
            progress = solution_number / instance_count * 100
            
            if progress < 10:   
                print_interval_modulo = 1    
            elif 10 <= progress < 20:
                print_interval_modulo = 1
            elif 20 <= progress < 50:
                print_interval_modulo = 1
            else:
                print_interval_modulo = 1
        
        elif verbosity == 1:
            # Print the progress
            progress = solution_number / instance_count * 100
            
            if progress < 10:   
                print_interval_modulo = 1    
            elif 10 <= progress < 20:
                print_interval_modulo = 5
            elif 20 <= progress < 50:
                print_interval_modulo = 10
            else:
                print_interval_modulo = 20
                
        stepped_progress = progress - (progress % (-print_interval_modulo))    
      
        if cache_progress < stepped_progress:
            if verbosity == 2:
                # Print progress according to print interval
                print(f"Progress: {cache_progress:.0f}%")
            
            elif verbosity == 1:
                # Print progress according to print interval
                if cache_progress < stepped_progress:
                    # For Solution 1, print progress without time estimate
                    if solution_number == 1:
                        print(f"Progress: {cache_progress:.0f}%")
                    # For remaining solutions, print progress along with time estimate
                    else:   
                        print(f"Progress: {cache_progress:.0f}% (Time left: {minutes_estimate:.0f} min {seconds_estimate:.0f} s)")
            
            cache_progress = stepped_progress
                

        #%% Run assignment: if this is first assignment, do this

        # If solution none, this assignment output is best solution
        # Else, take the best solution, then run the assignment again
        if best_solution is None:
           output_1 = assigner(num_groups, 
                                num_rows, 
                                data, 
                                True, 
                                algorithm = algorithm,
                                weight_modifier_dict = weight_modifier_dict,
                                temperature = temperature)
           
           current_solution = output_1[0].copy(deep=True)
           better_solution = output_1[0].copy(deep=True)
           best_solution = output_1[0].copy(deep=True)
            
           # Baseline initial diversity is when we start with sequential grouping
           baseline_initial_diversity = output_1[1]
           
           initial_diversity = output_1[1]
           final_diversity = output_1[2]
           better_diversity = output_1[2]
           best_diversity = output_1[2]
           check_homogen_flag = output_1[3]
           cache_final_diversity_deque.append(final_diversity)
           picked_solution = 1   
               
        #%% Run assignment: if this is subsequent assignment, consider whether to 
        ### carry over assignment output to next assigner() instance
        
        # If there is a solution then
        else:
          
            #%% Code to cut-off a plateau and random-restart 
            
            ### Detect plateau before flagging maxima
            ### if the same better_diversity score obtained 
            ### in specified number of times immediately in sequence
            
            if plateau_action_flag == True:
                if plateau_detected_signal == True:
                    # Shuffle assignment means instead of 
                    # starting from the better assignment
                    # We re-try a different search space, to look for any 
                    # higher hill-maximum areas
                    # Set shuffle_flag to TRUE to enable shuffling
                    if carry_over_flag  == True:
                        shuffle_flag = True  
                    else:
                        shuffle_flag = False
                        
                # Since plateau_detected_signal != True
                else:
                    if carry_over_flag  == True:
                        shuffle_flag = False  
                    else:
                        shuffle_flag = True
                    
            # Do this given plateau detection disabled:
            else:
                if carry_over_flag  == True:
                    shuffle_flag = False
                else:
                    shuffle_flag = True
                
            #%% Run the next assigner()
            
            output_2 = assigner(num_groups, 
                                num_rows, 
                                better_solution, 
                                shuffle_flag, 
                                algorithm = algorithm,
                                carried_over_homogen_result = check_homogen_flag, 
                                weight_modifier_dict = weight_modifier_dict,
                                temperature = temperature)
            
            current_solution = output_2[0].copy(deep=True)
            initial_diversity = output_2[1]
            final_diversity = output_2[2]
            check_homogen_flag = output_2[3]
            cache_final_diversity_deque.append(final_diversity)

            #%% Code to generate plateau_detected_signal
            ### After assigner() iteration complete, signal to 
            ### cut-off plateau and random-restart code
            
            cache_deque_length = len(cache_final_diversity_deque)
            plateau_detected_signal = False
            
            if cache_deque_length == num_groups: 
                check_cache_deque = cache_final_diversity_deque.pop()
                
                if check_cache_deque == better_diversity:
                    best_repeats_count = 1
                    for i in cache_final_diversity_deque:
                        if i == better_diversity:
                            best_repeats_count += 1
                    if best_repeats_count == num_groups:
                        plateau_detected_signal = True
                        if verbosity == 2:
                            print('Diversity score has reached plateau.')
                
                # return back the element because inspection completed
                cache_final_diversity_deque.append(check_cache_deque)
                # popleft() to keep cache_deque_length within specified size
                cache_final_diversity_deque.popleft()
                    
            #%% Code to select whether an assigner() output gets carried over to next iteration. 

            if final_diversity > better_diversity: 
                better_solution = current_solution.copy(deep=True)
                better_diversity = final_diversity
            
            if better_diversity > best_diversity:
                best_solution = better_solution.copy(deep=True)
                best_diversity = better_diversity
                picked_solution = solution_number
            
        #%% Code to stop stopwatch and report progress
            
        if solution_number == 1:
            stopwatch.stop()
            elapsed_clock = stopwatch.elapsed_time()
        
        if solution_number >= 1:
            solutions_left = instance_count - solution_number
            elapsed = solutions_left * elapsed_clock
        
            minutes_estimate = elapsed // 60
            seconds_estimate = elapsed % 60
        
        if verbosity == 2:
            print()
            print(f"Solution Number {solution_number:,}'s initial diversity score was {initial_diversity}")
            print(f"Solution Number {solution_number:,}'s final diversity score was {final_diversity}")  
            print()
            print(f"The baseline initial diversity score was {baseline_initial_diversity}")
            print(f"The best solution now is Solution Number {picked_solution:,}. The best diversity score achieved was {best_diversity}")
            
            if solution_number == 1:
                message_str = f": {minutes_estimate:.0f} min {seconds_estimate:.0f} s"
                print()
                print("Estimated time to complete" + message_str) 
            
            elif solution_number > 1:
                message_str = f": {minutes_estimate:.0f} min {seconds_estimate:.0f} s"
                print()
                print("Time left" + message_str) 
        
    #%% End iterator() and return outputs
        
    print("Progress: 100%")    
  
    best_solution = best_solution.copy(deep=True)
    return picked_solution, best_solution, best_diversity

#%% class Stopwatch 

# Stopwatch program. Used in estimating compute time. Credit: Mostly AI-generated
class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = perf_counter()

    def stop(self):
        self.end_time = perf_counter()

    def elapsed_time(self):
        estimator_modifier = 1.1 # slight modifier to over-estimate time. Better to over than under estimate.
        elapsed_seconds = (self.end_time - self.start_time) * estimator_modifier
        
        return elapsed_seconds   

#%% Iterate (sample counts of) iterator (1 full run of algorithm) 
    
def megaIterator(mega_instance, num_groups, data, filename_out, **kwargs):
    weight_modifier_dict = kwargs.get('weight_modifier_dict', None)
    algorithm = kwargs.get('algorithm', 'TwoHill')
    cooling_schedule = kwargs.get('cooling_schedule', 0.95)
    force_plateau_action_flag = kwargs.get('force_plateau_action_flag', True)
    verbosity = kwargs.get('verbosity', 2)
    mode = kwargs.get('mode', None)
    
    #%% Intialise parameters5
    
    if mode == 'MegaTester':
        sleep_seconds = 3
    else:
        if verbosity == 2:
            sleep_seconds = 10
        elif verbosity == 1:
            sleep_seconds = 3
    
    # Number of rows in data
    num_rows = len(data)
    
    # Number of features in data
    num_cols = len(data.columns)
    
    # Generate target number of instances
    exhaust_count, instance_count = heuristicEstimator(num_rows, num_groups, num_cols)
     
    # ## FOR FUTURE USE. NOT USED IN DIVERSEASSIGN.v.1.0.1
    # weight_dict =  weightModfier(data)
    
    #%% Messages
    
    def messageVerbose2():
        print()
        print("The programme is assigning groups now.")
        print()
        print(f"There are {exhaust_count:,} solutions possbile.")
        print()
        print(f"Optimising {instance_count:,} solutions using the algorithm: Diverse-Assign {algorithm}.")
        print()
        print("... working...")
        print()
        print('###############################################')

    def messageVerbose1():        
        print()
        print("The programme is assigning groups now.")
        print()
        print("... working...")
        print()
        print('###############################################')
    
    def messageTesterClosing():
        print()
        print(f"{instance_count:,} number of solutions completed. The best solution picked is Solution Number {picked_solution:,}. The best diversity score achieved was {best_diversity}")        
        print()
        print("Group assignment completed.")
        
    def messageProductionClosing(verbosity: int, best_solution):
        
        if verbosity == 2:    
            print()
            print("Group assignment completed.")
            print()
            print(f"{instance_count:,} number of solutions completed. The best solution picked is Solution Number {picked_solution:,}. The best diversity score achieved was {best_diversity:.3f}")            
            
        elif verbosity == 1:
            print()
            print("Group assignment completed.")
            print()
            print(f"The diversity score now is {best_diversity:.3f}") 
        
        print()
        print('###############################################')
        
        output_filename = askInputSave()
        best_solution.to_csv(output_filename, index = False)
        
        print()
        print("Group assignment has been saved into current folder.") 
        print()
        print(f"File saved as: \n \'{output_filename}\'")
        print()
        print("You can close this programme now. \nGoodbye!")
        print()
        input("... Press [ENTER] to quit.")
        
    def askInputSave():
        print()
        print("Saving output... please input a file name to save to?")
        
        while True:    
            try: 
                print()
                output_filename = input("\n **Input the output file name here (e.g. done.csv)**: ")
                if csvCheck(output_filename) == False:
                    raise ValueError() 
                    
            except Exception as e:
                print()
                print("Wrong input. File name must be valid and end with \'.csv\' (e.g. done.csv)")
                print("Please re-try.")
                continue
            
            break
        return output_filename        
        
    #%% Drive functions
    
    if verbosity == 2:
        messageVerbose2()    

    elif verbosity == 1:
        messageVerbose1()    
        
    sleep(sleep_seconds) # The time delay here is for UX purpose only. It is to give time to the user to read above message.
   

    # Run programme in production mode    
    writerMethod = None
    outputs = iterator(writerMethod, 
                       1, 
                       instance_count, 
                       num_groups, 
                       num_rows, 
                       data, 
                       weight_modifier_dict = weight_modifier_dict, 
                       verbosity = verbosity)
        
    picked_solution, best_solution, best_diversity = outputs
    
    messageProductionClosing(verbosity, best_solution)



#%% UI Screen Messages

'''
###############################################
UI Screen Messages
###############################################
'''

# The version number here is for the Diverse-Assign production mode
def messageWelcome(activate_ui_flag: False):
    
    def message():
        print()
        print("*** Diverse-Assign v.1.0.1.a ***")
        print()
        print(" --- Need help?")
        print(" --- Do you need a sample file to demo?") 
        print(" --- Please refer to the README file for help.")
        print()
        print('###############################################')
        
    if activate_ui_flag == True:
        return message()

def messageCSV(activate_ui_flag: False):
    
    msg_reminder0 = " --- File name must end with \'.csv\'"
    msg_reminder1 = " --- e.g. \'sample_class_group.csv\'"
    
    def message():
        print()
        print("Hi there! Please put the profile of your participants / items")
        print("into the same folder as this programme.")
        print()
        print("The file must be in \'.csv\' format.")
        print()
        input('When ready, press [ENTER] to proceed\n\n')
        print()
        print("Please input the name of your file below.") 
        print(msg_reminder0)
        print(msg_reminder1) 
        print()      
        
    def askInput():
        
        first_try_flag = True
        
        while True:  
            tip = " (e.g. my_participants.csv)"
            
            if first_try_flag == True:
                hint = ""
            else:
                hint = tip
            
            msg_question = f"** Input file name here{hint}: "
    
            try:        
                input_filename = input(msg_question)
                first_try_flag = False
                
                if csvCheck(input_filename):
                    data = read_csv(input_filename)
                else:    
                    raise ValueError() 
                
            except Exception or OSError as e:
                print()
                print()
                print("Wrong input or file does not exist in this folder.") 
                print("Please check your folder and re-try.")
                print(" --- File must be in the same folder as this progeamme.")
                print(msg_reminder0)
                print(msg_reminder1) 
                print()
                continue
            
            break
        
        return data

    if activate_ui_flag == True:
        message()
        data = askInput()
        print()
        print('###############################################')
        return data

def messageNumGroup(activate_ui_flag: False):
    
    def message():
        print()
        print("Please input the number of groups you wish to create.")
        print(" --- The programme will evenly split participants / items into groups.")
        
    def askInput():
        first_try_flag = True
        
        while True:
            print()  
            try:
                tip = " (e.g. 12)"
                
                if first_try_flag == True:
                    hint = ""
                else:
                    hint = tip
                
                msg_question = f"** Input the number of groups here{hint}: "
                first_try_flag = False
            
                num_groups = input(msg_question)
                num_groups = int(num_groups)
                num_rows = len(data)
                
                print()
                print(f"... Note: there are {num_rows} of participants / items in your profile.")
                
                
                if type(num_groups) != int:
                    raise ValueError() 
                elif num_groups < 2:
                    raise ValueError() 
                elif num_groups >= num_rows:
                    raise ValueError() 
                    
            except Exception as e:
                print()
                print()
                if type(num_groups) != int:
                    print("Wrong input. Number has to be in digits.") 
                    print("No commas or decimals. (e.g. 12)")
                    print("Please re-try.")
                    
                elif num_groups < 2:
                    print("Wrong input. Number of groups has to be greater than 1. Please re-try.")
                
                elif num_groups >= num_rows:
                    print(f"Wrong input. Number of groups must be smaller than {num_rows}.") 
                    print(f"There are {num_rows} participants / items. Please re-try.")
                
                continue
        
            break
        
        return num_groups

    if activate_ui_flag == True:
        message()
        num_groups = askInput()
        print()
        print('###############################################')
        return num_groups

def messageVerbose(activate_ui_flag: False):
    
    def message():
        print()
        print("Please select [DEFAULT] or [ADVANCED] job progress view.")
        print()
        print(" --- [DEFAULT] Recommended for most users. See basic job progress info. Input: '1'")
        print(" --- [AVANCED] Highly verbose progress updates. Input: '2'")
        print()

    def askInput():
        while True:
            print()  
            try:
                verbosity = input("**Please input '1' for [DEFAULT] or '2' for [ADVANCED]: ")
                verbosity = int(verbosity)
                
                if verbosity > 2 or verbosity < 1:
                    raise ValueError()
                    
            except Exception as e:
                print()
                print()
                print("Wrong input. Please input '1' for [DEFAULT] or '2' for [ADVANCED]. Please re-try.")
                continue
            
            break
        
        return verbosity
    
    if activate_ui_flag == True:
        message()
        verbosity = askInput()
        print()
        print('###############################################')
        return verbosity

#%% Driver code

'''
###############################################
DRIVER CODE
###############################################
'''
    
#%% Set working folder. Compatible with IDE or PyInstaller executable

if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    base_path = sys._MEIPASS
else:
    # Running normally as a Python script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.getcwd()

#%% Create weights

# ## WEIGHTS FOR FUTURE USE. NOT USED IN DIVERSEASSIGN.v.1.0.1

# ## The effect of weights is still being studied. 
# ## Users should study before enabling.
 
# ## WARNING: weight modifiers only makes sense when based on dataset.
# ## DO NOT BASE WEIGHTS ON SUBSET. Because subset (or 'groups') shift composition during swapping.

# weight_dict = weightModfier(input_data)

#%% Mode switch

# set below to TRUE to activate UI messages in the Diverse-Assign Production version
activate_ui_flag = True

#%% Normal UI <- UI used in compiled production executable or py script 

if activate_ui_flag == True:

    messageWelcome(activate_ui_flag)
    data = messageCSV(activate_ui_flag)
    num_groups = messageNumGroup(activate_ui_flag)
    verbosity = messageVerbose(activate_ui_flag)

    megaIterator(1, 
                 num_groups, 
                 data, 
                 None,
                 verbosity = verbosity)
    
