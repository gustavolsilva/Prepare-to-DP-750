# 🚀 Databricks Formation — Prepare to DP-750

[![Build Status](https://img.shields.io/badge/Verification-100%25%20Passing-00A972?style=for-the-badge&logo=databricks)](Makefile)
[![Microsoft Exam](https://img.shields.io/badge/Microsoft%20Exam-DP--750-0078D4?style=for-the-badge&logo=microsoftazure)](https://learn.microsoft.com/certifications/exams/dp-750)
[![Curriculum](https://img.shields.io/badge/Curriculum-15%20Lessons%20%7C%2015%20Labs-FF3621?style=for-the-badge)](lessons/)
[![Exam Bank](https://img.shields.io/badge/Exam%20Simulator-+180%20Questions%20%7C%208%20Cases-1B3139?style=for-the-badge)](simulados/)

Plataforma educacional interativa de alta performance para o exame oficial **Microsoft Certified: Azure Databricks Data Engineer Associate (Exam DP-750)**.

Inspirada no padrão ouro de engenharia de software e design editorial de Edward Tufte, a plataforma combina rigor técnico, a metodologia **Multi-Lente (6 Níveis de Profundidade)** e os **4 Canais Sensoriais VARK** para garantir retenção máxima e aprovação de primeira tentativa.

---

## 🌟 Pilares Pedagógicos e de Engenharia

### 1. Seletor Global e Persistente de 6 Lentes (`localStorage` + Atalhos `[0..5]`)
- `🌐 Visão Unificada Completa [0]`: Exibição fluida de todas as camadas.
- `🌱 Júnior (0 anos) [1]`: Fundamentos e analogias visuais intuitivas.
- `🛠️ Pleno [2]`: Implementação prática em PySpark, Spark SQL e configurações de cluster.
- `🎯 Sênior & Exame DP-750 [3]`: Matrizes de decisão arquitetural e pegadinhas clássicas de prova.
- `⚙️ Staff / Internals [4]`: Photon C++ SIMD, Catalyst Optimizer internals, protocolo Delta Log e Liquid Clustering internals.
- `🏛️ C-Level / FinOps [5]`: Governança no Unity Catalog, TCO, dimensionamento de DBUs e Serverless.

### 2. Os 4 Canais Sensoriais (VARK) em TODAS as 15 Lições
- **🎧 Auditivo (`[A]`):** Narração em áudio neural PT-BR (`assets/audio/lesson-XXXX-pt.mp3`) calibrada para termos em inglês + Player Sticky com controle de velocidade (1x, 1.25x, 1.5x, 2x).
- **👁️ Visual (`[V]`):** Diagramas arquiteturais SVG interativos com *hotspots* clicáveis + Captura de Tela Visual Simulada do Portal Azure Databricks (Dark UI `#111E24`).
- **📖 Leitura/Escrita (`[R]`):** Tipografia Tufte, sidenotes numeradas e tabelas ASCII de alta densidade comparativa.
- **🖐️ Cinestésico (`[K]`):**
  - **Hands-on Labs Passo a Passo no Padrão Microsoft Learn:** Exercícios guiados com cenários corporativos, tarefas numeradas, células de código prontas para copiar para os Notebooks Databricks e saídas esperadas.
  - **Requisito de Nuvem Azure Obrigatório:** Alerta claro de que a execução prática dos comandos, criação de clusters, Delta Live Tables (DLT) e Unity Catalog exige um **Azure Databricks Workspace alocado no Microsoft Azure** (Standard ou Premium).
  - **Instruções FinOps de Limpeza (Clean up resources):** Cada lab ensina o passo a passo de encerramento de clusters e exclusão de tabelas temporárias para evitar consumo indesejado de créditos de nuvem.
  - **Desafio Flash estilo DP-750:** Com **embaralhamento dinâmico (Fisher-Yates shuffle)** das alternativas toda vez que a página abre e botão *"🔀 Embaralhar Novamente"*.

---

## 📦 Estrutura do Currículo DP-750

### Módulo 0: Fundamentos de Apache Spark, Delta Lake & Lakehouse (Base)
- **Lição 0001:** Arquitetura Azure Databricks, Control Plane vs Compute Plane, Classic vs Serverless & DBUs.
- **Lição 0002:** Anatomia do Apache Spark (Driver, Executors, Shuffles, Catalyst & Photon Engine).
- **Lição 0003:** Protocolo Delta Lake à Fundo (`_delta_log`, ACID, Time Travel, `OPTIMIZE`, `VACUUM`).

### Módulo 1: Configurar o Ambiente Azure Databricks (15–20% do Exame)
- **Lição 0004:** Workspaces, Microsoft Entra ID (SCIM, Service Principals), VNet Injection (/26) & Private Link.
- **Lição 0005:** Governança de Computação: Cluster Policies JSON, Pools & Serverless SQL Warehouses.
- **Lição 0006:** Integração com Ecossistema Azure: Key Vault Secret Scopes & ADLS Gen2 External Locations.

### Módulo 2: Segurança e Governança com Unity Catalog (15–20% do Exame)
- **Lição 0007:** Unity Catalog: Metastore, Namespace de 3 Níveis (`cat.sch.tbl`), Managed vs External Tables & Volumes.
- **Lição 0008:** Controle de Acesso Fino: Privilégios Hierárquicos (GRANT/REVOKE), Row Filters & Column Masks.
- **Lição 0009:** Linhagem de Dados Automatizada, System Tables (`audit`, `billing`) & Delta Sharing.

### Módulo 3: Preparar e Processar Dados em Batch e Streaming (30–35% do Exame)
- **Lição 0010:** Ingestão Escalável: Auto Loader (`cloudFiles`), Schema Evolution, `_rescued_data` & `COPY INTO`.
- **Lição 0011:** Arquitetura Medallion: PySpark, Spark SQL, Window Functions & `MERGE INTO` (SCD1 e SCD2).
- **Lição 0012:** Engenharia de Tempo Real: Structured Streaming, Watermarking, Triggers & Stream Joins.
- **Lição 0013:** Otimização Física: Liquid Clustering (`CLUSTER BY`) vs Z-Order, Deletion Vectors & Caching.

### Módulo 4: Implantar e Manter Pipelines e Workloads (30–35% do Exame)
- **Lição 0014:** Pipelines Declarativos com Delta Live Tables (DLT): Streaming Tables, Views, Expectations & CDC.
- **Lição 0015:** Orquestração em Produção: Databricks Workflows (DAGs, Repair Run), DABs (`databricks.yml`), Spark UI & Spill.

### 📑 6 Folhas de Referência Rápida (`reference/`):
1. `01-spark-and-databricks-architecture-visual-guide.html`
2. `02-unity-catalog-security-and-governance-guide.html`
3. `03-ingestion-autoloader-and-dlt-decision-matrix.html`
4. `04-pyspark-and-spark-sql-engineering-cheatsheet.html`
5. `05-delta-lake-liquid-clustering-and-tuning-guide.html`
6. `06-workflows-dabs-cicd-and-system-tables-cheatsheet.html`

---

## 🎯 Centro Oficial de Simulados Pearson VUE (`simulados/index.html`)
- **+180 Questões Inéditas** cobrindo os 4 domínios oficiais.
- **8 Estudos de Caso Corporativos Split-Screen** com abas de contexto:
  - *Visão Geral, Arquitetura Atual, Requisitos de Dados, Segurança/Unity Catalog, Problemas de Pipeline*.
- **6 Modos de Treino:**
  1. Exame Oficial Pearson VUE (55 questões, 100 min, corte 700/1000).
  2. Maratona Estendida (90 questões, 160 min).
  3. Banco Completo (todas as 184 questões).
  4. Treino por Domínio Específico (Domínios 1, 2, 3 ou 4).
  5. Estudos de Caso Split-Screen.
  6. Revisão Rápida com Feedback Imediato.
- **Embaralhamento Total Fisher-Yates** das questões e posições das alternativas.

---

## 🛠️ Automação e Comandos Rápidos (`Makefile`)

```bash
# Executa a verificação completa (build-exam + test-labs + test)
make verify

# Executa todos os 15 labs Python
make test-labs

# Executa testes automatizados de integridade
make test

# Inicia servidor local em http://localhost:8000
make serve
```

---

## 🏛️ Licença e Conformidade
Material educacional independente projetado para o exame oficial Microsoft Certified: Azure Databricks Data Engineer Associate (Exam DP-750).

