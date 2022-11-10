import requests
import json
import pprint
import pandas as pd
from copy import deepcopy


move_list = []
locations_list = []
types_list = []
pkm_list = []
def req_pkms():
    print('Iniciando requisições, aguarde.')
    for id in range(1, 151):
        while True:
            try: 
                requisicao = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}/")
                print(f"https://pokeapi.co/api/v2/pokemon/{id}/")
                if requisicao.status_code == 200:
                    data = requisicao.json()
                    name = (data['name']).replace("'","")
                    move_list.clear()
                    for move in (data['moves']):
                        infos = {}
                        move = (move['move']['name']).replace("'","")
                        move_list.append(move)
                    types_list.clear()       
                    for types in (data['types']):
                        types = (types['type']['name']).replace("'","")
                        types_list.append(types)   
                    for stats in (data['stats']):
                        stats_name = (stats['stat']['name'])                                
                        base_stat = (stats['base_stat'])
                        # print(stats)
                        if stats_name == 'hp':
                            hp = base_stat 
                        if stats_name == 'attack':
                            attack = base_stat 
                        if stats_name == 'defense':
                            defense =  base_stat 

                    while True:
                        try:
                            location = (data['location_area_encounters'])
                            requisicao = requests.get(location)
                            if requisicao.status_code == 200:
                                locations = requisicao.json()
                                locations_list.clear()
                                for loc in locations:
                                    loc = (loc['location_area']['name'])
                                    locations_list.append(loc)      
                                    
              
                        except requests.exceptions.Timeout:
                            print('Timeout.')
                            continue       
                        break        
                    dict_pkm = {
                        'name': name,
                        'moves': move_list,
                        'types': types_list,
                        'locations': locations_list,
                        'hp': hp,
                        'attack': attack,
                        'defense': defense
                    }
                    #print(dict_pkm)
                    pkm_list.append(deepcopy(dict_pkm))            
                else:
                    pass    
            except requests.exceptions.Timeout:
                print('Timeout.')
                continue
            break
        
req_pkms()
       

def pkm_dataframe():
    df = pd.DataFrame(pkm_list)
    df = df.replace('[',"").replace("]","")
    print(df)
    df.to_csv('pokemons.csv', sep=';', index= False)
pkm_dataframe()    