from bs4 import BeautifulSoup
import requests
from clean_ingredients import clean_ingredients
import json
from multiprocessing import Pool

def scrape_giallozafferano(url):
    # Lista per memorizzare tutte le informazioni sulle ricette
    recipes = []

    response = requests.get(url)
    if response.status_code == 200:
    
        soup = BeautifulSoup(response.content, 'html.parser')
        
        recipe_blocks = soup.find_all('div', class_='gz-card-content')
        
        for block in recipe_blocks:
            recipe = {}
            
            category = block.find('div', class_='gz-category').text.strip()
            if category:
                recipe['category'] = category
            else:
                recipe['category'] = None
            
            title = block.find('h2', class_='gz-title').text.strip()
            if title:
                recipe['title'] = title
            else:
                recipe['title'] = None
            
            description = block.find('div', class_='gz-description').text.strip()
            if description:
                recipe['description'] = description
            else:
                recipe['description'] = None

            url = block.find('h2', class_='gz-title').a['href']
            if url:
                recipe['url'] = url
            else:
                recipe['url'] = None

            data_recipe = block.find_all('li', class_='gz-single-data-recipe')

            rating = block.find_all('li', class_='gz-single-data-recipe')[1].text.strip()
            if rating:
                recipe['rating'] = rating
            else:
                recipe['rating'] = None
            
            difficulty = block.find_all('li', class_='gz-single-data-recipe')[2].text.strip()
            if difficulty:
                recipe['difficulty'] = difficulty
            else:
                recipe['difficulty'] = None
            
            if(len(data_recipe) > 3):
                time = data_recipe[3].text.strip()
                if time:
                    recipe['time'] = time
                else:
                    recipe['time'] = None
            #Gli ingredienti sono sull'URL della singola ricetta quindi faccio lo scrape sul singolo URL
            response_single_recipe = requests.get(recipe['url'])
            if response_single_recipe.status_code == 200:
                soup_single_recipe = BeautifulSoup(response_single_recipe.content, 'html.parser')
                img_tag = soup_single_recipe.find('picture').find('img')
                if img_tag:
                    recipe['img'] = img_tag['src']
                else:
                    recipe['img'] = None
                ingredient_block = soup_single_recipe.find('div', class_='gz-ingredients')
                if ingredient_block:
                    ingredient_lists = ingredient_block.find_all('dl', class_='gz-list-ingredients')
                    ingredients = []
                    for ingredient_list in ingredient_lists:
                        ingredients += [ingredient.text.strip() for ingredient in ingredient_list.find_all('dd', class_='gz-ingredient')]
                    recipe['ingredients'] = clean_ingredients(ingredients)
                    recipes.append(recipe)
                else:
                    print("Warning: nessun ingrediente trovato!")
    return recipes


def get_total_pages(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        total_pages_element = soup.find('span', class_='total-pages')
        if total_pages_element:
            total_pages = int(total_pages_element.text.strip())
            return total_pages
    else:
       print("Impossibile reperire i dati, error 404")
       return 0


base_url = 'https://www.giallozafferano.it/ricette-cat/page{}/'

# Trova il numero totale di pagine
total_pages = get_total_pages(base_url.format(1))

# Funzione per il multiprocessing
def process_page(page_number):
    url = base_url.format(page_number)
    print(f"Pagina {page_number} scritta correttamente\n")
    return scrape_giallozafferano(url)

num_processes = 64

pool = Pool(processes=num_processes)
results = pool.map(process_page, range(1, total_pages + 1))
pool.close()
pool.join()

#List comprehension, prende la lista di pagina e la trasforma in una lista piatta (facilita la scrittura su file JSON)
flat_results = [item for sublist in results for item in sublist]

with open("recipes_data.json", "w") as file:
    json.dump(flat_results, file)
    print("Pagine inserite correttamente")

print("Data stored successfully")
