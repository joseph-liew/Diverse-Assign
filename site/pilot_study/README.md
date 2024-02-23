# Enhancing Diversity Optimisation: A Pilot Study Investigating the Performance of *Diverse-Assign* in Group Assignments

## Abstract
Maximising diversity in group assignments pose challenge, due to the varying features and attributes of the group elements. *Diverse-Assign* aims to surpass pseudorandom shuffling in diversity optimisation while addressing its limitations. We assess its effectiveness and the utility of *Diverse-Assign’s* algorithms and heuristic. Findings indicate *Diverse-Assign* definitively outperforms pseudorandom assignment, while mitigating homogeneity issues. *Diverse-Assign* outperformed pseudorandom shuffling in diversity by as much as 15,900x (median). Variance was almost negligible, the largest SEM to mean ratio was 0.01. Results were consistent and reproducible, suggesting its robustness. Further study and testing are recommended for enhancements. *Diverse-Assign* design and heuristics show promise in navigating suboptimal plateaus, enhancing diversity optimisation.

## Aim:
Using different data topologies, determine whether:
- *Diverse-Assign* outperforms pseudorandom assignment in maximising diversity, while avoiding homogenous features.
- *Diverse-Assign’s* heuristic can terminate search early, without reducing diversity maximisation.
Secondary aim:
- To support enhancements, analyse the performance *Diverse-Assign’s* component algorithm and heuristic to identify areas for improvement.

## Background
Many activities require the grouping or assignment of elements. For example, assigning students to classes or allocating interactive agents in combinatorial experiments. Often, the assignment objective is to maximise diversity within these groups, whether to foster understanding among individuals or to examine interactions among highly distinct agents in experiments. However, maximising diversity presents a non-trivial challenge, due to unique combination of features and attributes each element possesses. For instance, a student population may exhibit gender as a feature with binary attributes, alongside the multi-attribute feature education backgrounds. These features and attributes collectively form a unique feature profile within any population. Exploring all possible combinations of group assignments to maximise diversity is impractical. Example: Assigning 60 elements into groups of 6 yields over 50 million potential combinations. (<sub>n</sub>C<sub>r</sub> = 60 Choose 6 = 50,063,800 combinations)

In practice, a common approach is to randomly or pseudorandomly shuffle element into groups. However, such methods do not consistently maximise diversity. These stochastic methods sometimes yield lower diversity over multiple iterations. Moreover, random and pseudorandom techniques frequently produce groups with homogeneous features, thereby diminishing diversity. Similarly, sequential assignment encounters the same challenges.

### Proposed solution 
*Diverse-Assign* was developed to maximise diversity. By quantifying diversity as information gain, diversity can be maximised using constraint optimisation. This method aims to surpass the performance of pseudorandom shuffling. 

