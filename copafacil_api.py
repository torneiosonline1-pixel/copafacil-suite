"""
Cliente API da Copa Fácil
Todas as rotas de consulta disponíveis
"""

import requests
import json
from datetime import datetime
from config import COPAFACIL_API_KEY, TOURNAMENT_ID, LANGUAGE, GMT_OFFSET

BASE_URL = "https://copafacil.com"

class CopaFacilAPI:
    """Cliente para API v2 da Copa Fácil"""
    
    def __init__(self, api_key=None, tournament_id=None):
        self.api_key = api_key or COPAFACIL_API_KEY
        self.tournament_id = tournament_id or TOURNAMENT_ID
        self.base_url = BASE_URL
        
        if self.api_key == "SUA_API_KEY_AQUI":
            raise ValueError("❌ Configure SUA_API_KEY no config.py!")
    
    def _headers(self):
        """Headers padrão para todas as requisições"""
        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if LANGUAGE:
            headers["lang"] = LANGUAGE
        if GMT_OFFSET is not None:
            headers["gmt"] = str(GMT_OFFSET)
        return headers
    
    def _get(self, endpoint):
        """Fazer GET na API"""
        url = f"{self.base_url}/api2{endpoint}"
        try:
            response = requests.get(url, headers=self._headers(), timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    # ========== 1. FASES DO CAMPEONATO ==========
    def listar_fases(self):
        """Listar todas as fases do campeonato"""
        endpoint = f"/tournament/{self.tournament_id}/stages"
        return self._get(endpoint)
    
    # ========== 2. CLASSIFICAÇÃO ==========
    def tabela_classificacao(self, stage_id):
        """Tabela de classificação de uma fase"""
        endpoint = f"/tournament/{self.tournament_id}/stages/{stage_id}/table"
        return self._get(endpoint)
    
    def tabela_geral(self):
        """Pega a tabela da primeira fase (geral)"""
        fases = self.listar_fases()
        if fases and len(fases) > 0:
            return self.tabela_classificacao(fases[0]["id"])
        return None
    
    # ========== 3. RODADAS ==========
    def listar_rodadas(self, stage_id):
        """Listar rodadas de uma fase"""
        endpoint = f"/tournament/{self.tournament_id}/stages/{stage_id}/rounds"
        return self._get(endpoint)
    
    # ========== 4. PARTIDAS ==========
    def listar_partidas(self, stage_id, round_id):
        """Listar partidas de uma rodada"""
        endpoint = f"/tournament/{self.tournament_id}/stages/{stage_id}/rounds/{round_id}/matchs"
        return self._get(endpoint)
    
    def proximos_jogos(self, limite=5):
        """Buscar próximos jogos (ainda não realizados)"""
        fases = self.listar_fases()
        if not fases:
            return []
        
        jogos_futuros = []
        for fase in fases:
            rodadas = self.listar_rodadas(fase["id"])
            if rodadas:
                for rodada in rodadas:
                    partidas = self.listar_partidas(fase["id"], rodada["id"])
                    if partidas:
                        for partida in partidas:
                            # Verifica se jogo ainda não tem resultado definido
                            if partida.get("status") != "finalizado":
                                jogos_futuros.append(partida)
        
        return jogos_futuros[:limite]
    
    # ========== 5. RANKINGS ==========
    def listar_tipos_rankings(self):
        """Listar tipos de rankings disponíveis"""
        endpoint = f"/tournament/{self.tournament_id}/rankings"
        return self._get(endpoint)
    
    def ranking_jogadores(self, ranking_id):
        """Ranking específico (artilheiros, etc)"""
        endpoint = f"/tournament/{self.tournament_id}/rankings/{ranking_id}"
        return self._get(endpoint)
    
    def artilheiros(self, limite=10):
        """Busca ranking de artilheiros automaticamente"""
        tipos = self.listar_tipos_rankings()
        if not tipos:
            return None
        
        for tipo in tipos:
            if "gol" in tipo.get("title1", "").lower() or "artilheiro" in tipo.get("title1", "").lower():
                return self.ranking_jogadores(tipo["id"])
        
        # Se não encontrar, pega o primeiro
        if tipos:
            return self.ranking_jogadores(tipos[0]["id"])
        return None
    
    # ========== 6. GALERIA ==========
    def listar_fotos(self, max_fotos=20):
        """Listar fotos do campeonato"""
        endpoint = f"/tournament/{self.tournament_id}/gallery?max={max_fotos}"
        return self._get(endpoint)
    
    # ========== 7. RELATÓRIO DE JOGADORES ==========
    def listar_chaves_jogadores(self):
        """Chaves disponíveis para relatório de jogadores"""
        endpoint = f"/tournament/{self.tournament_id}/players/keys"
        return self._get(endpoint)
    
    def relatorio_jogadores(self, team_ids, keys=None, staff=False):
        """Relatório de jogadores"""
        endpoint = f"/tournament/{self.tournament_id}/players?"
        
        # Adicionar times
        for team_id in team_ids:
            endpoint += f"team={team_id}&"
        
        # Adicionar chaves
        if keys:
            for key in keys:
                endpoint += f"key={key}&"
        
        # Comissão técnica
        endpoint += f"staff={'true' if staff else 'false'}"
        
        return self._get(endpoint)
    
    def todos_jogadores(self):
        """Buscar todos os jogadores do campeonato (conveniência)"""
        # Pegar times da classificação
        tabela = self.tabela_geral()
        if not tabela or "teams" not in tabela:
            return None
        
        team_ids = [team["id"] for team in tabela["teams"]]
        return self.relatorio_jogadores(team_ids)


# Teste rápido
if __name__ == "__main__":
    print("🚀 Testando conexão com Copa Fácil API...")
    
    try:
        api = CopaFacilAPI()
        
        print("\n📋 Fases do campeonato:")
        fases = api.listar_fases()
        if fases:
            for fase in fases:
                print(f"  - {fase['title']} (ID: {fase['id']})")
        
        print("\n🏆 Tabela de classificação:")
        tabela = api.tabela_geral()
        if tabela and "teams" in tabela:
            for i, time in enumerate(tabela["teams"][:5], 1):
                print(f"  {i}. {time['name']}")
        
        print("\n✅ Conexão OK! Configure sua API key no config.py")
        
    except ValueError as e:
        print(f"\n{e}")
        print("💡 Troque SUA_API_KEY_AQUI no config.py pela sua chave real")
