import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from joboffer.models import JobOffer

class Recommender:

    df = None
    corrMatrix = None
    alljobs = None
    id2index = {}
    index2id = {}
    cosine_sim = None

    def __init__(self):
        self.update()

    def print_alljobs(self):
        print(self.alljobs)

    def update(self):
        self.df = pd.read_csv ('matching2.csv')
        #self.alljobs = pd.read_json(r'joblist.json')
        self.alljobs = JobOffer.objects.all()
        
        self.preprocessing()
        self.createBow()
        self.createSimilarityMatrix()
        allUserRatings = self.df.pivot_table(index=['userID'],columns=['jobID'],values='like')
        self.corrMatrix = allUserRatings.corr(method="pearson")

    def preprocessing(self):
        
        for index, row in self.df.iterrows():
            columns = ["description", "hashtags"]
            for col in columns:
                #cleaning data
                row[col] = str(row[col]).replace("­","")

    def createBow(self):
        
        #choose important columns
        columns = ["description","jobTitle","location"]
        wordlist = []
        for index, row in self.df.iterrows():
            #create Dictionaries for matrix
            self.id2index[row["jobID"]] = index
            self.index2id[index] = row["jobID"]
            words = ""
            for col in columns:
                if row[col] is not None:
                    words += str(row[col])
            wordlist.append(words)
        self.df["bow"] = wordlist
    
    def createSimilarityMatrix(self):
        
        # create vectorizer for bag of words
        count = CountVectorizer()
        # create count matrix
        cm = count.fit_transform(self.df["bow"])
        self.cosine_sim = cosine_similarity(cm)

    def get_similar_jobs(self, jobid):
        recommended_jobs = []
        #find index of given job in matrix
        idx = self.id2index[jobid]
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending = False)
        top_indices = list(score_series.iloc[1:2].index)
        for i in top_indices:
            topjobid = self.index2id[i] ## <- Tested: returns correct _id
            #print(topjobid)
            recommended_jobs.append(topjobid)
        return recommended_jobs

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
        return ratings

    def recommend(self, user_id):
        recommended_jobs = pd.DataFrame()
        userRatings = self.get_rated_jobs(user_id)
        #User didnt rate enough jobs for identifying similar users
        if len(userRatings) < 10:
            fewrated = self.df.groupby(by="jobID")["like"].count().sort_values(ascending = True)
            result = list(fewrated.iloc[:10].index)
        #User already rated enough jobs
        else:
            #print(userRatings)
            for jobid, rating in userRatings:
                recommended_jobs = recommended_jobs.append(self.evaluate(jobid, rating), ignore_index = True)

            recommended_jobs = recommended_jobs.sum().sort_values(ascending=False)
            recommended_jobs = list(recommended_jobs.iloc[:10].index)
            result = recommended_jobs
        
        #Remove jobs from list, that were already rated by User
        for jobid, rating in userRatings:
            if rating == 1:
                result += self.get_similar_jobs(jobid)

        result = result[:11]
        return result
        #return recommended_jobs
