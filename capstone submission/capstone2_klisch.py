# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 14:18:37 2018

@author: cherylK
"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

species=pd.read_csv('species_info.csv')
#print species.head()


# "How many different species are in the `species` DataFrame?" 5541
num_species=species.scientific_name.nunique()
print num_species

#"What are the different values of `category` in `species`?"
#Amphibian                    [Amphibian]
#Bird                              [Bird]
#Fish                              [Fish]
#Mammal                          [Mammal]
#Nonvascular Plant    [Nonvascular Plant]
#Reptile                        [Reptile]
#Vascular Plant          [Vascular Plant]
category=species.groupby('category').category.unique()
print category

#    "What are the different values of `conservation_status`?"
#Endangered                    [Endangered]
#In Recovery                  [In Recovery]
#Species of Concern    [Species of Concern]
#Threatened                    [Threatened]
conservation=species.groupby('conservation_status').conservation_status.unique()
print conservation

# "The column `conservation_status` has several possible values:\n",
#    "- `Species of Concern`: declining or appear to be in need of conservation\n",
#    "- `Threatened`: vulnerable to endangerment in the near future\n",
#    "- `Endangered`: seriously at risk of extinction\n",
#    "- `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range\n",
#    "\n",
#    "We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria."
#0          Endangered               16
#1         In Recovery                4
#2  Species of Concern              161
#3          Threatened               10
name_counts = species.groupby('conservation_status').scientific_name.count().reset_index()
print name_counts

#"As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.\n",
#    "\n",
#    "Paste the following code and run it to see replace `None` with `No Intervention`:\n",
#    "```python\n",
#    "species.fillna('No Intervention', inplace=True)\n",
#    "```"

species.fillna('No Intervention', inplace=True)

 #   "Great! Now run the same `groupby` as before to see how many species require `No Protection`." 5633
name_counts = species.groupby('conservation_status').scientific_name.count().reset_index()
print name_counts

#"Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.\n",
 #   "\n",
 #   "Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:\n",
 #   "```python\n",
 #   "protection_counts = species.groupby('conservation_status')\\\n",
#    "    .scientific_name.count().reset_index()\\\n",
#    "    .sort_values(by='scientific_name')\n",
#    "```"

protection_counts = species.groupby('conservation_status').scientific_name.count().reset_index().sort_values(by='scientific_name')

#"Now let's create a bar chart!\n",
#   "1. Start by creating a wide figure with `figsize=(10, 4)`\n",
#    "1. Start by creating an axes object called `ax` using `plt.subplot`.\n",
#    "2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.\n",
#    "3. Create an x-tick for each of the bars.\n",
#    "4. Label each x-tick with the label from `conservation_status` in `protection_counts`\n",
#    "5. Label the y-axis `Number of Species`\n",
#    "6. Title the graph `Conservation Status by Species`\n",
#    "7. Plot the grap using `plt.show()`"


plt.figure(figsize=(10,4))
ax=plt.subplot()
y = protection_counts.scientific_name.values
N = len(y)
x = range(N)

