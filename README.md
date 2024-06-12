GialloZafferano Recipe Scraper

This project is a web scraper for collecting recipe data from the GialloZafferano website. It extracts information such as title, description, ingredients, image, category, rating, difficulty, and preparation time for each recipe, and saves it in a JSON file. Additionally, it downloads and saves images of the recipes.
Features

    Scrapes recipe information from the GialloZafferano website.
    Downloads and saves images of the recipes.
    Cleans and formats the ingredients list.
    Utilizes multiprocessing for faster scraping.
    Saves the collected data in a JSON file.

Requirements

    Python 3.x
    BeautifulSoup4
    Requests
    Pillow

Installation

    Clone this repository:

    sh

git clone https://github.com/yourusername/giallozafferano-recipe-scraper.git
cd giallozafferano-recipe-scraper

Install the required packages:

sh

    pip install -r requirements.txt

Usage

    Run the scraper:

    sh

    python scraper.py

    The scraped data will be saved in recipes_data_with_images.json and the images will be saved in the recipe_images directory.

Project Structure

    scraper.py: Main script for scraping the recipes.
    requirements.txt: List of required packages.
    recipe_images/: Directory where the recipe images are saved.
    recipes_data_with_images.json: JSON file containing the scraped recipe data.

Code Overview
Recipe Class

The Recipe class stores the details of each recipe:

python

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

Functions

    clean_ingredients(ingredients): Cleans and formats the ingredients list.
    save_image(image_url, recipe_title): Downloads and saves the recipe image.
    scrape_giallozafferano(url): Scrapes recipes from a given URL.
    get_total_pages(url): Retrieves the total number of pages containing recipes.
    process_page(page_number): Processes a single page of recipes.

Main Script

The main script orchestrates the scraping process:

python

if __name__ == "__main__":
    num_processes = 64
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_page, range(1, total_pages + 1))
    
    flat_results = [item for sublist in results for item in sublist]

    try:
        with open("recipes_data_with_images.json", "w") as file:
            json.dump(flat_results, file)
            logging.info("Data successfully loaded")
    except Exception as e:
        logging.error(f"Unexpected error while writing on the JSON: {e}")

Logging

Logging is configured to provide information about the scraping status:

python

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Error Handling

The script includes error handling for network requests and image processing to ensure robustness.
