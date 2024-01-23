# **Diverse-Assign**

Version 0.2.3a. January 2024

Licence: Open-source [*GNU GPL Version 3*](https://github.com/joseph-liew/Diverse-Assign/blob/main/LICENSE)

## Manual and Code ##

Links to:
- [*Manual.*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Manual)
> How-to-use guide.

- [*UI-features. COMING SOON*](XXXXX)
> Documentation of intuitive UI design features.

- [*Compiling-notes. COMING SOON*](XXXXX)
> Quick note before you compile.

- [*Main-code.*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Main-code) 
> Ready to use in any IDE, notebook, command line, or compiled into an executable. 

- [*Debug-code.*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Debug-code)
>  Debug-code is identical to the main-code. But with additional lines added to trace important steps. Useful for debugging or understanding how the main-code works.

- [*Sample-data.*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Sample-data)
>  Folder for sample data. Include sample working data, and output data, for validation. ('Output data' = an example of what is produced after the programme assigns groups to the sample working data.) 

## Abstract ##

**Diverse-Assign** is a programme designed to maximise diversity in assigning members/items into groups. In other words, we aim to achieve high diversity among groups. The programme UI also aims to be intuitive and accessible.

### Ready to Use. Ready to Compile. Intuitive UI ### 
- Self-guided, text-driven UI. Easily used in any IDE, notebook or command line.
- Accessible features include input: validity checks, assignment progress indicator, estimated assignment completion time.
- Programme can be immediately compiled into an executable, as is. This can make the software accessible with no-code experience.
- Our aim is anyone who know what is a CSV file to use the software intuitively. 
- *Forthcoming:* Installable executable to be available on GitHub.

<a name="use"></a> 
### Use Cases ### 
- Assigning participants/students of different backgrounds into breakouts/classes. 
- Creating diverse groups for ice-breaking activities.
- Objective and impartial assignment of people / items into groups.
- Assigning experiments in A/B experiments to different customer segments.
- Assigning compounds in combinatorial chemistry and pharmaceutical interaction experiments.
- Homogenous admixture of multiple dependent variables for multi-factor experiments.
- Other uses: Programme is ordinal/nominal value agnostic. It can be easily used to assign anything into diverse groups. 

### Inspiration ###
**Diverse-Assign** was inspired by a frequent challenge in education. When designing workshops/classrooms, educators/teachers often assign participants/students into groups by hand. This is tedious, especially if the participant/student profile has many features.

Objectivity is another concern. For e.g.:
- If we can't have equal representation of genders and education levels in each group, which group should have equal gender representation? 
- Which should have equal education level representation? 
- Or should we unbalanced admixture of gender education?
- If so, how much?

This is mentally tedious. Furthermore, when we try to use CSP optimisation implementation, this is very challenging to implement and optimise. How should we write a CSP algorithm to cover *N* number of profile features.


## Software Engineering Features ## 

**Diverse-Assign** is different from the conventional AI approach used in group assignment. This yields several advantages.
- Traditional approach uses Constraint-Satisfaction-Problem (CSP) algorithms.
- Unlike traditional approach, the problem is simplified into maximum value problem. 
- Our approach: Simulated Annealing, driven by a production reduction and heuristics inspired by MAC (Maintaining Arc Consistency) algorithm in CSP. (See [*Algorithm*](#algo) and [*Heuristics*](#heu) for more info.)
- Ordinal/Nominal agnostic: Avoiding CSP, we avoid challenge of dealing with mixtures of ordinal/nominal data types.
- Other use cases: Ordinal/Nominal value agnostic means the programme can be easily used to assign anything into diverse groups. For example, grouping agents in combinatorial interaction studies. (See [*Use Cases*](#use).)    
- Simpler implementation makes it easy to adapt the software to support intuitive UI designs.
- Efficiency and optimisation might also be better than CSP approach (Needs study to ascertain.) 

Also, the simple implementation makes the code amenable to introducing weighted-values. Weighted-values can be used to improve representation of minority groups. Unlike CSP optimisation algorithm, the programme is relatively easy to scale fine-tune to any *N* number of features.

## Objective Solution ##

**Diverse-Assign** saves the headache and time of making groups diverse by hand. 
- It's also mentally tedious to assess diversity by sight.
- Assigning by hand is also subjective. If we want the maximum diversity, should a group have balanced representation of genders or education levels?
- Diversity is objectively measured, using an *Aggregate Diversity Score*. The score is derived from the *Shannon-Weaver index* (See [*Aggregate Diversity Score*](#ADS) and [*Shannon & Weaver, 1949*](#SW).)    

**Diverse-Assign** also overcomes the problem of random shuffling.  
- Unlike random shuffling, **Diverse-Assign** is less likely to create groups with clusters of similar profiles.
- The use of Simulated Annealing minimises the likelihood of getting trapped at the local maximum diversity.

When used to assign people with different backgrounds, we promote diverse interactions and understanding. A small step in making the world more inclusive. 

There are other use cases. It's particularly useful in:
- Assigning agents in experiments studying combinatorial interactions.
- Approximating homogenous admixture of items into groups.
(See [*Use Cases*](#use) for more info.)


<a name="ADS"></a> 
## Aggregate Diversity Score ##

In information theory, the Shannon-Weaver index is a measure of entropy. It is used to quantify the entropy of information within a dataset. ([*Shannon & Weaver, 1949*](#SW)) The index has also been coopted into diversity measure of groups in ecology and population genetic studies. 

The measure is defined as:

$$
\ H^{\prime} = -\sum_{n=1}^{n} \left(p_{\mathrm{x}}^{*} \ln p_{\mathrm{x}}\right) \
$$

> where *H′* is the Shannon-Weaver index, *x* are values sharing a common value, *p<sub>x</sub>* is the proportion of *x* values in the sample, and *ln p<sub>x</sub>* is the natural logarithm of this proportion. 

This index yields a positive score. The greater score, the higher greater the diversity in a sample.

In this programme, we propose an *Aggregate Diversity Score* to measure whether a group has, in aggregate, a more diverse profile of features. Aggregate Diversity Score is adapted from the Shannon-Weaver index.

A group of values can be represented as a table. We can determine the diversity of each column (each column is a profile feature), using the Shannon-Weaver index. Each column is a sample; each value in the column could be any unique *x* value. 

By taking the aggregate Shannon-Weaver index of all columns in a group, we obtain the *Aggregate Diversity Score* for that group. A group with greater Aggregate Diversity Score is more diverse than another group with a lower score.

The Aggregate Diversity Score serves as a convenient value measure to assign groups using maximum-value algorithm. Importantly, we can try different group assignments, and take the grand sum of Aggregate Diversity Score across groups. Each solution of group assignments yields a different grand sum. The optimal solution is where grand sum is the global maximum.

<a name="algo"></a>
## Algorithm ##

1. First, assign all rows in the data evenly into groups.
2. Split the data into groups (pandas dataframe subsets).   
3. Determine the [*Aggregate Diversity Score* ](#ADS) of each group.
4. Generate a deque queue of shuffled row indices to swap. 
5. Initialise a set to store swapped rows indices. (Hash)
6. For each *i* row in the data, popleft the deque to obtain a pointer's value.
7. While there is no new swap:
> 7a. If the rows iteration is complete, or the deque is empty, end the 'For' loop. Solution is obtained.
> 
> 7b. Else, check whether the pointer's value is in the collection of swapped indices.
> 
> 7c. If no, continue to swap. Else skip this row, since it's already swapped.
> 
> 7d. If the pointer's value is different from the *i* row, proceed. Else, skip to the next *i*th row. Move the pointer's value to the deque end (Prevent self-swapping and row-swapping within same group.)
> 
> 7e. Using Simulated Annealing, if swap yields a greater total diversity, accept swap. Break the 'while' loop.
>
> 7f. Or based on the *annealing probability*, pick the next element in the deque as the new pointer. Revert the swap. Move the old pointer's value to the deque end. (The deque end will eventually be cycled to the front.) Break the 'while' loop.

8. Continue iterations of each row, until 'for' loop ends.
9. Repeat steps 1 to 8 over *M* instances. Pick the highest scoring instance as solution. 

In steps 7e to 7f, Simulated Annealing is used to reduce the likelihood of ending up with a local maximum. This is crucial, since maximum-value approach is not a complete solution. Global maximum might not be achieved before the solution is complete. However, depending on the user's use case, a complete assignment is usually unnecessary. This is especially important, because exhaustive search is not trivial. For a cohort of 60 people, splitting into 10 groups means there are more than 75 billion solutions. In step 9, the search space is limited to *M* instances (or *M* solutions).  

Steps 4 to 8 (excluding steps 7e and 7f) is designed to reduce the problem size with every iteration. It is inspired by the MAC (Maintaining Arc Consistency) algorithm in CSP. While the overall algorithm is not CSP, the problem size is reduced with each iteration. 

To further reduce the size of the problem, rate of the problem reduction is determined by [*heuristics*](#heu).

<a name="heu"></a>
## Heuristics ##

### Search Heuristic ###
In Simulated Annealing, the reduction rate is determined by the cooling rate.

In thermodynamics, the original formula used to describe annealing is:

$$
P = e^{-\frac{\Delta E}{k \ \cdot \ T}} \
$$

> where *P* is the probability that the energy will increase by delta E, *delta E* is change in energy (new energy - previous energy), *k* is the Boltzmann Constant (1.380649 × 10<sup>−23</sup> joule per kelvin), *T* is temperature. 

For the programme, we modified the original thermodynamics equation and combined both geometric reduction and linear reduction rules. Reduction rules are important in simulated annealing, because they promote exploration early in the search, and exploitation later in the search. In exploration, the goal is to increase the likelihood of landing near global maximum, through a more agressive probability of accepting an alternative solution. After exploration comes exploitation, where the probabilty of accepting an alternative solution is weakened, converging the solution towards the maximum.

In the programme, the probability of accepting a neigbour solution (*P*) was modified to be more aggressive at the start. The aggression is reduced as the problem size (number of elements unassigned into groups) reduces over the assignment iterations:

$$
P = e \ ^{\frac{\Delta E}{k \ \cdot \ cooling \ rate}} \
$$

Note that *delta E* was modififed to become a positive value. This agggressive modifier is controlled by the geometrical reduction rule *cooling rate*:

$$
cooling \ rate = T \cdot problem \ size
$$

> where *T* is temperature. 

During development, a small sample study showed that geometrical reduction was vital in escaping local maximums. This is crucial in cases where clustering of similar features can happen due to over-dominance of features. For example, in assigning project groups among multi-discipline students, autocorrelation of features are common. E.g. a computing project may have more computer science students than informatics students.

*problem size* is determined from the linear reduction rule:

$$
problem \ size = \frac{(total \ number \ of \ elements \ - \ number \ of \ elements \ assigned \ into \ groups)}{total \ number \ of \ elements}
$$

Thus, through the linear reduction, the annealing schedule is coupled to the iterative "MAC-like" problem reduction. The aim of this coupling is to avoid over-exploration and over-exploitation.

### Search Space Capping ###
Regardless of the search heuristic, the problem size (or search space) has to be further reduced. Splitting 60 people into 10 groups means there are more than 75 billion solutions. (<sub>n</sub>C<sub>r</sub> = '60 Choose 10')

The programme caps the solutions to ***(<sub>n</sub>C<sub>2</sub>*** instances. The rationale is the algorithm does pair-wise swapping. Hence, the optimal solution should be within ***(<sub>n</sub>C<sub>2</sub>***. This ignores that sequence of possible swaps are randomly generated and non-exhaustive. It also ignores alternative solutions generated during annealing is probable. 

Hence, the actual optimal solution might be _near_ ***(<sub>n</sub>C<sub>2</sub>*** number of instances generated. This was also seen in small sample experiments. However, the programme still uses ***(<sub>n</sub>C<sub>2</sub>*** as a relaxed heuristic. Depending on the use case, the difference between the best solution picked by the programme and the most diverse assignments could be acceptable to users. Computing a more accurate heuristic has diminishing returns. Currently, ***(<sub>n</sub>C<sub>2</sub>*** is preferred. given it is computationally light, and easy to scale to any *N* number of features. 

## Limitations ##

- As a non-CSP approach, users cannot introduce CSPs, such as "Every group must have at least one person from R&D."
> However, it is possible to adapt the code to increase the weight of certain columns. This is useful for increasing the representation of minority groups.

- While current implementation maximises value, the solution is not complete. And this could mean we do not arrive at the global maximum. I.e. it's possible to get stuck on a local maximum.
> Potentially, the "MAC-like" problem reduction could be replaced with a two-agent adversarial search. This might create a complete solution, by pruning suboptimal solutions. (I.e. we are sure the global maximum was achieved.)

- As the number of rows or features increases, processing time can increase significantly.
> This could be addressed by tweaking the Simulated Annealing cooling rate and the number of instances to create. (At the cost of increased likelihood of getting stuck at a local maximum.)

## Collaboration ##

Code is open-source, GPL-3. Anyone is free to improve the programme or adapt the software in other / their projects, subject to GPL-3 licence. 

Feel free to collab and contribute!

Corrections to documentation or code are greatly appreciated :)

## Future Work ##

- Further experiment and improve heuristics. 
- Installable executable to be available on GitHub.
- ~~Improve efficiency by minimising list generation through memoisation.~~ *Done*
- Refactor code into OOP for easier maintenance.
- Branch project into a less verbose UI and reduced options. While more options are great for technical users, these can be easily tweaked in the code. Non-technical users may find the programme more accessible if some options are invisible defaults.

## References ##

<a name="SW"></a>Shannon, C. E., and Weaver, W., 1949. The Mathematical Theory of Communication. Urbana: University of Illinois Press.
[*Article extract*](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

