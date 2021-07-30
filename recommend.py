import json
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_pickle('model\\30\\df.pkl')

with open('model\\30\\cosine_similarities.pkl', 'rb') as f:
    similarity = pickle.load(f)

with open('model\\30\\restaurant_cuisines.pkl', 'rb') as f:
    restaurant_cuisines = pickle.load(f)


def recommend_similar(name, similarity_matrix=similarity, df=df, location=''):
    # List to put top 10 restaurants
    recommend_restaurant = []

    indices = pd.Series(df.index)

    # Find the index of the hotel entered
    idx = indices[indices == name].index[0]

    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(
        similarity_matrix[idx]).sort_values(ascending=False)

    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)

    # Names of the top 30 restaurants
    for each in top30_indexes:
        recommend_restaurant.append(list(df.index)[each])

    # Creating the new data set to show similar restaurants
    recommendation_df = pd.DataFrame(
        columns=['cuisines', 'Mean Rating', 'cost'])

    # Create the top 30 similar restaurants with some of their columns
    for each in recommend_restaurant:
        recommendation_df = recommendation_df.append(pd.DataFrame(
            df[['cuisines', 'rest_type', 'Mean Rating', 'cost', 'location']][df.index == each].sample()))

    recommendation_df.index.name = 'name'
    recommendation_df.reset_index(inplace=True)

    recommendation_df = recommendation_df.drop_duplicates(
        subset=['name', 'Mean Rating', 'location', 'cost'])

    recommendation_df = recommendation_df.sort_values(
        by='Mean Rating', ascending=False).head(10)
    recommendation_df.reset_index(drop=True, inplace=True)

    return recommendation_df.to_json(orient='index')

# def recommend_cuisine(cuisine_list):
#     return '{"0":"Jalsa"}'


def sim_with_all(user_cuisines, cuisine_list, restaurant_cuisines):
    test_list = [0 for i in range(len(cuisine_list))]
    for i in user_cuisines:
        test_list[cuisine_list.index(i)] = 1

    cosine_sim = cosine_similarity(
        np.array(restaurant_cuisines), np.array([test_list]))

    sim_list = []
    for j in range(len(cosine_sim)):
        sim_list.append(float(cosine_sim[j][0]))

    sim_list = list(enumerate(sim_list))
    sim_list.sort(key=lambda x: x[1], reverse=True)
    return sim_list


def recommend_cuisine(user_cuisines, restaurant_cuisines=restaurant_cuisines, df=df, location=''):
    cuisine_list = list(restaurant_cuisines.columns)
    sim_list = sim_with_all(user_cuisines, cuisine_list, restaurant_cuisines)

    recommendation = []
    for x in sim_list[0:31]:
        recommendation.append(x[0])

    recommendation_df = df.iloc[recommendation, :].copy()
    recommendation_df.drop(['online_order', 'book_table',
                           'rate', 'reviews_list', 'city'], axis=1, inplace=True)

    recommendation_df.index.name = 'name'
    recommendation_df.reset_index(inplace=True)

    recommendation_df = recommendation_df.loc[recommendation_df.astype(
        str).drop_duplicates(subset=['name', 'Mean Rating', 'cost'], keep=False).index]

    recommendation_df = recommendation_df.sort_values(
        by='Mean Rating', ascending=False).head(10)
    recommendation_df.reset_index(drop=True, inplace=True)

    return recommendation_df.to_json(orient='index')


if __name__ == "__main__":
    recommendation = recommend_similar('Mast Kalandar')
    # recommendation = recommend_cuisine(['North Indian'])
    print(recommendation)