Constraint optimisation, also known as Constraint Programming (CP), are algorithms designed to meet specified constraints while optimising solutions. [(Heipcke, 1999)](#HEIPCKE)  *Diverse-Assign* employs a CP finite domain tree-search to achieve optimised solutions. This method utilises a swap-search technique to enforce the constraint that prohibits groups from containing homogeneous features. The search begins by provisionally assigning elements to groups. Through element exchanges between groups, diversity is enhanced while ensuring adherence to the constraint against homogeneity.

*Diverse-Assign* combines several algorithms to drive the swap-search optimisation. Swap-search is driven using "Unclosed AC3" algorithm, an adaptation of the widely employed AC3 algorithm in Constraint Satisfaction Problems (CSP). As the search progress, unclosed AC3 prunes solutions that fail to meet specified constraints, significantly streamlining solution exploration. Augmenting the search, simulated annealing is used to select swaps that maximise diversity. Sub-optimal diversity score plateaus are navigated using a random restart hill-climbing algorithm, which re-directs the programme to explore different search directions. For details on the algorithms, heuristic, and diversity measurement, see *Diverse-Assign’s* [technical abstract here.](https://github.com/joseph-liew/Diverse-Assign/tree/main/tech_abstract)

### Plateau detection heuristic
For *Diverse-Assign* to be efficient, a plateau detection heuristic is needed to navigate through sub-optimal diversity score plateaus. Inherent to hill climbing, there is a challenge to distinguish whether an optimisation plateau is an optimal solution convergence, or convergence at a sub-optimal plateau. This is explained in detail by [Norvig and Russell (2021)](#HILL). A plateau is formed when the current search direction converges on a local maximum score. Changing the direction or local search space might lead to an even higher local maximum. Ideally, the algorithm should converge on a global maximum plateau -- the highest plateau possible. 

Without a heuristic, the algorithm will not terminate upon maximum convergence, continuing indefinitely. Neither will the algorithm explore another direction upon hitting any plateau. A heuristic-less algorithm will assume any plateau as convergence on the optimal plateau.

### Evaluation goals 
The goal of this study to assess whether *Diverse-Assign* outperforms pseudorandom shuffling in maximise diversity, while mitigating the flaws in the latter approach. Additionally, we investigate the efficacy of the *Diverse-Assign’s* plateau detection heuristic to facilitate convergence on maximum diversity. Lastly, to support improvements, we analyse the performance of *Diverse-Assign’s* algorithm and heuristic components to look for areas for improvement.

## Method

### Dataset
Datasets were pseudorandomly generated using the software at ["generatedata.com"](https://github.com/benkeen/generatedata). Datasets simulated the assignment of a population of workshop participants into groups.

Two datasets were created to simulate two different population sizes; one twice the size of the other population: 
1) “1× population” with 61 participants
2) “2× population” with 122 participants

Each dataset had two columns of unique features and four columns of constant features. Unique features are features that had the same number of unique categories as number of participant (or dataset rows). Constant features are features with the same proportion of categories in both datasets. The number combinations of unique row combinations were doubled respectively in the two populations (1× population = 3,904; 2× population = 7,808). [(See Tables A and B)](#TABLES_AB) 

Datasets used in this study can be [downloaded from here](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/spreadsheets/pilot_study/sample_data).

<a name="TABLES_AB"></a>**Table A: Feature profile of 1× population dataset**
![Table A: Feature profile of 1× population dataset](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableA.PNG)

**Table B: Feature profile of 2× population dataset**
![Table B: Feature profile of 2× population dataset](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableB.PNG)

### Experiment design
To test algorithm performance on different data topologies, a 2 × 2 experiment design matrix was conducted. The matrix tests two different population sizes and counts of group to assign. [(See Table C.)](#TABLES_C) 

The count of groups tested were based on:
1) Assignment into groups of 12 to 13 participants (1× group count)
2) Assignment into groups of 6 to 7 participants (2× group count)

<a name="TABLES_C"></a>**Table C: Experiment design matrix**
![Table C: Experiment design matrix](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableC.PNG)

### Sample size
For all experiments, sample size was *(n) = 30*. A complete run of an algorithm constitutes a sample. Each run has 115 iteration steps or "iteration instances". An algorithm completes group assignments in each iteration instance. Depending on the algorithm, the assignments are either improved in the next iteration instance, or restart from scratch. Group diversity were measured in each iteration instance.

### Time measurement
Time taken by each algorithm was compared using the number of iteration instances taken. This enabled the comparison of different algorithms on the same time-points. Each iteration instance was numbered from 1 to 115 in ascending order, indicating the sequence of instances in a sample. 

### Algorithms
Algorithms and heuristic components tested were based on *Diverse-Assign* v.0.3.0a. A total of eight algorithms were tested (six test algorithms and their variants; plus two control algorithms). For control, pseudorandom shuffling and *Diverse-Assign’s* unclosed AC3 were used. [Refer to Table D to learn more about each algorithm's characteristics](#TABLE_D) The code and reference python packages used can be [found here](https://github.com/joseph-liew/Diverse-Assign/blob/main/Main-code/variants/DiverseAssignv0.3.0b.py). Reference python version was v.3.11.7.

<a name="TABLES_D"></a>**Table D: Algorithms tested and their characteristics.**
![Table D: Algorithms tested and their characteristics.](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableD.PNG)

The efficacy of the plateau detection heuristic was studied by comparing two variants of each test algorithm: (1) plateau-capped, and (2) no-capping. Comparisons were also performed between tests and controls. 

No-capping variants do not restart the search when a plateau is detected. The solution from every instance iteration is carried over to the next instance iteration for further search exploitation.

In contrast, plateau-capped variants stop carrying over the solution when a plateau was detected. In the next instance iteration, the algorithm restarts the search using a pseudorandom search starting point. 

Comparing capping variants supported two analyses: (1) Whether maximum convergence occurred at the first plateau. (2) Whether pushing beyond the initial plateau resulted in a convergence on a higher plateau.

### Testing constraint propagation
Pseudorandom search starting point was initialised by assigning groups through stratification. (E.g. elements 1 to 10 are assigned to 10 groups in order, from groups 1 to 10.) Then, groups assignments are pseudorandomly shuffled across the population. For algorithms that observe the constraint of no homogenous features, assignments were pseudorandomly shuffled until the constraint was satisfied. 

Test algorithms and the (control) unclosed AC3 all feature constraint propagation. These algorithms ensure that the constraint was satisfied during the search. On the other hand, the pseudorandom control does not have constraint propagation. Comparisons were conducted between tests and controls to compare the efficacy of the constraint satisfaction adherence.

### Statistics

#### Measurements 
Diversity of group assignments was measured using information entropy, using the grand sum of *Aggregated Diversity Score*, described in [Diverse-Assign (2024)] (#TECH). Diversity was measured before and after an instance iteration. 

"Baseline initial diversity" was defined as diversity score of assigning groups through stratification. Because the stratification method is constant for all algorithms, baseline initial diversity is constant across all algorithms using the same data topology.

Local maximums for each sample were identified from the diversity score. A local maximum was defined by criteria:
1)	Diversity score is the highest within a sequence of iteration instances. (A sequence is defined as beginning from the first iteration instance or from any pseudorandom restart point.) 
2)	Diversity score must be higher than the baseline initial diversity.
3)	Diversity score must be equal or higher to previous local maximum.

In this study, local diversity maximums are termed “maxima”. The largest maxima achieved was termed “maximum maxima”. To compare diversity score within and across algorithms, “delta maxima” was used. Delta maxima is the delta difference of a maxima diversity and a common baseline initial diversity. The largest delta maxima achieved was termed “maximum delta maxima”. 

A plateau was defined by *Diverse-Assign’s* heuristic. A plateau is defined as repeating the same maxima across a count equivalent to the number of groups. 

#### Comparisons tested
The following comparisons were conducted:

1) Detection of homogenous features in group assignment.
    - Validated whether the unclosed AC3 algorithm can ensure adherence to no-homogenous feature constraint.
