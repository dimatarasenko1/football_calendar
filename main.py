import requests
from EloRatings import ClubElos
import numpy as np
import string

# This function will get elo rating of each club and plus them
def calculate_elo(club1, club2):
  fixture_rating = 0
  for club in club_elo_ratings_for_today:
    if club1 in club:
      club1_elo = club[1]
      break
    else:
      club2_elo = 0
  for club in club_elo_ratings_for_today:
    if club2 in club:
      club2_elo = club[1]
      break
    else:
      club2_elo = 0
  combined_elo = club1_elo + club2_elo   
  if club1_elo - club2_elo >= 200 or club2_elo - club1_elo >= 200:
    fixture_rating =  combined_elo * 0.95
  else: fixture_rating = combined_elo
  return fixture_rating   

# this will return the top 5 games in terms of total elos as a list of indices in the original list in receives.
def top_five(list_of_elos):
  pass

#parameters = {"team":value, "date": value}

elo_ratings_for_day = ClubElos()
club_elo_ratings_for_today = elo_ratings_for_day.get_elos()

response = requests.get("http://api.clubelo.com/Fixtures")
content = response.content
string_content = content.decode("utf-8")

#The api is set up in a way that \n acts as a delimiter for each fixture. Within fixtures, , is a delimiter. 
#The programme will create a list of lists where each fixture has a sub-list.
#The first list is the table headers that we can use to create a dictionary for most likely result. 
list_content = string_content.split("\n")
list_of_lists = []

for game in list_content:
  game_list = game.split(",")
  list_of_lists.append(game_list)

# Save results from calculate_elo to a list with same indices as the corresponding fixture in list_of_lists. 
dict_keys = list_of_lists[0]
probability_keys = dict_keys[4:]
result_prob_keys = probability_keys[:13]
list_of_lists = list_of_lists[1:-3]
elo_list = []
game_counter = 0

print(probability_keys)

for lst in list_of_lists:
  home_team = lst[2]
  away_team = lst[3]
  total_elo = calculate_elo(home_team, away_team)
  elo_list.append(total_elo)
  game_counter += 1 

#top_five_games_indices = top_five(elo_list)

print(game_counter)
arr = np.array(elo_list)
top_indices = arr.argsort()[-5:][::-1]

for index in top_indices:
  match = list_of_lists[index]
  match_only = match [:4]
  match_probs = match[4:]
  float_probabilities = []
  print(match_only)
  for prob in match_probs:
    float_probabilities.append(float(prob))

    home_win = 0
    away_win = 0
    draw = 0
    #print(float_probabilities)
    prob_dict = dict(zip(result_prob_keys, float_probabilities))
    #print(prob_dict)
  for i in prob_dict:
    if "-" in i:
      away_win += prob_dict.get(i, 0)
    elif i == "GD=0":
      draw += prob_dict.get(i, 0)
    else:
      home_win += prob_dict.get(i, 0)
  likely_result = max([home_win, away_win, draw])
  exp_result_dirty = np.argwhere([home_win, away_win, draw] == np.amax([home_win, away_win, draw]))
  games_results = exp_result_dirty.flatten().tolist()
  #print(games_results)
  if likely_result == draw:
    print("draw")
  elif likely_result == home_win:
    print("home")
  elif likely_result == away_win:
    print("away")

  



  #most_likely_result_dirty = np.argwhere(float_probabilities == np.amax(float_probabilities))
 # most_likely_result_index = most_likely_result_dirty.flatten().tolist()
 # most_likely_result = []
  #for index in most_likely_result_index:
  #  most_likely_result.append(probability_keys[index])
   
 # print(most_likely_result)

