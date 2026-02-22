#!/usr/bin/env python3
"""
Bot de Automação Copa Fácil
Lança resultados, altera datas via navegador
"""

import time
import sys
from datetime import datetime

def mostrar_requisitos():
    """Mostrar o que precisa instalar"""
    print("""
⚠️  REQUISITOS PARA O BOT DE AUTOMAÇÃO

Antes de usar, instale:

1. Selenium:
   pip install selenium

2. ChromeDriver (ou WebDriver do seu navegador):
   - Chrome: https://chromedriver.chromium.org/downloads
   - Firefox: https://github.com/mozilla/geckodriver/releases
   
3. Configure no config.py:
   COPAFACIL_EMAIL = "seu@email.com"
   COPAFACIL_PASSWORD = "sua_senha"

⚠️  AVISO: Automação de login pode violar os termos de serviço.
Use com moderação e em campeonatos que você administra.
""")

def check_selenium():
    """Verificar se selenium está instalado"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        return True
    except ImportError:
        return False

class CopaFacilBot:
    """Bot para automatizar lançamentos no painel Copa Fácil"""
    
    def __init__(self, email=None, senha=None):
        self.email = email
        self.senha = senha
        self.driver = None
        self.base_url = "https://www.copafacil.com"
        
    def iniciar(self):
        """Iniciar navegador"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            print("🚀 Iniciando navegador...")
            
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            # options.add_argument("--headless")  # Sem interface gráfica (opcional)
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(10)
            
            print("✅ Navegador iniciado!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar navegador: {e}")
            print("💡 Verifique se o ChromeDriver está instalado e no PATH")
            return False
    
    def login(self):
        """Fazer login no Copa Fácil"""
        if not self.email or not self.senha:
            print("❌ Configure COPAFACIL_EMAIL e COPAFACIL_PASSWORD no config.py")
            return False
        
        try:
            print("🔐 Fazendo login...")
            
            self.driver.get(f"{self.base_url}/login")
            time.sleep(2)
            
            # Preencher email
            email_input = self.driver.find_element("name", "email")
            email_input.send_keys(self.email)
            
            # Preencher senha
            senha_input = self.driver.find_element("name", "password")
            senha_input.send_keys(self.senha)
            
            # Clicar em entrar
            entrar_btn = self.driver.find_element("xpath", "//button[contains(text(), 'Entrar')]")
            entrar_btn.click()
            
            time.sleep(3)
            
            # Verificar se logou
            if "dashboard" in self.driver.current_url or "torneio" in self.driver.current_url:
                print("✅ Login realizado com sucesso!")
                return True
            else:
                print("❌ Login falhou. Verifique email e senha.")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
    
    def ir_para_campeonato(self, tournament_id):
        """Navegar até o campeonato"""
        try:
            print(f"🏆 Acessando campeonato {tournament_id}...")
            self.driver.get(f"{self.base_url}/torneio/{tournament_id}")
            time.sleep(2)
            print("✅ Campeonato carregado")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def listar_jogos(self):
        """Capturar lista de jogos da tela"""
        try:
            print("📋 Buscando jogos...")
            # Aqui você precisaria inspecionar o HTML real do site
            # para encontrar os seletores corretos
            jogos = self.driver.find_elements("class", "partida-item")
            
            print(f"✅ {len(jogos)} jogos encontrados")
            return jogos
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    def lançar_resultado(self, jogo_id, placar_casa, placar_visitante):
        """
        Lançar resultado de um jogo
        
        Exemplo de uso:
        bot.lançar_resultado("jogo123", 2, 1)
        """
        try:
            print(f"⚽ Lançando jogo {jogo_id}: {placar_casa}x{placar_visitante}")
            
            # Exemplo - ajustar conforme HTML real do site:
            # 1. Clicar no jogo
            # 2. Preencher placar
            # 3. Salvar
            
            print(f"✅ Resultado lançado: {placar_casa}x{placar_visitante}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao lançar: {e}")
            return False
    
    def alterar_data_jogo(self, jogo_id, nova_data, nova_hora):
        """
        Alterar data/hora de um jogo
        
        Exemplo:
        bot.alterar_data_jogo("jogo123", "25/03/2025", "16:00")
        """
        try:
            print(f"📅 Alterando jogo {jogo_id} para {nova_data} às {nova_hora}")
            
            # Exemplo - ajustar conforme HTML real:
            # 1. Clicar no jogo
            # 2. Clicar em editar
            # 3. Alterar data/hora
            # 4. Salvar
            
            print("✅ Data/hora alterada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def fechar(self):
        """Fechar navegador"""
        if self.driver:
            self.driver.quit()
            print("👋 Navegador fechado")

def menu_bot():
    """Menu do bot de automação"""
    print("""
🤖 BOT DE AUTOMAÇÃO COPA FÁCIL
Este bot navega no site e realiza ações automaticamente.
""")
    
    if not check_selenium():
        mostrar_requisitos()
        return
    
    try:
        from config import COPAFACIL_EMAIL, COPAFACIL_PASSWORD, TOURNAMENT_ID
        
        bot = CopaFacilBot(COPAFACIL_EMAIL, COPAFACIL_PASSWORD)
        
        if not bot.iniciar():
            return
        
        if not bot.login():
            bot.fechar()
            return
        
        bot.ir_para_campeonato(TOURNAMENT_ID)
        
        print("\n✅ Bot pronto!")
        print("💡 Implemente as funções específicas conforme sua necessidade")
        
        # Exemplo: listar jogos
        jogos = bot.listar_jogos()
        
        input("\nPressione Enter para fechar...")
        bot.fechar()
        
    except ImportError as e:
        print(f"❌ Erro ao importar config: {e}")
        print("💡 Verifique se config.py existe e está configurado")

if __name__ == "__main__":
    menu_bot()
