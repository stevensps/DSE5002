# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:05:37 2024

@author: steve
"""

import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt

#Import the Data
col_df = pd.read_csv("Week_8/Project/cost_of_living.csv")
#Note: pip install openpyxl required to resolve errror
country_codes_df = pd.read_excel("Week_8/Project/country_codes.xlsx")
salaries_df = pd.read_csv("Week_8/Project/ds_salaries.csv")
salary_detail_df = pd.read_csv("Week_8/Project/Levels_Fyi_Salary_Data.csv")



#Initial Data Cleansing
"""
-col file - split "City" into 3 columns - City, State (if applies), and Country
-separate by comma
"""
col_df[['City','Country']] = col_df['City'].str.rsplit(',',n=1,expand=True)

    #Need second str.rsplit to account for states/provinces
col_df[['City','State or Province']] = col_df['City'].str.rsplit(',',n=1,expand=True)

    #Reorder dataframe
col_df = col_df[['Rank','City','State or Province','Country','Cost of Living Index','Rent Index',
                 'Cost of Living Plus Rent Index','Groceries Index',
                 'Restaurant Price Index','Local Purchasing Power Index']]


"""
levels_fyi (salary detail) column
-Perform similar split to separate city from state from country
-Will need to add United States into data set if only two columns
"""
#separate city and state through split
salary_detail_df[['city','state or province']] = salary_detail_df['location'].str.split(',',n=1,expand=True)

#separate state from country with second rsplit
salary_detail_df[['state or province','country']] = salary_detail_df['state or province'].str.rsplit(',',n=1,expand=True)

#mask variables used as temp variable for reordering dataframe as done below
mask1 = salary_detail_df.pop('city')
salary_detail_df.insert(6, mask1.name, mask1)

mask2 = salary_detail_df.pop('state or province')
salary_detail_df.insert(7, mask2.name, mask2)

mask3=salary_detail_df.pop('country')
salary_detail_df.insert(8, mask3.name, mask3)

#strip white space for easier reading and maintain data cleanliness
salary_detail_df['city']=salary_detail_df['city'].str.strip()
salary_detail_df['state or province']=salary_detail_df['state or province'].str.strip()
salary_detail_df['country']=salary_detail_df['country'].str.strip()

#print head to show dataframe
print(salary_detail_df.iloc[:, :5])


"""
Salaries file
-rename first column to id
"""
salaries_df.rename(columns={'Unnamed: 0':'index'}, inplace=True)
print(salaries_df.iloc[:, :5])

"""
#Build Currency Converter - NO LONGER NEEDED
def convert_currency(amount, from_currency, to_currency):
    base_url = "https://api.exchangerate-api.com/v4/latest/"

    # Fetch latest exchange rates
    response = requests.get(base_url + from_currency)
    data = response.json()

    if 'rates' in data:
        rates = data['rates']
        if from_currency == to_currency:
            return amount

        if from_currency in rates and to_currency in rates:
            conversion_rate = rates[to_currency] / rates[from_currency]
            converted_amount = amount * conversion_rate
            return converted_amount
        else:
            raise ValueError("Invalid currency!")
    else:
        raise ValueError("Unable to fetch exchange rates!")
        """
        
        
#Joins
"""
1) Join ds_salaries to country codes to get two digit country code in table
2) join levels fyi to country codes to get two digit country code
3) join two tables above to get salary in levels fyi in USD 
"""

    #1
#Create new column in salaries_df to create common join field





"""
Not sure if I even need this

#Rename country to Country in salary detail to match country codes for common join field
salary_detail_df.rename(columns={'country':'Country'}, inplace=True)

salary_detail_df.loc[salary_detail_df['Country'] == 'None', 'Country'] = 'United States of America (the)'

left_saldet_codes = salary_detail_df.merge(country_codes_df, how='left', on='Country')

#Join two tables together
left_saldet_dsal = left_saldet_codes.merge(left_dsal_codes, how='left', on='Alpha-2 code')
"""

#ds_salaries manipulation

"""
1) group by country, find mean, median, standard deviation
"""

"""
#May not need this
sum_sal_stats = left_dsal_codes.groupby(['work_year']).agg(
    mean_salary_usd=('salary_in_usd', np.mean),
    median_salary_usd=('salary_in_usd', np.median),
    std_salary_usd = ('salary_in_usd', np.std)
    )

#May not need this
sum_sal_stats_experience = left_dsal_codes.groupby(['experience_level']).agg(
    mean_salary_usd=('salary_in_usd', np.mean),
    median_salary_usd=('salary_in_usd', np.median),
    std_salary_usd = ('salary_in_usd', np.std)
    )
