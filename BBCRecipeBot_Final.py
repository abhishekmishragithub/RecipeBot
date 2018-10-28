from bs4 import BeautifulSoup
import requests
import unicodedata
#data = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/53.0.2785.143 Safari/537.36"})

query= raw_input("enter recipe name or ingredient with you want to cook \n")

headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
webpage = requests.get('http://www.bbcgoodfood.com/search/recipes?query=%s'%(query),headers=headers)

soup = BeautifulSoup(webpage.content)
recipes_source, recipes,cooktime,skilllevel,rating, final_rating = [],[],[],[],[],[]
#recipe_list = soup.find_all("div",{'class' : 'view-content'})
#food_type = soup.find("li",{"class":"teaser-item__info-item teaser-item__info-item--vegetarian"})
#food_type = str(food_type.text)
#print(food_type)
k=0
for i in soup.find_all("div",{'class' : 'view-content'}):
    #print(i)
    for j in (i.find_all('a',{'itemprop': 'url'})):
        #print(j)
        recipes_source.append('https://www.bbcgoodfood.com' + j['href'])
        #rating.append(i.find_all('p',{'class':'fivestar-summary fivestar-summary-'})[k].text)
        rating.append(unicodedata.normalize('NFKD',i.find_all('p',{'class':'fivestar-summary fivestar-summary-'})[k].text).encode('ascii','ignore'))
        skilllevel.append(i.find_all("li",{"class":"teaser-item__info-item teaser-item__info-item--skill-level"})[k].text)
        cooktime.append(i.find_all("li",{"class":"teaser-item__info-item teaser-item__info-item--total-time"})[k].text)
        k=k+1
        #print('linksss',hrefs)
        if (j.find_all('span', {'itemprop': 'name'})):
            #recipes.append(j.find_all('span', {'itemprop': 'name'})[0].text)
            recipes.append(unicodedata.normalize('NFKD',j.find_all('span', {'itemprop': 'name'})[0].text).encode('ascii','ignore'))
        else:
            pass
#print(rating)
for i in rating:
    #print(i[1:-1])
    final_rating.append(i[1:-1])
#for i in skilllevel:
#    print(i)

#for i in cooktime:
#    print(i)


print("###############################################################################################")



def write_to_csv(data1,data2,data3,data4,data5):
    import csv
    with open('BBCRecipeBot_Recipes.csv', 'w') as newFile:
            newFileWriter = csv.writer(newFile,lineterminator='\n')
            for i, j, k, l, m in zip(data1,data2,data3,data4,data5):
                    newFileWriter.writerow([i, j, k, l, m])

write_to_csv(recipes,recipes_source,final_rating,skilllevel,cooktime)



print("################################################################################################")

def get_recipe_source():
    
    def get_recipe_list():
        import csv

        with open('BBCRecipeBot_Recipes.csv', 'r') as csvfile:

            csvreader = csv.reader(csvfile)

            # This skips the first row of the CSV file.
            # csvreader.next() also works in Python 2.
            next(csvreader)

            source = [row for row in csvreader]

        csvfile.close()
        return source
    recipeSource = get_recipe_list()
    
    for i in recipeSource:
        print(i[0])

    recipe_input=raw_input("Enter your choice \n ")

    for i in range(0,len(recipeSource)):
        if recipe_input == recipeSource[i][0].lower():
            source = recipeSource[i][1]
            return source,recipeSource[i][2],recipeSource[i][3],recipeSource[i][4]
        else:
            pass
    
###########################################################  Calling get_recipe_source()       ###########################################3
source_url,rating,skill,total_time = get_recipe_source()
#print(source_url)
#print(rating)
#print(skill)
#print(total_time)

print("###########################################################################################################")






def get_recipe(source_url):
    from bs4 import BeautifulSoup
    import requests
    import unicodedata
    import bleach
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    webpage = requests.get(source_url,headers=headers)

    soup = BeautifulSoup(webpage.content)
    #serving,cook_time, food_type, nutrition, method, ingredients = [],[],[],[],[],[],[]
       
    
    serves = str(soup.find("span",{"class":"recipe-details__text" , "itemprop": "recipeYield"}).text)
    
    nutri = soup.find_all("span",{"class":"nutrition__label"})
    #nutri_name = []
    #for i in nutri:
        #nutri_name.append(str(i.text))
    #nutri_value = soup.find_all("span",{"class":"nutrition__value"})
    nutri_name=["kcal","fat","saturates","carbs","sugars","fibre","protein","salt"]
    kcal = str(soup.find("span",{"itemprop":"calories"}).text)
    fat = str(soup.find("span",{"itemprop":"fatContent"}).text)
    saturates = str(soup.find("span",{"itemprop":"saturatedFatContent"}).text)
    carbs = str(soup.find("span",{"itemprop":"carbohydrateContent"}).text)
    sugars = str(soup.find("span",{"itemprop":"sugarContent"}).text)
    fibre = str(soup.find("span",{"itemprop":"fiberContent"}).text)
    protein = str(soup.find("span",{"itemprop":"proteinContent"}).text)
    salt = str(soup.find("span",{"itemprop":"sodiumContent"}).text)
    nutri_value=[kcal,fat,saturates,carbs,sugars,fibre,protein,salt]
    nutrition =str({k:v for k,v in zip(nutri_name,nutri_value)})   
    x=1
    method,ingredient = [],[]
    for i in soup.find_all("li",{"class":"method__item","itemprop":"recipeInstructions"}):
        for j in i:
            method.append(str(x)+" . " +unicodedata.normalize('NFKD',j.text).encode('ascii','ignore'))
            x=x+1
          
    #print(method)   
    
    for i in soup.find_all("li",{"class":"ingredients-list__item","itemprop":"ingredients"}):
        for j in i:
 
                if j.name == 'span' or j.name == 'div' :
                    j.decompose()
                        
                else:
                    pass
        #print(i.text)         

        ingredient.append(unicodedata.normalize('NFKD',i.text).encode('ascii','ignore'))
    return serves,nutrition,ingredient,method




###########################################################  get Recipe      ###########################################

serves,nutrition,ingredient,method = get_recipe(source_url)

print("No. of Rating :" ,rating)
print("#######################################################################################################")

print("Skill Level : ",skill)

print("###########################################################################################################")

print("Total Time to Cook ",total_time)

print("###########################################################################################################")

print("Serving : ",serves)

print("###########################################################################################################")

print("Nutritions from Food : \n")
print(nutrition)

print("###########################################################################################################")

print("Ingrediants for Recipe :  \n")
for i in ingredient:
    print(i)

print("###########################################################################################################")

print("Cooking Method :  \n")
for i in method:
    print(i+'\n')



