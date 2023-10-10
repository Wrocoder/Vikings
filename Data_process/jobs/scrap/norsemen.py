import re

from Data_process.helper.helper import get_selenium_driver, get_config, get_dom, csv_load, get_img, \
    download_image_to_bytes
from Data_process.logger import LOGGER


def actors_proc(blocks, browser):
    CONFIG = get_config()
    main_info = []
    for actor in blocks:
        single_act = {'main_url': CONFIG['scraper']['norsemen']['url']['masterUrl'],
                      'href': actor.find('a')['href']}
        try:
            single_act['href_img'] = actor.find('img', class_='ipc-image')['src']
        except Exception as e:
            LOGGER.warning(e)

        actor_dom = get_dom(
            url=CONFIG['scraper']['norsemen']['url']['masterUrl'] + single_act['href'],
            browser=browser)

        href_element = actor_dom.find('a', {'class': 'ipc-overflowText-overlay', 'aria-label': 'See more'})
        actor_details = get_dom(
            url=CONFIG['scraper']['norsemen']['url']['masterUrl'] + href_element['href'], browser=browser)

        mini_bio_element = actor_details.find_all('div', {'class': 'ipc-html-content-inner-div'})
        actor_name = re.search(r'^(.+?) - Biography - IMDb$', actor_details.title.get_text()).group(1)
        single_act['actor_name'] = actor_name
        try:
            single_act['overview'] = mini_bio_element[0].get_text(strip=True)
            single_act['mini_bio'] = mini_bio_element[1].get_text(strip=True)
            single_act['add'] = mini_bio_element[2].get_text(strip=True)
        except Exception as e:
            LOGGER.warning(e)

        try:
            single_act['image_bytes'] = download_image_to_bytes(single_act['href_img'])
        except Exception as e:
            LOGGER.warning(e)

        if single_act.get('href_img') is not None:
            save_directory = CONFIG['scraper']['norsemen']['imgPath']
            get_img(single_act['href_img'], save_directory, single_act['actor_name'].replace(' ', '_'))

        LOGGER.info(single_act)
        main_info.append(single_act)

    return main_info


def main_norsemen():
    browser = get_selenium_driver()
    CONFIG = get_config()
    dom = get_dom(
        url=CONFIG['scraper']['norsemen']['url']['serialUrl'],
        browser=browser)
    block_act = dom.find("div",
                         class_='ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l '
                                'ipc-shoveler__grid')
    actors = block_act.find_all("div", class_='sc-bfec09a1-5 kUzsHJ')
    data = actors_proc(actors, browser)
    csv_load(data, CONFIG['scraper']['norsemen']['filePath'])


if __name__ == "__main__":
    LOGGER.info("Starting process")
    main_norsemen()
