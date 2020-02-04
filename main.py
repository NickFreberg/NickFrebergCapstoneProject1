import requests

# def pagination(json_url,curr_page):


json_url = "https://jobs.github.com/positions.json?page="
# test "https://jobs.github.com/positions.json?page=1&description=python&location=new+york"
f = open("jsonderulo.txt",'w')
total_listings = 0
for i in range(0, 5):
    pageurl = json_url + str(i + 1)
    pgres = requests.get(pageurl)
    if pgres.status_code == 200:
        page_json = pgres.json()
        total_listings = total_listings + int((len(page_json)))
        for j in range(0, len(page_json)):
            f.write("~~~~~~~~~~~~~~~~~~~START OF POSTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            f.write(dict.get(page_json[i], 'id') + "\n")
            f.write(dict.get(page_json[i], 'type') + "\n")
            f.write(dict.get(page_json[i], 'url') + "\n")
            f.write(dict.get(page_json[i], 'created_at') + "\n")
            f.write(dict.get(page_json[i], 'company') + "\n")
            f.write(dict.get(page_json[i], 'company_url') + "\n")
            f.write(dict.get(page_json[i], 'location') + "\n")
            f.write(dict.get(page_json[i], 'title') + "\n")
            # f.write(dict.get(page_json[i], 'description') + "\n")
            f.write(dict.get(page_json[i], 'how_to_apply') + "\n")
            f.write(dict.get(page_json[i], 'company_logo') + "\n")
            f.write("~~~~~~~~~~~~~~~~~~~END OF POSTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Finished reading a page! Total listings: " + str(total_listings))
