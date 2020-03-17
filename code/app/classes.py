from selenium import webdriver
# from bs4 import BeautifulSoup
# import requests
# import time


class PageScraper:
    def __init__(self):
        self.rootURL = None
        self.driver = webdriver.Chrome()
        self.players = dict()

    def open_root_url(self):
        self.driver.get(self.rootURL)

    def get_player_points(self):
        player_elements = self.driver.\
            find_elements_by_css_selector("tr[class='ElementTable__ElementRow-sc-1v08od9-3 kfPHcJ']")
        player_name_elements = [p.find_element_by_css_selector("div[class='ElementInTable__Name-y9xi40-1 bsSrWV']")
                                for p in player_elements]
        player_point_elements = [p.find_elements_by_css_selector("td")[-1]
                                 for p in player_elements]
        player_names = [p.text for p in player_name_elements]
        player_points = [p.text for p in player_point_elements]

        players = zip(player_names, player_points)
        for p in players:
            self.players[p[0]] = {'Points': p[1]}




test = PageScraper()
test.rootURL = 'https://fantasy.premierleague.com/statistics'
test.open_root_url()
test.get_player_points()