"""
#join col_df to country codes
col_df['Country']=col_df['Country'].str.strip()
col_df['Country']=col_df['Country'].str.replace('United States','United States of America (the)')
left_col_codes = col_df.merge(country_codes_df, how='left', on='Country')



#NEED THIS
#create new column in salary detail for alpha code
salaries_df['Alpha-2 code'] = salaries_df['employee_residence'].str.split(',',n=1,expand=True)

#create join from salary detail to country code
left_dsal_codes = salaries_df.merge(country_codes_df, how='left', on='Alpha-2 code')

#group by table above to get mean, median, standard deviation
sum_sal_stats_country = left_dsal_codes.groupby(['Country','Alpha-2 code']).agg(
    mean_salary_usd=('salary_in_usd', np.mean),
    median_salary_usd=('salary_in_usd', np.median),
    std_salary_usd = ('salary_in_usd', np.std)
    )

#det_sal_stats_country = salary_detail_df.groupby([''])


#Join to cost_of_Living to summary statistics grouped table above
left_col_sumstats = left_col_codes.merge(sum_sal_stats_country, how='left', on='Alpha-2 code')

#Add columnn that takes mean of sumstats index ratings
left_col_sumstats['Average Index Rating']=left_col_sumstats.iloc[:, 4:10].mean(axis=1)

#Divide mean_salary_usd by mean index ratings - Call this column salary_score
left_col_sumstats['salary_score']=left_col_sumstats['mean_salary_usd'] / left_col_sumstats['Average Index Rating']

#populate rank based on salary_score
left_col_sumstats['Rank'] = (left_col_sumstats['salary_score']
                 .rank(method='dense', ascending=False)
                )

#group summary stats by country to get avg. salary score by country
left_col_sumstats_grouped = left_col_sumstats.groupby(['Country']).agg(
    average_salary_score=('salary_score', np.mean))

#left_col_sumstats_grouped_city = left_col_sumstats.groupby(['Rank','City','Country']).agg(
    #average_salary_score=('salary_score', np.mean))

#top 5 countries with city included to plot based on salary score for countries
top_5_by_city = left_col_sumstats[left_col_sumstats['Country'].isin(
    ['Malaysia', 'Algeria', 'Iraq', 'Puerto Rico', 'Bulgaria'])]


#Salary Detail - Filter to top 5 countries in detail dataset to examine top 5 country in additional viz below
top_5_det = salary_detail_df[salary_detail_df['country'].isin(
    ['Malaysia', 'Algeria', 'Iraq', 'Puerto Rico', 'Bulgaria'])]

#top_5_by_gender = top_5_by_gender_det.dropna(subset=['gender'])

#Group salary detail by title to show and count most common jobs available
title_counts = top_5_det.groupby(['country', 'title']).size().reset_index(name='counts')



#Visuals
#
top_5_countries = left_col_sumstats_grouped.nlargest(5, 'average_salary_score')

sns.barplot(x='average_salary_score', y='Country', data=top_5_countries)
plt.xlabel('Salary Score')
plt.ylabel('Country')
plt.title('Top 5 Countries by Salary Score')
plt.show()

#Citites in top 5
sns.set_theme(style="whitegrid", palette="muted")

ax = sns.swarmplot(data=top_5_by_city, x="salary_score", y="Country", hue="City")
ax.set(ylabel="Country")
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="City")
plt.title("Average Salary Scores by City and Country")
plt.show()

#Title Counts in Detail Dataset
plt.figure(figsize=(10, 6))
sns.barplot(x='country', y='counts', hue='title', data=title_counts)

plt.title('Count of Each Title by Country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.show()


"""
As can be seen in the visuals above, the five top countries where salary would go the farthest
in USD are as follows (1=salary goes the furthest):
1) Malaysia
2) Algeria
3) Iraq
4) Puerto Rico
5) Bulgaria


To produce this list, I took an average of all indexes in the cost of living file across the columns.
Then, I pulled in the mean salary by country based on the ds_salaries file in USD.
Finally, I created a salary_score by dividing the mean salary for the country by the
average quality of life index. Taking the average again across country,
I was able to find the top 5 countries where salary would go the farthest in USD.


I was then able to provide some additional visuals around cities and types of jobs.
As can be seen within the graphs, there is a large gap in salary_score between
the top cities in Malaysia vs the bottom cities in Bulgaria. Even though they're both
in the top 5, I imagine life to be pretty different between these two places based on the
variance of the salary score.

In the third graph derived from the salary detail file, software developers 
seem to have the best chance across the board of landing a position in one of these countries. 
However, if given the chance, I would like to explore this data further to gather more information, 
as Algeria is not included in the detail salary dataset.
"""
















