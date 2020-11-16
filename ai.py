import json
import tensorflow as tf
from tensorflow.keras import layers

class AI:

    def __init__(self):
        # TODO this is a placeholder, load trained model here
        # model = tf.keras.models.load_model("path/to/location")
        model = tf.keras.Sequential([
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu")
    	])

    def get_recommendations(self, user_json, jobs_json):
        user = json.loads(user_json)
        jobs = json.loads(jobs_json)

        #filter useful information and tokenize
        tokenized_job_data = jobs
        tokenized_user_data = user

        predictions = []

        for job in tokenized_job_data:
            predictions.append([job["_id"], model.predict([tokenized_user_data, job])])






#%%
import json
with open("user.json") as user_file, open("jobs.json") as jobs_file:
	ai = AI()
	ai.get_recommendations(user_file.read(), jobs_file.read())

#%%
