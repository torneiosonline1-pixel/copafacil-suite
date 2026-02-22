"""
Configuração do Copa Fácil Suite
Só edite este arquivo com suas credenciais
"""

# ========== API DA COPA FÁCIL ==========
# Obtenha em: Aplicativo Copa Fácil → Perfil → API
COPAFACIL_API_KEY = "SUA_API_KEY_AQUI"  # <-- TROQUE APÓS COMPRAR

# ID do seu campeonato (número na URL)
TOURNAMENT_ID = "12345"  # <-- TROQUE PELO SEU

# Configurações opcionais
LANGUAGE = "pt"          # pt, en, es, etc
GMT_OFFSET = -3          # -3 para Brasil (BRT)

# ========== LOGIN DO PAINEL WEB ==========
# Para automação via navegador
COPAFACIL_EMAIL = "seu@email.com"     # <-- SEU LOGIN
COPAFACIL_PASSWORD = "sua_senha"      # <-- SUA SENHA

# URL do campeonato no painel
PAINEL_URL = "https://www.copafacil.com/torneio/" + TOURNAMENT_ID
