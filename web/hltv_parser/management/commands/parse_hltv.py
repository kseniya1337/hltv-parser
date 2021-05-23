from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import requests
import time


class Command(BaseCommand):

    def get_html(self, url):
        r = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        })
        return r.text

    def handle(self, *args, **options):
        url_results = 'https://www.hltv.org/results'

        response = self.get_html(url_results)
        soup = BeautifulSoup(response, 'html.parser')
        score = []
        for match_soup in soup.find_all('div', {'class': 'result-con'}):
            score_soup = match_soup.find('td', {'class': 'result-score'})
            first, second = score_soup.find_all('span')
            score.append(first.text+ '-'+second.text)
            # print(team_won)
        print(score)
        team_names = []
        for team_soup in soup.find_all('td', {'class': 'team-cell'}):
            team = team_soup.find('div', {'class': 'team'}).text
            team_names.append(team)
        print(team_names)


