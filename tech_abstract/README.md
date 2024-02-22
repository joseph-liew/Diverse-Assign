# Technical Paper: **Diverse-Assign**

*Diverse-Assign* is a constraint optimisation programme for maximising diversity of group assignments.  This page covers the technical background and explains its method. It also introduces the pseudocode and key innovations. 


## Page overview
-	[Background](#back)
-	[Key features innovations](#key)
-	[Method: how *Diverse-Assign* works](#method)
-	[Quantifying diversity](#ads)
-	[Pseudocode](#pseudo)
-	[Algorithm and heuristic design](#design)
-	[Limitations](#limit)


## Background <a name="back"></a>

Many activities require the grouping or assignment of elements. For example, assigning students to classes or allocating interactive agents in combinatorial experiments. Often, the assignment objective is to maximise diversity within these groups, whether to foster understanding among individuals or to examine interactions among highly distinct agents in experiments. However, maximising diversity presents a non-trivial challenge, due to unique combination of features and attributes each element possesses. For instance, a student population may exhibit gender as a feature with binary attributes, alongside the multi-attribute feature education backgrounds. These features and attributes collectively form a unique feature profile within any population. Exploring all possible combinations of group assignments to maximise diversity is impractical. Example: Assigning 60 elements into groups of 6 yields over 50 million potential combinations. (<sub>n</sub>C<sub>r</sub> = 60 Choose 6 = 50,063,800 combinations)

*Diverse-Assign* was developed as a group assignment tool that maximise diversity. By quantifying diversity as information gain, diversity can be maximised using constraint optimisation. A [pilot study](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/pilot_study/README.md) showed that *Diverse-Assign* outperformed pseudorandom shuffling in diversity by as much as 15,900x (median) and SEM to mean ratio of 0.01. Variance was almost negligible.


## Key feature and innovations <a name="key">

Keys features:
- *Diverse-Assign* is data type agnostic. Supports a wide range of applications. 
- Assign elements into groups, regardless of discrete / continuous / ordinal / nominal data. (All data are interpreted as nominal data.)
- Supports any number of data features and attributes.
- Creates groups that are free from homogenous features. Heuristically relaxes this constraint if not possible.
- Supports the use of weights to increase / decrease the importance of selected features.
Key innovations
- Innovative use of information gain to objectively quantify diversity.
- Development of constraint specific swap-search, based on the AC3 algorithm used in Constraint Satisfaction Problems (CSP). 
-  Hybridised integration of multiple algorithms to positively mutually reinforce each other algorithm’s search properties. This achieves convergence with less time complexity.

<a name="method">## Method: how *Diverse-Assign* works

*Diverse-Assign* employs a finite domain tree-search constraint optimisation. This method utilises a swap-search technique to enforce the constraint that prohibits groups from containing homogeneous features. The search begins by provisionally assigning elements to groups. Through element exchanges between groups, diversity is enhanced while ensuring adherence to the constraint against homogeneity.
 
*Diverse-Assign* combines several algorithms to drive the swap-search optimisation. Swap-search is driven by "Unclosed AC3" algorithm, an adaptation of the widely employed AC3 algorithm in Constraint Satisfaction Problems (CSP). As the search progress, unclosed AC3 prunes solutions that fail to meet specified constraints, significantly streamlining solution exploration. Augmenting the search, diversity is measured using [information gain], and optimised using simulated annealing. Simulated annealing is used to select swaps that maximise the sum diversity of both groups. To navigate sub-optimal plateaus of diversity scores, a heuristic determines whether the diversity score has reached plateau. Upon detection, random restart hill-climbing is enabled to drive the simulated annealing to a different search direction. 

In some populations, strict prohibition of groups to contain homogeneous features is not possible. In these populations, an attribute might be over-dominant in the population. This situation forces at least one group to fill the entire group with elements of the same attribute; there is no space left in the other groups to take on these elements. In *Diverse-Assign*, a heuristic determines whether to relax the constraint, enabling group assignments to proceed.

*Section shortcuts*

[Click here to learn how diversity is measured](#ads).

[Click here for the pseudocode](#pseudo). 

[Click here to know more about the algorithm and heuristic design](#design).

<a name="ads"></a>## Quantifying diversity

In information theory and computer science, information gain is measured using Shannon’s entropy.  This measurement measures the entropy of information in a dataset. Entropy is a function of the number of unique elements of information, and the proportional quantity of each unique elements. ([*Shannon & Weaver, 1949*](#SW)) To increase entropy, there must be more unique elements, while the proportional quantity decreases to allow the presence of other unique elements. In other words, entropy increases when the dataset is more heterogenous. Intuitively, entropy analogous to diversity. Both diversity and entropy increases with heterogeneity. In ecology and population genetics, Shannon entropy is coopted to measure diversity, where it known as the “Shannon-Weaver index”. 

The Shannon-Weaver index is defined as:

$$
\ H^{\prime} = -\sum_{n=1}^{n} \left(p_{\mathrm{x}} \cdot \ln p_{\mathrm{x}}\right) \
$$

> where *H′* is the Shannon-Weaver index, *x* is a unique element, *p<sub>x</sub>* is the proportion of *x* elements in the population count, and *ln p<sub>x</sub>* is the natural logarithm of this proportion. 

This index yields a positive score. The greater score, the greater the diversity (or heterogeneity).

In *Diverse-Assign*, we propose an *Aggregate Diversity Score* to measure whether a group has, in aggregate, a more diverse profile of features. Aggregate Diversity Score is adapted from the Shannon-Weaver index.

A group of elements and their profiles can be represented using a 2-d matrix. This is the most universally known way to represent profiles. Each row represent an element. The columns are different features that each element has. Each element has an attribute of the feature, represented as the row index of the feature column. For example, a unique person at row 0 has gender as a feature column. The intersection of row 0 feature column has the gender attribute.

We can determine the diversity of groups using the Shannon-Weaver index. Let *x* be a unique feature attribute. The total counts of each unique *x* attribute in a feature makes the group population. By taking the aggregate Shannon-Weaver index of all features, we obtain the *Aggregate Diversity Score* for the group population. A group with greater Aggregate Diversity Score (ADS) is more diverse than another group with a lower ADS.

By using the ADS, we can easily measure and compare the diversity of groups. Importantly, if the ADS of each group is increased, grand sum of Aggregate ADS across all groups will also increase. If we exchange group assignment between two elements, we can measure the ADS to easily determine whether the swap increased the diversity at the group and all-groups level.

Another benefit of ADS is support for using weights to direct the programme to modulate the importance certain attributes or features. By multiplying a weight with the Shannon-Weaver index of a feature or attribute, we change the impact the feature or attribute has on ADS and homogeneity. A practical application is to improve the importance of minority attributes, directing the programme to increase minority presence evenly across all groups.

*Section shortcuts*

[Click here for the pseudocode](#pseudo). 

[Click here to know more about the algorithm and heuristic design](#design).


## Pseudocode <a name="pseudo"></a>

Introduction to the pseudocode:
- *Diverse-Assign* is comprised of 2 functions: *Iterator( )* and *Assigner( )*. 
- Data is first input into *Iterator( )*. 
- Within *Iterator( )*, data is passed into *Assigner( )* for group assignment and swaps-search optimisation.
- Next, *Iterator( )* iteratively passes the assignments back to *Assigner( )* for further optimisation. The number of iterations is controlled by simulated annealing’s cooling rate.
- Between each iteration, *Iterator( )* only select solutions with an improved diversity to pass into *Assigner( )* for further optimisation.
- When the iterations end, *Iterator( )* returns the most optimised solution.

*Section shortcut:* [Click here for pseudocode flowchart.](#causal). Or read on to read pseudocode.

Pseudocode for *Iterator( )* and *Assigner( )*:

```python
ITERATOR(Input Dataframe):

Target Temperature = Cooling Schedule ^ Target Instance Count

while Temperature > Target Temperature:
	
	update Temperature based on Cooling Schedule

 
	if Solution is None: 
	
		enable shuffle group assignment in Assigner() 
		
		Final Diversity Score, Best Solution  = Assigner(Input Dataframe)
		
		Best Diversity Score = Final Diversity Sore
		
		update deque queue Cache to track diversity score plateau
	
	else:
	
		enable Random-Restart Algorithm in Assigner() 
		
		check deque queue Cache

			if Diversity Score Plateau:
		
				enable shuffle group assignment in Assigner() (enable Random-Restart optimisation)

			else:
				
				disable shuffle group assignment in Assigner() 
			
		do Basic Hill-Climbing:	
			
			Final Diversity Score, Solution  = Assigner(Best Solution)
			
			compare Final Diversity Score with Best Diversity Score
			
			pick solution with better score to use as starting point for next iteration of Assigner() 
			
			update Best Solution, Best Diversity Score, Cache
				

return Best Solution, Best Diversity Score 


ASSIGNER(Input Dataframe or Solution):

do heuristic check, whether relaxation of no-homogenous-feature-in-any-group required
	if required:
		enable constraint propagation of no-homogenous-feature-in-any-group
	else:
		disable constraint propagation

if shuffle group assignment is enabled:
	assign groups sequentially by stratification, to Input Dataframe or overwrite Solution
	if constraint propagation enabled, re-shuffle until constraint is satisfied.


backup a copy of assignments in Input Dataframe or overwrite Solution 

do Unclosed AC3 Algorithm on Input Dataframe or Solution:

	initialise empty set Previous Index

	initialise deque queue of Targets row indices to swap group assignment
	
	shuffle deque queue Targets
	
	initialise empty hashmap Visited Nodes to track Row Index visited nodes.
	
	initialise empty hashmap Homogenous Nodes to a track Row Index attempted nodes that failed homogenous feature check.

	while True
	
		initialise Restart Flag as FALSE
		
		for Row Index in Input Dataframe or Solution:
			
			update hashmap Visited Nodes with Row Index: empty set 
			
			update hashmap Homogenous Nodes with Row Index: empty set
			
			initialise empty hashmap Homogenous Nodes to a track Row Index attempted nodes that failed homogenous feature check.
			
			while Targets length > 1:
			
				if Restart Flag TRUE:
					
					break 'for' loop to restart the search from first index iterrows()
			
				Pointer = POP-LEFT Targets
			
				if Row Index in Previous Index:
					
					break 
					'(Note: Because this index has already been swapped or rejected,'
					'it is in the set. This is a cycle detection that will'
					'break the 'while' loop once all indices are in the set.)'
				
				check Visited Nodes hashmap, whether Row Index has Pointer
					
					if True:
					
						break
						
					else:
						
						APPEND-RIGHT Pointer back to Target to keep this Pointer for other Row Index to swap				
				
				do swap of Row Index's assignment with that in Pointer:		
					
					do constraint propagation:										
					
						check: 				
						
							either Homogenous Nodes hashmap, whether Row Index's set has Pointer
							
								if TRUE: 
									
									cycle detected
									(Note: This means the Pointer has already been checked for 
									homogenous feature and failed. No alternative Pointers remaining.)
							
							or Row Index's group has homogenous feature
								
								if TRUE:
								
									the swaps has left this Row Index with constraint satisfaction failure
									'(Note: This means the entire solution is not valid)'
							
							if either checks were TRUE, then:
								
								restore entire dataset's group assignments to backup assignments
								
								create and shuffle a new Targets deque for restart
								
								set Restart Flag TRUE
								
								continue

						check whether homogenous-feature constraint is found in either Row Index or Pointer new group:
							
							if TRUE: 
							
								revert the swaps
								
								in Homogenous Nodes, add Pointer into Row Index set
								
								continue 
					
					check whether Row Index == Pointer or both assignments are the same group:
					
						if True:
					
							revert the swaps
							
							APPEND-RIGHT Pointer back to Target to keep this Pointer for other Row Index to swap
							
							continue 
							'(Note: This prevents self-swapping and swapping within the same group.'
							'It also loops back the 'while' loop to find another Pointer to swap.)'
						
					do Simulated Annealing Algorithm:
					
						'calculate change in diversity' (also known as Delta Diversity)
						
						if Delta Diversity > 0:
				
							use probability to select whether current swap is accepted or reverted
							'(Note: the probability of reversion decreases with each iteration,' 
							'due to the reduction in temperature)'
							
							if accepted:
							
								add Row Index and Pointer to Previous Index set
								
								break
								
							else: 
								revert swaps
								
								APPEND-RIGHT Pointer back to Target to keep this Pointer for other Row Index to swap
								
								break
								
						else:
							
							revert the swaps
							
							add Row Index and Pointer to Previous Index set
							
							APPEND-RIGHT Pointer back to Target to keep this Pointer for other Row Index to swap
							
							if Delta Diversity < 0:
							
								use probability to select whether to re-try swap with a different Pointer or to just break
								'(Note: the probability of re-trying decreases with each iteration,' 
								'due to the reduction in temperature)'
								
								if re-try:
								
									continue
									
								else:
								
									break 
								
		if Restart Flag TRUE:
			
			set Restart Flag FALSE
			
			continue to restart the search from first index iterrows()
		
		else:
			
			'break from restart loop and proceed programme'
			
	calculate Final Diversity Score
	
	Solution = Input Dataframe or Solution
	
	return Final Diversity Score, Solution
```

*Section shortcuts*

[Click here to learn how diversity is measured](#ads).

[Click here to know more about the algorithm and heuristic design](#design).


## Algorithm and heuristic design <a name="design"></a>

A key design is the hybridised integration of multiple algorithms to positively mutually reinforce each other algorithm’s search properties.  This section explains why the algorithms were implemented as shown in the [pseudocode](#pseudo).
 
This section also covers how the heuristics work and their design considerations.


### Rationale for hybridised integration

Early designs of *Diverse-Assign* could increase diversity. However, they could not achieve maximum diversity convergence. I.e. given identical starting inputs, parameters and iterations, achieve a similar diversity score. These designs focused on a single state to optimise -- the right groups assignment swaps that increased diversity.

Further experiments found that the efficiency and effectiveness of swap-search optimisation depended on multiple factors:
-	Optimising the right swaps that increased diversity. (Optimising swapped group assignment as a state.)
-	Optimising the sequence of swaps to increase diversity. (Optimising swap sequence as a state.)
-	Optimising the simulated annealing action that determines whether to try the standard or alternative swap. (Optimising annealing action as a search state.)
-	Optimisation in the early iterations should promote exploration, and exploitation in later iterations. This applies to all above states.
-	Eliminate duplicate swaps that had failed to increase diversity.
-	Eliminate duplicate swaps that had resulted in homogenous feature(s).
-	Eliminate wasted optimisations. Solutions from each iteration should feed into the next iteration for further optimisation.
-	Avoid repeating the same search direction if a diversity hill-climb plateau has been reached. Explore alternative search directions to find alternate break-through.

The reason for optimising the indicated states is that these states determine whether the best swaps could be made first. Swapping is combination without replacement. Hence the best swaps cannot be made if the right pair of elements had swapped groups. 

Eliminating duplicates and wastes directly affects efficiency. It increases the likelihood of the programme converging on a common result within the same number of iterations. 

Avoiding the same search direction meant simulated annealing alone was insufficient to change the search directions. This is because simulated annealing affects which elements are swapped. It does not affect which elements are inspected first. If the current iteration uses the previous iteration output for optimisation, this sequence is already determined. Hence, over multiple iterations, simulated annealing can make gradual changes to the assignments. But these gradual changes sometimes not different enough to change the search direction and overcome a sub-optimal diversity plateau. This is especially true in later iterations, where the annealing probability to accept alternatives is low.

The solution is to use multiple algorithms to optimise multiple states. The assignment from each optimisation are be fed into the next iteration for further optimisation. If a plateau is detected, switch from simulated annealing to a method more aggressive exploration method. [Figure 1](#causal) summarises how multiple algorithms are connected in *Diverse-Assign*.  


<a name="causal"></a> **Figure 1: Flowchart of *Diverse-Assign’s* swap-search algorithms, with causal loop diagram overlay.** Flowchart summarises how algorithms operate at each optimisation iteration. The shaded areas shows where the algorithms overlap and integrate into each other. A causal loop diagram is overlaid to show how one algorithm’s properties reinforce another algorithm’s properties.
![Figure 1: Flowchart of *Diverse-Assign’s* swap-search algorithms, with causal loop diagram overlay.](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/tech_paper/causal_loop.png)

As shown in [Figure 1](#causal), *Diverse-Assign's* algorithms are integrated into each other. This is to use each algorithm’s search properties to reinforce the other’s properties. This also important in larger problems, where we want to quickly prune down the search space, focus optimisation efforts to achieve optimisation, and quickly explore alternative direction to break-through sub-optimal plateau.

Another reason for the hybridisation is to minimise time complexity. All algorithms are part of a single iteration loop, forming a single optimisation instance.  Hybridised integration’s time complexity is O(*n*). This is lower than other possible designs

Alternatively, reinforced integration can be implemented as either a linear chain or in a nested designs. A one loop for each algorithm; each loop connected to the other in a chain. One chain is one optimisation iteration. Time complexity is O(*b n*), where *b* is the number algorithm. In nested design, the algorithms are nested into each other. Time complexity is factorial time.


### Algorithm: Design of Unclosed AC3 swap-search 
The original AC3 algorithm is used allocate elements into groups, while adhering to constraints. In essence, [(Norvig and Russell, 2021)](#HILL) each group (or ‘domain’ in CSP terminology) begins with a collection of all elements. The algorithm inspects between pairs of domains. As the domain pairs are inspected, elements that fail constraint satisfaction are removed from the domain. A queue keeps track of which pair of domains have not been inspected. Importantly, AC3 propagates the decision of satisfactory allocation, while pruning off unsatisfactory allocations. A collection which swaps have already been visited and failed. This prunes unsatisfactory allocations reducing the number of allocation combinations to explore. This is useful in shrinking the size of large problems.

In *Diverse-Assign*, unclosed AC3 was developed to drive constraint satisfaction swap-search. It is a modification of the AC3 algorithm. Similar to AC3, unclosed AC3’s queue keeps track of the pairs inspect. If a target element for swapping was unsatisfactory or did not improve diversity, that element was sent to the end of the queue to try swapping with a different element. A hash map is used to remember which swaps have already been visited or failed, pruning invalid solutions.

In contrast, unclosed AC3 does not initialise with every element in all domains. Also, the pairs inspected are different. Instead, unclosed AC3 provisionally assigns elements to domains, ensuring that the same element is not repeated across different domains. The domain assignments are then exchanged. If the exchange fails to satisfy constraints, elements are swapped with those from another domain. When used with search optimisation, the constraint that swaps must increase diversity is introduced as a constraint, adding optimisation to the swap-search.

Another critical difference between AC3 and unclosed AC3 is in the final step. In AC3, the algorithm inspects satisfaction between the final domain with the first domain. This is to ensure that the first and final domains satisfy the constraints. In unclosed AC3, the algorithm only checks the domain of the final element for constraint satisfaction, leaving the final loop ‘unclosed’. 


#### Unclosed AC3’s lower complexity in this problem
If the domain of the final element in unclosed AC3 fails satisfaction, unclosed AC3 restarts the swap from the beginning. It begins with a different sequence of elements in the queue to swap, exploring a different combination. Two reasons for this design: (1) the given constraint (prohibition against homogeneity constrain) is only applied to within a domain, not across domains. (2) In this problem, unclosed AC3 tree-search has a lower time complexity.

Firstly, the given constraint (prohibition against homogeneity) is only applied within a domain. AC3’s comparison between pairs of domains adds a duplicate process for each domain. Evaluating the duplicate process increases the time, while tracking another set of elements for the duplicate adds space complexity.

Secondly, unclosed AC3 swap-search has a lower time complexity than AC3 in this problem. Unclosed AC3 is O(</em>2 <sub>n</sub>C<sub>2</sub></em>) v.s. AC3’s O(<em><sub>n</sub>C<sub>n / no. of groups</sub></em>). This has to do with diversity being a function of both the variety of attributes in a feature as well as the attribute’s proportion to the population. In both algorithms, as the composition of a domain changes with each allocation or assignment, diversity for the entire domain must re-calculated. This means that any node backtracking in AC3 has to be revisited and tested to check for the change in diversity.

In contrast, for unclosed AC3, the number of changes is determined by the number of pairs to swap. The swap is always 2 pairs of elements, across the population. (O(<em>2<sub>n</sub>C<sub>2</sub></em>).) 

Note, in *Diverse-Assign*, prior to unclosed AC3, the initial provisional assignments are pre-sorted to remove homogenous features in any group. This prevents unclosed AC3 inheriting elements in a group with homogenous features, triggering a search restart. While pre-sorting adds time complexity, it halves unclosed AC3’s time complexity, by avoiding a restart. In *Diverse-Assign*, pre-sort is a simple reshuffle until the constraint is satisfied. Even with reshuffling, for large problems, unclosed AC3’s is still smaller than AC3’s O(<em>n C n / no. of groups </sub></em>).

#### Unclosed AC3 supports constraint relaxation
Unclosed AC3 can be used with optimisation to support a relaxed constraint. This relaxation is useful when there is one or more extremely features that are over-dominated by an attribute. The relax constraint is that features can be homogenous in group, but minimised element dominance in any feature. 

This new constraint is an optimisation problem; it is not a constraint satisfaction problem. This relaxed constraint can be simply applied by disabling the constraint check. No constraint needs to be propagated. This is because diversity only increases when element variety in features increase, while dominance decreases. Hence, selecting for increased diversity will also minimise element dominance in all groups, satisfying the constraint.

In contrast, AC3 will be pointless if the constraint relaxed. The duplicate comparison between pairs of domains are duplicates process that does not contribute to the solution.


### Algorithm: Simulated annealing optimisation
In *Diverse-Assign*, hill climbing is implemented at two levels of search states:
1)	First level: During the unclosed AC3 swap-search. Domains (or groups) are exchanged if exchange leads to positive delta diversity of both groups.
2)	Second level: At the end of optimisation iteration, if the new assignments have better diversity than the best solution of past iteration, the new assignments become the best solution. Use the best solution as the initial state in the next  optimisation iteration.

In *Diverse-Assign*, simulated annealing acts at both levels. In the first-level, it selects for element swaps that leads to increased diversity of both groups. At the second-level, the completed swaps are then fed into the next iteration, for simulated annealing to further optimise. 

With each iteration, small tweaks to the annealing action are made. The goal is to explore whether the small tweaks result in a more diverse solution at the end of the optimisation iteration. Whether small tweaks are made is based on the annealing probability. As simulated annealing iteration is completed, the probability to select the tweak decreases. This probability continues to decrease, until the target temperature hits and iterations halt. As explained by [Norvig and Russell (2021)](#HILL), the probability is high initially, to quickly explore different search space at the start. As the iterations proceed, the probability is reduced to promote exploitation. This is because large tweaks might lead to large changes that miss the peak diversity score, appearing as a sub-optimal score instead. Thus, simulated annealing can push through sub-optimal diversity plateaus, through the exploration and exploitation of different search spaces. 


#### Simulated annealing: standard annealing action and alternate tweak
In *Diverse-Assign*, standard and alternate annealing action are states that are explored and exploited during optimisation. [Table 1](#table1) summarises what are the standard and alternate actions, and the rationale.

 
<a name="table1"></a>**Table 1: Annealing actions and rationale**
![Table 1: Annealing actions and rationale](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/tech_paper/tech_paper_table1.PNG)

#### Annealing probability and cooling schedule
The annealing probability determine by a swap’s change in diversity, and the decrease in temperature. The annealing probability formula is a modification of the annealing probability in thermodynamics.

In thermodynamics, annealing probability formula is:

$$
P = e^{-\frac{\Delta E}{k \ \cdot \ T}} \
$$

> where *P* is the probability that the energy will increase by delta E, *delta E* is change in energy (new energy - previous energy), *k* is the Boltzmann Constant, *T* is temperature.

In *Diverse-Assign*, the annealing probability is:

$$
P = e \^{-\frac{\Delta \ ADS}{T}} \
$$

> where *Delta ADS* is the change in *Aggregate Diversity Score* sum of both groups after the groups are exchanged.

If *Delta ADS* < 0, the negative sign is removed from Euler’s power term. This is to ensure that *P* is a valid probability between 0 and 1:

$$
P = e \^{\frac{\Delta \ ADS}{T}} \
$$

The temperature is controlled by the cooling schedule. At each instance, temperature is reduced, using the cooling schedule:

$$
T = T \cdot cooling \ schedule
$$

> where cooling schedule = 0.95

In effect, this sets the number of optimisation iterations to exactly 115 iterations. This means that time complexity for optimisation scales with constant time. This makes *Diverse-Assign* appealing even in large problems.

The number of iteration instance was selected to maintain a target annealing probability for a target delta diversity. The targets are: delta diversity = -0.01, target probability < 0.03, cooling schedule = 0.95:

$$
Target \ temperature = {\frac{\ given \ \Delta ADS}{\ln(target \ probability)}}
\cdot number \ of \ iteration \ instances  = \log_{target \ temperature}{cooling \ schedule}
$$

In other words, fixes the cooling schedule to a target response sensitivity to delta diversity. There is a 0.03 probability to look for alternate solutions, when the changes in diversity as small as -0.01, upon the 115th iteration.

### Algorithm: Random restart hill-climbing 
Hill-climbing’s limitation is its tendency to get trapped at a sub-optimal solution. This happens when the algorithm reaches a local maximum. [(Norvig and Russell, 2021)](#HILL)  A local maximum is the solution with the best result, within the direction of search. Despite multiple attempts in the current search space, the attempts converge on the plateau for that local search space. Changing the direction or local search space lead to an even higher local maximum. The ideal outcome is to find the global maximum; highest local maximum across every possible solution. Alternatively, the algorithm can also remain trapped at a plateau. A plateau forms when the alternative solutions yield the same score.

Experiments show that simulated annealing is sometimes insufficient to push through plateaus. This is because simulated annealing makes gradual changes, which are not large enough to change search direction and break-through the plateau. With each iteration to optimise the previous solution, changes are gradual. This is especially true in later iterations, where the annealing probability to accept alternatives is low.

To aggressively change the search direction, Random restart hill-climbing is used when a plateau is reached. Random restart hill-climbing picks a pseudorandom starting point for the search. Unlike simulated annealing, the direction of the search is not gradually shifted over time. The aim is to force algorithm to start a very different solution from the one used by simulated annealing, helping to expand the search space. In problems where there are few local maximums, random restart can be very effective, picking the most optimal direction in within a small number of iterations. [(Norvig and Russell, 2021)](#HILL)  


### Heuristic: Plateau detection
A plateau detection heuristic is needed to navigate through sub-optimal diversity score plateaus. Inherent to hill climbing, there is a challenge to distinguish whether an optimisation plateau is an optimal solution convergence, or convergence at a sub-optimal plateau. This is explained in detail by [Norvig and Russell (2021)](#HILL/). A plateau is formed when the current search direction converges on a local maximum score. Changing the direction or local search space might lead to an even higher local maximum. Ideally, the algorithm should converge on a global maximum plateau -- the highest plateau possible. 

Without a heuristic, the algorithm will not terminate upon maximum convergence, continuing indefinitely. Neither will the algorithm explore another direction upon hitting any plateau. A heuristic-less algorithm will assume any plateau as convergence on the optimal plateau.

*Diverse-Assign* proposes a simple heuristic to determine whether a plateau is the maximum convergence. A plateau is defined as achieving the same diversity score across a repeated count equivalent to the number of groups. This heuristic was selected based on experiments. Once a plateau is identified, the heuristic enables random restart within the simulated annealing sub-algorithm. This will change the search direction to explore for higher plateaus.

The observation that the number of repeats for the sub-optimal plateau is related to the number of groups to assign could be due to mathematical structure. The algorithm must try each element in every group before it finds a break-through. If it can’t find a break-through, even after changing the search direction, this plateau is the maximum convergence. However, the actual relationship is likely a cumulative probability multiplied by the factor of the number of groups instead. This is because simulated annealing and random restart are probabilistic methods. Mathematical modelling is needed to study the relationship and optimise the plateau detection heuristic.


### Heuristic: Constraint relaxation
In some populations, strict prohibition of groups to contain homogeneous features is not possible. In these populations, an attribute might be over-dominant in the population. This situation forces at least one group to fill the entire group with elements of the same attribute; there is no space left in the other groups to take on these elements. In *Diverse-Assign*, a heuristic determines whether to relax the constraint, enabling group assignments to proceed.

*Diverse-Assign* uses a simple heuristic formula to detect over-dominant attributes. The number of elements in each attributes is counted, and the following rule is applied:

$$
\text{If TRUE:}
$$

$$
\left\lfloor \frac{\text{Population size} - \text{count of elements with attribute}}{\text{number of groups to assign}} \right\rfloor \leq 0 
$$

$$
\text{THEN: OVER-DOMINANT}
$$

Testing this heuristic and induction through mathematical modelling might discover more areas for enhancement.


## Limitations <a name="limit"></a>

A [pilot study](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/pilot_study/README.md) found *Diverse-Assign* to have strong performance, with consistent and reproducible results. Nonetheless, *Diverse-Assign* has limitations.

While *Diverse-Assign* can greatly optimise group diversity and achieve convergence, more study is need to determine whether this is the global maximum. 

Also, while the [pilot study](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/pilot_study/README.md) found the current design to perform well in a broad range of data topology, the study also found that different algorithms perform performed  better in certain range of topologies. A heuristic could be designed to analyse the data topology and select the most efficient and effective optimisation algorithms. 

*Diverse-Assign’s* current heuristics has performed well, but there is room for improvement. Mathematical modelling and more detailed experiments would be helpful to guide enhancements.


## References
<a name="SW"></a>Shannon, C. E., and Weaver, W., 1949. The Mathematical Theory of Communication. Urbana: University of Illinois Press.
[*Article extract*](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

<a name="HILL"></a>Norvig, P., Russell, S. (2021). Local Search and Optimization Problems In: Artificial Intelligence. A Modern Approach. 4th US Edition. Prentice Hall
