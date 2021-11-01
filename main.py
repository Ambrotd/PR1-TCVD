from helpers import *
import time
import ssl
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN
from selenium import webdriver

USE_NORDVPN = True
if USE_NORDVPN:
    ssl._create_default_https_context = ssl._create_unverified_context
    settings = initialize_VPN(save=1, area_input=['complete rotation'])
    rotate_VPN(settings, google_check=1)


def get_property(id_property, proxies=None):

    url_in = f"https://www.idealista.com/inmueble/{id_property}/"
    # Headers from the browser to avoid been block
    headers = get_headers()
    # proxies = get_proxy()
    #random_time()
    try:
        r = requests.get(url_in, headers=headers, proxies=proxies)
        print(f"[*] Getting data from property_id {id_property} ->{r}")
    except:
        print("connection failure")
        r = 403
    if r.status_code == 200:
        soup = bs(r.text, 'lxml')
        listing = soup.find("span", {"class": "main-info__title-main"}).text
        location = soup.find("span", {"class": "main-info__title-minor"}).text
        # price as int
        price = int(
            soup.find("div", {"class": "info-data"}).find("span", {"class": "info-data-price"}).text.replace(".",
                                                                                                             "").replace(
                "€", ""))
        # price before discount not always exists
        try:
            price_before = int(
                soup.find("div", {"class": "info-data"}).find("span", {"class": "pricedown_price"}).text.replace(".",
                                                                                                                 "").replace(
                    "€", ""))
            discount = soup.find("div", {"class": "info-data"}).find("span",
                                                                     {"class": "pricedown_icon icon-pricedown"}).text
        except:
            print("Not Discounted")
            price_before = 0
            discount = "0%"
        try:
            attributes = soup.find("div", {"class": "info-features"}).find_all("span")
            meters = attributes[1].text
            rooms = attributes[3].text
        except:
            meters = 0
            rooms = 0
        try:
            if "Garaje" not in attributes[5].text:
                floor = attributes[5].text
                garage = ""
            else:
                garage = attributes[5].text
                floor = ""
        except:
            floor = ""
            garage = ""
        try:
            description = soup.find("div", {"class": "comment"}).find("p").text[1:-1]
        except:
            description = ""
        sq_meter_price = soup.find("p", {"class": "flex-feature squaredmeterprice"}).text.split('\n')[2]
        data = [id_property, listing, location, price, price_before, discount, meters, sq_meter_price, rooms, floor, garage, description]
        # print(listing, location, price, price_before, discount, meters, rooms, floor)
        print(data)
        return data


def get_zones(map_location, proxies=None):
    search_location = map_location
    url_search = f"https://www.idealista.com/venta-viviendas/{search_location}/"
    zones = []
    retries = 1
    while True:
        #random_time()
        try:
            # We need selenium for interacting with the js of the page
            driver = webdriver.Chrome(executable_path="driver/chromedriver.exe")
            driver.get(f"{url_search}mapa")
            element = driver.find_element_by_id("sublocations-showall-btn").click()
            time.sleep(1)
            print(f"[+] getting zones from {search_location}")
        except:
            print("Connection failure")
        soup = bs(driver.page_source, "lxml")
        find_zones = soup.find('div', {"id": "dynamicDialogContainer"}).find('ul', {"id": "sublocations"}).find_all("a")
        #print(find_zones)
        for zone in find_zones:
            link = zone.get('href')
            #print(link)
            zones.append(re.findall(r'/venta-viviendas/(.*?)/mapa', link))

        if len(zones) != 0:
            break
        else:
            retries += 1
            if retries == 3:
                if USE_NORDVPN:
                    try:
                        rotate_VPN(settings, google_check=1)
                    except:
                        print("Something went wrong with the VPN")
                    retries = 1
                else:
                    break
        driver.quit()
    return zones[1:]


def search_module(location, start, end, proxies=None):
    search_location = location
    url_search = f"https://www.idealista.com/venta-viviendas/{search_location}/"
    print(url_search)
    i = start
    last = end
    listing_ids = []
    retries = 1
    while True:
        headers = get_headers()
        #random_time()
        try:
            r = requests.get(f"{url_search}pagina-{i}.htm", headers=headers, proxies=proxies)
            print(f"[+] getting listings from {location} page {i} -> {r}")
        except:
            print("Connection failure")
            r = 403
        if r.status_code == 200:
            retries = 1
            soup = bs(r.text, "lxml")
            # print(soup1)
            current_page = int(soup.find("div", {"class": "pagination"}).find("li", {"class": "selected"}).text)
            #print(f"Current page -> {current_page}, i -> {i} last -> {last}")
            if current_page == i and current_page != last:
                articles = soup.find("main", {"class": "listing-items"}).find_all("article")
                for article in articles:
                    id_inmueble = article.get("data-adid")
                    if id_inmueble != None:
                        listing_ids.append(id_inmueble)
                    # print(id_inmueble)
                # Increasing the page
                i += 1
            else:
                # print(listing_ids)
                break
        else:
            retries += 1
            if retries == 3:
                if USE_NORDVPN:
                    try:
                        rotate_VPN(settings, google_check=1)
                    except:
                        print("Something went wrong with the VPN")
                    retries = 1
                else:
                    break

    return listing_ids


def main():

    csv_name = "madrid"
    create_csv(csv_name)
    zones = get_zones("madrid-provincia")
    for zone in zones:
        start = 1
        end = start + 60
        listing_ids = search_module(zone[0], start, end)
        print(f"[*] List from Idealista {listing_ids}")
        id_csv = check_csv_list(csv_name)
        new_ids = remove_list_duplicates(listing_ids,id_csv)
        print(f"[*] List of new listings {new_ids}")
        for id_property in new_ids:
            success = False
            retries = 1
            while not success:
                if retries == 3:
                    if USE_NORDVPN:
                        try:
                            rotate_VPN(settings, google_check=1)
                        except:
                            print("Something went wrong with the VPN")
                    success = True
                    retries = 1
                data_prop = get_property(id_property)
                if data_prop != None:
                    success = True
                    append_csv(csv_name, data_prop)
                retries += 1
                # print(listing_ids)
    if USE_NORDVPN:
        terminate_VPN()




def test():
    #check_csv_list("test")
    #get_property("88315117")
    print(get_zones("madrid-provincia"))


if __name__ == "__main__":
    main()
