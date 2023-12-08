from re import T
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, to_rgba
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv

teamOneScore = []
teamTwoScore = []

with open('all_scores.csv','r') as csvfile:
    lines = csv.reader(csvfile)
    next(csvfile)
    for row in lines:
        row[0] = row[0].split("'")
        teamOneScore.append(int(row[0][1]))
        teamTwoScore.append(int(row[0][3]))
difference = max(teamOneScore) - min(teamOneScore)
fig, ax = plt.subplots(tight_layout=True)
hist = ax.hist2d(teamOneScore, teamTwoScore, bins=difference, cmap='gist_heat_r')
fig.colorbar(hist[3], ax=ax)

path = []
for i in range(min(teamOneScore),max(teamOneScore) + 1):
    path.append([i,i])
    if (i != max(teamOneScore)):
        path.append([i,i+1])
path.append([max(teamOneScore),min(teamOneScore)])

tri=mpatches.Polygon(path, 
                        fill = True,
                        color = "black")
                        #color = "#D3D3D3")
plt.gca().add_patch(tri)
plt.title("NBA Score Outcomes")
plt.ylabel("Team 1")
plt.xlabel("Team 2")
  
plt.show()