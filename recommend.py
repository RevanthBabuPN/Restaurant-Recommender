import json
import numpy as np
import pandas as pd
import pickle

df = pd.read_pickle('model\\df.pkl')

with open('model\\cosine_similarities.pkl', 'rb') as f:
    similarity = pickle.load(f)

def recommend_similar(name, similarity_matrix = similarity, df = df, location=''):
    # List to put top 10 restaurants
    recommend_restaurant = []

    indices = pd.Series(df.index)
    
    # Find the index of the hotel entered
    idx = indices[indices == name].index[0]

    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(similarity_matrix[idx]).sort_values(ascending=False)
    
    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)
    
    # Names of the top 30 restaurants
    for each in top30_indexes:
        recommend_restaurant.append(list(df.index)[each])
    
    # Creating the new data set to show similar restaurants
    recommendation_df = pd.DataFrame(columns=['cuisines', 'Mean Rating', 'cost'])
    
    # Create the top 30 similar restaurants with some of their columns
    for each in recommend_restaurant:
        recommendation_df = recommendation_df.append(pd.DataFrame(df[['cuisines','rest_type','Mean Rating', 'cost','location']][df.index == each].sample()))
    
    recommendation_df.index.name = 'name'
    recommendation_df.reset_index(inplace = True)

    recommendation_df = recommendation_df.drop_duplicates(subset = ['name','Mean Rating','location','cost'])
    # Please uncomment the following 5 lines to get distance from customer location
#     l_l = []    
#     for l in recommendation_df.location:
#         l_l.append(Get_distance(l,location))
#     recommendation_df.insert(2, "Distance(km)",l_l, True) 
#     recommendation_df = recommendation_df[recommendation_df['Distance(km)'] < 20]

    recommendation_df = recommendation_df.sort_values(by='Mean Rating', ascending=False).head(10)
    recommendation_df.reset_index(drop=True, inplace=True)
    
    return recommendation_df.to_json(orient = 'index')

def recommend_cuisine(cuisine_list):
    return '{"0":"Jalsa"}'

if __name__ == "__main__":
    recommendation = recommend_similar('Jalsa', similarity, df, 'BTM Layout')
    print(recommendation)
