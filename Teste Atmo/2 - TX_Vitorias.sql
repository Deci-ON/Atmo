#Id
#tx_vitorias
#num_partidas

select idplayer,
qtd_Vitorias / contagem_partidas * 100 as tx_vitorias,
contagem_partidas
from (
SELECT idplayer,
	   SUM(flWinner) as qtd_Vitorias,
	   count(idLobbyGame) as contagem_partidas
from CSGO.tb_lobby_stats_player	   
group by idplayer
)a
where contagem_partidas > 10
order by tx_vitorias desc
limit 50;