from selenium import webdriver
# from bs4 import BeautifulSoup
# import requests
# import time


class Database:
    def __init__(self, connection_name):
        self.connection = connection_name
        self.database = None


class Team:
    def __init__(self):
        self.initial_points = 100
        self.available_points = 100
        self.team = {'Goalkeepers': [],
                     'Defenders': [],
                     'Midfielders': [],
                     'Forwards': []}
        self.max_gk_len = 2
        self.max_def_len = 5
        self.max_mid_len = 5
        self.max_fwd_len = 3


def extract_name(element):
    return element.find_element_by_css_selector("div[class='ElementInTable__Name-y9xi40-1 bsSrWV']").text


def extract_position(element):
    return element.find_element_by_css_selector("div[class='Media__Body-sc-94ghy9-2 kjxYPi']").\
            find_elements_by_css_selector("span")[1].text


def extract_price(element):
    return element.find_elements_by_css_selector("td")[2].text


def extract_points(element):
    return element.find_elements_by_css_selector("td")[-1].text


def add_metric(obj, metric_css, metric):
    obj.choose_new_metric(f'{metric_css}')
    obj.get_player_specific(f'{metric_css}')
    obj.next_page(0)
    for i in range(19):
        obj.get_player_specific(f'{metric}')
        obj.next_page()
        obj.get_player_specific(f'{metric}')


class PageScraper:
    def __init__(self):
        self.rootURL = None
        self.driver = webdriver.Chrome()
        self.players = dict()

    def open_root_url(self):
        """Open the root URL page to begin scraping from."""
        self.driver.get(self.rootURL)

    def next_page(self, opt=1):
        """Click next page button."""
        buttons = self.driver.find_elements_by_css_selector("button[class='PaginatorButton__Button-xqlaki-0 lgWpws']")
        buttons[opt].click()

    def get_player_base_info(self):
        """"""
        player_elements = self.driver.\
            find_elements_by_css_selector("tr[class='ElementTable__ElementRow-sc-1v08od9-3 kfPHcJ']")

        player_names = [extract_name(p) for p in player_elements]
        player_positions = [extract_position(p) for p in player_elements]
        player_prices = [extract_price(p) for p in player_elements]
        player_points = [extract_points(p) for p in player_elements]

        players = zip(player_names, player_positions, player_points, player_prices)
        for p in players:
            self.players[p[0]] = {'Position': p[1], 'Points': int(p[2]), 'Cost': p[3]}

    def get_player_specific(self, metric):
        player_elements = self.driver.\
            find_elements_by_css_selector("tr[class='ElementTable__ElementRow-sc-1v08od9-3 kfPHcJ']")

        player_names = [extract_name(p) for p in player_elements]
        specs = [extract_points(p) for p in player_elements]

        info = zip(player_names, specs)
        for p in info:
            self.players[p[0]][f'{metric}'] = p[1]

    def choose_new_metric(self, metric):
        elem = self.driver.\
            find_elements_by_css_selector("select[class='FieldRenderers__Select-sc-1qxt7mw-7 dBadbV']")[1]
        metric_elem = elem.find_element_by_css_selector(f"option[value={metric}]")
        metric_elem.click()


test = PageScraper()
test.rootURL = 'https://fantasy.premierleague.com/statistics'
test.open_root_url()

test.get_player_base_info()
test.next_page(0)
for i in range(19):
    test.get_player_base_info()
    test.next_page()
test.get_player_base_info()

add_metric(test, 'event_points', 'Round Points')
add_metric(test, 'influence', 'Influence')

print(test.players['Rashford'])
print(test.players['De Bruyne'])
print(test.players['Fernandes'])
