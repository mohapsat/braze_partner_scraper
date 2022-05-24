import requests
from bs4 import BeautifulSoup
import csv


url = "https://www.braze.com/partners/technology-partners"
page = requests.get(url)
# page = "page.html"

# soup = BeautifulSoup(open(page), "html.parser")
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="results")
companies = list()

company_urls = results.find_all(class_="h-full w-full flex flex-col items-center justify-center")
for company_url in company_urls:
    companies.append(company_url['href'])

# companies = companies[:2]
print(len(companies))

final_list = list()

for company in companies:
    # r = requests.get(company)
    print(company)
    c_page = requests.get(company)
    c_soup = BeautifulSoup(c_page.content, "html.parser")

    try:
        location = c_soup.find(class_="link font-normal").text
    except:
        location = None

    try:
        topic = c_soup.select("#content > div.px-s.max-w-screen-2xl.mx-auto > section > div:nth-child(3) > div.col-span-3.space-y-big > div:nth-child(2) > div")[0].text
    except:
        topic = None

    proses = c_soup.find_all(class_="prose")
    proses = proses[:2]

    # print(proses)
    what_list = list()
    for prose in proses:
        what_list.append(prose.find(class_="text-22 leading-9 my-m").text)

    what = ' '.join(what_list)

    com_url = c_soup.select("#content > div.px-s.max-w-screen-2xl.mx-auto > section > div:nth-child(3) > div.col-start-5.col-span-6.space-y-grand.mt-bigger.md\\:mt-0 > div:nth-child(1) > div > div:nth-child(3) > a")

    try:
        comp_url = com_url[0]['href']
    except:
        comp_url = None

    final_list.append([location, topic, what, comp_url])

print(len(final_list))

# [
# ['Location', 'Personalization', 'AccuWeather tracks weather and delivers up-to-date commercial forecasting services across the globe. What’s more, AccuWeather software provides up-to-date weather conditions. AccuWeather and Braze enable you to use dynamic weather content to create relevant messaging experiences across channels.', 'https://developer.accuweather.com/'],
# ['Deep linking & Attribution', None, 'Adjust is a mobile attribution and analytics company that combines attribution for advertising sources with advanced analytics for a comprehensive picture of business intelligence. Adjust allows you to import paid install attribution data to segment more intelligently within your lifecycle campaigns.', 'https://www.adjust.com/']
# ]

fields = ['Category', 'Topic', 'Description', 'URL']

with open('braze_tech_partners.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(final_list)


