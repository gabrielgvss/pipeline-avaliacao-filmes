# Pipeline de Avaliação de Filmes

Um pipeline de engenharia de dados moderno para extrair, transformar e carregar dados de avaliações de filmes do Kaggle em um storage S3 (MinIO).

## 📋 Visão Geral

Este projeto implementa um **pipeline ETL** (Extract, Transform, Load) completo que:
- 📥 Extrai dados de filmes do dataset Kaggle [Movies](https://www.kaggle.com/datasets/abdallahwagih/movies)
- 🔄 Transforma os dados em formato otimizado (Parquet)
- 💾 Armazena em um storage S3 compatível (MinIO) em diferentes camadas (Bronze, Silver, Gold)
- 📊 Fornece análises de avaliações de filmes
- 🔗 **Em desenvolvimento:** Integração com APIs **OMDB** e **TMDB** para enriquecer dados com informações adicionais (ratings, cast, crew, sinopses, etc.)

## 🏗️ Arquitetura

O projeto segue a **arquitetura Medallion** (Bronze → Silver → Gold):

```
Raw Data (Kaggle)
        ↓
    Bronze
  (Raw data)
        ↓
    Silver
  (Cleaned & validated)
        ↓
    Gold
  (Aggregated & ready for BI)
```

## 📁 Estrutura do Projeto

```
pipeline_avaliacao_filmes/
├── dags/                      # DAGs do Airflow (orquestração futura)
├── scripts/                   # Scripts Python reutilizáveis
│   ├── create_bucket.py      # Gerenciamento de buckets S3
│   ├── extract/              # Extração de dados
│   │   ├── kaggle_extraction.py
│   │   └── notebook_test.ipynb
│   ├── load/                 # Carregamento de dados
│   └── transform/            # Transformação de dados
├── object-storage/           # Armazenamento local (MinIO)
│   └── movies/
│       └── bronze/           # Dados brutos em Parquet
├── main.py                   # Ponto de entrada principal
├── pyproject.toml           # Dependências do projeto
├── docker-compose.yaml      # Serviços Docker (MinIO)
└── README.md                # Este arquivo
```

## 🚀 Começando

### Pré-requisitos

- **Python** 3.13+
- **Docker** e **Docker Compose** (para MinIO)
- **uv** (gerenciador de pacotes Python) - [instalação](https://docs.astral.sh/uv/)
- Conta **Kaggle** com API key configurada

### Configuração da API do Kaggle

1. Crie uma conta em [Kaggle.com](https://www.kaggle.com)
2. Vá para Settings → API e clique em "Create New API Token"
3. Coloque o arquivo `kaggle.json` em `~/.kaggle/`
4. Configure as permissões: `chmod 600 ~/.kaggle/kaggle.json` (Linux/Mac)

### Instalação

1. **Clone ou navegue para o repositório:**
   ```bash
   cd pipeline_avaliacao_filmes
   ```

2. **Instale as dependências:**
   ```bash
   uv sync
   ```

3. **Ative o ambiente virtual:**
   ```bash
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   # ou
   source .venv/bin/activate   # Linux/Mac
   ```

### Configuração do MinIO

O projeto utiliza **MinIO** como storage S3 compatível. Configure as credenciais:

1. **Crie um arquivo `.env`** na raiz do projeto:
   ```env
   MINIO_ACCESS_KEY=admin
   MINIO_SECRET_KEY=admin123
   ```

2. **Inicie os serviços Docker:**
   ```bash
   docker-compose up -d
   ```

3. **Acesse o MinIO Console:**
   - URL: http://localhost:9001
   - Usuário: `admin`
   - Senha: `admin123`

## 🔧 Como Usar

### Executar a Extração de Dados

Extraia dados de filmes do Kaggle e salve em Parquet:

```bash
uv run python -m scripts.extract.kaggle_extraction
```

Este comando:
1. ✅ Baixa o dataset de filmes do Kaggle
2. ✅ Cria o bucket `movies` no MinIO (se não existir)
3. ✅ Salva os dados em `s3://movies/bronze/movie_titles.parquet`

### Verificar os Dados

Para verificar os dados salvos:

```bash
# Abra um Python REPL interativo
python

# Dentro do Python:
>>> import polars as pl
>>> df = pl.read_parquet(
...     "s3://movies/bronze/movie_titles.parquet",
...     storage_options={
...         "aws_access_key_id": "admin",
...         "aws_secret_access_key": "admin123",
...         "aws_endpoint_url": "http://localhost:9000",
...     }
... )
>>> df.head()
```

## 📦 Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `boto3` | ≥1.42.91 | Cliente AWS S3 |
| `kagglehub` | ≥1.0.0 | Download de datasets Kaggle |
| `polars` | ≥1.40.0 | Processamento de dados (alternativa a Pandas) |
| `pyarrow` | ≥23.0.1 | Suporte para Parquet |
| `minio` | ≥7.2.20 | Cliente MinIO Python |
| `duckdb` | ≥1.5.2 | Análise de dados (SQL) |
| `python-dotenv` | ≥1.2.2 | Gerenciamento de variáveis de ambiente |
| `requests` | ≥2.33.1 | Requisições HTTP |

## 📊 Fluxo de Dados

```
┌─────────────────────┐
│  Kaggle Dataset     │
│  (movies.csv)       │
└──────────┬──────────┘
           │ kagglehub.dataset_download()
           ↓
┌──────────────────────────────┐
│  Bronze Layer (S3)           │
│  movie_titles.parquet        │
│  (Raw data - not processed)  │
└──────────┬───────────────────┘
           │ Transformações
           ↓
┌──────────────────────────────┐
│  Silver Layer (S3)           │
│  (Cleaned & Validated data)  │
└──────────┬───────────────────┘
           │ Agregações
           ↓
┌──────────────────────────────┐
│  Gold Layer (S3)             │
│  (Ready for BI/Analytics)    │
└──────────────────────────────┘
```

## 🔍 Scripts Disponíveis

### `scripts/extract/kaggle_extraction.py`
- **Função:** Extrai dados de filmes do Kaggle
- **Output:** Arquivo Parquet em S3
- **Uso:** `uv run python -m scripts.extract.kaggle_extraction`

### `scripts/create_bucket.py`
- **Função:** Gerencia buckets S3
- **Funções principais:**
  - `create_bucket()`: Cria um novo bucket
  - `ensure_bucket_exists()`: Garante que um bucket existe

## 🐳 Serviços Docker

### MinIO
- **Container:** `minio`
- **Porta Console:** 9001 (http://localhost:9001)
- **Porta API S3:** 9000
- **Dados persistidos em:** `./object-storage/`

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```env
# MinIO Credentials
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123

# AWS S3 (se usar produção)
# AWS_ACCESS_KEY_ID=seu_acess_key
# AWS_SECRET_ACCESS_KEY=sua_secret_key
```

## 🚢 Próximos Passos

### Integrações com APIs Externas
- [ ] Integrar com API **OMDB** para enriquecer dados com ratings de usuários
- [ ] Integrar com API **TMDB** para obter informações de elenco, diretor e sinopses
- [ ] Implementar cache de requisições de API para otimizar performance
- [ ] Criar scripts de sincronização incremental com APIs externas

### Pipeline ETL
- [ ] Implementar transformações na camada Silver
- [ ] Implementar agregações na camada Gold
- [ ] Criar DAGs do Airflow para orquestração
- [ ] Adicionar testes unitários e integração
- [ ] Documentar modelos de dados
- [ ] Configurar CI/CD
- [ ] Adicionar logs e monitoramento
- [ ] Implementar validação de qualidade de dados

## 🤝 Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
2. Commit suas mudanças: `git commit -m 'Add some feature'`
3. Push para a branch: `git push origin feature/minha-feature`
4. Abra um Pull Request

## 🌐 APIs Externas (Em Desenvolvimento)

### OMDB - The Open Movie Database
- **Documentação:** [OMDb API](http://www.omdbapi.com/)
- **Uso:** Ratings de usuários e informações de filmes
- **Autenticação:** API Key obrigatória
- **Plano:** Integração para enriquecer dados com ratings externos

### TMDB - The Movie Database
- **Documentação:** [TMDB API](https://www.themoviedb.org/settings/api)
- **Uso:** Informações detalhadas (elenco, diretor, sinopses, genomas)
- **Autenticação:** API Key obrigatória
- **Plano:** Enriquecimento de dados com informações profissionais de filme

### Plano de Enriquecimento de Dados

```
Kaggle Dataset (Base)
        ↓
    Bronze
(Raw data do Kaggle)
        ↓
   Enriquecer com:
   • OMDB (ratings)
   • TMDB (elenco, diretor)
        ↓
    Silver
(Dados consolidados)
        ↓
    Gold
(Ready for BI)
```

## 📄 Licença

Este projeto está sob a licença MIT.

## 📞 Suporte

Para problemas, dúvidas ou sugestões, abra uma issue no repositório.

---

**Última atualização:** Abril 2026
