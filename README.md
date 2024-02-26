# **Diverse-Assign**
Licence: Open-source [*GNU GPL Version 3*](https://github.com/joseph-liew/Diverse-Assign/blob/main/LICENSE)

## Intro
**Diverse-Assign** is an AI tool to effortlessly create highly diverse groups, leveraging on [evidence-backed algorithms](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study). Effortlessly increase your group diversity by up to 15,900x. No more filtering and sorting for hours. **Diverse-Assign** can group anything and any feature – people, items, shopping carts, diet preferences… If there’s a profile, it can group it.  

*Just prepare a CSV of your participant/item profiles. Let AI handle the rest.* Below is an example. You can use anything for the features!
![Just load a table of your participant/item profiles. Let AI handle the rest](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/sample_input.PNG)

Links:
  - [*Windows and Mac download*](https://github.com/joseph-liew/Diverse-Assign/releases)
      - For non-technical users. Download the app version. No coding and installation required.    
  - [*Python script download*](https://github.com/joseph-liew/Diverse-Assign/releases)
  - [*Manual*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Manual)
      - How-to-use guide.
  - [*Code*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Code) 
      - Code repository and version history.
  - [*Sample data*](https://github.com/joseph-liew/Diverse-Assign/tree/main/Sample-data)
      - Link to download sample data. Includes sample input and output data. 
  - [*Pilot study*](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study)
      - Evidence and tests of **Diverse-Assign’s** effectiveness.
  - [*Technical Paper*](https://github.com/joseph-liew/Diverse-Assign/blob/main/tech_abstract/README.md)
      - Interested in the computer science? Check out the technical paper. Explanation, pseudocode, designs and heuristics can be found here.


## Features
- Create diverse group assignments, powered by AI.
- Intuitive to use. Self-guided, text-driven UI. Download and run the app.
- Or, run the python script, if you prefer.
- Just put the profile of your participants/ items in a CSV file. The AI will do the rest.
- Simple to use. Follow the on-screen prompts.
  
  *E.g. of a prompt*

  ![E.g. of a prompt](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/other_prompt.png)
- Input checks. Typed something wrong? No worries. The app will guide you on what to correct.
  
  *Guided input correction*

  ![Guided input correction](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/validation.png)
- Job progress indicators and time left to complete.
  
  *Default job progress view*

  ![Default job progress view](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/default_job_progress.PNG)
- For advanced users: comprehensive details on progreess.
  
  *Advanced job progress view*

  ![Advanced job progress view](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/advanced_job_progress.PNG)


<a name="use"></a> 
## Other use cases 
- Assigning participants/students of different backgrounds into breakouts/classes. 
- Creating diverse groups for ice-breaking activities.
- Objective and impartial assignment of people / items into groups.
- Assigning experiments in A/B experiments to different customer segments.
- Assigning compounds in combinatorial chemistry and pharmaceutical interaction experiments.
- Homogenous admixture of multiple dependent variables for multi-factor experiments.
- Other uses: The app is ordinal/nominal value agnostic. It assigns anything into diverse groups. 

## How does it work?
- The AI uses a scoring system to measure the diversity.
- The [scoring system](https://github.com/joseph-liew/Diverse-Assign/blob/main/tech_abstract/README.md#ads) measures diversity based on the uniqueness of each profile feature and how common the features are.
- The AI then assigns the groups. It will ensure that the person/item profile in each group is as different as possible.
- The AI can intelligently assign groups, even if every person/item has the same feature. E.g. "Everyone likes fish." The AI will split everyone based on other features you have given. 

## Does my data go online? Does it connect to the Internet?
No. The app doesn't connect to the Internet. It completely runs on your computer only. 

## Inspiration
**Diverse-Assign** was inspired by a frequent challenge in education. When designing workshops/classrooms, educators/teachers often assign participants/students into groups by hand. This is tedious, especially when there are many profile features to compare.

Ever used a random tool to randomise groups? These aren’t the best at giving us the mix we're after. We often see groups that look too similar. And then we have to moving rows of spreadsheet by hand. **Diverse-Assign** is [proven](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study) to be more effective than randomisation. Up to 15,900x better. Load your file, let it run, get highly diverse groupings. No more hours of staring at the screen.

Objectivity is another concern. When we start to pick by hand, how do we stay objective? For e.g.:
- If we can't have equal representation of genders and education levels in each group, which group should have equal gender representation? 
- Which group should have equal education level representation? 
- Or should we somehow spread-out gender and education?
- If so, how much to spread?

## Objective method to assign groups  
**Diverse-Assign** solves the subjective problem by objectively measuring the diversity of the people/item profile. It uses a [scoring system](https://github.com/joseph-liew/Diverse-Assign/blob/main/tech_abstract/README.md#ads) to measure the number of unique profile features and how common they are.

Diversity is especially important in today’s world. By improving the diversity of our groups, we promote diverse interactions and understanding among participants. A small step in making the world more inclusive. 

## Collaborations are welcome!

Code is open-source, GPL-3. Anyone is free to improve the app or adapt the software in other / their projects, subject to GPL-3 licence. 

Feel free to collab and contribute!

Corrections to documentation or code are greatly appreciated :)

Please contact us:  
  - GitHub: https://github.com/joseph-liew/Diverse-Assign/issues
  - Email: josephgzliew@gmail.com

### Future work 

- Enhance heuristics.
- Develop weights to modulate the importance of select features or attributes.
- Refactor code into OOP for easier maintenance.
