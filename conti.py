from playwright.sync_api import sync_playwright
import csv
from selectolax.parser import HTMLParser
import os


def extract_book_info(page, book_link):

    try:
        page.goto(book_link)
        page.wait_for_selector('.widget-title')


        tree = HTMLParser(page.content())
        divs = tree.css('.wrap')


        book_title = book_type = author = publisher = price = year = "N/A"

        for i in divs:
            book_title = i.css_first('.widget-title').text() if i.css_first(
                '.widget-title') else "N/A"
            book_type = i.css_first('h6:nth-child(6) > a').text() if i.css_first(
                'h6:nth-child(6) > a') else i.css_first(
                'h6:nth-child(5) > a').text() if i.css_first('h6:nth-child(5) > a') else 'N/A'

            author = i.css_first('h6:nth-child(3) > a').text() if i.css_first(
                'h6:nth-child(3) > a') else "N/A"
            publisher = i.css_first('h6:nth-child(4) > a').text() if i.css_first(
                'h6:nth-child(4) > a') else "N/A"
            price = i.css_first('.price').text() if i.css_first('.price') else "N/A"
            year = i.css_first('h6:nth-child(9) > a').text() if i.css_first('h6:nth-child(9) > a') else i.css_first(
                'h6:nth-child(8) > a').text() if i.css_first('h6:nth-child(8) > a') else 'N/A'

        return book_title, book_type, author, publisher, price, year

    except Exception as e:
        print(f"Error extracting book info from {book_link}: {e}")
        return "Error", "Error", "Error", "Error", "Error", "Error"


def main():

    start_link = 'https://www.noolulagam.com/product/?pid=49177'

    try:

        output_file = 'new_books_info.csv'


        file_exists = os.path.exists(output_file)
        file_empty = not file_exists or os.stat(output_file).st_size == 0


        with open('books.csv', mode='r', encoding='utf-8') as infile, \
             open(output_file, mode='a+', newline='', encoding='utf-8') as outfile:

            writer = csv.writer(outfile)


            if file_empty:
                writer.writerow(['நூல் பெயர்', 'வகை', 'எழுத்தாளர்', 'பதிப்பகம்', 'விலை', 'ஆண்டு'])  # Column headers

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()


                reader = csv.reader(infile)
                next(reader)
                start_processing = False

                for row in reader:
                    title, link = row


                    if link == start_link:
                        start_processing = True
                        print(f"Starting to scrape from the link: {link}")

                    if start_processing:
                        print(f"Visiting {title}: {link}")

                        try:
                            book_info = extract_book_info(page, link)


                            writer.writerow(book_info)
                            print(f"Extracted info for {book_info[0]}")

                        except Exception as e:
                            print(f"Error processing link {link}: {e}")
                            writer.writerow(["Error", "Error", "Error", "Error", "Error", "Error"])  # Write error row

                browser.close()

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except csv.Error as csv_error:
        print(f"CSV error: {csv_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
