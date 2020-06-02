# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import re
from dicttoxml import dicttoxml
import csv

page = None

html = urlopen('https://www.placardefutebol.com.br/')
page = BeautifulSoup(html, 'lxml')
res = page

titles = page.find_all('h3', class_ = 'match-list_league-name')
championships = page.find_all('div', class_ = 'container content')

csv_columns = ['match', 'status', 'league', 'scoreboard', 'summary', 'start-in']
csv_file = open("crawres.csv", "w", encoding = "utf-8", newline = "")
writer = csv.DictWriter(csv_file, fieldnames = csv_columns)
writer.writeheader()

results = []

for id, championship in enumerate(championships):
    matchs = championship.find_all('div', class_ = 'row align-items-center content')

    for match in matchs:
        status = match.find('span', class_ = 'status-name').text
        teams = match.find_all('div', class_ = 'team-name')
        scoreboard = match.find_all('span', class_ = 'badge badge-default')

        team_home = teams[0].text.strip()
        team_visitor = teams[1].text.strip()

        info = {
            'match': '{} x {}'.format(team_home, team_visitor),
            'status': status,
            'league': titles[id].text
        }

        score = {}


        # Se o jogo já começou então existe placar
        try:
            score['scoreboard'] = {
                team_home: scoreboard[0].text,
                team_visitor: scoreboard[1].text
            }
            score['summary'] = '{} x {}'.format(scoreboard[0].text, scoreboard[1].text)

            # Caso não tenha começado, armazeena o horário de início
        except:
            score['start-in'] = status
            score['status'] = 'EM BREVE'

        info.update(score)
        results.append(info)

        writer.writerow(info)
        
csv_file.close()