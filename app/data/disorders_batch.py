import json

from app.models.resources import Disorder, Link


def get_disorders_data():
    with open("app/data/disorders.json") as json_disorders:
        disorders_data = json.load(json_disorders)
        for disorder in disorders_data:
            try:
                disorder_content = Disorder.objects.create(details=disorder["content"], name=disorder["name"], url_pattern=disorder["url_pattern"])
            except:
                disorder_content = Disorder.objects.get(name=disorder["name"])
                if disorder_content.details != disorder["content"]:
                    disorder_content.details = disorder["content"]
                    disorder_content.save()
                if disorder_content.url_pattern != disorder["url_pattern"]:
                    disorder_content.url_pattern = disorder["url_pattern"]
                    disorder_content.save()

            for link in disorder["links"]:
                try:
                    disorder_link = Link.objects.get(content=link)
                except:
                    disorder_link = Link.objects.create(content=link, disorder=disorder_content)
                    disorder_link.save()
    
    print("All disorder data has been added or updated to database.")