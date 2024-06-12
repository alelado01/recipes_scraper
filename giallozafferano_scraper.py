from bs4 import BeautifulSoup
import requests
import json
from multiprocessing import Pool
import logging
import time
import re
import os
from PIL import Image
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




#Creates a basic Recipe class
class Recipe:
    def __init__(self, title, description, ingredients, img_path, category, rating, difficulty, prep_time):
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.img_path = img_path
        self.category = category
        self.rating = rating
        self.difficulty = difficulty
        self.prep_time = prep_time



#Clean formatting of the ingredients
def clean_ingredients(ingredients):
    cleaned_ingredients = []
    for ingredient in ingredients:
        # Removes '\n', '\t' and multiple ' '
        cleaned_ingredient = re.sub(r'\s+', ' ', ingredient).strip()
        cleaned_ingredients.append(cleaned_ingredient)
    
    return cleaned_ingredients



#Saves every img of the recipe in a folder, in the json file there'll be the paths to the recipes
def save_image(image_url, recipe_title):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        #Some imgs are not available and the script won't download them

        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img = img.resize((100, 100), Image.LANCZOS)
        
        if not os.path.exists('recipe_images'):
            os.makedirs('recipe_images')
        
        img_path = os.path.join('recipe_images', f"{recipe_title}.jpg")
        img.save(img_path, format='JPEG', quality=85)
        return img_path
    except requests.RequestException as e:
        logging.error(f"Error while downloading img {image_url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error while saving img {recipe_title}: {e}")
        return None



#Scrapes gialloZafferano website
def scrape_giallozafferano(url):
    recipes = []
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error while addressing request to URL {url}: {e}")
        return recipes
    
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_blocks = soup.find_all('div', class_='gz-card-content')
    
    for block in recipe_blocks:
        recipe = {}
        category = block.find('div', class_='gz-category').text.strip() if block.find('div', 'gz-category') else None
        title = block.find('h2', class_='gz-title').text.strip() if block.find('h2', 'gz-title') else None
        description = block.find('div', class_='gz-description').text.strip() if block.find('div', 'gz-description') else None
        url = block.find('h2', 'gz-title').a['href'] if block.find('h2', 'gz-title') else None
        rating = block.find_all('li', 'gz-single-data-recipe')[1].text.strip() if len(block.find_all('li', 'gz-single-data-recipe')) > 1 else None
        difficulty = block.find_all('li', 'gz-single-data-recipe')[2].text.strip() if len(block.find_all('li', 'gz-single-data-recipe')) > 2 else None
        prep_time = block.find_all('li', 'gz-single-data-recipe')[3].text.strip() if len(block.find_all('li', 'gz-single-data-recipe')) > 3 else None
        
        recipe.update({'category': category, 'title': title, 'description': description, 'url': url, 'rating': rating, 'difficulty': difficulty, 'prep_time': prep_time})

        if recipe['url']:
            for _ in range(5):  # Tentativi massimi
                try:
                    response_single_recipe = requests.get(recipe['url'])
                    response_single_recipe.raise_for_status()
                    break
                except requests.RequestException as e:
                    logging.error(f"Error while addressing request to the recipe URL {recipe['url']}: {e}")
                    time.sleep(2)  # Ritardo tra i tentativi
            else:
                logging.error(f"Repeated failure while requesting to URL {recipe['url']}")
                continue

            soup_single_recipe = BeautifulSoup(response_single_recipe.content, 'html.parser')
            img_tag = soup_single_recipe.find('picture').find('img')
            img_path = save_image(img_tag['src'], title) if img_tag else None
            
            ingredient_block = soup_single_recipe.find('div', 'gz-ingredients')
            if ingredient_block:
                ingredient_lists = ingredient_block.find_all('dl', 'gz-list-ingredients')
                ingredients = [ingredient.text.strip() for ingredient_list in ingredient_lists for ingredient in ingredient_list.find_all('dd', 'gz-ingredient')]
                cleaned_ingredients = clean_ingredients(ingredients)
                recipes.append(Recipe(title, description, cleaned_ingredients, img_path, category, rating, difficulty, prep_time).__dict__)
            else:
                logging.warning(f"No ingredient found for the recipe: {title}")
    
    return recipes


#Gets the number of the pages containing recipes
def get_total_pages(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error while addressing request to URL {url}: {e}")
        return 0

    soup = BeautifulSoup(response.content, 'html.parser')
    total_pages_element = soup.find('span', 'total-pages')
    return int(total_pages_element.text.strip()) if total_pages_element else 0



#giallozafferano URL
base_url = 'https://www.giallozafferano.it/ricette-cat/page{}/'
total_pages = get_total_pages(base_url.format(1))


#Shows the scraping status
def process_page(page_number):
    url = base_url.format(page_number)
    logging.info(f"Processing page {page_number}")
    return scrape_giallozafferano(url)


#Multiprocessing to speed up the scraping
if __name__ == "__main__":
    num_processes = 64
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_page, range(1, total_pages + 1))
    
    flat_results = [item for sublist in results for item in sublist]

    try:
        #Saves in a json all the datas about the recipes
        with open("recipes_data_with_images.json", "w") as file:
            json.dump(flat_results, file)
            logging.info("Data successfully loaded")
    except Exception as e:
        logging.error(f"Unexpected error while writing on the JSON: {e}")
