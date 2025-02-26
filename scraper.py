import re
from playwright.sync_api import sync_playwright
import pandas as pd

url = "https://www.sreality.cz/hledani/byty/praha"

data = []

with sync_playwright() as p:
    print("Launching new browser")
    browser = p.chromium.launch() 
    page = browser.new_page()
    print("Redirecting to URL")
    page.goto(url) 

    print("Loading page")
    page.wait_for_load_state() 
    page.wait_for_timeout(1000)

    consent = page.locator("button", has_text = "Souhlasím")
    consent.wait_for(state="visible")

    page.screenshot(path="first_ss.png",full_page=True)

    if consent:
        consent.click(force=True)
        page.wait_for_timeout(2000)
        page.screenshot(path="second_ss.png",full_page=True)

    def extract_apartments():
        apartments = page.query_selector_all("div.css-18g5ywv")
        print(f"{len(apartments)} Apartments fetched")
        page.screenshot(path="third ss.png",full_page=True)


        for apartment in apartments:
            title = apartment.query_selector("p.css-d7upve:nth-child(1)").text_content()
            location = apartment.query_selector("p.css-d7upve:nth-child(2)").text_content()
            price = apartment.query_selector("p.css-ca9wwd").text_content()
        
            if 'Pronájem' in title:
                type = 'For Rent'
                match_price = re.search(r"(\d+\s?\d+)", price)

                
                if match_price:
                    price = match_price.group().replace("\xa0", "").replace(" ", "")
                else:
                    price = None

                if price and price.isdigit():
                    price = int(price)
                else:
                    price = 0


            elif 'Prodej' in title:
                type = 'For Sale'
                match_price = re.search(r"[\d\s]+",price)
                
                if match_price:
                    price = match_price.group().replace("\xa0", "").replace(" ", "")
                else:
                    price = None

                if price and price.isdigit():
                    price = int(price)
                else:
                    price = 0
            
            match_location = re.search("(?<=-\s).*$",location)

            if match_location:
                district = match_location.group()
            else:
                district = None

            match_title = re.search("(\d+\+\w+)\s+(\d+)\s*m²",title)

            if match_title:
                layout = match_title.group(1) 
                area = match_title.group(2)

            data.append({
            "Title": title,
                "Location": location,
                "District": district,
                "Property Type": type,
                "Price CZK": price,
                "Layout": layout,
                "Area M2": area,
            })
                
            
    for page_number in range(0,101):
        print(f"Scraping page {page_number}")

        extract_apartments()

        next_page_button = page.locator("button",has_text="Další stránka")
        next_page_button.wait_for(state="visible")
        next_page_button.scroll_into_view_if_needed()

        if next_page_button.is_visible():    
            next_page_button.click(force=True)
            page.wait_for_timeout(2000)
        else:
            print("no more pages")
            break


    browser.close()

df = pd.DataFrame(data)

df.to_csv("prague_apartments.csv")

print(df)
