import requests

json_url = "https://jobs.github.com/positions.json?page=1&description=python&location=new+york"
f = open("jsonderulo.txt",'w')
response = requests.get(json_url)

if response.status_code == 200:
    print("Successfully obtained json data")
    print("'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'")

    json = response.json()
    print(json[1])
    for i in range(0, len(json)):
        print(dict.get(json[i]))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # once json data is obtained, save it to a file


elif response.status_code == 404:
    print("json data not found")