from pybaseball import statcast_batter, spraychart
from pybaseball import playerid_lookup
from pybaseball import statcast



#data = statcast_batter('2024-03-20', '2024-10-30', 592450)
#sub_data = data[data['home_team'] == 'NYY']
#spraychart(sub_data, 'yankees', title='Judge: 2024 Season')


data = statcast("2024-10-30", team="NYY")

print(list(data['pitch_type']))