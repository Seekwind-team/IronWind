import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from yellowbrick.text import FreqDistVisualizer

class Recommender:
    df = None
    corrMatrix = None

    def __init__(self):
        self.update()

    def update(self):
        self.df = pd.read_csv ('matching2.csv')
        allUserRatings = self.df.pivot_table(index=['userID'],columns=['jobID'],values='like')
        self.corrMatrix = allUserRatings.corr(method="pearson")

    def evaluate(self,jobID,rating):
        
        similar_ratings = self.corrMatrix[jobID]*(rating)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings
    
    def get_rated_jobs(self, user_id):
        rated_jobs = self.df[self.df["userID"] == user_id]
        ratings = []
        for index, row in rated_jobs.iterrows():
            tmp = [row["jobID"],row["like"]]
            ratings.append(tmp)
        #print("Ratings of user: ", user_id)
        #print(ratings)
        return ratings

    def recommend(self, user_id):
        recommended_jobs = pd.DataFrame()
        userRatings = self.get_rated_jobs(user_id)
        #User didnt rate any jobs yet
        if len(userRatings) == 0:
            print("Random Job")
            
        #User already rated jobs
        else:
            #print(userRatings)
            for jobid, rating in userRatings:
                recommended_jobs = recommended_jobs.append(self.evaluate(jobid, rating), ignore_index = True)

        recommended_jobs = recommended_jobs.sum().sort_values(ascending=False)
        print(recommended_jobs[:10])
        recommended_jobs = list(recommended_jobs.index)
        #Remove jobs from list, that were already rated by User
        #for jobid, rating in userRatings:
            #if rating == 1:
                #print("ID = ", jobid)
                #recommended_jobs.remove(jobid)
        
        top10 = recommended_jobs[:10]
        return top10
        #return recommended_jobs
