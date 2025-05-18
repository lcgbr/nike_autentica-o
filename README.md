# Aplicação Flask - Relatório de Produtos

Esta aplicação permite gerar relatórios de produtos com base em SKUs informados manualmente ou via CSV, e canal de venda selecionado. O sistema conta com autenticação de usuários e painel administrativo com login exclusivo.

---

## 🚀 Deploy (Cloud Run + Container Registry)

### Pré-requisitos
- Projeto GCP com Cloud Run e Artifact Registry ativados
- Docker e gcloud CLI instalados

### Passos

1. **Build da imagem Docker**
   docker build -t us-central1-docker.pkg.dev/crawlers-fisia/relatorio-gateway/relatorio-gateway .

2. **Push da imagem para o Artifact/Container Registry**
   docker push us-central1-docker.pkg.dev/crawlers-fisia/relatorio-gateway/relatorio-gateway

3. **Deploy da imagem no Cloud Run**
   gcloud run deploy relatorio-gateway \
   --image us-central1-docker.pkg.dev/crawlers-fisia/relatorio-gateway/relatorio-gateway \
   --region=us-central1 \
   --allow-unauthenticated \
   --env-vars-file=env.yaml

---

## 📁 Estrutura de arquivos

.
├── app.py
├── relatorio.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── .env
├── env.yaml
├── templates/
│   ├── login.html
│   ├── form.html

---

## 🔐 Variáveis de ambiente

### Arquivo `.env`(rodar localmente)

### Arquivo `env.yaml` (para o Cloud Run)
GCP_PROJECT: crawlers-fisia
GCP_PROJECT_ID: crawlers-fisia
GOOGLE_CLOUD_PROJECT: crawlers-fisia

---

## 🔑 Login

- **Usuários comuns**: via `/login`

---

## 📤 Geração de Relatórios

1. Acesse `/`
2. Preencha os SKUs ou envie um CSV
3. Selecione ou informe o canal
4. Clique em **Gerar Relatório**

---

## 🛠️ Comandos úteis

Reiniciar ambiente local:
docker compose down
docker build -t us-central1-docker.pkg.dev/crawlers-fisia/relatorio-gateway/relatorio-gateway .
docker run -p 8080:8080 us-central1-docker.pkg.dev/crawlers-fisia/relatorio-gateway/relatorio-gateway
