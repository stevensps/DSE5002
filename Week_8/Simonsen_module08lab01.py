# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:01:43 2024

@author: steve
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import chain

#1
credits_df = pd.read_csv('Week_8/Data/Netflix/credits.csv')
titles_df = pd.read_csv('Week_8/Data/Netflix/titles.csv')

#Print # of unique genres
#Convert output of titles['genres'].unique() to a list
#Iterate over list
#replace the following characters: []'
#split the individual strings to list items and flatten the list using chain()
genres=titles_df['genres']
genre_list = [str(g).replace("[","").replace("]","").replace("'","").replace(",","") for g in genres]

flattened_genres = list(chain(*[g.split() for g in genre_list]))


unique_genres = set(flattened_genres)

print(len(unique_genres))

#2
#Print release year nad imdb score of highest average score of all movies by year
#aggregate the means by year
#convert pandas series to df
#set index as a column (release year)
#Find the numerical index with the highest average imdb score
titles_df_cleaned = titles_df.dropna(subset=['imdb_score'])

agg_mean_year = titles_df_cleaned.groupby(['release_year']).agg(
    mean_score=('imdb_score', np.mean))

highest_scoring_year=max(agg_mean_year['mean_score'].items(), key=lambda item: item[1])

print(highest_scoring_year)

#3
#There were 208 actors in the movie with the most credited actors. 
#What is the title of that movie? Nulls and NaN values do not count. 
#left join credits to titles
#drop na
#group by movie titles
#count actors and find max

lfjoin_titles_credits = credits_df.merge(titles_df, how='inner', on='id' )

lfjoin_titles_credits = lfjoin_titles_credits.dropna(subset=['name'])

most_actors = lfjoin_titles_credits.groupby('title')['name'].count()

most_actors.sort_values(ascending=False, na_position='first')

#4
#slice rows to filter for robert only
#sort desc by scores
#create plot
rd_scores = lfjoin_titles_credits[
    lfjoin_titles_credits["name"] =='Robert De Niro']

rd_scores_sorted = rd_scores.sort_values(by=['imdb_score'], ascending=False)

rd_score_plot=sns.kdeplot(data=rd_scores, x="imdb_score")
rd_score_plot.set_title('Robert De Niro IMDB Scores')
plt.show

#5
#Create two new boolean columns
#true when the description contains war or gangster.
#Call these columns war_movies and gangster_movies
#How many movies are there in both categories? 
# Which category has a higher average IMDB score?
#Show the IMDB score kernel density estimations of both categories

titles_df['war_movies'] = titles_df['description'].str.contains('war')
titles_df['gangster_movies']=titles_df['description'].str.contains('gangster')

count_war = titles_df['war_movies'].sum()
count_gangster = titles_df['gangster_movies'].sum()

imdb_war = titles_df.groupby('war_movies').agg(
    avg_imdb_score=('imdb_score', np.mean))

imdb_gangster = titles_df.groupby('gangster_movies').agg(
    avg_imdb_score=('imdb_score', 'mean'))
#War Movies
war_plot = sns.kdeplot(data=imdb_war, x='avg_imdb_score')
war_plot.set_title('Distribution of Average IMDb Scores for War Movies')
plt.show()


#Gangster Movies
gangster_plot=sns.kdeplot(data=imdb_gangster, x='avg_imdb_score')
gangster_plot.set_title('Distribution of Average IMDb Scores for Gangster Movies')
plt.show()







    

        



