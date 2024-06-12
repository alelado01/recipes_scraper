# GialloZafferano Recipe Scraper

This project is a web scraper for collecting recipes from the GialloZafferano website. It extracts information such as title, description, ingredients, category, rating, difficulty, and preparation time for each recipe, and saves it in a JSON file. Furthermore, it downloads and saves images of each recipe in a folder.

## Features

- Scrapes recipe information from the GialloZafferano website.
- Downloads and saves images of the recipes.
- Formats the ingredients list.
- Saves the collected data in a JSON file.

## Requirements

- Python 3.x
- BeautifulSoup4
- Requests
- Pillow

## Installation

 Clone this repository:

   ```sh

   git clone https://github.com/yourusername/giallozafferano-recipe-scraper.git
   cd giallozafferano-recipe-scraper

   ```

 Install the required packages:

    pip install -r requirements.txt 
    
 Usage

   Run the scraper:

    python scraper.py

   The scraped data will be saved in recipes_data_with_images.json and the images will be saved in the recipe_images directory.


## Code Overview

### Recipe Class

The `Recipe` class stores the details of each recipe:

```python
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
```

### Main Script

The main script orchestrates the scraping process:

```python

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
```

## Issues

- Some images are not available and the script won't download them
- There are some recipes which have no ingredients, the script will only print a warning without saving anything

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
