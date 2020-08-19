from flask import Flask, render_template, request
import os
import requests
from pprint import pprint as pp

app = Flask(__name__)

apikey = os.environ['LoL-API-KEY']


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

    url_GameId = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(account_Id)
    res_GameId = requests.get(url=url_GameId, headers=headers)
    Matches = res_GameId.json()['matches']
    # match_Id = res_GameId.json()['gameId']

    # url_MatchId = "https://kr.api.riotgames.com/lol/match/v4/matches{}".format(match_Id)
    # res_MatchId = requests.get(url=url_MatchId, headers=headers)
    # Teams = res_GameId.json()['']
    Game_Ids = []
    Match_list = []
    for match in range(0, 20):
        Game_Ids.append(Matches[match].get('gameId'))
        Match_list.append(Matches[match])

    print(Match_list)
    print(Game_Ids)

    return render_template('search.html', sum_name=sum_name, Game_Ids=Game_Ids, Match_list=Match_list)


# @app.route('/data')
# def search():
#     sum_name = request.args.get('name')
#     url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
#     headers = {
#         "Origin": "https://developer.riotgames.com",
#         "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
#         "X-Riot-Token": apikey,
#         "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
#     }
#     res = requests.get(url=url, headers=headers)
#     encrypted_id = res.json()['id']
#     url_league = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/{}".format(encrypted_id)
#     res_league = requests.get(url=url_league, headers=headers)
#     league_dicts = res_league.json()
#
#     print(league_dicts)
#
#     print('-------------------------------')
#     def get_league_info(league_dict):
#         resp = [
#             league_dict.get('queueType'),
#             league_dict.get('tier'),
#             league_dict.get('rank'),
#             league_dict.get('wins'),
#             league_dict.get('losses'),
#             league_dict.get('leagueName'),
#             league_dict.get('leaguePoints')
#         ]
#         return resp
#
#     results = []
#     for league_dict in league_dicts:
#         results.append(get_league_info(league_dict))
#     length = len(results)
#
#     return render_template('search.html', sum_name=sum_name, results=results, length=length)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
