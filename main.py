import requests

json_url = "https://jobs.github.com/positions.json?page="
# test "https://jobs.github.com/positions.json?page=1&description=python&location=new+york"
f = open("jsonderulo.txt",'w')
total_listings = 0
for i in range(0, 5):
    pageurl = json_url + str(i + 1)
    pgres = requests.get(pageurl)
    if pgres.status_code == 200:
        print("Successfully obtained json data")
        print("'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'")
        page_json = pgres.json()
        total_listings = total_listings + int((len(page_json)))
        print(page_json[1])
        for j in range(0, len(page_json)):
            print(dict.get(page_json[i], 'id'))
            print(dict.get(page_json[i], 'type'))
            print(dict.get(page_json[i], 'url'))
            print(dict.get(page_json[i], 'created_at'))
            print(dict.get(page_json[i], 'company'))
            print(dict.get(page_json[i], 'company_url'))
            print(dict.get(page_json[i], 'location'))
            print(dict.get(page_json[i], 'title'))
            print(dict.get(page_json[i], 'description'))
            print(dict.get(page_json[i], 'how_to_apply'))
            print(dict.get(page_json[i], 'company_logo'))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Total listings: " + str(total_listings))

    # once json data is obtained, save it to a file


