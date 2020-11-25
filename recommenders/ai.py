import json
import os
import tensorflow as tf
from tensorflow.keras import layers

class AI:

    def __init__(self):
        # TODO this is a placeholder, load trained model here
        # model = tf.keras.models.load_model("path/to/location")
        self.model = tf.keras.Sequential([
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu")
    	])
        # TODO this is a placeholder, load tokenizer used in training here
        # https://stackoverflow.com/questions/45735070/keras-text-preprocessing-saving-tokenizer-object-to-file-for-scoring
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer



    def get_recommendations(self, user_json, jobs_json):
        user_data = json.loads(user_json)
        job_data = json.loads(jobs_json)

        tokenized_user_data = self.prepare_user_data(user_data)
        tokenized_job_data = self.prepare_job_data(job_data)

        predictions = dict()

        for job in tokenized_job_data:
            predictions[job["_id"]] = self.model.predict([tokenized_user_data, job])

        return json.dumps(predictions)


    def prepare_user_data(self, user_data):
        pass
        # ^^ placeholder because python doesnt allow empty functions
        # prepare all user data the same way it was prepared for training

    def prepare_job_data(self, job_data):
        pass
        # ^^ placeholder because python doesnt allow empty functions
        # prepare all job data the same way it was prepared for training


path = os.path.dirname(__file__)
with open(path + "\\user.json") as user_file, open (path + "\\jobs.json") as jobs_file:
    ai = AI()
    ai.get_recommendations(user_file.read(), jobs_file.read())