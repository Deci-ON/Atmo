#id
#pais
#idade
#k/D

SELECT 
idplayer,
descCountry,
idade,
kills/deaths as KD
FROM (
SELECT 
a.idplayer,
SUM(qtkill) AS kills,
SUM(qtdeath) as deaths,
descCountry,
TIMESTAMPDIFF(YEAR,dtbirth,CURDATE()) AS idade

FROM CSGO.tb_lobby_stats_player a
JOIN tb_players b on a.idPlayer  = b.idPlayer
group by a.idplayer)a
order by kd desc