2) Maximum delta maxima achieved at the earliest plateau.
    - Determined whether *Diverse-Assign* will converge on maximum maxima at the first plateau. 
3) Visualisation of delta maxima over time. 
    - Compared the rate of diversity gain between algorithms in a sample.	
4) Fastest algorithm. 
    - Compared the probability of an algorithm achieving maximum delta maxima at different time-points. 
5) Performance of algorithms across each data topology.
    - Average maximum delta maxima for each algorithm were compared using statistical tests to identify the best performer.

#### Statistical Analyses
All significance test used the rejection criterion α < 0.05. Normality was tested using the Shapiro-Wilk test (*(n) = 30 < 50*). Comparisons with non-normal distributions were compared using the Kruskal-Wallis (multiple independent samples) or Mann-Whitney U test (two independent samples). 95% confidence intervals for means were constructed using the *t*-distribution and the Standard Error of the Mean (SEM).

The probability rate for an algorithm to achieve max delta maxima at any time-point was estimated using the hazard rate (survival analysis). The hazard rate represents the relative probability for an algorithm to achieve max maxima, across different timepoints. Hazard rate was estimated using the Nelson-Aalen estimator. For the estimator, the observed event was defined as an algorithm reaching the first max delta maxima. Complete survival is achieved if an algorithm completes all 115 iteration instances without reaching any maxima.

