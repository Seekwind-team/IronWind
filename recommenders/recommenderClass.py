### Offene Fragen:

### STEP 1: IMPORT DATA

from rake_nltk import Rake
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from yellowbrick.text import FreqDistVisualizer

class Recommender:
    df = None
    id2index = {}
    index2id = {}
    cosine_sim = None
    def __init__(self):
        
        self.update()

    def update(self):
        
        self.df = pd.read_json (r'https://api.cohooyo.com/jobs')
        self.preprocessing()
        self.createBow()
        self.createSimilarityMatrix()
    
    def preprocessing(self):
        
        for index, row in self.df.iterrows():
            columns = ["description", "hashtags"]
            for col in columns:
                #cleaning data
                row[col] = row[col].replace("­","")
    
    def createBow(self):
        
        #choose important columns
        columns = ["description"]
        wordlist = []
        for index, row in self.df.iterrows():
            #create Dictionaries for matrix
            self.id2index[row["_id"]] = index
            self.index2id[index] = row["_id"]
            words = ""
            for col in columns:
                if row[col] is not None:
                    words += str(row[col])
            wordlist.append(words)
        self.df["bow"] = wordlist

    def createSimilarityMatrix(self):
        
        # create vectorizer for bag of words
        tfidf = TfidfVectorizer(analyzer="word",max_df=0.2)
        # create count matrix
        cm = tfidf.fit_transform(self.df["bow"])
        self.cosine_sim = cosine_similarity(cm)
    
    def recommend(self, jobid):
        recommended_jobs = []
        #find index of given job in matrix
        idx = self.id2index[jobid]
        score_series = pd.Series(self.cosine_sim[idx]).sort_values(ascending = False)
        top_indices = list(score_series.iloc[1:6].index)
        for i in top_indices:
            topjobid = self.index2id[i] ## <- Tested: returns correct _id
            #print(topjobid)
            recommended_jobs.append(topjobid)
        return recommended_jobs



"""
## Rows are jobs and columns are attributes
df = pd.read_json (r'https://api.cohooyo.com/jobs')

### STEP 2: DATA PREPROCESSING

for index, row in df.iterrows():
    columns = ["description", "hashtags"]
    for col in columns:
        #cleaning data
        row[col] = row[col].replace("­","")

### STEP 3: COMBINE IMPORTANT COLUMNS TO BAG OF WORDS = bow


#dictionaries to convert jobids to indeces and indeces to jobids
id2index = {}
index2id = {}
#choose important columns
columns = ["description"]
wordlist = []
for index, row in df.iterrows():
    #create Dictionaries for matrix
    id2index[row["_id"]] = index
    index2id[index] = row["_id"]
    words = ""
    for col in columns:
        if row[col] is not None:
            words += str(row[col])
    wordlist.append(words)
df["bow"] = wordlist


### STEP 4: CREATE VECTOR REPRESENTATION FOR Bag_of_words AND SIMILARITY MATRIX

count = CountVectorizer()
tfidf = TfidfVectorizer(analyzer="word",max_df=0.2)
# create count matrix
cm = count.fit_transform(df["bow"])
cm2 = tfidf.fit_transform(df["bow"])
ftc = count.get_feature_names()
ftt = tfidf.get_feature_names()

#visualizer = FreqDistVisualizer(features=ftc, orient='v')
#visualizer.fit(cm)
#visualizer.show()
visualizer2 = FreqDistVisualizer(features=ftt, orient='v')
visualizer2.fit(cm2)
visualizer2.show()

# print(cm.shape)
# print(cm2.shape)
cosine_sim = cosine_similarity(cm)
cosine_sim2 = cosine_similarity(cm2)

### STEP 5: RUN AND TEST RECOMMENDER MODEL

def recommend(jobid, cosine_sim):
    recommended_jobs = []
    idx = id2index[jobid]
    #print(indices[indices == job])
    #idx = indices[indices == job].index[0]
    ### idx ist noch Job4 -> abtrennen nach job und int casten
    #idx = int(idx[3:]) falls dieser idx unten idx-1
    #print("idx = ",idx)
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_indices = list(score_series.iloc[1:6].index)
    #print(top_indices)
    print(score_series.iloc[1:6])
    for i in top_indices:
        topjobid = index2id[i] ## <- Tested: returns correct _id
        #print(topjobid)
        recommended_jobs.append(list(df["jobTitle"])[i])
    return recommended_jobs


### READY FOR TESTING
### Insert IDs of Jobs you liked, job titles of recommended jobs will be printed on screen

for i in range(10):
    print("\n","Jobvorschläge für: ",df.loc[i, "jobTitle"])
    print("Jobvorschläge count: ",recommend(df.loc[i, "_id"], cosine_sim))
    print("Jobvorschläge tfidf: ",recommend(df.loc[i, "_id"], cosine_sim2))

def get_similar(jobid, like):
    similar_score = pd.DataFrame(data=(cosine_sim[jobid]*like),columns=["score"])
    
    similar_score = similar_score.sort_values(by=["score"],ascending=False)
    print(similar_score)
    return similar_score


## Jobid,Like?(1=True,0=False)
maler = [(1,1)]

similar_scores = pd.DataFrame()
for job,like in maler:
    similar_scores = similar_scores.append(get_similar(job,like), ignore_index = True)


similar_scores.sum().sort_values(ascending=False)
"""