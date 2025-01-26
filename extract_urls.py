import requests
import json

url="http://localhost:32768/search"

response = requests.get(url, params = {"q": "Indian IT companies hiring scenario in 2025", "format":"json"})
print(response.url, response.status_code)
print(response.text)
parsed_json = json.loads(response.text)
urls=[]
for result in parsed_json["results"]:
    try:
        url = result["url"]
        urls.append(result["url"])
    except KeyError as e:
        print(f"KeyError: {e}")
print("Extracted URLs: ", "No. of URLs: ",urls, len(urls))
        

#http://localhost:32768/search?q=india&format=json&image_proxy=False&default_lang=en