import requests
import datetime

class ClubElos:
  def __init__(self):
    self.today = datetime.datetime.today().strftime('%Y-%m-%d')
    self.club_list = self.get_elos()

  def get_elos(self):
    response = requests.get("http://api.clubelo.com/" + self.today)
    content = response.content
    string_content = content.decode("utf-8")
    list_content = string_content.split("\n")
    list_content = list_content[1:-3]
    lists_in_list = []
    for item in list_content:
     clean_items = item.split(",")
     lists_in_list.append(clean_items)

    cleaned_content = []
    for item in lists_in_list:
      clean_item = [item[1], int(float(item[4]))]
      cleaned_content.append(clean_item)
    return cleaned_content
      
    