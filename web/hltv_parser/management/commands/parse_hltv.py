from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup
from traceback import print_exc
import requests
import time

from hltv_parser.models import Team, Match


class Command(BaseCommand):
    base_url = 'https://www.hltv.org/'

    def handle(self, *args, **options):
        for url in self._parse_matches_urls():
            self._parse_match(url)

    def _parse_veto(self):
        pass

    def _parse_match(self, url):
        soup = self._get_html(url)
        match_id = url.split('/')[2]
        teams_soup = soup.find('div', {'class': 'teamsBox'})
        team1_soup, team2_soup = teams_soup.find_all('div', {'class': 'team'})
        team1 = self._parse_team(team1_soup)
        team2 = self._parse_team(team2_soup)

        tournament = soup.find('event').text

        match_type = soup.find_all('div', {'class': 'veto-box'})[0].split('\n')[0]

        score_soup = soup.find_all('div', class_=lambda c: c in ['won', 'lost'])
        result_team_1, result_team_2 = int(score_soup[0].text), int(score_soup[1].text)

        date = soup.find('date')
        try:
            return Match.objects.get(hltv_id=match_id)
        except:
            match = Match(hltv_id=match_id, match_type=match_type, first_team=team1, second_team=team2,
                          first_team_score=result_team_1, second_team_score=result_team_2, match_date=date,
                          tournament=tournament)
            match.save()
            return match

    def _parse_team(self, soup):
        team_id = soup.find('a', href=True)['href'].split('/')[2]
        team_name = soup.find('div', {'class': 'teamName'}).text
        try:
            return Team.objects.get(hltv_id=team_id)
        except Team.DoesNotExist:
            team = Team(hltv_name=team_id, name=team_name)
            team.save()
            return team

    def _parse_matches_urls(self):
        soup = self._get_html('/results')
        match_urls = []
        for match_soup in soup.find_all('div', {'class': 'result-con'}):
            match_urls.append(match_soup.find('a', href=True)['href'])
        return match_urls[:3]

    def _get_html(self, url):
        r = requests.get(self.base_url + url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }).text
        soup = BeautifulSoup(r, 'html.parser')
        time.sleep(0.5)
        return soup
