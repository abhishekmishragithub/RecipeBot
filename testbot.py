from bs4 import BeautifulSoup
import requests
import logging
import csv

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
cooktime_class = "teaser-item__info-item teaser-item__info-item--total-time"
k = 0
for i in soup.find_all("div", {'class': 'view-content'}):
    for j in (i.find_all('h3', {'class': 'teaser-item__title'})):
        # for j in (i.select('teaser-item__image')):
        href_a = j.find('a')['href']
        recipes_source.append('https://www.bbcgoodfood.com' + href_a)
        rating.append(i.find_all(
            'p',
            {'class': 'fivestar-summary fivestar-summary-'}
            )[k].text.strip()
        )
        skilllevel.append(i.find_all(
            "li",
            {"class":
                "teaser-item__info-item teaser-item__info-item--skill-level"}
            )[k].text.strip()
        )
        cooktime.append(i.find_all(
            "li",
            {
                "class":
                    cooktime_class}
            )[k].text.strip()
        )
        k = k + 1
        recipes_title = j.find('a').text
        recipes.append(recipes_title.strip())
for i in rating:
    final_rating.append(i[1:-1])


def write_to_csv(data1, data2, data3, data4, data5):
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


def get_recipe_source():
    with open('BBCRecipeBot_Recipes.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # This skips the first row of the CSV file.
        next(csvreader)
        source = [row for row in csvreader]
    recipeSource = source
    for i in recipeSource:
        print((i[0]))
    recipe_input = input("Enter your choice \n ")
    for s in range(0, len(recipeSource)):
        if recipe_input.lower() == recipeSource[s][0].lower():
            source = recipeSource[s][1]
            rating = recipeSource[s][2]
            skill = recipeSource[s][3]
            total_time = recipeSource[s][4]
            return source, rating, skill, total_time
        else:
            pass


source_url, rating, skill, total_time = get_recipe_source()


def get_recipe(source_url):
    webpage = requests.get(source_url, headers=headers)
    soup = BeautifulSoup(webpage.content, "lxml")
    serves = str(soup.find(
        "span",
        {"class": "recipe-details__text", "itemprop": "recipeYield"}).text
    )
    nutri_name = ["kcal", "fat", "saturates", "carbs"]
    nutri_name.extend(["sugars", "fibre", "protein", "salt"])
    kcal = str(soup.find(
        "span",
        {"itemprop": "calories"}).text
    )
    fat = str(soup.find("span", {"itemprop": "fatContent"}).text)
    saturates = str(soup.find(
        "span",
        {"itemprop": "saturatedFatContent"}).text
    )
    carbs = str(soup.find("span", {"itemprop": "carbohydrateContent"}).text)
    sugars = str(soup.find("span", {"itemprop": "sugarContent"}).text)
    fibre = str(soup.find("span", {"itemprop": "fiberContent"}).text)
    protein = str(soup.find("span", {"itemprop": "proteinContent"}).text)
    salt = str(soup.find(
        "span",
        {"itemprop": "sodiumContent"}).text
    )
    nutri_value = [kcal, fat, saturates, carbs, sugars, fibre, protein, salt]
    nutrition = str({k: v for k, v in zip(nutri_name, nutri_value)})
    x = 1
    method, ingredient = [], []
    for i in soup.find_all(
        "li", {"class": "method__item", "itemprop": "recipeInstructions"}
    ):
        for j in i:
            method.append(str(x) + " . " + j.text)
            x = x + 1
    # print(method)
    for i in soup.find_all(
        "li",
        {"class": "ingredients-list__item", "itemprop": "ingredients"}
    ):
        for j in i:
            if j.name == 'span' or j.name == 'div':
                j.decompose()
            else:
                pass
        # print(i.text)
        ingredient.append(i.text)
    return serves, nutrition, ingredient, method


serves, nutrition, ingredient, method = get_recipe(source_url)
logging.info(serves)
logging.info(nutrition)
logging.info(ingredient)
logging.info(method)
