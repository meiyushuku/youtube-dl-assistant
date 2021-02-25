import requests
import json

def test(url):
    response = requests.get(url)
    if json.loads(response.text)["error"]["errors"][0]["reason"] != "badRequest":
        test = 1 # 1
    else:
        test = 0 # 0
    return test

url = "https://www.googleapis.com/youtube/v3/videos?key=AIzaSyAVKnfeGxZe3fMlpvNrlkrhD8hEs4DU6j"
print(test(url))