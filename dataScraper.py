# needed libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def team_scores():

  final_scores = []
  frames = []
  # Loop through every year
  for year in range(1950,2023):
    # Get url for that year
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'
    table_html = BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = re.compile('advanced-team'))[0].findAll('a')
    team_name = []
    team_abrv = []
    # Loop through teams list and make list of abbreviations for each team from that year
    for html in table_html:
      abrv = html.get('href')
      pattern = re.compile(r'([A-Z]{3})')
      team_abrv.append(pattern.search(abrv).group())
      team_name.append(html.text)
    team_abrv = list(zip(team_name,team_abrv))
    team_abbrevation = [i[1] for i in team_abrv] # get list of team abbrevation
    # Loop through each team from that year
    for team in team_abbrevation:
      if (year == 1955 and team == 'BLB'):
        continue
      # Go to URL for that teams schedule from that year
      page = requests.get(f"https://www.basketball-reference.com/teams/{team}/{year}_games.html")
      soup = BeautifulSoup(page.content, 'html.parser')
      # Save all teams final scores
      team_score = soup.find_all('table', id='games')[0].find_all('td', {"data-stat": "pts"})
      opp_score = soup.find_all('table', id='games')[0].find_all('td', {"data-stat": "opp_pts"})
      teams = [pt.get_text() for pt in team_score]
      opponents = [pt.get_text() for pt in opp_score]
      for i in range(len(teams)):
        final_scores.append([teams[i],opponents[i]])
    myData = pd.DataFrame({
      "final_scores": final_scores
    })
  # Save to csv file
  frames.append(myData)
  final_data = pd.concat(frames)
  final_data.to_csv("all_scores.csv", index=False)

team_scores()