plt.bar(x, y)
ax.set_xticks(range(len(y)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.xlabel('Conservation Status')
plt.title('Conservation Status by Species')

plt.show()  

# "Are certain types of species more likely to be endangered?"
# "Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise."
species['is_protected'] = species.apply(lambda x:
                                    'True'
                                    if x['conservation_status'] != 'No Intervention'
                                    else 'False',
                                    axis=1)
print species.head(10)

#"Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`."
category_counts=species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()
print category_counts

#"It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:\n",
#    "- `columns` is `conservation_status`\n",
#    "- `index` is `category`\n",
#    "- `values` is `scientific_name`\n",
#    "\n",
#    "Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end."
#df.pivot(columns='ColumnToPivot',
#         index='ColumnToBeRows',
#         values='ColumnToBeValues')

category_pivot=category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
print category_pivot

#"Use the `.columns` property to  rename the categories `True` and `False` to something more description:\n",
#    "- Leave `category` as `category`\n",
#    "- Rename `False` to `not_protected`\n",
#    "- Rename `True` to `protected`"

category_pivot.rename(columns={'False': 'not_protected'}, inplace=True)
category_pivot.rename(columns={'True': 'protected'}, inplace=True)
print category_pivot

#"Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species 
#that are protected) divided by `protected` plus `not_protected` (the total number of species)."

category_pivot['percent_protected']=(category_pivot.protected/(category_pivot.protected+category_pivot.not_protected))
print category_pivot


#"It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, 
#consider the following questions:\n",
#    "- Is the data numerical or categorical?\n", categorical
#    "- How many pieces of data are you comparing?" more than 2

#"Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:\n",
#    "\n",
#    "||protected|not protected|\n",
#    "|-|-|-|\n",
#    "|Mammal|?|?|\n",
#    "|Bird|?|?|\n",
#    "\n",
#    "Create a table called `contingency` and fill it in with the correct numbers"

from scipy.stats import chi2_contingency

# Contingency table
#         not_protected|  protected
# ----+------------------+------------
# Amphibian | 72       |  7
# Bird      | 413      |  75
# Fish      | 115      |  11
# Mammal    | 146      |  30
# Nonvasc   | 328      |  5
# Reptile   | 73       |  5
# Vascular  | 4216     |  46

X = [[72, 7.],
    [413, 75.],
    [115, 11.],
    [146, 30.],
    [328, 5.],
    [73, 5.],
    [4216, 46.]]
    
contingency= [[146, 30],
              [413, 5]]
chi2, pval, dof, expected = chi2_contingency(contingency)
print pval


#   "It looks like this difference isn't significant!\n",
#    "\n",
#    "Let's test another.  Is the difference between `Reptile` and `Mammal` significant?" Yes because pvalue is less than .05 (.038356)

contingency2 = [[73, 5.],
    [146, 30.]]
chi2, pval, dof, expected = chi2_contingency(contingency2)
print pval

#between amphibian and fish
contingency3= [[72, 7.],
               [115, 11.]]
chi2, pval, dof, expected = chi2_contingency(contingency3)
print pval
         
#between nonvascular and vascular plants
contingency4= [[328, 5.],
               [4216, 46.]]
               
chi2, pval, dof, expected = chi2_contingency(contingency4)
print pval

   
#  "Conservationists have been recording sightings of different species at several national parks for the past 7 days.  
#  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data."

observations=pd.read_csv('observations.csv')
print observations.head()

# "Some scientists are studying the number of sheep sightings at different national parks.  
#There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  
#Notice that the following code will tell us whether or not a word occurs in a string:"
# "# Does \"Sheep\" occur in this string?\n",
#    "str1 = 'This string contains Sheep'\n",
#    "'Sheep' in str1"

#"# Does \"Sheep\" occur in this string?\n",
#    "str2 = 'This string contains Cows'\n",
#    "'Sheep' in str2"

str1 = 'This string contains Sheep'

str2 = 'This string contains Cows'

# "Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise."

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
print species.head(10)

#"Select the rows of `species` where `is_sheep` is `True` and examine the results."

print species[species.is_sheep]

# "Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`."

sheep_species=species[(species.is_sheep) & (species.category == 'Mammal')]

# "Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`."
sheep_observations = pd.merge(sheep_species, observations)
print sheep_observations

#"How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.\n",
#    "\n",
#    "This is the total number of sheep observed in each park over the past 7 days." 

obs_by_park=sheep_observations.groupby('park_name').observations.sum().reset_index()
print obs_by_park

# "Create a bar chart showing the different number of observations per week at each park.\n",
#   "\n",
#    "1. Start by creating a wide figure with `figsize=(16, 4)`\n",
#    "1. Start by creating an axes object called `ax` using `plt.subplot`.\n",
#    "2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.\n",
#    "3. Create an x-tick for each of the bars.\n",
#    "4. Label each x-tick with the label from `park_name` in `obs_by_park`\n",
#    "5. Label the y-axis `Number of Observations`\n",
#    "6. Title the graph `Observations of Sheep per Week`\n",
#    "7. Plot the grap using `plt.show()`"

plt.figure(figsize=(16,4))
ax=plt.subplot()
y = obs_by_park.observations.values
N = len(y)
x = range(N)

plt.bar(x, y)
ax.set_xticks(range(len(y)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.xlabel('Park Name')
plt.title('Observations of Sheep per Week')

plt.show()  

# "Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National 
# Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  
# They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, 
# they'd like to be able to know this, with confidence.\n",
#    "\n",
#    "Use the sample size calculator at <a href=\"https://www.optimizely.com/sample-size-calculator/\">Optimizely</a> to 
#    calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).\n",
#    "\n",
#    "Remember that \"Minimum Detectable Effect\" is a percent of the baseline."
#   ]

#sample size is 520

# "How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  2.08
bryce=520/250.
print bryce

#  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?" 1.02
yellowstone=520/507.
print yellowstone

yosemite=520/282.
print yosemite

smoky=520/149
print smoky