The Jupyter notebook used to generate the statistical analyses can be [be accessed here](https://github.com/joseph-liew/Diverse-Assign/blob/main/studies/pilot_studyv030/pilot_stats_v030.ipynb). 

## Results

### Descriptive statistics of maximum delta maxima achieved by each algorithm
Table E shows summarises each algorithm’s maximum delta maxima. <a name="TABLES_E"></a>[(Table E can be downloaded from here.)](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/spreadsheets/pilot_study/Table_E.xlsx) The following results are presented in Table E: mean maximum delta maxima, quartiles, *t*-distribution SEM and 95% Confidence Interval (95% CI), and normality test.

### Detection of homogenous features in group assignment
[Table F](#TABLES_F) compares the proportion of solutions where a homogenous feature was present in at least one group. *Diverse-Assign* and all algorithms using the unclosed AC3 algorithm were effective in ensuring the no-homogenous features constraint satisfaction. None of these algorithms had any homogenous features present. Depending on data topology, *Diverse-Assign* outperformed pseudorandom control by as much as 74.7%.

Only the pseudorandom control had homogenous features present. Homogenous features were absent in the data topology “1x group count, 2x population size”. However, homogenous features were present in the other data topologies, ranging from 0.3% to 74.7% of solutions. Presence appeared to increase with the increase of either group count or population size.

<a name="TABLES_F"></a>**Table F: Comparison across algorithms: Proportion of solutions where a homogenous feature was present in at least one group.** Proportion is pooled across all samples.
![Table F: Comparison across algorithms: Proportion of solutions where a homogenous feature was present in at least one group](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableF.PNG)

### Maximum delta maxima achieved at the earliest plateau.
Among test algorithms, maximum delta maxima was not always achieved at the earliest plateau. The results support the importance of having a plateau detection heuristic and algorithm to search for a higher plateau. Depending on the algorithm and data topology, maximum convergence at the first plateau occurred between 3.3% to 50.0% of the time. [(Table F)](#TABLES_F) 

Maximum convergence at the first plateau appears to be less common with either the decrease in group count or population size. 

<a name="TABLES_G"></a>**Table G: Comparison across algorithms: Proportion of samples achieving maximum delta maxima at the first plateau.** Proportion is pooled across all samples.
![Table G: Comparison across algorithms: Proportion of samples achieving maximum delta maxima at the first plateau](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableG.PNG)

### Comparison between plateau-capped and no-capping variants 
[Table H](#TABLES_H) Table H compares the maximum delta maxima between variant counter-parts, matched for algorithm and data topology. Only one algorithm no-capping variant had a higher median measurement with a significantly different distribution. (SimAnneal with the data topology *2x group count, 1x population size*.) The other algorithms either had comparable distribution, or the plateau-capped variant had higher median with a significantly different distribution. 

For all variant pairs, at least one variant had non-parametric distribution. Hence, Mann-Whitney U test was used to test the difference in distribution. Due to the difference in distribution shapes, only statistical conclusion about the distribution difference could be made. No statistical inference about the medians could be made.

<a name="TABLES_H"></a>**Table H: Comparison of maximum delta maxima, between plateau-capped and no-capping variants** 
![Table H: Comparison of maximum delta maxima, between plateau-capped and no-capping variants](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableH.PNG)

To further analyse the performance of test algorithms, the best performing variants from each algorithm were shortlisted. The best variant were the variant with a higher median and statistically different distribution. Where the distributions were comparable, the plateau-capping variant was preferred. This was because plateau-capping theoretically could cover more search spaces, with a new pseudorandom search starting point. The comparison of mean and median max delta maxima of shortlisted variants found in [Table I](#TABLES_I) 

<a name="TABLES_I"></a>**Table I: Top algorithm variants selected for further study** 
![Table I: Top algorithm variants selected for further study](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableI.PNG)

### Visualisation of delta maxima over time. 
[Figure 1](#FIG_1) visualises the mean diversity gain for each of the shortlisted algorithms, and for each control. Test variants achieved maximum convergence, across all samples. The tight spread of data points suggests tests variants had low variance and highly reproducible delta maxima.

Only test variants showed maximum convergence. In test variants (blue, orange and green data points), mean delta maxima increase rapidly in the initial phase. The mean delta maxima then plateau-off at the maximum convergence with time. (Time = iteration instance). Generally, RandomRestart showed the fastest rate of diversity gain, followed by TwoHill and then SimAnneal.

<a name="#FIG_1"></a>**Figure 1: Top algorithm variants: Mean delta maxima achieved over time**. *((n) = 30)* 
![Figure 1: Top algorithm variants: Mean delta maxima achieved over time](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_fig1.PNG)

The graphs of the test controls also show that all three test algorithms could navigate through early diversity plateaus in the search. Note that the trend of diversity gain is tight with little variance. Despite having at least half of the delta maximum maxima occurring after the first plateau, [(reported in Table F)](#TABLES_F) test variants could achieve higher delta maxima, without creating a break in the trend of diversity gain. 

The results also suggested that another type of hill-climbing algorithm, stochastic hill-climbing, would not converge if it was tested. Note that pseudorandom control’s result [(Figure 1, purple data points)](#FIG_1) closely approximate stochastic hill-climbing.  This is because of the study criterion where diversity score is only a maxima if the score is equal or higher than the previous maxima. 

For pseudorandom control, the large spread of data points in Figure 1 also demonstrate that there was large variance in diversity among the algorithm sample. This is further supported by the SEM reported in [Table E](#TABLES_E). The SEM of pseudorandom controls ranged between 0.20× to 3.8× of the mean maximum maxima.

### Fastest algorithm
[Figure 2](#FIG_2) compares the probability of an algorithm achieving maximum delta maxima at different time-points. The comparison was estimated using the hazard rate for achieving maximum delta maxima. Notably, all test variants showed a similar hazard rate. The exception was RandomRestart, in *1x group count* data topologies, where the hazard of achieving maximum delta maxima was shorter by 1.4x to 5.7x, compared to other test variants.

<a name="#FIG_2"></a>**Figure 2: Top algorithm variants: Cumulative hazard rate for achieving maximum delta maxima.** *((n) = 30)*
![Figure 2: Top algorithm variants: Cumulative hazard rate for achieving maximum delta maxima](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_fig2.PNG)

### Performance of algorithms across each data topology.
Statistical comparison of average maximum delta diversity of the tested variants and control showed significant difference in distributions. This was true in all data topologies. [Table J](#TABLES_J) Kruskal-Wallis test for used because the test variant distributions were non-parametric. Histogram comparison of the distributions (not shown) also indicated that test variants and controls shared different distribution shapes. As such, statistical inference on the tested variants and controls was limited to distribution difference.

<a name="TABLES_J"></a>**Table J: Top variants: statistical comparison of average maximum delta diversity**  
![Table J: Top variants: statistical comparison of average maximum delta diversity](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableJ.PNG)

To further understand the performance of *Diverse-Assign’s*, post-hoc analyses were performed. [Table K](#TABLES_K) TwoHill plateau-capped performed well against teste variants and controls.

<a name="TABLES_K"></a>**Table K: Top variants: post-hoc analyses**  
![Table K: Top variants: post-hoc analyses](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_tableK.PNG)

Two-sided post-hoc analyses were conducted between TwoHill plateau-capped to each tested variant and control. TwoHill was selected because the algorithm contained all *Diverse-Assign’s* component algorithms and heuristic tested. Among tested variants, TwoHill plateau-capped performed well in half of the comparisons. Half of the post-hoc tests achieved comparable or significantly higher median compared to tested variants. (2 comparable medians, 2 significantly higher medians; total 4 out of 8 post-hoc comparisons.) Because tested variants have similar distribution shape, statistical inferences about the medians could be made.

Between TwoHill plateau-capped and controls, statistical inference was that the distributions were significantly different. This was due to the distinct difference in the non-parametric TwoHill plateau-capped and parametric control distributions. [Table K](#TABLES_K) However, we can extra-statistically infer that the median of TwoHill plateau-capped was practically higher than the control medians. 

In all data topologies, TwoHill plateau-capped’s entire distribution was high above both controls’ distributions. [Figure 3](#FIG_3) Furthermore, depending on data topology, TwoHill plateau-capped’s median was 3.1x to 15,900x higher than pseudorandom control [(Table K)](#TABLES_K). The largest difference in median was seen in the largest data topology *2x group count, 2x population size*. In this data topology, TwoHill plateau-capped had a smaller SEM to mean ratio, less than 0.5% of pseudorandom’s SEM to mean ratio. [(Table E)](#TABLES_E) The largest SEM to mean ratio for TwoHill plateau-capped was 0.01. Variance was almost negligible. This finding is coheres to the low data point spread seen in mean diversity gain plotted in [Figure 1](#FIG_1). 

Lastly, the results also demonstrate the poor performance of pseudorandom methods in maximising diversity. ([Table E](#TABLES_E) and [Figure 3](#FIG_3)) In data topology *2x group count, 2x population size*, delta diversity decreased beyond 0. The 25<sup>th</sup> percentile delta diversity was at -0.31.

<a name="#FIG_3"></a>**Figure 3: Top algorithm variants: violin plot comparisons**
![Figure 3: Top algorithm variants: violin plot comparisons](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/pilot_study/pilot_v030_fig3.PNG)

## Discussion
The results indicated that *Diverse-Assign* v.0.30 greatly outperformed pseudorandom shuffling in all tested data topologies. Depending on data topology, could achieve a higher maximum delta diversity by 15,900x. Also, *Diverse-Assign's* assignments were reproducible. *Diverse-Assign* converged on the maximum delta diversity with high reproducibility and negligible SEM. Last but not least, *Diverse-Assign* avoided the formation of groups with homogenous features, a key flaw of pseudorandom and sequential assignment methods.

*Diverse-Assign's* combination of several components was designed to support a broad range of data topologies. This is to avoid limiting its application by over-specialisation to a narrow range. The results also showed that the number of algorithms included were not extraneous. In half of the post-hoc tests, *Diverse-Assign* performed the same or better than just using one of the component algorithm. The plateau detection heuristic also enabled to *Diverse-Assign* to navigate beyond sub-optimal plateaus. 

The findings indicated that in some data topologies, using random restart hill-climbing without simulated annealing could improve the probability rate of maximum delta maxima convergence by up to 5.7×. While somewhat stochastic, random restart has been shown to be very effective in problems where the number of alternative solutions are small. This leads to a high average probability of picking the most optimum solution in a small number of iterations. [(Norvig and Russell, 2021)](#HILL)  

### Limitations and future improvements 

The limitation of this study was the range of data topology tested. While a range of topology was tested, testing over wider range of data topologies might yield more findings. Another limitation was we could not confirm that the maximum delta diversity covers the global maximum.  Future tests can explore the use of smaller data topologies with known global maximums. Together with mathematical modelling, results could be extrapolated to a wide range of topologies. With additional testing, more areas for improvement can be identified.

An area for improvement is *Diverse-Assign’s* heuristic to switch to different optimisation algorithms. Our findings show that different algorithms perform better in certain topologies. Enhancing this heuristic to match the heuristic to topology will greatly shorten the processing time. 

In *Diverse-Assign*v.0.3.0, there is a heuristic not tested in this study. This heuristic determines whether to relax the constraint that all groups must not have homogenous features. It activates upon detection very skewed datasets, where an attribute is overly dominant in the population. Attribute over-dominance render the strict constraint impossible. Testing this heuristic and induction through mathematical modelling might discover more areas for enhancement.

## Conclusion
Data show that *Diverse-Assign* definitively outperforms pseudorandom assignment in maximising diversity, while avoiding homogenous features. *Diverse-Assign’s* results were also reproducible, with little variance. To support enhancements, additional testing and study are recommended.

# References
<a name="HILL"></a>Norvig, P., Russell, S. (2021). Local Search and Optimization Problems In: Artificial Intelligence. A Modern Approach. 4th US Edition. Prentice Hall
<a name=”TECH”></a> Diverse-Assign.(2024) https://github.com/joseph-liew/Diverse-Assign/tree/main/tech_abstract
<a name="HEIPCKE"></a> Heipcke, S. (1999). Comparing Constraint Programming and Mathematical Programming Approaches to Discrete Optimisation-The Change Problem. The Journal of the Operational Research Society, 50(6), 581–595. https://doi.org/10.2307/3010615
