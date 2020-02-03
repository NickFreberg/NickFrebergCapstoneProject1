import requests

json_url = "https://jobs.github.com/positions.json?page=5&description=python&location=new+york"

response = requests.get(json_url)

if response.status_code == 200:
    print("Successfully obtained json data")
    #once json data is obtained, save it to a file



elif response.status_code == 404:
    print("json data not found")