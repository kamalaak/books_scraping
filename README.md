# noolulagam_books_scraping 
This script scrapes book details from a website and saves the information to a CSV file. It reads book URLs from an input CSV, extracts information such as book title, type, author, publisher, price, and publication year, and writes the data to an output CSV.

    Input: CSV file with book titles and URLs.
    Output: CSV file with extracted book details.
    Libraries: Uses httpx for HTTP requests and selectolax for HTML parsing.
    Flow: Starts scraping from a specific URL (start_link) and processes subsequent books.
    Dependencies: Requires httpx and selectolax Python libraries.
