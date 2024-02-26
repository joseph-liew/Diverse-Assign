**==========================**

**Diverse-Assign v.1.0.1a** 

**================February 2024**

# HOW TO USE THE APP

<br>

## Steps:

=========

1) The input file of what to assign must be a CSV file. The file must have the profile features must be arranged with features in the columns. The people/items to assign must be in rows.

    *E.g. of an input file. The people to assign in the groups and the profile features are in columns.*

    ![E.g. of an input file. The people to assign in the groups and the profile features are in columns.](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/sample_input.PNG)

<br>

2) Save the CSV file to the same folder as this app (“DiverseAssign_v1.0.1a”).

<br>

3) Open the app “DiverseAssign_v1.0.1a”

<br>

4) Follow the on-screen instructions and answer the prompts.

    *E.g. of a prompt*

    ![E.g. of a prompt](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/other_prompt.png)

<br>

5) The app will ask to select [Default] or [Advanced] job progress view. Choose [Default] to see the time remaining. Select [Advanced] for more comprehensive progress information.

    *Select [Default] or [Advanced] job progress view*

    ![Select [Default] or [Advanced] job progress view](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/job_progress_options.PNG)

<br>

6) Done!

<br>

The app adds one column to the end (“right”) of the CSV file. The column is “assigned_group”. This column indicates the assigned groups. The groups are numbered from 1 to the number of groups you wanted. E.g. If you wanted 10 groups, the rows are assigned ‘1’ to ‘10’.

<br>

*E.g. of a completed group assignment. The app has added the yellow column on the right of the CSV. These are the group assignments.*

![E.g. of a completed group assignment. The app has added the yellow column on the right of the CSV. These are the group assignments.](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/added_columns.png)

You can also try out the below demo.

<br>

## DEMO: 

=========

The below demo is a demo of creating 20 groups. It uses a demo input file: "sample_input.csv"
 
1) Copy and paste the sample file “sample_input.csv” from the “samples” folder to the same folder as the app.

2) Run the app. Set the number of groups to 20.

3)	Follow the on-screen instructions.

4) When the app has finished assigning, it will ask for a file name to save to. 

5) Input a a file name and save.

In this demo, the app will inform you the diversity score is 151.136. 

<br>

## FAQ: 

=========

**Q: What's the difference between [Default] and [Advanced] job progress view?**

<br>

**A:** 

  - [Default] basic progress updates such as % completed and time left.

    
    *Default job progress view*

    ![Default job progress view](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/default_job_progress.PNG)
    
  - [Advanced] provides same info as default, and additional details such as:
      - Diversity score for each optimisation iteration.
      - Trace how the assignments are generated and optimised.
  
    *Advanced job progress view*

    ![Advanced job progress view](https://github.com/joseph-liew/Diverse-Assign/blob/main/site/images/advanced_job_progress.PNG)

<br>

**Q: What's the [Advanced] job progress view used for?**

<br>

**A:**

  - Advanced users who want to trace how the assignments are generated and optimised.
  
  - Advanced users who want to understand how the AI works.
  
  - Users who are familiar with hill-climbing algorithm can see info on the number of solutions generated, which solution has been done well, whether plateaus are formed, and which solution is selected for further optimisation.
  
  - To know more about the algoritm, see the Technical Abstract at: https://github.com/joseph-liew/Diverse-Assign/tree/main/tech_abstract

<br>

**Q: When I run the app repeatedly, why are the group assignments for each person/item different for each time? I'm using the same inputs.**

<br>

**A:**

  - Usually, there are more than one group combination that can achieve the highest diversity.

  - E.g.
      - There are 3 oranges and 3 apples in total.
      - Group A has 2 oranges and 1 apple.
      - Group B as 1 oranges and 2 apples.
        
  - The total diversity is the same as:
      - Group A has 1 orange and 2 apples.
      - Group B as 2 oranges and 1 apple.

<br>

**Q: Why is the diversity score sometimes slightly different? I'm repeating group assignments using the same inputs.**

<br>

**A:**

  - These rarely happens. **Diverse-Assign** is designed to give a difference +/- 1%. 
  
  - We can improve the accuracy and precision, but this will increase the amount of time needed to finish the group assignments. Some users might not need the accuracy/precision and find it takes too much time.
    
  - If you'd like a more accurate and precise system, please contact us. We are improving the app through users feedback. We are exploring to enable users to control accuracy and precision settings. We'd love to hear from you how to make it easy to use.
    
  - GitHub: https://github.com/joseph-liew/Diverse-Assign/issues
    
  - Email: josephgzliew@gmail.com

<br>
<br>

Spot any errors? 
Want to collaborate? Please contact us:  
  - GitHub: https://github.com/joseph-liew/Diverse-Assign/issues
  - Email: josephgzliew@gmail.com

<br>

To learn more about the algorithms, see the Technical Abstract at: https://github.com/joseph-liew/Diverse-Assign/tree/main/tech_abstract

Sample input data was generated using "generatedata.com". Credits to the team at https://github.com/benkeen/generatedata for creating this magnificent mock data generator.
