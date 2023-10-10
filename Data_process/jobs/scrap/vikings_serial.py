import re


from Data_process.helper.helper import get_selenium_driver, get_config, get_dom, csv_load, get_img, \
    download_image_to_bytes
from Data_process.logger import LOGGER


def processing_jobs(items, browser):
    """Getting data from groups"""
    CONFIG = get_config()
    main_lst = []
    for hero in items:
        group_dict = {}
        href = hero.find("a").get("href")
        img = hero.find("img").get("src")
        hero_name = hero.find("div", class_="details").find("strong").text.strip()
        pattern = r'Played by (.+)'
        match = re.search(pattern, hero.find("div", class_="details").find("small").text.strip())
        if match:
            actor_name = match.group(1)

        actor_dom = get_dom(CONFIG['scraper']['vikings']['url']['MasterUrl'] + href, browser=browser)
        article = actor_dom.find('article', class_="main-article").text.strip()

        group_dict['main_url'] = CONFIG['scraper']['vikings']['url']['MasterUrl']
        group_dict['href'] = href
        group_dict['img_url'] = img
        group_dict['hero_name'] = hero_name
        group_dict['actor_name'] = actor_name
        group_dict['article'] = article
        group_dict['image_bytes'] = download_image_to_bytes(group_dict['img_url'])

        # Check image
        # image = Image.open(io.BytesIO(group_dict['Image_Bytes']))
        # image.show()

        main_lst.append(group_dict)

        save_directory = CONFIG['scraper']['vikings']['imgPath']
        get_img(img, save_directory, actor_name)

    return main_lst


def main_vikings():
    browser = get_selenium_driver()
    CONFIG = get_config()
    dom = get_dom(
        url=CONFIG['scraper']['vikings']['url']['MasterUrl'] + CONFIG['scraper']['vikings']['url']['heroesUrl'],
        browser=browser)
    block = dom.find("div", class_='main-content center-content full-width')
    heroes = block.find_all("li", class_='')
    data = processing_jobs(heroes, browser)
    csv_load(data, CONFIG['scraper']['vikings']['filePath'])


if __name__ == "__main__":
    LOGGER.info("Starting process")
    main_vikings()
