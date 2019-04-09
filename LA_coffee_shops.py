import requests
from bs4 import BeautifulSoup
import pandas

data = []

base_url = "https://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=Los%20Angeles%2C%20CA&page="
# looping through the first 5 pages
for page in range(1, 6):
    r = requests.get(base_url + str(page))
    soup = BeautifulSoup(r.content, "html.parser")
    g_data = soup.find_all("div", class_="info")

    # looping through each coffee shop
    for item in g_data:
        d = {}
        d["Business Name"] = item.contents[0].find("a", class_="business-name").text
        try:
            d["Street Address"] = item.contents[1].find_all("span", class_="street-address")[0].text
        except:
            pass
        d["Locality"] = item.contents[1].find_all("span", class_="locality")[0].text.replace(",", "")
        d["State"] = item.contents[1].find_all("p", class_="adr")[0].find_all("span")[-2].text
        d["Zip Code"] = item.contents[1].find_all("p", class_="adr")[0].find_all("span")[-1].text
        d["Phone Number"] = item.contents[1].find_all("div", class_="primary")[0].text
        data.append(d)

# saving the data into a csv file
df = pandas.DataFrame(data)
df.to_csv("LA_Coffee_Shops.csv")
