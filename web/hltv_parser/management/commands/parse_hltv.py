from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import regex
import requests
import time

from django.db import transaction

from hltv_parser.models import Team, Match, MatchVeto, Map, MatchMap, Tournament


class Command(BaseCommand):
    base_url = 'https://www.hltv.org/'

    def handle(self, *args, **options):
        for url in self._parse_matches_urls():
            with transaction.atomic():
                self._parse_match(url)

    def _parse_match(self, url):
        soup = self._get_html(url)
        match_id = url.split('/')[2]
        teams_soup = soup.find('div', {'class': 'teamsBox'})
        team1_soup, team2_soup = teams_soup.find_all('div', {'class': 'team'})
        team1 = self._parse_team(team1_soup)
        team2 = self._parse_team(team2_soup)

        tournament_soup = soup.find('div', {'class': 'event'})
        tournament_name = tournament_soup.find('a').text
        try:
            tournament = Tournament.objects.get(name=tournament_name)
        except Tournament.DoesNotExist:
            tournament = Tournament(name=tournament_name)
            tournament.save()
        score_soup = soup.find_all('div', class_=lambda c: c in ['won', 'lost'])
        result_team_1, result_team_2 = int(score_soup[0].text), int(score_soup[1].text)

        date = soup.find('div', {'class': 'date'}).text

        match_veto_soup = soup.find_all('div', {'class': 'veto-box'})
        match_type_soup = soup.find_all('div', {'class': 'veto-box'})[0].text.split('\n')
        match_type_new = [value for value in match_type_soup if value != '']
        match_type = match_type_new[0]

        if len(match_veto_soup) < 2:
            return
        match = Match(hltv_id=match_id, match_type=match_type, first_team=team1, second_team=team2,
                      first_team_score=result_team_1, second_team_score=result_team_2, match_date=date,
                      tournament=tournament)
        match.save()
        for line in match_veto_soup[1].text.split('\n'):
            if not line:
                continue
            match_veto_dict = regex.search(
                '^(?P<number>\d+)\. ((?P<team>.+) (?P<action>picked|removed) (?P<map>.+)|('
                '?P<map>.+) (?P<action>was left over))$', line).groupdict()
            if match_veto_dict['action'] == 'removed' and team1.name == match_veto_dict['team']:
                result = MatchVeto.RESULT.ban_team
            elif match_veto_dict['action'] == 'picked' and team1.name == match_veto_dict['team']:
                result = MatchVeto.RESULT.pick_team
            elif match_veto_dict['action'] == 'removed' and team2.name == match_veto_dict['team']:
                result = MatchVeto.RESULT.ban_enemy
            elif match_veto_dict['action'] == 'picked' and team2.name == match_veto_dict['team']:
                result = MatchVeto.RESULT.pick_enemy
            else:
                result = MatchVeto.RESULT.last
            try:
                map = Map.objects.get(name=match_veto_dict['map'])
            except Map.DoesNotExist:
                map = Map(name=match_veto_dict['map'])
                map.save()
            match_veto = MatchVeto(match=match, map=map, number_of_action=match_veto_dict['number'], result=result)
            match_veto.save()

        match_map_soup = soup.find_all('div', {'class': 'mapholder'})
        score_lst = []
        map_lst = []
        for element in match_map_soup:
            match_map_name = element.find_all('div', {'class': 'mapname'})
            for map in match_map_name:
                map_lst.append(map.text)
            match_map_score = element.find_all('div', {'class': 'results-team-score'})
            for score in match_map_score:
                score_lst.append(score.text)
        new_score_lst = ['{}-{}'.format(score_lst[i], score_lst[i + 1]) for i in range(0, len(score_lst), 2)]
        map_score_dict = dict(zip(map_lst, new_score_lst))
        for key, value in map_score_dict.items():
            if value != '---':
                match_map = MatchMap(match=match, map=Map.objects.get(name=key), score=value)
                match_map.save()

    def _parse_team(self, soup):
        team_id = soup.find('a', href=True)['href'].split('/')[2]
        team_name = soup.find('div', {'class': 'teamName'}).text
        team_logo = soup.find('img', src=True)['src']
        try:
            return Team.objects.get(hltv_id=team_id)
        except Team.DoesNotExist:
            team = Team(hltv_id=team_id, name=team_name, logo=team_logo)
            team.save()
            return team

    def _parse_matches_urls(self):
        soup = self._get_html('/results')
        match_urls = []
        for match_soup in soup.find_all('div', {'class': 'result-con'}):
            url = match_soup.find('a', href=True)['href']
            if Match.objects.filter(hltv_id=url.split('/')[2]).exists():
                break
            match_urls.append(url)
        return match_urls

    def _get_html(self, url):
        r = requests.get(self.base_url + url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }).text
        soup = BeautifulSoup(r, 'html.parser')
        time.sleep(0.5)
        return soup