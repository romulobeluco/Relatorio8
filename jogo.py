class Jogo:
    def __init__(self, banco_de_dados):
        self.db = banco_de_dados

    def criar_jogador(self, nome):
        query = "CREATE (:Player {name: $nome})"
        parametros = {"nome": nome}
        self.db.execute_query(query, parametros)

    def atualizar_jogador(self, nome_antigo, nome_novo):
        query = "MATCH (p:Player {name: $nome_antigo}) SET p.name = $nome_novo"
        parametros = {"nome_antigo": nome_antigo, "nome_novo": nome_novo}
        self.db.execute_query(query, parametros)

    def deletar_jogador(self, nome):
        query = "MATCH (p:Player {name: $nome}) DETACH DELETE p"
        parametros = {"nome": nome}
        self.db.execute_query(query, parametros)

    def criar_partida(self, nomes_jogadores, resultado):
        query = """
        UNWIND $nomes_jogadores AS nome_jogador
        MATCH (p:Player {name: nome_jogador})
        WITH collect(p) AS jogadores
        CREATE (m:Match {result: $resultado})
        FOREACH (jogador IN jogadores | CREATE (jogador)-[:PARTICIPATES_IN]->(m))
        """
        parametros = {"nomes_jogadores": nomes_jogadores, "resultado": resultado}
        self.db.execute_query(query, parametros)

    def atualizar_resultado_partida(self, id_partida, novo_resultado):
        query = "MATCH (m:Match {id: $id_partida}) SET m.result = $novo_resultado"
        parametros = {"id_partida": id_partida, "novo_resultado": novo_resultado}
        self.db.execute_query(query, parametros)

    def obter_jogadores(self):
        query = "MATCH (p:Player) RETURN p.name AS name"
        resultados = self.db.execute_query(query)
        return [resultado["name"] for resultado in resultados]

    def obter_partidas_jogador(self, nome_jogador):
        query = """
        MATCH (p:Player {name: $nome_jogador})-[:PARTICIPATES_IN]->(m:Match)
        RETURN m.id AS match_id, m.result AS result
        """
        parametros = {"nome_jogador": nome_jogador}
        self.db.execute_query(query, parametros)

    def obter_partida(self, id_partida):
        query = "MATCH (m:Match {id: $id_partida}) RETURN m.result AS result"
        parametros = {"id_partida": id_partida}
        self.db.execute_query(query, parametros)

    def deletar_partida(self, id_partida):
        query = "MATCH (m:Match {id: $id_partida}) DETACH DELETE m"
        parametros = {"id_partida": id_partida}
        self.db.execute_query(query, parametros)
