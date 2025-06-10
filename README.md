# Beer Scraping and Analysis Project

A Python script to scrape, clean, and visualize beer data from **SoySuper.com**, a Spanish online supermarket.

## Description

This script executes the following steps in order:

1. **Scraping**  
   - Uses Selenium to navigate the beer search page on SoySuper.com.  
   - Scrolls to load all products.  
   - Extracts links for each beer product and visits each page to retrieve:  
     - Name  
     - Main price and lot size  
     - Supermarket-specific prices (if available)  
     - Description  
     - Image URL  
   - Saves the raw data to `beers_spain.xlsx`.

2. **Data Cleaning & Visualization**  
   - The notebook `notebook/data_frame_beers.ipynb` loads the Excel output, cleans the DataFrame (types, duplicates, missing values), and generates charts for:  
     - Price distributions  
     - Price comparisons between supermarkets  
     - Other relevant metrics

## Requirements

- Python 3.7 or higher

Install production dependencies:

```bash
pip install -r requirements.txt
```

For development (linting, notebooks, tests):

```bash
pip install -r requirements-dev.txt
```

## Project Structure

```text
spanish-supermarket-beer-scraper/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── beer_scraper/
│       ├── __init__.py
│       └── main.py             # Main scraping script
└── notebook/
    └── data_frame_beers.ipynb  # Notebook for cleaning & visualization
```

## Usage

1. **Run the scraper**:

    ```bash
    python src/beer_scaper/main.py
    ```

    This will generate `beers_spain.xlsx` in the current directory.

2. **Open the notebook**:

    ```bash
    jupyter notebook notebook/data_frame_beers.ipynb
    ```

    Run the cells to clean and visualize the scraped data.

## Best Practices Implemented

- Standalone script (not a library).  
- Centralized configuration and selectors in the code.  
- Automated WebDriver management with `webdriver-manager`.  
- Robust error handling via `try/except` blocks.  
- Separate requirements for production and development.  
- `.gitignore` to exclude temporary files and caches.  
- MIT License included.

## Contact

For questions or contributions, open an issue or contact: ascm1980@gmail.com
