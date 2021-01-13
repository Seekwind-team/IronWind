from joboffer.models import *
import json

class GenCSV():
    def __init__(self):
        swipes = Swipe.objects.all()

        with open("gen_matching.json", "w") as w_file:
            data = ""
            for s in swipes:
                data += ('{beg}"job_id":{j_id}, "user_id":{u_id}, "like":{like}, "description":"{desc}", "location":"{loc}", "jobtitle":"{j_title}"{end}'.format(beg="{", end="}", j_id=s.job_offer.id, u_id=s.candidate.id, like=str(s.liked).lower(), desc=s.job_offer.description, loc=s.job_offer.location, j_title=s.job_offer.job_title))
            
            w_file.write(data)
            w_file.close