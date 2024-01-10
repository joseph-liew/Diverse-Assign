# **Diverse-Assigner**

Version 0.2.2a. January 2024
Licence: Open-source[*GNU GPL Version 3*](https://www.gnu.org/licenses/gpl-3.0.html)
Copyright: Joseph Liew (Liew Guangzhi Joseph)

## Manual and Code ##
Links to:
- [*Manual.*](XXXXX) How-to-use guide.
- [*UI-features.*](XXXXX) Documentation of intuitive UI design features.
- [*Compiling-notes.*](XXXXX) Quick note before you compile.
- [*Main-code.*](XXXXX) Ready to use in any IDE, notebook, command line, or compiled into an executable. 
- [*Debug-code.*](XXXXX) Debug-code is identical to the main-code. But with additional lines added to trace important steps. Useful for debugging or understanding how the main-code works.

## Abstract ##
**Diverse-Assigner** is a programme designed to assign members/items into groups, with maximum diversity. In other words, each group will have the maximum diversity possible. The programme UI aims to be intuitive and accessible.

**Ready to Use. Ready to Compile. Intuitive UI**
- Self-guided, text-driven UI. Easily used in any IDE, notebook or command line.
- Accessible features include input: validity checks, assignment progress indicator, estimated assignment completion time.
- Programme can be immediately compiled into an executable, as is. This can make the software accessbile with no-code experience.
- Our aim is anyone who know what is a CSV files to understand the software intuitively. 
- *Forthcoming:* Installable executable to be available on GitHub.

**Software Engineering Features** 
**Diverse-Assigner** is different from traditional AI approach. This yields several advantages.
- Traditional approach uses Constraint-Satisfaction-Problem (CSP) algorithms.
- Unlike traditional approach, problem is simplified into a maximum value problem. 
- Our approach: Simulated Annealing, driven by a production-reduction-approach inspired by MAC (Maintaining Arc Consistency) algorithim in CSP. (See [*Algorithm*](#algo) for more info.)
- Ordinal/Nominal agnostic: Avoiding CSP, we avoid challenge of dealing with mixtures of ordinal/nominal data types.
- Other use cases: Ordinal/Nominal agnostic means the programme can be easily used to assign anything into diverse groups. For example, grouping agents in combinatorial interaction studties.
- Simpler implementation makes it easy to adapt the software to support intuitive UI designs.
- Efficiency and optimisation might also be better than CSP approach (Needs study to ascertain.) 

Also, the simple implementation has potential to introduce weighted-values. Weighted-values can be used to improve representation of minority groups. Unlike CSP optimisation problem, the solution is relatively easy to fine-tune to *N* number of features.

**Objective Solution** 
**Diverse-Assigner** saves the headache and time of making groups diverse by hand. 
- It's also mentally tedious to assess diversity by sight.
- Assigning by hand is also subjective. If we want the maximum diversity, should a group have balanced genders or balanced education level?
- Diversity is objectively measured, using an *Aggregate Diversity Score*. The score is derived from the *Shannon-Weaver Index* (See [*Aggregate Diversity Score*](#ADS) and [*Shannon & Weaver, 1949*](#SW).)    

**Diverse-Assigner** also overcomes the problem of random shuffling. However: 
- Unlike random shuffling, **Diverse-Assigner** is less likely to create groups with clusters of similar profiles.
- The use of Simulated Annealing helps minimises local-maximums, increasing our likelihood of getting the most diverse grouping possible.

When used to assign people with different backgrounds, we promote diverse interactions and understanding. A small step in making the world more inclusive. 

There are other possible use cases. It's particularly useful in:
- Assigning agents in experiments studying combinatorial interactions.
- Approximating homogenous admixture of items into groups.
(See [*Use Cases*](#use) for more info.)

##<a name="use"></a> Use Cases ##
- Assigning participants/students of different backgrounds into breakouts/classes. 
- Creating diverse groups for ice-breaking activities.
- Objective and impartial assigment of people / items into groups.
- Assigning experimnents in A/B experiments to different customer segments.
- Assigning compounds in combinatorial chemisty and pharmaceutical interaction experiments.
- Homogenous admixture of multiple dependent variables for multi-factor experiments.
- Other uses: Programme is ordinal/nominal agnostic. It can be easily used to assign anything into diverse groups. 

## Inspiration ##
**Diverse-Assigner** was inspired by a frequent challenge in education. When designing workshops/classrooms, educators/teachers often assign participants/students into groups by hand. This is tedious, especially if the participant/student profile has many features.

Objectivity is another concern. For e.g.:
- If we can't have equal genders and education in each group, which group should have equal gender? 
- Which should have equal education? 
- Or should we unbalanced admixture of gender education?
- If so, how much?

This is mentally tedious. Furthermore, as a CSP optimisation implemenation, this is very challenging to implement and optimise to cover *N* number of profile features.

##<a name="ADS"></a> Aggregate Diversity Score##

The Shannon-Weaver index is a measure in information theory. It is used to quantify the diversity of information in a dataset. [*Shannon & Weaver, 1949*](#SW) It has also been coopted as a diversity measure in ecology and population genetic studies 

The measure is defined as:
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msup>
    <mi>H</mi>
    <mo>&#x2032;</mo>
  </msup>
  <mo>=</mo>
  <mo>&#x2212;<!-- − --></mo>
  <munderover>
    <mo movablelimits="false">&#x2211;<!-- ∑ --></mo>
    <mrow class="MJX-TeXAtom-ORD">
      <mi>x</mi>
      <mo>=</mo>
      <mn>1</mn>
    </mrow>
    <mi>S</mi>
  </munderover>
  <msub>
    <mi>p</mi>
    <mi>x</mi>
  </msub>
  <mi>ln</mi>
  <mo>&#x2061;<!-- ⁡ --></mo>
  <msub>
    <mi>p</mi>
    <mi>i</mi>
  </msub>
</math>

where *H′* is the Shannon-Weaver index, *x* are values sharing a common value, *p<sub>x</sub>* is the proportion of *x* values in the sample, and *ln p<sub>x</sub>* is the natural logarithm of this proportion. This yeilds a positive score. The greater score, the higher greater the diversity in a sample.

In this programme, we propose an *Aggregate Diversity Score* to measure whether a group has, in aggregate, a more diverse profile of features. Aggregate Diversity Score is adapted from the Shannon-Weaver index.

A group of values can be represented as a table. We can determine the diversity of each column (each column is a profile feature), using the Shannon-Weaver index. Each column is a sample; each value in the column could be any unique *x* value. 

By taking the aggregate Shannon-Weaver index of all columns in a group, we obtain the *Aggregate Diversity Score* for that group. A group with greater a Aggregate Diversity Score is more diverse than another group with a lower score.

The Aggregate Diversity Score serves as a convenient value measure to assign groups using maximum-value algorithm. Importantly, we can try different group assignments, and take the grand sum of Aggregate Diversity Score across groups. Each solution of group assignments yields a different grand sum. The optimal solution is where grand sum is the global maximum.

##<a name="algo"></a> Algorithm ##

1. First, assign all rows in the data evenly into groups.
2. Split the data into groups (pandas dataframe subsets).   
3. Determine the [*Aggregate Diversity Score* ](#ADS) of each group.
4. Generate a deque queue of shuffled row indices to swap. 
5. Initialise a collection to store swapped rows indices.
6. For each *i* row in the data, popleft the deque to obtain a pointer row.
7. If the rows iteration is complete, or the deque is empty, end the 'For' loop. Solution is obtained.
8. Check whether the pointer row is in the collection of swapped indices. If no, continue to swap. Else skip this row, since it's already swapped.
9. If the pointer row value is different from the row, swap the values. Else popleft and append the pointer to the end of the deque. (So that this pointer can be eventually used for another row.)
10. Using Simulated Annealing, accept the swap if swap yeilds a greater total diversity, or based on the annealing probaility, reject the swap.
11. If a swap is rejected, reverse the swaps and pops and appends. I.e. revert data to before the swap.
12. Else, transfer the row index and pointer index in this iteration to the collection of swapped row indices.
13. Continue iterations of each row, until 'For' loop breaks at step 7.

In step 10, memoisation is used to minimise duplicate calculation of Aggregate Diversity Scores for groups that are not invovled in the swapping. Memoisation is also employed in other areas of the programme to conserve memory and time (steps 6 to 12). 

In step 10, Simulated Annealing is used to reduce the likelihood of ending up with a local minimum. This is crucial, since maximum-value approach is not a complete solution. However, depending on the user's use case, a complete assignment is usually unnecessary. Unless the user is works with a very large number of rows or features. In such scenarios, the user might be satisfied with tweaking the cooling rate for the Simulated Annealing, balancing the needs time and completeness.

Steps 4 to 13 (excluding 10) is designed to reduce the problem and complexity size with every iteration. It is inspired MAC (Maintaining Arc Consistency) algorithim in CSP. While the overall algorithm is not CSP, the problem is reduced with each iteration.

Because the solution is not compelte, there is a step 14:

14. Repeat steps 1 to 13 over *k* instances. Pick the highest scoring instance as solution. Users can input the value for *k*. (At the expense of time.)

This is to further minimise the chance of getting stuck on a local maximum. 

## Limitations ##
- As a non-CSP approach, users cannot introduce CSPs, such as "Every group must have at least one person from R&D."
- However, it is possible to adapt the code to increase the weight of certain columns. This is useful to increase representation of minority groups.

- While current implementation maximises input, the solution is not complete. I.e. it's possible to get stuck on a local minimum.
- Potentially, the "MAC-like" problem reduction could be swapped with a two-agent adverserial search, to obtain a complete solution. (I.e. definite global maximum.)

- As the number of rows or features increases, processing time can increase significantly.
- This could be addressed by tweaking the Simulated Annealinmg  cooling rate and the number of instances to create. (At the cost of increased likelihood of getting stucked at a local maximium.)

## Collaboration ##
Code is open-source, GPL-3. Anyone is free to improve the programme or adapt the software in other / their projects, subject to GPL-3 licence. 

Feel free to collab and contribute!

Corrections to documetation or code are greatly appreciated :)

## Future Work ##
- Installable executable to be available on GitHub.
- Improve efficiency by mimimising list generation through memoisation.
- Refactor code into OOP for easier maintenance.
- Branch project into a less verbose UI and reduced options. While more options are great for technical users, these can be easily tweaked in the code. Non-technical users may find the programme more accessible if some options are invisble defaults.

## References ##
<a name="SW"></a>Shannon, C. E., and Weaver, W., 1949. The Mathematical Theory of Communication. Urbana: University of Illinois Press.
[*Article extract*](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
