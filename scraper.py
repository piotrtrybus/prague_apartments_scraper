import re
from playwright.sync_api import sync_playwright

url = "https://www.sreality.cz/hledani/byty/praha"

with sync_playwright() as p:
    print("Launching new browser")
    browser = p.chromium.launch() 
    page = browser.new_page()
    print("Redirecting to URL")
    page.goto(url) 

    print("Loading page")
    page.wait_for_load_state() 
    page.wait_for_timeout(1000)

    print("Getting the label")
    intro_page = page.locator("button", has_text = "Souhlasím")
    intro_page.click()
    page.wait_for_timeout(2000)

    #page.wait_for_timeout(2000)
    products_1 = page.query_selector_all("div.MuiBox-root.css-56t0k4")
    print(f"{len(products_1)} Products fetched")

    for product in products_1:
        title = product.query_selector("p.MuiTypography-root.MuiTypography-body1.css-1cww02:nth-child(1)").text_content()
        location = product.query_selector("p.MuiTypography-root.MuiTypography-body1.css-1cww02:nth-child(2)").text_content()
        if 'Pronájem' in title:
            type = 'For Rent'
        elif 'Prodej' in title:
            type = 'For Sale'
        price = product.query_selector("p.MuiTypography-root.MuiTypography-body1.css-c8gwq8").text_content()
        print(title)
        print(location)
        print(type)
        print(price)
    
    next_page_button = page.locator("button",has_text="Další stránka")
    next_page_button.wait_for(state="visible")
    next_page_button.scroll_into_view_if_needed()
    print(next_page_button)
    print("Found next page button")
    next_page_button.click(force=True)
    print("Next page button clicked")
    page.wait_for_timeout(2000)

    products_2 = page.query_selector_all("div.MuiBox-root.css-56t0k4")
    print(f"{len(products_2)} Products fetched")
     
    for product in products_2:
        title = product.query_selector("p.MuiTypography-root.MuiTypography-body1.css-1cww02:nth-child(1)").text_content()
        location = product.query_selector("p.MuiTypography-root.MuiTypography-body1.css-1cww02:nth-child(2)").text_content()
        if 'Pronájem' in title:
            type = 'For Rent'
        elif 'Prodej' in title:
            type = 'For Sale'
        price = product.query_selector("p.MuiTypography-root.MuiTypography-body1.css-c8gwq8").text_content()
        print(title)
        print(location)
        print(type)
        print(price)

