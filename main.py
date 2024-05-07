from database import Database
from jogo import Jogo


db = Database("bolt://3.84.21.57:7687", "neo4j", "input-slit-strips")
db.drop_all()


jogo_db = Jogo(db)

jogo_db.criar_jogador("Carlos")
jogo_db.criar_jogador("Julia")
jogo_db.criar_jogador("Pedro")


jogo_db.criar_partida(["Carlos", "Julia"], "Carlos wins")


jogo_db.criar_partida(["Pedro", "Julia"], "Julia wins")
jogo_db.criar_partida(["Carlos", "Pedro"], "Pedro wins")

# Atualizando o nome de um jogador
jogo_db.atualizar_jogador("Carlos", "Luiz")

print(jogo_db.obter_jogadores())



jogo_db.deletar_jogador("Pedro")


jogo_db.deletar_partida(1)



db.close()