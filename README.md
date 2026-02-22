# 🏆 Copa Fácil Suite

Suite completa para gerenciar campeonatos da **Copa Fácil**

---

## 📦 O que está incluso

| Módulo | Descrição | Status |
|--------|-----------|--------|
| `copafacil_api.py` | Cliente Python para API | ✅ Pronto |
| `dashboard.py` | Dashboard de consulta | ✅ Pronto |
| `bot_lancador.py` | Automação via navegador | ✅ Pronto |
| `config.py` | Configurações | ✅ Editar |

---

## 🚀 Como usar

### Passo 1: Configurar

Edite o arquivo `config.py`:

```python
# API da Copa Fácil
COPAFACIL_API_KEY = "SUA_API_KEY_AQUI"  # <-- OBTENHA NO APP
TOURNAMENT_ID = "12345"                  # <-- SEU CAMPEONATO

# Login (para automação)
COPAFACIL_EMAIL = "seu@email.com"
COPAFACIL_PASSWORD = "sua_senha"
```

### Passo 2: Instalar dependências

```bash
# Para consulta (API)
pip install requests

# Para automação (opcional)
pip install selenium
```

### Passo 3: Usar

---

## 📊 MÓDULO 1: Dashboard (Consulta via API)

### Ver tabela de classificação:
```bash
python dashboard.py
# Depois escolha opção 1
```

### Exemplo de saída:
```
🏆 TABELA DE CLASSIFICAÇÃO
============================================================
Pos  Time                      P   J   SG  
------------------------------------------------------------
1    Flamengo                 45  19  +28
2    Palmeiras                42  19  +22
3    Atlético-MG              38  19  +15
```

### Funções disponíveis:
- ✅ Tabela de classificação
- ✅ Próximos jogos
- ✅ Artilheiros
- ✅ Lista de fases
- ✅ Todas as partidas
- ✅ Galeria de fotos
- ✅ Relatório de jogadores

---

## 🤖 MÓDULO 2: Bot de Automação (Navegador)

O bot abre o Chrome e simula suas ações no site.

### Usar:
```bash
python bot_lancador.py
```

### Ações possíveis (implementar conforme necessidade):
- 🔐 Login automático
- ⚽ Lançar resultados
- 📅 Alterar data/hora de jogos
- 🔄 Atualizar placares em massa

### ❗ Atenção:
- Requer Chrome instalado
- Requer ChromeDriver instalado
- Use com moderação

---

## 📋 Obtendo API Key

1. Baixe o app **Copa Fácil**
2. Vá em: Perfil → Configurações → API
3. Copie a chave (paga)
4. Cole em `config.py`

---

## 🛠️ Estrutura do projeto

```
copafacil-suite/
├── README.md              # Este arquivo
├── config.py              # Configure aqui!
├── copafacil_api.py       # Cliente API
├── dashboard.py           # Dashboard
├── bot_lancador.py        # Automação
└── requirements.txt       # Dependências
```

---

## 💡 Exemplo de uso no código

```python
from copafacil_api import CopaFacilAPI

# Criar cliente
api = CopaFacilAPI()

# Listar fases
fases = api.listar_fases()
print(f"Campeonato tem {len(fases)} fases")

# Ver tabela
for time in api.tabela_geral()["teams"]:
    print(f"{time['position']}. {time['name']}")

# Próximos jogos
for jogo in api.proximos_jogos():
    print(f"{jogo['teams']['team_1']['name']} vs {jogo['teams']['team_2']['name']}")
```

---

## 🆘 Suporte

- Documentação API: https://www1.copafacil.com/doc_api/pt.html
- Suporte Copa Fácil: contato@copafacil.com

---

Feito para automatizar seu campeonato! 🚀
