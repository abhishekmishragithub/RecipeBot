from bs4 import BeautifulSoup
import requests
import unicodedata
import logging

logging.basicConfig(
    filename="app.log",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

''' data = requests.get(url, headers={"User-Agent": \
 "Mozilla/5.0 (Windows NT6.3;/
 WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
 Chrome/53.0.2785.143 Safari/537.36"})
'''
query = input("enter recipe name or ingredient with you want to cook \n")

headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/47.0.2526.80 Safari/537.36"
    }

webpage = requests.get(
    'http://www.bbcgoodfood.com/search/recipes?query=%s'
    % (query), headers=headers
    )

soup = BeautifulSoup(webpage.content, "lxml")
recipes_source, recipes, cooktime = [], [], []
skilllevel, rating, final_rating = [], [], []

k = 0
for i in soup.find_all("div", {'class': 'view-content'}):
    for j in (i.find_all('div', {'class': 'teaser-item__image'})):
        # for j in (i.select('teaser-item__image')):
        href_a = j.find('a')['href']
        recipes_source.append('https://www.bbcgoodfood.com' + href_a)
        # rating.append(i.find_all('p', {'class': \
        # 'fivestar-summary fivestar-summary-'})[k].text)
        rating.append(unicodedata.normalize('NFKD', i.find_all(
            'p',
            {'class': 'fivestar-summary fivestar-summary-'}
            )[k].text).encode('ascii', 'ignore'))
        skilllevel.append(i.find_all(
            "li",
            {"class":
                "teaser-item__info-item teaser-item__info-item--skill-level"}
            )[k].text)
        cooktime.append(i.find_all(
            "li",
            {
                "class":
                    "teaser-item__info-item teaser-item__info-item--total-time"}
            )[k].text)
        k = k + 1
        if (j.find_all('span', {'itemprop': 'name'})):
            # recipes.append(j.find_all('span', {'itemprop': 'name'})[0].text)
            recipes.append(unicodedata.normalize(
                'NFKD',
                j.find_all('span', {'itemprop': 'name'})
                [0].text).encode('ascii', 'ignore')
            )
        else:
            pass
for i in rating:
    final_rating.append(i[1:-1])


def write_to_csv(data1, data2, data3, data4, data5):
    import csv
    with open('BBCRecipeBot_Recipes.csv', 'w') as newFile:
        newFileWriter = csv.writer(newFile, lineterminator='\n')
        for i, j, k, l, m in zip(data1, data2, data3, data4, data5):
            newFileWriter.writerow([i, j, k, l, m])


write_to_csv(recipes, recipes_source, final_rating, skilllevel, cooktime)
logging.info(recipes)
logging.info(recipes_source)
logging.info(final_rating)
logging.info(skilllevel)
logging.info(cooktime)
