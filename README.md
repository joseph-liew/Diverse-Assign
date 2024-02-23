# **Diverse-Assign**

Version 1.0.0. February 2024

Licence: Open-source [*GNU GPL Version 3*](https://github.com/joseph-liew/Diverse-Assign/blob/main/LICENSE)

## Intro
**Diverse-Assign** is an AI tool to effortlessly create highly diverse groups, leveraging on [evidence-backed algorithms](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study). Increase diversity by up to 15,900x effortlessly. Just input a table of your participant/item profiles and let AI handle the rest. No more filtering and sorting for hours. **Diverse-Assign** can group anything – people, items, shopping carts… If there’s a profile, it can group it.  

Links:
  - [*Windows and Mac download*](https://github.com/joseph-liew/Diverse-Assign/releases)
      - For non-technical users. Download the app version. No coding and installation required.    
  - [*Python script download*](https://github.com/joseph-liew/Diverse-Assign/releases)
  - [*Manual*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Manual)
      - How-to-use guide.
  - [*UI deatures.*](https://github.com/joseph-liew/Diverse-Assign/tree/main/UI-features)
      - Highlights on the UI design.
  - [*Code*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Code) 
      - Code repository.
  - [*Sample data*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Sample-data)
      - Link to download sample data. Includes sample input and output data. 
  - [*Pilot study*](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study)
      - Evidence and tests of **Diverse-Assign’s** effectiveness.
  - [*Technical Paper*](https://github.com/joseph-liew/Diverse-Assign/blob/main/tech_abstract/README.md)
      - Interested in the computer science? Check out the technical paper. Explanation, pseudocode, designs and heuristics can be found here.


## Features
- Intuitive to use. Self-guided, text-driven UI. Download and run the app.
- Or, run the python script, if you prefer.
- Simple to use. Just put the profile of your participants/ items in a CSV file. The AI will do the rest.
- Input checks. Typed something wrong? No worries. The programme will check and guide you on the correct input.
- Assignment progress indicator
- Estimated assignment completion time

<a name="use"></a> 
## Use cases 
- Assigning participants/students of different backgrounds into breakouts/classes. 
- Creating diverse groups for ice-breaking activities.
- Objective and impartial assignment of people / items into groups.
- Assigning experiments in A/B experiments to different customer segments.
- Assigning compounds in combinatorial chemistry and pharmaceutical interaction experiments.
- Homogenous admixture of multiple dependent variables for multi-factor experiments.
- Other uses: The programme is ordinal/nominal value agnostic. It assigns anything into diverse groups. 

## Inspiration
**Diverse-Assign** was inspired by a frequent challenge in education. When designing workshops/classrooms, educators/teachers often assign participants/students into groups by hand. This is tedious, especially when there are many profile features to compare.

Ever used a random tool to randomise groups? These aren’t the best at giving us the mix we're after. We often see groups that look too similar. And then we have to moving rows of spreadsheet by hand. **Diverse-Assign** is [proven](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study) to be more effective than randomisation. Up to 15,900x better. Load your file, let it run, get highly diverse groupings. No more hours of staring at the screen.

Objectivity is another concern. When we start to pick by hand, how do we stay objective? For e.g.:
- If we can't have equal representation of genders and education levels in each group, which group should have equal gender representation? 
- Which group should have equal education level representation? 
- Or should we somehow spread-out gender and education?
- If so, how much spreading is enough?

## Automatically assign objectively 
**Diverse-Assign** solves the subjective problem by objectively measuring the diversity of your people/item profile. It uses a [scoring system](https://github.com/joseph-liew/Diverse-Assign/blob/main/tech_abstract/README.md#ads) to measure the uniqueness of each profile and how common they are. **Diverse-Assign** then assigns them into groups, ensuring every profile is as different as possible.

Diversity is especially important in today’s world. By improving the diversity of our groups, we promote diverse interactions and understanding among participants. A small step in making the world more inclusive. 

## Collaborations are welcome!

Code is open-source, GPL-3. Anyone is free to improve the programme or adapt the software in other / their projects, subject to GPL-3 licence. 

Feel free to collab and contribute!

Corrections to documentation or code are greatly appreciated :)

### Future work 

- Enhance heuristics.
- Develop weights to modulate the importance of select features or attributes.
- Refactor code into OOP for easier maintenance.
