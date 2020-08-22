from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

app = Flask(__name__)

apikey = os.environ['LoL-API-KEY']


#
# url = 'https://www.op.gg/summoner/userName=' + Name
# req = requests.get(url, headers=hdr)
# html = req.text
# soup = BeautifulSoup(html, 'html.parser')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def data():
    sum_name = request.args.get('name')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": apikey
    }
    url_SummonerName = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
    res_SummonerName = requests.get(url=url_SummonerName, headers=headers)
    account_Id = res_SummonerName.json()['accountId']  # account Id 가져오기
    encryptedSummonerId = res_SummonerName.json()['id']  # encryptedId 가져오기

    url_Matches = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(account_Id)
    res_Matches = requests.get(url=url_Matches, headers=headers)
    matches = res_Matches.json()['matches']

    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(encryptedSummonerId)
    res_league = requests.get(url=url_league, headers=headers)
    user_infos = res_league.json()

    print(user_infos)
    print('-------------------------------')

    url_Mastery = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}".format(
        encryptedSummonerId)
    res_Mastery = requests.get(url=url_Mastery, headers=headers)
    user_masteries = res_Mastery.json()

    print(user_masteries)
    print('-------------------------------')

    def get_champ_mastery(user_mastery):
        resp_mastery = [
            user_mastery.get('championId'),
            user_mastery.get('championLevel'),
            user_mastery.get('championPoints'),
            user_mastery.get('championPointsUntilNextLevel'),
        ]
        return resp_mastery

    results_champ_mastery = []
    for user_mastery in user_masteries:
        results_champ_mastery.append(get_champ_mastery(user_mastery))
    length_champ_mastery = len(results_champ_mastery)

    print(results_champ_mastery)
    print('-------------------------------')

    def get_user_info(user_info):
        resp_user_info = [
            user_info.get('queueType'),
            user_info.get('tier'),
            user_info.get('rank'),
            user_info.get('wins'),
            user_info.get('losses'),
            user_info.get('leagueName'),
            user_info.get('leaguePoints')
        ]

        return resp_user_info

    results_user_info = []
    for user_info in user_infos:
        results_user_info.append(get_user_info(user_info))
    length_user_info = len(results_user_info)

    Game_Ids = []
    Match_list = []
    for match in range(0, 20):
        Game_Ids.append(matches[match].get('gameId'))
        Match_list.append(matches[match])

    url_MatchId = "https://kr.api.riotgames.com/lol/match/v4/matches{}".format(Game_Ids[0])
    res_MatchId = requests.get(url=url_MatchId, headers=headers)

    result_list = []
    player_list = []
    teams_list = []

    for gameid in Game_Ids:
        url_gameId = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameid)
        res_gameId = requests.get(url_gameId, headers=headers)
        data = res_gameId.json()
        players = res_gameId.json()["participants"]
        teams = res_gameId.json()['teams']
        result = "패배"
        if (data["teams"][0]["win"] == "Fail"):
            for i in range(5, 10):
                if (data["participantIdentities"][i]["player"]["summonerName"].replace(" ", "").lower() == sum_name):
                    result = "승리"
        if (data["teams"][0]["win"] == "Win"):
            for i in range(0, 5):
                if (data["participantIdentities"][i]["player"]["summonerName"].replace(" ", "").lower() == sum_name):
                    result = "승리"

        result_list.append(result)
        player_list.append(players)
        teams_list.append(teams)

    print(teams_list)

    # print(result_list) // 승리 패배만 뽑아줌

    return render_template('search.html', sum_name=sum_name, Game_Ids=Game_Ids, Match_list=Match_list,
                           player_list=player_list, teams_list=teams_list, results_user_info=results_user_info,
                           results_champ_mastery=results_champ_mastery, length_champ_mastery=length_champ_mastery,
                           length_user_info=length_user_info)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
