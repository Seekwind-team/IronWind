import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from joboffer.models import *

class Recommender:

    swipesdf = None #<-- DataFrame for all swipes with userid, jobid, like, 
    jobsdf = None#<-- DataFrame for all jobs with (job-) description, location and title
    corrMatrix = None #<-- Matrix of all jobs and their similarity based on user votes 
    id2index = {} ### 2 dictionaries to look up real job ids and their indexes in a matrix
    index2id = {} ###
    cosine_sim = None # Matrix of all jobs and their similarity based on NLP

    def __init__(self):
        self.update()

    #update the matching data and the similarity matrices
    def update(self):
        # filling Swipe-Dataframe and Job-Dataframe
        self.getSwipesData()
        self.getJobsData()

        self.preprocessing()
        self.createBow()
        self.createSimilarityMatrix()
        self.createCorrelationMatrix()

    #collect data of all swipes and store them in a DataFrame "swipesdf"
    def getSwipesData(self):
        self.swipesdf = pd.DataFrame()
        swipes = Swipe.objects.all()
        jobidlist = []
        useridlist = []
        likelist = []

        #iterate over all swipes and collect data in lists
        for s in swipes:
            jobidlist.append(s.job_offer.id)
            useridlist.append(s.candidate.id)
            likelist.append(s.liked)
        
        #store data of lists in DataFrame
        self.swipesdf["job_id"] = jobidlist
        self.swipesdf["user_id"] = useridlist
        self.swipesdf["like"] = likelist

    #collect data of all jobs and store them in a Dataframe "jobsdf"
    def getJobsData(self):
        self.jobsdf = pd.DataFrame()
        jobs = JobOffer.objects.all()
        jobidlist = []
        descriptionlist = []
        locationlist = []
        titlelist = []

        #iterate over all jobs and collect data in lists
        for j in jobs:
            jobidlist.append(j.id)
            descriptionlist.append(j.description)
            locationlist.append(j.location)
            titlelist.append(j.job_title)

        #store data of lists in DataFrame
        self.jobsdf["job_id"] = jobidlist
        self.jobsdf["description"] = descriptionlist
        self.jobsdf["location"] = locationlist
        self.jobsdf["jobtitle"] = titlelist


    #clean data of relevant columns
    def preprocessing(self):
        for index, row in self.jobsdf.iterrows():
            columns = ["description","jobtitle","location"]
            for col in columns:
                #cleaning data
                row[col] = str(row[col]).replace("­","")

    #create a bag of words for each job to measure similarity of jobs based on features
    def createBow(self):
        #index for matrix that is created later
        matrixidx = 0
        #choose important columns to collect words from.
        #all collected words will be stored in a "bag of words" for each jobs
        columns = ["description","jobtitle","location"]
        wordlist = []
        for index, row in self.jobsdf.iterrows():
            #create Dictionaries for matrices
            self.id2index[row["job_id"]] = matrixidx #necessary because the indices of the similarity Matrix
            self.index2id[matrixidx] = row["job_id"] #are integers (starting by 0) and not the jobids
            matrixidx += 1
            words = ""
            for col in columns:
                if row[col] is not None:
                    words += str(row[col])
            wordlist.append(words)
        self.jobsdf["bow"] = wordlist 
    
    #create a similarity matrix based on job features
    def createSimilarityMatrix(self):
        # create vectorizer for bag of words
        count = CountVectorizer()
        # create count matrix
        cm = count.fit_transform(self.jobsdf["bow"])
        self.cosine_sim = cosine_similarity(cm)

    #get similar jobs to liked jobs
    def get_similar_jobs(self, jobid):
        recommended_jobs = []
        #find index of given job in matrix
        idx = self.id2index[jobid]
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending = False)
        top_indices = list(score_series.iloc[1:3].index)
        for i in top_indices:
            topjobid = self.index2id[i] #<-- convert matrix index to job_id
            recommended_jobs.append(topjobid)
        return recommended_jobs

    #create a correlation matrix based on user votes    
    def createCorrelationMatrix(self):
        allUserRatings = self.swipesdf.pivot_table(index=['user_id'],columns=['job_id'],values='like')
        self.corrMatrix = allUserRatings.corr(method="pearson")

    #get jobs rated similarly to already rated jobs
    def evaluate(self,jobID,rating):
        similar_ratings = self.corrMatrix[jobID]*(rating)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings
    
    #get all jobs rated by one user
    def get_rated_jobs(self, user_id):
        rated_jobs = self.swipesdf[self.swipesdf["user_id"] == user_id]
        ratings = []
        for index, row in rated_jobs.iterrows():
            tmp = [row["job_id"],row["like"]]
            ratings.append(tmp)
        return ratings

    #get a list of top10 jobs that might be interesting for the user
    #based on jobs similar to those he already liked and jobs that other users liked
    def recommend(self, user_id):
        result = []
        recommended_jobs = pd.DataFrame()
        userRatings = self.get_rated_jobs(user_id)
        #User didnt rate enough jobs for identifying similar users
        if len(userRatings) < 10:
            fewrated = self.swipesdf.groupby(by="job_id")["like"].count().sort_values(ascending = True)
            result = list(fewrated.iloc[:10].index)
        #User already rated enough jobs
        else:
            for jobid, rating in userRatings:
                recommended_jobs = recommended_jobs.append(self.evaluate(jobid, rating), ignore_index = True)

            recommended_jobs = recommended_jobs.sum().sort_values(ascending=False)
            recommended_jobs = list(recommended_jobs.iloc[:10].index)
            result = recommended_jobs
        
        #Add jobs to list, that are similar to jobs user already liked
        for jobid, rating in userRatings:
            if rating == 1:
                result += self.get_similar_jobs(jobid)

        result = result[:10]
        return result
        #return recommended_jobs
