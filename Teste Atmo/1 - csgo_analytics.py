
import mysql.connector
import pandas as pd
from skimpy import clean_columns

def mydbConnection(host_name, user_name, user_password, user_database):
    connection = None
    print(f'Iniciando Conexão com o banco de dados {user_database}')
    for i in range(0,100):
        while True:    
            try:
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password,
                    database=user_database
                )
                connection.autocommit=True
                
            except mysql.connector.Error as err:
                print(f"The error '{err}' occurred")
                continue
            break
    print("Conexao com o banco feita com sucesso.")       
    return connection

connection = mydbConnection("atmo-db.cncfsgdjnfjz.sa-east-1.rds.amazonaws.com", "candidato", "analista_atmo", "CSGO")


def df_lobby(connection):
    cursor = connection.cursor()
    print('Inicio Select Lobby Stats Player, aguarde.')

    try:
        #QUERY LIMITADA EM 50 REGISTROS PARA NÃO SOBRECARREGAR O BANCO DA ATMO
        cursor.execute('SELECT idLobbyGame, idPlayer, idRoom, qtKill, qtAssist, qtDeath, qtHs, qtBombeDefuse, qtBombePlant, qtTk, qtTkAssist, qt1Kill, qt2Kill, qt3Kill, qt4Kill, qt5Kill, qtPlusKill, qtFirstKill, vlDamage, qtHits, qtShots, qtLastAlive, qtClutchWon, qtRoundsPlayed, descMapName, vlLevel, qtSurvived, qtTrade, qtFlashAssist, qtHitHeadshot, qtHitChest, qtHitStomach, qtHitLeftAtm, qtHitRightArm, qtHitLeftLeg, qtHitRightLeg, flWinner, dtCreatedAt FROM CSGO.tb_lobby_stats_player limit 50')
        lobby = cursor.fetchall()
        
        df = pd.DataFrame(lobby, columns=cursor.column_names)
        #snake case
        df = clean_columns(df)
        print(df)
        df.to_csv('lobby.csv', sep= ';')
    except mysql.connector.Error as err:
        print(err)
        
df_lobby(connection)
        
def df_medals(connection):    
    print('Inicio Select Medals, aguarde.')
    cursor = connection.cursor()    
    try:
        cursor.execute('SELECT idMedal, descMedal, descTypeMedal FROM CSGO.tb_medalha;')
        medals = cursor.fetchall()
        df = pd.DataFrame(medals, columns=cursor.column_names)
        #snake case
        df = clean_columns(df)
        print(df)
        df.to_csv('medals.csv', sep= ';')
    except mysql.connector.Error as err:
        print(err)   
       
df_medals(connection)       

def df_players(connection):
    cursor = connection.cursor()           
    print('Inicio Select Players, aguarde.')    
    try:
        cursor.execute('SELECT idPlayer, flFacebook, flTwitter, flTwitch, descCountry, dtBirth, dtRegistration FROM CSGO.tb_players;')
        players = cursor.fetchall()
        df = pd.DataFrame(players, columns=cursor.column_names)
        #snake case
        df = clean_columns(df)
        print(df)
        df.to_csv('players.csv', sep= ';')
    except mysql.connector.Error as err:
        print(err)   
    
df_players(connection)    
   
def df_players_medalhas(connection):
    cursor = connection.cursor()      
    print('Inicio Select Players Medalhas, aguarde.')    
    try:
        cursor.execute('SELECT id, idPlayer, idMedal, dtCreatedAt, dtExpiration, dtRemove, flActive FROM CSGO.tb_players_medalha;')
        pl_md = cursor.fetchall()
        df = pd.DataFrame(pl_md, columns=cursor.column_names)
        #snake case
        df = clean_columns(df)
        print(df)
        df.to_csv('player_medals.csv', sep= ';')
    except mysql.connector.Error as err:
        print(err)   
                 
df_players_medalhas(connection)
    
