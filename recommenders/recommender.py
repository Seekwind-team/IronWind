import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from joboffer.models import Swipe, JobOffer


class Recommender:
    swipesdf = None  # <-- DataFrame for all swipes with userid, jobid, like,
    jobsdf = None  # <-- DataFrame for all jobs with (job-) description, location and title
    corrMatrix = None  # <-- Matrix of all jobs and their similarity based on user votes
    id2index = {}  ### 2 dictionaries to look up real job ids and their indexes in a matrix
    index2id = {}  ###
    cosine_sim = None  # Matrix of all jobs and their similarity based on NLP
    inactivejobs = []  # Swipe data includes inactive jobs to keep the rating history --> remove inactive jobs from result list

    def __init__(self):
        self.update()

    # update the matching data and the similarity matrices
    def update(self):
        # filling Swipe-Dataframe and Job-Dataframe
        self.getSwipesData()
        self.getJobsData()

        self.createBow()
        self.createSimilarityMatrix()
        self.createCorrelationMatrix()

    # collect data of all swipes and store them in a DataFrame "swipesdf"
    def getSwipesData(self):
        self.swipesdf = pd.DataFrame()
        swipes = Swipe.objects.all()
        jobidlist = []
        useridlist = []
        likelist = []

        # iterate over all swipes and collect data in lists
        for s in swipes:
            jobidlist.append(s.job_offer.id)
            useridlist.append(s.candidate.id)
            likelist.append(s.liked)
            if not s.job_offer.is_active:
                self.inactivejobs.append(s.job_offer.id)

        # store data of lists in DataFrame
        self.swipesdf["job_id"] = jobidlist
        self.swipesdf["user_id"] = useridlist
        self.swipesdf["like"] = likelist

    # collect data of all jobs and store them in a Dataframe "jobsdf"
    def getJobsData(self):
        self.jobsdf = pd.DataFrame()
        jobs = JobOffer.objects.all()
        jobidlist = []
        descriptionlist = []
        locationlist = []
        titlelist = []

        # iterate over all jobs and collect data in lists
        for j in jobs:
            jobidlist.append(j.id)
            descriptionlist.append(j.description)
            locationlist.append(j.location)
            titlelist.append(j.job_title)
            if j.is_deleted:
                self.inactivejobs.append(j.id)

        # store data of lists in DataFrame
        self.jobsdf["job_id"] = jobidlist
        self.jobsdf["description"] = descriptionlist
        self.jobsdf["location"] = locationlist
        self.jobsdf["jobtitle"] = titlelist

    # create a bag of words for each job to measure similarity of jobs based on features
    def createBow(self):
        # index for matrix that is created later
        matrixidx = 0
        # choose important columns to collect words from.
        # all collected words will be stored in a "bag of words" for each jobs
        columns = ["description", "jobtitle", "location"]
        wordlist = []
        for index, row in self.jobsdf.iterrows():
            # create Dictionaries for matrices
            self.id2index[row["job_id"]] = matrixidx  # necessary because the indices of the similarity Matrix
            self.index2id[matrixidx] = row["job_id"]  # are integers (starting by 0) and not the jobids
            matrixidx += 1
            words = ""
            for col in columns:
                if row[col] is not None:
                    words += str(row[col])
            wordlist.append(words)
        self.jobsdf["bow"] = wordlist

        # create a similarity matrix based on job features

    def createSimilarityMatrix(self):
        # create vectorizer for bag of words
        count = CountVectorizer()
        # create count matrix
        cm = count.fit_transform(self.jobsdf["bow"])
        self.cosine_sim = cosine_similarity(cm)

    # get similar jobs to liked jobs
    # if used with ascend = True, jobs different to job with jobid are added
    def get_similar_jobs(self, jobid, ascend=False):
        recommended_jobs = []
        # find index of given job in matrix
        idx = self.id2index[jobid]
        # extract indices and similarity from matrix by using the index, sort them descending
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending=ascend)
        top_indices = list(score_series.iloc[1:3].index)
        # convert those found indices to the original jobid, add them to the list and return it
        for i in top_indices:
            topjobid = self.index2id[i]  # <-- convert matrix index to job_id
            recommended_jobs.append(topjobid)
        return recommended_jobs

    # create a correlation matrix based on user votes
    def createCorrelationMatrix(self):
        allUserRatings = self.swipesdf.pivot_table(index=['user_id'], columns=['job_id'], values='like')
        allUserRatings = allUserRatings.astype(float)
        self.corrMatrix = allUserRatings.corr(method="pearson")

    # get jobs rated similarly to already rated jobs
    def evaluate(self, jobID, rating):
        similar_ratings = self.corrMatrix[jobID] * (rating)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings

    # get all jobs rated by one user
    def get_rated_jobs(self, user_id):
        # limit DataFrame 'swipes', so that only ratings by user himself appear
        rated_jobs = self.swipesdf[self.swipesdf["user_id"] == user_id]
        ratings = []
        # add all jobids and ratings of this user to a list and return it
        for index, row in rated_jobs.iterrows():
            tmp = [row["job_id"], row["like"]]
            ratings.append(tmp)
        return ratings

    # get a list of top10 jobs that might be interesting for the user
    # based on jobs similar to those he already liked and jobs that other users liked
    def recommend(self, user_id):
        self.update()
        result = []
        recommended_jobs = pd.DataFrame()
        userRatings = self.get_rated_jobs(user_id)
        # User didnt rate jobs yet
        if len(userRatings) == 0:
            # get often rated jobs, unless there are no swipes at all yet
            if not self.swipesdf.empty:
                jobs = self.swipesdf.groupby(by="job_id")["like"].count().sort_values(ascending=False)
                jobs = jobs.to_frame()
                for index, row in jobs.iterrows():
                    result.append(index)
            else:
                # special case: no one has ever rated anything yet
                for index, row in self.jobsdf.iterrows():
                    result.append(row["job_id"])

        # User rated jobs already
        else:
            for jobid, rating in userRatings:
                # add evaluated jobs and their like rating to recommended jobs
                recommended_jobs = recommended_jobs.append(self.evaluate(jobid, rating), ignore_index=True)

            # Sum up ratings of recommended jobs, then sort ratings descending and add them to result list
            recommended_jobs = recommended_jobs.sum().sort_values(ascending=False)
            result = list(recommended_jobs.iloc[:10].index)

            # Add jobs to list, that are similar to jobs a user liked and different to jobs he didnt like
            for jobid, rating in userRatings:
                if rating == 1:  # like
                    result += self.get_similar_jobs(jobid)
                else:  # dislike
                    result += self.get_similar_jobs(jobid, ascend=True)

        # Remove duplicates, in case jobs are recommended due to content similarity and like history
        result = [i for j, i in enumerate(result) if i not in result[:j]]
        for index, row in self.jobsdf.iterrows():
            if row["job_id"] not in result and row["job_id"] not in self.inactivejobs:
                result.append(row["job_id"])

        # Remove inactive jobs from results
        for r in result:
            if r in self.inactivejobs:
                result.remove(r)

        # Return top 10
        result = result[:10]

        # Turn IDs into job offers
        recommendations = []
        for r in result:
            recommendations.append(JobOffer.objects.filter(id=r).get())

        return recommendations
