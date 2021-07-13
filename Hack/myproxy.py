import mitmproxy.http
from mitmproxy import ctx, http
import copy
import json
print("############ import success")

# True: Max All Operators' Status
# False: No Change to Operators' Status
allMight = True

# You cannot increase the number of operators you have. i.e. you can not use bpipe if you do not own it.
# BUT, you can replace one operator you own (any, say myrtle), with one you do not own (say bpipe). 

# customChar ==> dict:
#   {InstallID: character ID}
# InstallID:
#   The InstallID of the operator you'd like to replace (from).
#   InstallID is different per operator per true user (account). You have to modify according to your own situation.
#   InstallID is probably in the order of when you get the specific operator.
#   InstallID should not > the total number of operators you truly own. (either > or >=, I am not sure.)
#   The original Operator with this ID should not be a 2-star or 1-star operator.
# character ID:
#   The characterID of the operator you'd like to replace (to).
#   The characterID is available from character_table.json.
customChar = {
    "5": "char_222_bpipe",
    "15": "char_151_myrtle",
    "18": "char_103_angel",
    "13": "char_180_amgoat",
    "16": "char_293_thorns",
    "7": "char_311_mudrok",
    "12": "char_485_pallas",
    "9": "char_147_shining",
    "11": "char_172_svrash",
    "6": "char_1012_skadi2",
    "10": "char_332_archet"
}


Debug = True
Servers = ["ak-gs-gf.hypergryph.com"]  # Mainland Server.
# if you are from other servers, modify accordingly.


class Armada:
    def __init__(self):
        self.chars = json.loads(open('./character_table.json', 'r', encoding='UTF-8').read())
        self.squadFormation = {}
        self.squadFormationID = 0
        self.customChar = customChar

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        print(flow.request.host)
        if flow.request.host not in Servers and False is Debug:
            flow.response = http.HTTPResponse.make(404)

    def request(self, flow):
        if flow.request.host in Servers and flow.request.path.startswith("/quest/battleStart"):
            data = flow.request.get_content()
            print('Start Battle >>>')
            j = json.loads(data)
            for i, d in enumerate(j['squad']['slots']):
                if d is not None:
                    d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/campaign/battleStart"):
            data = flow.request.get_content()
            print('battle start >>>')
            j = json.loads(data)
            for i, d in enumerate(j['squad']['slots']):
                if d is not None:
                    d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            data = flow.request.get_content()
            j = json.loads(data)
            self.squadFormation = {flow.request.headers['uid']: {'slots': copy.deepcopy(j['slots']),
                                                                 'squadId': copy.deepcopy(j['squadId'])}}
            for i, d in enumerate(j['slots']):
                if j['slots'][i] is not None:
                    j['slots'][i]['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host in Servers and flow.request.path.startswith("/account/syncData"):
            text = flow.response.get_text()
            j = json.loads(text)
            print('Gold Squad ' + j['user']['status']['nickName'] + '#' + flow.request.headers['uid'] + ' initializing...')
            j['user']['status']['secretary'] = 'char_147_shining'
            j['user']['status']['secretarySkinId'] = "char_147_shining#2"
            print(len(j['user']['troop']['chars']))

            if len(j['user']['troop']['chars']) < 10:
                print('Not Enough Ops')
            else:
                for c in customChar:
                    tmp_skills = []
                    j['user']['troop']['chars'][c]['charId'] = customChar[c]
                    for s in self.chars[customChar[c]]['skills']:
                        tmp_skills.append({"skillId": s['skillId'],
                                           "unlock": 1,
                                           "state": 0,
                                           "specializeLevel": 0,
                                           "completeUpgradeTime": -1})
                        j['user']['troop']['chars'][c]['skills'] = tmp_skills


            if allMight:
                for lv in j['user']['troop']['chars']:
                    j['user']['troop']['chars'][lv]['potentialRank'] = 5
                    j['user']['troop']['chars'][lv]['mainSkillLvl'] = 7
                    j['user']['troop']['chars'][lv]['favorPoint'] = 240000
                    charId = j['user']['troop']['chars'][lv]['charId']
                    rarity = self.chars[charId]['rarity']

                    if rarity == 2:
                        j['user']['troop']['chars'][lv]['level'] = 55
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 1
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 0
                    elif rarity == 3:
                        j['user']['troop']['chars'][lv]['level'] = 70
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 1
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"
                    elif rarity == 4:
                        j['user']['troop']['chars'][lv]['level'] = 80
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 1
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"
                    elif rarity == 5:
                        j['user']['troop']['chars'][lv]['level'] = 90
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 2
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"

                    for e, skill in enumerate(j['user']['troop']['chars'][lv]['skills']):
                        j['user']['troop']['chars'][lv]['skills'][e]['unlock'] = 1
                        j['user']['troop']['chars'][lv]['skills'][e]['specializeLevel'] = 3

                    print('%s OP %s' % (lv, self.chars[j['user']['troop']['chars'][lv]['charId']]['name']))

            print('')
            print('Gold Squad Start')
            print('')
            flow.response.set_text(json.dumps(j))
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            text = flow.response.get_text()
            print('Form Squad >>>')
            j = json.loads(text)
            j['playerDataDelta']['modified']['troop']['squads'][
                self.squadFormation[flow.request.headers['uid']]['squadId']]['slots'] = \
                self.squadFormation[flow.request.headers['uid']]['slots']
            flow.response.set_text(json.dumps(j))
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)


addons = [
    Armada()
]