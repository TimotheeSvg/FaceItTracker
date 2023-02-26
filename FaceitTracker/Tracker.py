
import requests
import os


class Game:
    def __init__(self) -> None:
        self.tabJoueur = []
    
    def addJoueur(self, nom):
        stat = []
        addFlag = False
        maps = 0
        url = "https://faceitelo.net/player/"+nom
        x = requests.get(url)
        if 'profile does not' in x.text:
            return f"ERROR Page Non trouvée {url}"
        else:
            fichier = open(f"page.txt", "w")
            fichier.write(x.text)
            fichier.close()
    
            with open(f"page.txt", 'r') as pg:
                temp = []
                lignes = pg.readlines()
                for ligne in lignes:
                    if '<h2>Maps' in ligne:
                        addFlag = True    
                    if addFlag and '<td class="text-center">' in ligne:
                        value = ligne.strip('<td class="text-center">').strip('</td>\n').split()

                        if len(value)>1:
                            stat.append(temp) if len(temp) != 0 else 0
                            temp = []
                            temp.append(value[len(value)-1])
                        elif len(value)>0:
                            temp.append(value[0])
                stat.append(temp)
            if addFlag == True:
                self.tabJoueur.append(Joueur(nom, stat))
                pg.close()
                os.remove(f"page.txt")
                return "Joueur ajouté à la partie"
            else: 
                pg.close()
                os.remove(f"page.txt")
                return "Probleme Inconnu"
    def printInfo(self):
        print(f"Game {len(self.tabJoueur)} joueurs")
        for e in self.tabJoueur:
            e.printInfo()

class Joueur:

    def __init__(self, name, stat) -> None:
        self.tabWinRate = {}
        self.tabMatches = {}
        self.tabMap = []
        self.name = name

        for e in stat:
            self.addMap(e)

    def addMap(self, stat):
        self.tabMap.append(CMap(stat))
        
    def setWinRate(self):
        for map in self.tabMap:
            self.tabWinRate[map.name] = int(map.Win_Rate.strip('%'))
    def setMatches(self):
        for map in self.tabMap:
            self.tabMatches[map.name] = int(map.Matches)
        
        
    def printInfo(self):
        print(f"    Joueur Nom : {self.name}")
        print("    Map :")
        for e in self.tabMap:
            e.printInfo()


class CMap:

    def __init__(self,tab):
        self.name = tab[0][3:]
        self.stat = tab[1:]
        self.Matches=self.stat[0]
        self.Win_Rate=self.stat[1]
        self.Avg_KR=self.stat[3]
        self.Avg_KD=self.stat[4]
        self.Avg_HS=self.stat[6]
        self.Penta_kills=self.stat[10]
        
    def printInfo(self):
        print("Map : " + self.name + "\n  nbr map  : " + self.Matches + "\n  Win Rate : " + self.Win_Rate + "\n  KR : " + self.Avg_KR+ "\n  KD : " + self.Avg_KD+ "\n  penta : " + self.Penta_kills)
        #print("        " + self.name )


DEBUGFLAG = False

game = Game()
tabJoueur = []
reponse = []
tabWinrateGloba = []
tabSommeMapJouer = []
mapJouer = {}
nbrJoueurParMap = {}
sommeTabWinRate= {}
mapBan = ['cbble','cache']

if DEBUGFLAG:
    tabJoueur=["JbzTmort", "fanett00"]

else:
    os.system('cls')

    while True:
        pseudo = input("Saisir Pseudo : ")
        if pseudo != "":
            tabJoueur.append(pseudo)
        else:
            break

    print("Enregitrsment des joueurs : ")
    for e in tabJoueur:
        print(f"  {e}")


for j in tabJoueur:
    x = game.addJoueur(str(j))
    print(j, x)

for joueur in game.tabJoueur:
    joueur.setWinRate()
    joueur.setMatches()
    tabSommeMapJouer.append(joueur.tabMatches)
    tabWinrateGloba.append(joueur.tabWinRate)


for stat in tabWinrateGloba:
    for k in stat:
        if k in sommeTabWinRate:
            sommeTabWinRate[k] += stat[k]
            nbrJoueurParMap[k] +=1
        else:
            sommeTabWinRate[k] = stat[k]
            nbrJoueurParMap[k] = 1

for player in tabSommeMapJouer:
    for map_ in player:
        if map_ in mapJouer:
            mapJouer[map_] += player[map_] 
        else:
            mapJouer[map_] = player[map_]


os.system('cls')

sommeTabWinRate = {k: v for k, v in sorted(sommeTabWinRate.items(), key=lambda item: item[1])}
# open('reponse.txt', 'w')
print(" Map   WR Played Player ")
for k in sommeTabWinRate:
    if k not in mapBan:
        reponse.append(f"{k}: {sommeTabWinRate[k]//nbrJoueurParMap[k]}% ({mapJouer[k]}) ({nbrJoueurParMap[k]}) ")
        # with open('reponse.txt', 'a') as pg:
        #     pg.write(f"{k} : {round(sommeTabWinRate[k],1)}% ({nbrJoueurParMap[k]})\n ")

input()



        


    



