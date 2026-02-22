#!/usr/bin/env python3
"""
Dashboard Copa Fácil
Consulte tabela, jogos e estatísticas
"""

from copafacil_api import CopaFacilAPI
import json
from datetime import datetime

def mostrar_tabela():
    """Mostrar classificação formatada"""
    print("\n" + "="*60)
    print("🏆 TABELA DE CLASSIFICAÇÃO")
    print("="*60)
    
    try:
        api = CopaFacilAPI()
        tabela = api.tabela_geral()
        
        if not tabela or "teams" not in tabela:
            print("❌ Não foi possível carregar a tabela")
            return
        
        print(f"\n{'Pos':<4} {'Time':<25} {'P':<3} {'J':<3} {'SG':<4}")
        print("-" * 60)
        
        for time in tabela["teams"][:10]:
            pos = time.get("position", "-")
            nome = time.get("name", "Desconhecido")[:24]
            
            # Pega dados da tabela
            dados = {d.get("cod", ""): d.get("value", "-") for d in time.get("tableData", [])}
            
            pontos = dados.get("points", "-") if isinstance(dados.get("points"), str) else "-"
            jogos = dados.get("matches", "-") if isinstance(dados.get("matches"), str) else "-"
            sg = dados.get("goals_diff", "-") if isinstance(dados.get("goals_diff"), str) else "-"
            
            print(f"{pos:<4} {nome:<25} {pontos:<3} {jogos:<3} {sg:<4}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def mostrar_proximos_jogos():
    """Mostrar próximos jogos"""
    print("\n" + "="*60)
    print("⚽ PRÓXIMOS JOGOS")
    print("="*60)
    
    try:
        api = CopaFacilAPI()
        jogos = api.proximos_jogos(limite=5)
        
        if not jogos:
            print("📭 Nenhum jogo agendado")
            return
        
        for jogo in jogos:
            time1 = jogo.get("teams", {}).get("team_1", {}).get("name", "?")
            time2 = jogo.get("teams", {}).get("team_2", {}).get("name", "?")
            status = jogo.get("status", "agendado")
            
            print(f"\n{time1} vs {time2}")
            print(f"  Status: {status}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def mostrar_artilheiros():
    """Mostrar artilheiros"""
    print("\n" + "="*60)
    print("🥅 ARTILHEIROS")
    print("="*60)
    
    try:
        api = CopaFacilAPI()
        ranking = api.artilheiros(limite=5)
        
        if not ranking or "players" not in ranking:
            print("📭 Ranking não disponível")
            return
        
        print(f"\n{'Pos':<4} {'Jogador':<25} {'Time':<15} {'Gols':<5}")
        print("-" * 60)
        
        for jogador in ranking["players"][:10]:
            pos = jogador.get("position", "-")
            nome = jogador.get("name", "Desconhecido")[:24]
            time = jogador.get("teamName", "-")[:14]
            dados = jogador.get("data", [])
            gols = dados[0] if dados else "-"
            
            print(f"{pos:<4} {nome:<25} {time:<15} {gols:<5}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def menu():
    """Menu interativo"""
    while True:
        print("\n" + "="*60)
        print("📊 DASHBOARD COPA FÁCIL")
        print("="*60)
        print("\n1. 🏆 Ver classificação")
        print("2. ⚽ Próximos jogos")
        print("3. 🥅 Artilheiros")
        print("4. 📋 Todas as fases")
        print("5. 🔄 Atualizar tudo")
        print("0. ❌ Sair")
        print("-"*60)
        
        opcao = input("Escolha: ").strip()
        
        if opcao == "1":
            mostrar_tabela()
        elif opcao == "2":
            mostrar_proximos_jogos()
        elif opcao == "3":
            mostrar_artilheiros()
        elif opcao == "4":
            listar_fases()
        elif opcao == "5":
            mostrar_tabela()
            mostrar_proximos_jogos()
            mostrar_artilheiros()
        elif opcao == "0":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")

def listar_fases():
    """Listar fases do campeonato"""
    print("\n" + "="*60)
    print("📋 FASES DO CAMPEONATO")
    print("="*60)
    
    try:
        api = CopaFacilAPI()
        fases = api.listar_fases()
        
        if not fases:
            print("❌ Nenhuma fase encontrada")
            return
        
        for fase in fases:
            print(f"\n• {fase.get('title', 'Sem título')}")
            print(f"  ID: {fase.get('id', 'N/A')}")
            print(f"  Rodada única: {'Sim' if fase.get('round_robin') else 'Não'}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    menu()
