import pandas as pd
import warnings
import streamlit as st
warnings.filterwarnings("ignore")


def ipl_top_players(playing):
    bat = pd.read_csv("bat.csv")
    bowl = pd.read_csv("bowl.csv")

    match_type = 'IPL'
    ipl_bat = bat[bat['Type'] == match_type]
    ipl_bowl = bowl[bowl['Type'] == match_type]

    # print(ipl_bat['Team'].unique())
    # print(ipl_bowl['Team'].unique())

    point = {"6s": 2, "50": 8, "100": 16, "200": 32,
             "Wkts": 25, "4W": 8, "5W": 16, "10W": 32}

    bat_data = ipl_bat[['Player', 'Team', 'Runs',
                        'BF', 'SR', '4s', '6s', '50', '100', '200']]
    bowl_data = ipl_bowl[['Player', 'Wkts', 'Econ', 'B', '5W', '10W']]

    players = pd.merge(bat_data, bowl_data, how='outer', on='Player')
    # print(players.head())

    players['Batting Points'] = players['Runs'] + players['4s'] + players['6s']*point['6s'] + \
        players['50']*point['50'] + players['100'] * \
        point['100'] + players['200']*point['200']
    players['Bowling Points'] = players['Wkts']*point['Wkts'] + \
        players['5W']*(point['4W'] + point['5W']) + players['10W']*point['10W']

    for i in range(len(players)):
        sr = players.iloc[i]['SR']
        bf = players.iloc[i]['BF']
        b = players.iloc[i]['B']
        if sr < 50:
            players.iloc[i]['Batting Points'] += (-6) * (bf / 100)
        elif sr >= 50 and sr < 60:
            players.iloc[i]['Batting Points'] += (-4) * (bf / 100)
        elif sr >= 60 and sr <= 70:
            players.iloc[i]['Batting Points'] += (-2) * (bf / 100)
        eco = players.iloc[i]['Econ']
        if eco > 11:
            players.iloc[i]['Bowling Points'] += (-6) * (b / 6)
        elif eco <= 11 and eco > 10:
            players.iloc[i]['Bowling Points'] += (-4) * (b / 6)
        elif eco <= 10 and eco >= 9:
            players.iloc[i]['Bowling Points'] += (-2) * (b / 6)
        elif eco <= 6 and eco >= 5:
            players.iloc[i]['Bowling Points'] += 2 * (b / 6)
        elif eco < 5 and eco >= 4:
            players.iloc[i]['Bowling Points'] += 4 * (b / 6)
        elif eco < 4:
            players.iloc[i]['Bowling Points'] += 6 * (b / 6)

    players['Total Points'] = players['Batting Points'] + \
        players['Bowling Points']
    # print(players.head())

    df = players[['Player', 'Team', 'Batting Points',
                  'Bowling Points', 'Total Points']]
    # print(df.head())

    df_playing = df[df['Player'].isin(playing)]

    bat_rankings = df_playing.sort_values(by='Batting Points', ascending=False).reset_index(
        drop=True)[['Player', 'Team', 'Batting Points']]
    # print("Top 3 Batters: ")
    # print(bat_rankings.head(3))

    bowl_rankings = df_playing.sort_values(by='Bowling Points', ascending=False).reset_index(
        drop=True)[['Player', 'Team', 'Bowling Points']]
    # print("Top 3 Bowlers: ")
    # print(bowl_rankings.head(3))

    net_rankings = df_playing.sort_values(by='Total Points', ascending=False).reset_index(
        drop=True)[['Player', 'Team', 'Total Points']]
    # print("Top 3 All-Rounders: ")
    # print(net_rankings.head(3))

    return bat_rankings.head(3), bowl_rankings.head(3), net_rankings.head(3)


# playing = []
# n = int(input("Enter number of players you want to select: "))
# print("Enter the names of " + str(n) + " players playing today: ")
# for i in range(n):
#     playing.append(input("Player " + str(i+1) + ": "))
# bat, bowl, net = ipl_top_players(playing)
# print("\nTop 3 Batters: ")
# print(bat)
# print("\nTop 3 Bowlers: ")
# print(bowl)
# print("\nTop 3 All-Rounders: ")
# print(net)

playing = []
st.title("IPL Expert Predictor")
st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
n = st.text_input("Enter number of players you want to select: ")
if n:
    with st.spinner("Browsing through Statistics..."):
        n = int(n)
        st.markdown("Enter the names of " + str(n) +
                    " players playing today: ")
        for i in range(n):
            playing.append(st.text_input("Player " + str(i+1) + ": "))
        bat, bowl, net = ipl_top_players(playing)
        st.markdown("\nTop 3 Batters: ")
        st.write(bat)
        st.markdown("\nTop 3 Bowlers: ")
        st.write(bowl)
        st.markdown("\nTop 3 All-Rounders: ")
        st.write(net)
