import csv
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser


def main():
    # Prepare the CSV file to store the data
    with open('books.csv', mode='w+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])  # Write the headers

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)

                # Create a new page and set custom headers
                page = browser.new_page()


                # Go to the URL
                page.goto('https://www.noolulagam.com/tamil-books/page/2094/?sortby&view') # https://www.noolulagam.com/books/?sortby&view=grid
                page.wait_for_selector('.page-numbers')

                while True:
                    try:
                        tree = page.content()
                        divs = HTMLParser(tree)
                        div = divs.css('.product')

                        print(f'Found {len(div)} products on the current page.')

                        for i in div:
                            try:
                                link = i.css_first('a').attributes['href']
                                title = i.css_first('a').text()

                                # Write the title and link to the CSV file
                                writer.writerow([title, link])

                                print(f"Title: {title} | Link: {link}")

                            except Exception as e:
                                print(f"Error extracting data for an item: {e}")

                        # Click to next page
                        try:
                            next_page_button = page.locator('a:has-text("→")').first
                            if not next_page_button:
                                print("No more pages found.")
                                break

                            next_page_button.click()
                            page.wait_for_selector('//*[@id="post-95"]/div/div[3]/span[4]/nav/ul/li[7]/a',
                                                   timeout=4000)
                        except Exception as e:
                            print(f"Error navigating to the next page: {e}")
                            break

                    except Exception as e:
                        print(f"Error parsing the page: {e}")
                        break

            except Exception as e:
                print(f"Error launching browser or loading page: {e}")

            finally:
                browser.close()


if __name__ == "__main__":
    main()
