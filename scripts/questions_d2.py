#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Domínio 2: Segurança e Governança com Unity Catalog (15–20%) — 38 Questões (39 a 76)
"""

def get_d2_questions():
    d2_specs = [
        # Q39
        {
            "scenario": "Um analista de BI tenta consultar uma tabela chamada 'vendas_ouro' no Unity Catalog executando 'SELECT * FROM vendas_ouro;'. A consulta falha com erro informando que a tabela não foi encontrada no catálogo padrão. Qual é a sintaxe oficial recomendada pelo exame DP-750 para referenciar qualquer objeto no Unity Catalog?",
            "options": [
                ("Utilizar a nomenclatura de 3 níveis totalmente qualificada (Three-Level Namespace): catalog.schema.table (ex: prod_lakehouse.financeiro.vendas_ouro).", True, "Correto. O Unity Catalog exige ou recomenda fortemente o uso do namespace de 3 níveis (catalog.schema.table) para garantir portabilidade e evitar ambiguidades."),
                ("Montar a tabela no DBFS local com dbutils.fs.mount() e ler via /mnt/vendas_ouro.", False, "Incorreto. O DBFS mount é um padrão legado desaconselhado pelo exame."),
                ("Executar a query precedida por %sql default.vendas_ouro.", False, "Incorreto. Apenas 2 níveis aponta para o catálogo padrão da sessão, sem qualificação explícita."),
                ("Converter a tabela para formato CSV e fazer o download no computador do analista.", False, "Incorreto. Não resolve a consulta no Azure Databricks e viola normas de segurança corporativa.")
            ],
            "explanation": "No Unity Catalog, o 3-Level Namespace (catalog.schema.table) é a convenção fundamental para identificar unicamente tabelas, views e volumes em qualquer workspace conectado ao metastore."
        },
        # Q40
        {
            "scenario": "Uma organização de saúde armazena laudos médicos e exames em formato PDF e imagens DICOM que não são dados tabulares. A equipe precisa aplicar controle de acesso governado (RBAC) com auditoria nesses arquivos não estruturados. Qual objeto do Unity Catalog atende perfeitamente a esse requisito?",
            "options": [
                ("Criar um Unity Catalog Volume (Managed ou External Volume).", True, "Correto. Volumes no Unity Catalog governam arquivos não tabulares (PDFs, imagens, CSVs brutos) com permissões SQL (READ VOLUME, WRITE VOLUME) e auditoria nativa."),
                ("Gravar todos os arquivos em uma coluna do tipo BINARY em uma Managed Table Delta.", False, "Incorreto. Gravar arquivos pesados em colunas binárias degrada o log de transações e a performance de leitura do Delta Lake."),
                ("Colocar os arquivos no DBFS raiz público FileStore.", False, "Incorreto. O FileStore não oferece governança RBAC nem auditoria fina do Unity Catalog."),
                ("Exigir que os médicos enviem os arquivos por e-mail para a equipe de TI.", False, "Incorreto. Inviável e viola regras de conformidade e privacidade.")
            ],
            "explanation": "Volumes do Unity Catalog são objetos de primeira classe desenhados especificamente para governar, auditar e acessar arquivos não estruturados e semi-estruturados em caminhos do tipo `/Volumes/catalogo/schema/volume_name/`."
        },
        # Q41
        {
            "scenario": "Qual é a diferença fundamental entre uma Managed Table e uma External Table no Unity Catalog quando o comando DROP TABLE é executado?",
            "options": [
                ("Em uma Managed Table, o DROP TABLE exclui os metadados no catálogo E todos os arquivos Parquet de dados do storage; em uma External Table, exclui APENAS os metadados, preservando os arquivos de dados intactos no ADLS Gen2.", True, "Correto. Essa é a distinção mais testada no DP-750: tabelas gerenciadas perdem dados e metadados no DROP, enquanto tabelas externas mantêm os dados subjacentes."),
                ("Em uma Managed Table, os dados nunca podem ser excluídos mesmo com DROP TABLE.", False, "Incorreto. O DROP TABLE em Managed Tables remove permanentemente os arquivos de dados do storage gerenciado."),
                ("External Tables não suportam o formato Delta Lake nem comandos SQL.", False, "Incorreto. External Tables suportam Delta Lake, Parquet, JSON, etc."),
                ("Managed Tables residem exclusivamente na memória RAM volátil do nó Driver.", False, "Incorreto. Managed Tables persistem dados em arquivos Parquet no ADLS Gen2 subjacente ao metastore.")
            ],
            "explanation": "Managed Tables têm seu ciclo de vida totalmente gerenciado pelo Unity Catalog (dados e metadados apagados no DROP). External Tables preservam os arquivos de dados no container do ADLS Gen2 caso a tabela seja excluída do catálogo."
        },
        # Q42
        {
            "scenario": "Um engenheiro de dados precisa configurar o Unity Catalog para acessar um container no ADLS Gen2 ('abfss://raw@datalake.dfs.core.windows.net/'). Qual objeto de infraestrutura do Unity Catalog deve ser criado PRIMEIRO para encapsular as credenciais de autenticação baseadas no Azure Access Connector?",
            "options": [
                ("Storage Credential (utilizando a Managed Identity do Azure Access Connector).", True, "Correto. A Storage Credential encapsula a identidade gerenciada da Azure; em seguida, a External Location utiliza essa credencial para conceder acesso ao path do storage."),
                ("External Location.", False, "Incorreto. A External Location depende de uma Storage Credential pré-existente para se autenticar."),
                ("Catalog.", False, "Incorreto. O catálogo pode ser criado a qualquer momento, mas o acesso ao storage físico requer a Storage Credential e a External Location."),
                ("Row Filter.", False, "Incorreto. Row Filter é uma política de segurança de linhas de tabela, não infraestrutura de conexão com o Azure Storage.")
            ],
            "explanation": "No Unity Catalog, o fluxo de infraestrutura de storage exige primeiro a criação de uma `Storage Credential` (vinculada à Managed Identity do Access Connector com `Storage Blob Data Contributor`) e depois a `External Location` que mapeia a URL do container àquela credencial."
        },
        # Q43
        {
            "scenario": "Qual comando SQL cria corretamente uma External Location associando o container de dados à credencial de armazenamento 'cred_corp' no Unity Catalog?",
            "options": [
                ("CREATE EXTERNAL LOCATION loc_adls_raw URL 'abfss://raw@datalake.dfs.core.windows.net/' WITH (STORAGE CREDENTIAL cred_corp);", True, "Correto. Essa é a sintaxe oficial ANSI SQL do Unity Catalog para criar uma External Location."),
                ("ATTACH STORAGE 'abfss://raw@datalake.dfs.core.windows.net/' USING PASSWORD 'cred_corp';", False, "Incorreto. Sintaxe inexistente."),
                ("MOUNT 'abfss://raw@datalake.dfs.core.windows.net/' TO '/mnt/raw' WITH CREDENTIAL cred_corp;", False, "Incorreto. Sintaxe de montagem legada DBFS, não Unity Catalog."),
                ("GRANT ALL PRIVILEGES ON CONTAINER raw TO cred_corp;", False, "Incorreto. Sintaxe inválida no Databricks.")
            ],
            "explanation": "A sintaxe oficial do Unity Catalog é: `CREATE EXTERNAL LOCATION <nome> URL '<caminho-abfss>' WITH (STORAGE CREDENTIAL <nome-credencial>);`."
        },
        # Q44
        {
            "scenario": "Um usuário do grupo 'analistas_marketing' precisa consultar a tabela 'prod.crm.clientes'. O administrador concedeu o privilégio 'GRANT SELECT ON TABLE prod.crm.clientes TO analistas_marketing;'. Ao executar a query, o analista recebe erro de acesso negado. Qual concessão adicional é estritamente obrigatória no modelo hierárquico do Unity Catalog?",
            "options": [
                ("Conceder USE CATALOG no catálogo 'prod' E conceder USE SCHEMA no schema 'crm' para o grupo 'analistas_marketing'.", True, "Correto. No Unity Catalog, para atravessar a hierarquia e acessar um objeto folha (tabela/view/volume), o usuário precisa obrigatoriamente de USE CATALOG no catálogo pai e USE SCHEMA no schema pai."),
                ("Conceder permissão de Subscription Owner na assinatura do Microsoft Azure.", False, "Incorreto. Viola o princípio do menor privilégio e não resolve privilégios internos do Unity Catalog."),
                ("Alterar a senha do analista para a mesma senha do Metastore Admin.", False, "Incorreto. Totalmente inseguro e viola normas de auditoria."),
                ("Mudar o modo do cluster para Unrestricted e desativar o Unity Catalog.", False, "Incorreto. Viola a governança de dados e desabilita a segurança.")
            ],
            "explanation": "Essa é a pegadinha clássica de segurança do DP-750: No Unity Catalog, possuir apenas `SELECT` na tabela é insuficiente. É obrigatório ter `USE CATALOG` no catálogo e `USE SCHEMA` no schema pai para poder resolver e ler a tabela."
        },
        # Q45
        {
            "scenario": "A equipe de segurança corporativa exige que analistas de atendimento ao cliente visualizem apenas os registros de clientes do seu respectivo país (ex: analistas do Brasil só veem clientes onde pais = 'BR'), enquanto gerentes globais visualizam todos os países. Qual funcionalidade moderna do Unity Catalog atende a esse requisito sem criar views duplicadas?",
            "options": [
                ("Criar uma função SQL (UDF) com is_account_group_member() e associá-la à tabela como um Row Filter.", True, "Correto. Row Filters no Unity Catalog aplicam predicados de filtragem dinâmicos na tabela física baseados no grupo do usuário atual, sem necessidade de views intermediárias."),
                ("Criar uma view separada para cada um dos 195 países do mundo e conceder permissões manuais.", False, "Incorreto. Pesadelo de manutenção operacional e inviável em escala."),
                ("Executar um job noturno que divide a tabela em 195 tabelas físicas diferentes no ADLS Gen2.", False, "Incorreto. Duplica storage, aumenta custos de DBUs e fragmenta a governança."),
                ("Instruir os analistas a sempre lembrarem de digitar WHERE pais = 'BR' em todas as queries.", False, "Incorreto. Não provê segurança; analistas poderiam alterar a cláusula WHERE e vazar dados de outros países.")
            ],
            "explanation": "Row Filters no Unity Catalog utilizam UDFs que retornam um booleano: `CREATE FUNCTION filtro(pais STRING) RETURN IF(is_account_group_member('gerentes_globais'), true, pais = 'BR');`. O filtro é vinculado diretamente à tabela via `ALTER TABLE tbl SET ROW FILTER filtro ON (pais);`."
        },
        # Q46
        {
            "scenario": "Uma tabela de recursos humanos contém a coluna 'salario_base' e 'numero_cpf'. A equipe de auditoria deve ver os valores originais, mas qualquer outro usuário deve ver o CPF mascarado como '***.***.12' e o salário como nulo. Qual funcionalidade do Unity Catalog resolve essa necessidade de conformidade?",
            "options": [
                ("Criar funções SQL de mascaramento dinâmico e aplicá-las às colunas como Column Masks.", True, "Correto. Column Masks interceptam consultas de usuários não autorizados e retornam valores mascarados ou nulos, preservando os dados brutos para auditoria."),
                ("Excluir as colunas de CPF e salário permanentemente da base de dados.", False, "Incorreto. Os auditores e o RH precisam consultar esses dados."),
                ("Criptografar o disco rígido da máquina virtual do analista com BitLocker.", False, "Incorreto. Não afeta os resultados das queries executadas no Lakehouse."),
                ("Impedir todos os usuários da empresa de acessarem o Databricks.", False, "Incorreto. Inviabiliza a operação da empresa.")
            ],
            "explanation": "Column Masks no Unity Catalog permitem definir funções de transformação por coluna vinculadas com `ALTER TABLE tbl ALTER COLUMN cpf SET MASK func_mascara;`, garantindo privacidade de dados PII em conformidade com a LGPD e GDPR."
        },
        # Q47
        {
            "scenario": "Um arquiteto precisa saber quem foi o usuário que executou um comando DROP TABLE em uma tabela financeira confidencial na semana passada e a partir de qual endereço IP a ação foi disparada. Qual tabela do sistema provê essa trilha de auditoria?",
            "options": [
                ("system.access.audit", True, "Correto. A tabela system.access.audit registra todos os eventos de auditoria do Unity Catalog, incluindo user_identity.email, service_name, action_name, request_params e client_ip_address."),
                ("system.billing.usage", False, "Incorreto. system.billing.usage monitora consumo de DBUs para faturamento, não comandos de auditoria DDL/DML."),
                ("system.information_schema.tables", False, "Incorreto. Mostra metadados de tabelas atuais, não o histórico temporal de ações de auditoria."),
                ("system.dlt.event_log", False, "Incorreto. O event log do DLT é restrito a pipelines Delta Live Tables.")
            ],
            "explanation": "A tabela `system.access.audit` do Unity Catalog é o repositório centralizado de auditoria de conformidade, registrando operações DDL, acessos a dados, alterações de privilégios e IPs de origem."
        },
        # Q48
        {
            "scenario": "Uma organização precisa compartilhar uma tabela de cotações financeiras em tempo real com três bancos parceiros. Dois desses bancos utilizam AWS e Google Cloud e NÃO possuem Azure Databricks. Qual recurso do Databricks permite esse compartilhamento seguro e sem cópia física de dados?",
            "options": [
                ("Delta Sharing no modo Open Sharing (via protocolo REST aberto e arquivo de credencial bearer token).", True, "Correto. O Delta Sharing é um protocolo aberto que permite a qualquer cliente (Python, Pandas, Power BI, Apache Spark em qualquer nuvem) consultar tabelas compartilhadas diretamente do ADLS Gen2 sem ter Databricks."),
                ("Exportar os dados para arquivos CSV e enviá-los por e-mail com senha no arquivo ZIP.", False, "Incorreto. Inseguro, sujeito a limites de tamanho de anexo e perda total de governança."),
                ("Montar um servidor FTP Windows Server 2008 dentro da VNet do Databricks.", False, "Incorreto. Tecnologicamente defasado, inseguro e de alta manutenção."),
                ("Exigir que todos os bancos parceiros comprem assinaturas corporativas do Azure Databricks.", False, "Incorreto. O Delta Sharing Open Sharing elimina expressamente a necessidade de o destinatário possuir Databricks.")
            ],
            "explanation": "O Delta Sharing oferece compartilhamento aberto (Open Sharing) baseado em padrões abertos REST. O provedor gera um link de ativação onde o destinatário baixa um arquivo de credenciais seguro e acessa a tabela em tempo real sem duplicação de dados."
        },
        # Q49
        {
            "scenario": "Qual comando SQL cria um compartilhamento no Delta Sharing e adiciona a tabela 'prod.logistica.remessas' a ele?",
            "options": [
                ("CREATE SHARE share_logistica; ALTER SHARE share_logistica ADD TABLE prod.logistica.remessas;", True, "Correto. Essa é a sintaxe oficial ANSI SQL do Unity Catalog para criação e inclusão de tabelas em um Share."),
                ("EXPORT TABLE prod.logistica.remessas TO DELTA_SHARE 'share_logistica';", False, "Incorreto. Sintaxe inexistente."),
                ("GRANT DELTA_SHARING ON TABLE prod.logistica.remessas TO ALL;", False, "Incorreto. Delta Sharing exige a criação de um objeto Share e posterior atribuição a Recipients."),
                ("CREATE EXTERNAL RECIPIENT ON TABLE prod.logistica.remessas;", False, "Incorreto. Recipient representa o consumidor externo, não o conjunto de tabelas.")
            ],
            "explanation": "A gestão de Delta Sharing no Unity Catalog utiliza: `CREATE SHARE <nome_share>;` seguido por `ALTER SHARE <nome_share> ADD TABLE <nome_tabela>;`."
        },
        # Q50
        {
            "scenario": "Um engenheiro de dados precisa ler um arquivo de configuração JSON armazenado em um Volume do Unity Catalog localizado no caminho: catalogo 'lakehouse', schema 'parametros', volume 'configs', arquivo 'setup.json'. Qual caminho de sistema de arquivos deve ser passado para o código Python?",
            "options": [
                ("/Volumes/lakehouse/parametros/configs/setup.json", True, "Correto. Os Volumes do Unity Catalog são expostos no sistema de arquivos local do cluster através do ponto de montagem padrão /Volumes/<catalog>/<schema>/<volume>/<file>."),
                ("/dbfs/mnt/lakehouse/parametros/configs/setup.json", False, "Incorreto. /dbfs/mnt é a convenção de montagens legadas descontinuada."),
                ("abfss://setup.json@datalake.blob.core.windows.net", False, "Incorreto. Não utiliza o namespace de 3 níveis do Volume no Unity Catalog."),
                ("http://localhost:8080/configs/setup.json", False, "Incorreto. Volumes não são acessados via porta HTTP local.")
            ],
            "explanation": "Volumes no Unity Catalog utilizam a convenção de caminho POSIX padronizada: `/Volumes/<catalog_name>/<schema_name>/<volume_name>/<path_to_file>`."
        },
        # Q51
        {
            "scenario": "Qual privilégio do Unity Catalog deve ser concedido a um usuário para que ele consiga fazer upload de novos arquivos Parquet para dentro de um Volume existente?",
            "options": [
                ("WRITE VOLUME", True, "Correto. O privilégio WRITE VOLUME permite fazer upload, atualizar e excluir arquivos dentro de um volume no Unity Catalog."),
                ("SELECT", False, "Incorreto. SELECT aplica-se a tabelas e views, não a volumes."),
                ("EXECUTE", False, "Incorreto. EXECUTE aplica-se a funções SQL definidas por usuários (UDFs)."),
                ("USE CATALOG ONLY", False, "Incorreto. USE CATALOG apenas permite ver o catálogo, não escrever em volumes.")
            ],
            "explanation": "As permissões em Unity Catalog Volumes são: `READ VOLUME` (para leitura e download de arquivos) e `WRITE VOLUME` (para gravação, upload e deleção de arquivos)."
        },
        # Q52
        {
            "scenario": "Uma empresa precisa transferir a propriedade (ownership) de todas as tabelas de um schema para um novo grupo corporativo chamado 'engenharia_dados_lead'. Qual comando SQL transfere corretamente o proprietário de uma tabela?",
            "options": [
                ("ALTER TABLE prod.financeiro.contas OWNER TO `engenharia_dados_lead`;", True, "Correto. A instrução ALTER TABLE ... OWNER TO transfere a propriedade do objeto para o novo usuário ou grupo no Unity Catalog."),
                ("GRANT ALL PRIVILEGES ON TABLE prod.financeiro.contas TO `engenharia_dados_lead`;", False, "Incorreto. Conceder privilégios não altera o Owner do objeto."),
                ("UPDATE system.information_schema.tables SET owner = 'engenharia_dados_lead';", False, "Incorreto. Information Schema é somente leitura e não aceita comandos UPDATE diretos."),
                ("DROP TABLE prod.financeiro.contas; CREATE TABLE ...", False, "Incorreto. Recriar a tabela causaria indisponibilidade e perda de histórico de Delta Log.")
            ],
            "explanation": "No Unity Catalog, o comando oficial para alterar o dono de um objeto securable é `ALTER <OBJECT_TYPE> <object_name> OWNER TO <principal>;`."
        },
        # Q53
        {
            "scenario": "A equipe de governança de dados precisa rastrear o impacto de alterar o tipo de dados da coluna 'id_cliente' na tabela Bronze. Eles precisam visualizar todas as tabelas Silver, Gold e relatórios downstream que leem essa coluna. Qual funcionalidade nativa do Unity Catalog provê essa visualização gráfica?",
            "options": [
                ("Linhagem Automatizada de Dados (Automated Column-Level Lineage) no Catalog Explorer.", True, "Correto. O Unity Catalog captura e visualiza automaticamente a linhagem em nível de tabela e de coluna gerada por queries, notebooks, workflows e dashboards."),
                ("Exportar todos os scripts PySpark em PDF e realizar busca textual com Ctrl+F.", False, "Incorreto. Manual, sujeito a falhas e não captura fluxos de dados reais em produção."),
                ("Executar o comando VACUUM em todas as tabelas para ver quais falham.", False, "Incorreto. VACUUM limpa arquivos órfãos e não provê análise de impacto de colunas."),
                ("Criar um trigger de erro em cada tabela Silver.", False, "Incorreto. Inviabilizaria o pipeline em produção.")
            ],
            "explanation": "O Unity Catalog oferece Linhagem de Dados Automatizada (Lineage) nativa em nível de tabela e coluna, sem necessidade de instrumentação de código, permitindo análise completa de impacto upstream e downstream."
        },
        # Q54
        {
            "scenario": "Para classificar dados em conformidade com políticas de privacidade corporativas, os engenheiros precisam associar metadados indicando que uma coluna contém informações confidenciais (PII = true). Qual comando SQL aplica tags oficiais de governança no Unity Catalog?",
            "options": [
                ("ALTER TABLE prod.crm.clientes ALTER COLUMN email SET TAGS ('PII' = 'true', 'Compliance' = 'LGPD');", True, "Correto. A cláusula SET TAGS no Unity Catalog associa metadados estruturados de chave-valor a tabelas e colunas para catalogação e auditoria."),
                ("COMMENT ON COLUMN prod.crm.clientes.email IS 'PII=true';", False, "Incorreto. COMMENT insere apenas uma descrição em texto livre, não uma Tag de governança indexável."),
                ("LABEL TABLE prod.crm.clientes AS PII;", False, "Incorreto. Sintaxe inexistente no Databricks."),
                ("CREATE TAG ON DATABASE crm VALUES ('PII');", False, "Incorreto. Sintaxe inválida.")
            ],
            "explanation": "O Unity Catalog suporta governança através de Tags aplicadas diretamente a catálogos, schemas, tabelas e colunas via `SET TAGS ('chave' = 'valor')`, permitindo busca e classificação no Catalog Explorer."
        },
        # Q55
        {
            "scenario": "Qual é a permissão máxima que um usuário pode ter em todo o Metastore do Unity Catalog, com capacidade de criar catálogos, associar workspaces e delegar privilégios globais?",
            "options": [
                ("Metastore Admin (Administrador do Metastore).", True, "Correto. O Metastore Admin é a identidade com autoridade máxima de governança no Unity Catalog, responsável por gerenciar catálogos, concessões globais e external locations."),
                ("Workspace Admin.", False, "Incorreto. O Workspace Admin tem autoridade apenas sobre o workspace específico (criação de clusters, usuários locais), não governança global do Metastore."),
                ("Catalog Owner.", False, "Incorreto. Tem privilégios apenas dentro do catálogo que possui."),
                ("Subscription Reader no Azure.", False, "Incorreto. Permissão somente leitura no portal Azure.")
            ],
            "explanation": "No Unity Catalog, o `Metastore Admin` é o papel de mais alto nível de governança, acima dos administradores de workspaces individuais, controlando o metastore compartilhado por múltiplos workspaces."
        },
        # Q56
        {
            "scenario": "Uma empresa precisa consultar tabelas armazenadas em um banco de dados relacional Azure SQL Database diretamente a partir de consultas SQL no Azure Databricks, sem precisar copiar ou ingerir os dados previamente para o Lakehouse. Qual recurso do Unity Catalog provê essa federação de consultas?",
            "options": [
                ("Lakehouse Federation (criando uma Connection e um Foreign Catalog no Unity Catalog).", True, "Correto. O Lakehouse Federation permite criar Foreign Catalogs mapeados para fontes externas (Azure SQL, Snowflake, PostgreSQL, etc.), consultando-as com sintaxe SQL unificada sem replicação física."),
                ("Fazer o backup do Azure SQL em fita magnética e restaurar no Databricks.", False, "Incorreto. Inviável e não é uma solução analítica em nuvem."),
                ("Criar um script em Bash que exporta tabelas para arquivos TXT via FTP a cada minuto.", False, "Incorreto. Extremamente lento, não escalável e inseguro."),
                ("Desabilitar o Unity Catalog e usar JDBC puro sem governança.", False, "Incorreto. Perde o catálogo unificado e as políticas de governança centralizadas.")
            ],
            "explanation": "Lakehouse Federation no Unity Catalog permite criar conexões com bancos de dados externos e mapeá-los como 'Foreign Catalogs', viabilizando consultas federadas cross-source (ex: unindo Azure SQL com Delta Lake) sem movimentação de dados."
        },
        # Q57
        {
            "scenario": "Uma organização financeira precisa migrar 500 tabelas legadas do Hive Metastore tradicional (default) para o Unity Catalog. Qual comando automatizado ou ferramenta é fornecida pela Databricks para criar cópias sincronizadas ou atualizar metadados sem duplicar arquivos Parquet?",
            "options": [
                ("Utilizar o utilitário SYNC (ou Unity Catalog Upgrade Wizard) para sincronizar schemas e tabelas legadas para o Unity Catalog.", True, "Correto. O comando SYNC e o assistente de atualização de tabelas (Upgrade Wizard) facilitam a transição do Hive Metastore legado para o Unity Catalog de forma assistida."),
                ("Excluir todas as tabelas legadas com DROP DATABASE CASCADE e começar do zero.", False, "Incorreto. Causaria perda de dados históricos corporativos."),
                ("Criar links simbólicos no Windows Explorer apontando para os arquivos DBFS.", False, "Incorreto. Não tem relação com o ecossistema de nuvem Databricks."),
                ("Substituir o Spark por um banco de dados Microsoft Access local.", False, "Incorreto. Incompatível com volumes de Big Data corporativos.")
            ],
            "explanation": "O comando `SYNC SCHEMA <target> FROM <source>` e o Upgrade Wizard integrado na UI do Databricks permitem migrar metadados de tabelas externas do Hive Metastore diretamente para o Unity Catalog."
        },
        # Q58
        {
            "scenario": "Um usuário que possui apenas o privilégio 'SELECT' em uma tabela do Unity Catalog tenta executar o comando 'DELETE FROM prod.vendas.pedidos WHERE status = 'CANCELADO';'. O que acontece com a execução?",
            "options": [
                ("A consulta falha com erro de permissão negada, pois o comando DELETE exige o privilégio MODIFY na tabela.", True, "Correto. Operações de modificação de dados (INSERT, UPDATE, DELETE, MERGE) no Unity Catalog exigem o privilégio MODIFY."),
                ("A consulta executa com sucesso, pois SELECT inclui privilégios de exclusão.", False, "Incorreto. SELECT concede estritamente leitura de dados."),
                ("A consulta apaga todos os dados do catálogo inteiro.", False, "Incorreto. Cláusulas WHERE filtram linhas e privilégios impedem execuções não autorizadas."),
                ("O Databricks reinicia o nó Driver automaticamente.", False, "Incorreto. Erros de privilégio retornam exceção SQL padrão sem reiniciar hardware.")
            ],
            "explanation": "No Unity Catalog, o privilégio `SELECT` é de somente leitura. Para alterar dados (operações de escrita, update, delete, merge), o usuário ou grupo deve possuir obrigatoriamente o privilégio `MODIFY`."
        },
        # Q59
        {
            "scenario": "Como deve ser declarada uma função SQL no Unity Catalog para servir de Column Mask mascarando o endereço de e-mail de usuários para quem não pertence ao grupo 'rh_auditoria'?",
            "options": [
                ("CREATE OR REPLACE FUNCTION seguranca.mascarar_email(email STRING) RETURN IF(is_account_group_member('rh_auditoria'), email, '***@empresa.com');", True, "Correto. Funções de Column Mask recebem o valor original como parâmetro e retornam o valor original se autorizado ou o valor mascarado se o usuário não pertencer ao grupo aprovado."),
                ("CREATE MASK FUNCTION email ON TABLE clientes HIDE ALL;", False, "Incorreto. Sintaxe inexistente no SQL do Databricks."),
                ("ALTER FUNCTION email SET PASSWORD 'rh_auditoria';", False, "Incorreto. Sintaxe inválida."),
                ("DROP COLUMN email WHERE user <> 'rh_auditoria';", False, "Incorreto. DROP COLUMN remove a coluna da tabela para todos os usuários.")
            ],
            "explanation": "Funções de mascaramento são UDFs SQL padrão que avaliam o contexto do usuário com `is_account_group_member()` ou `current_user()`, retornando o dado real ou a máscara."
        },
        # Q60
        {
            "scenario": "Um desenvolvedor precisa revogar o privilégio de criação de tabelas de um grupo de contratados externos no schema 'homologacao'. Qual comando SQL deve ser executado?",
            "options": [
                ("REVOKE CREATE TABLE ON SCHEMA dev_catalog.homologacao FROM `contratados_externos`;", True, "Correto. O comando ANSI SQL oficial para remover permissões no Unity Catalog é REVOKE <privilege> ON <securable> FROM <principal>."),
                ("DELETE PERMISSION CREATE TABLE FROM `contratados_externos`;", False, "Incorreto. Sintaxe inválida."),
                ("DENY CREATE TABLE TO `contratados_externos`;", False, "Incorreto. O Unity Catalog opera com modelo explícito de concessão (GRANT) e revogação (REVOKE)."),
                ("REMOVE USER FROM SCHEMA dev_catalog.homologacao;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "No Unity Catalog, permissões concedidas previamente via `GRANT` são revogadas utilizando a instrução padrão `REVOKE <privilégio> ON <objeto> FROM <identidade>;`."
        },
        # Q61
        {
            "scenario": "Por que o modelo de governança do Unity Catalog é considerado superior às antigas Table Access Controls (Table ACLs) legadas do Hive Metastore?",
            "options": [
                ("O Unity Catalog centraliza a governança em múltiplos workspaces e clouds, suporta 3-Level Namespace, Volumes, Row/Column security e Linhagem automática independente do runtime.", True, "Correto. O Unity Catalog oferece uma plataforma unificada e desacoplada dos workspaces, enquanto Table ACLs legadas eram limitadas ao workspace local e não suportavam arquivos não estruturados ou linhagem."),
                ("Table ACLs legadas exigiam o pagamento de US$ 10.000 adicionais por usuário.", False, "Incorreto. Table ACLs não tinham custo adicional de licença, eram apenas tecnicamente limitadas."),
                ("O Unity Catalog desliga todos os servidores da nuvem a cada hora.", False, "Incorreto. O Unity Catalog é um serviço de governança altamente disponível."),
                ("Table ACLs legadas só funcionavam em máquinas locais sem internet.", False, "Incorreto. Funcionavam na nuvem, porém presas ao workspace legado.")
            ],
            "explanation": "O Unity Catalog resolve as limitações das Table ACLs legadas, fornecendo governança regional multi-workspace, auditoria centralizada em `system.access.audit`, linhagem ponta a ponta e suporte a volumes."
        },
        # Q62
        {
            "scenario": "Um arquiteto precisa configurar um alerta que dispara sempre que um usuário do workspace tentar conceder privilégios administrativos a outra pessoa. Qual consulta na tabela system.access.audit filtra essas ações?",
            "options": [
                ("SELECT * FROM system.access.audit WHERE service_name = 'unityCatalog' AND action_name IN ('grantPermissions', 'revokePermissions');", True, "Correto. Ações de controle de acesso do Unity Catalog registram action_name como 'grantPermissions' e 'revokePermissions'."),
                ("SELECT * FROM system.billing.usage WHERE sku_name = 'ADMIN_ALERT';", False, "Incorreto. system.billing.usage monitora apenas cobrança de DBUs."),
                ("SELECT * FROM system.information_schema.table_privileges WHERE is_grantable = 'ALERT';", False, "Incorreto. Consulta inválida."),
                ("SELECT * FROM system.dlt.event_log WHERE event_type = 'SECURITY';", False, "Incorreto. DLT event log registra execução de pipelines de dados, não auditoria de governança do catálogo.")
            ],
            "explanation": "Na tabela `system.access.audit`, os eventos do Unity Catalog contêm `service_name = 'unityCatalog'` e registram concessões e revogações com `action_name` igual a `grantPermissions` ou `revokePermissions`."
        },
        # Q63
        {
            "scenario": "Ao criar uma tabela externa no Unity Catalog, um engenheiro digita: CREATE TABLE cat.sch.tbl_ext LOCATION 'abfss://raw@datalake.dfs.core.windows.net/vendas'. A query falha com erro informando que o caminho especificado não é coberto por nenhuma External Location aprovada. Como resolver?",
            "options": [
                ("Criar previamente uma External Location no Unity Catalog que englobe o caminho 'abfss://raw@datalake.dfs.core.windows.net/vendas' associada a uma Storage Credential válida.", True, "Correto. O Unity Catalog proíbe a criação de tabelas externas em caminhos que não estejam explicitamente cobertos por uma External Location registrada e autorizada."),
                ("Adicionar a chave da conta de armazenamento (Storage Account Key) diretamente no comando CREATE TABLE.", False, "Incorreto. Chaves em texto claro no SQL são bloqueadas e violam a segurança do Unity Catalog."),
                ("Mudar o caminho para um disco rígido C:\\ local da máquina de desenvolvimento.", False, "Incorreto. Caminhos locais de desktop não são suportados em clusters de nuvem."),
                ("Excluir o catálogo e utilizar uma pasta temporária do Linux.", False, "Incorreto. Não cria a tabela corporativa externa necessária.")
            ],
            "explanation": "Tabelas e volumes externos no Unity Catalog exigem que o caminho de armazenamento na nuvem esteja contido dentro de uma `External Location` previamente registrada e governada."
        },
        # Q64
        {
            "scenario": "Em uma instituição financeira, pesquisadores precisam analisar dados clínicos, mas não podem ter acesso aos nomes completos dos pacientes. Uma Column Mask foi associada à coluna 'nome_paciente'. O que é retornado para um pesquisador que executa 'SELECT nome_paciente FROM clinica.pacientes;'?",
            "options": [
                ("O resultado da transformação definida na função de mascaramento (ex: 'PACIENTE_ANONIMO' ou iniciais), enquanto as demais colunas não mascaradas são retornadas normalmente.", True, "Correto. A Column Mask substitui os valores daquela coluna específica dinamicamente em tempo de execução sem afetar as outras colunas da consulta."),
                ("Uma mensagem de erro de compilação bloqueando a execução da consulta inteira.", False, "Incorreto. A consulta executa com sucesso; apenas o conteúdo da coluna mascarada é transformado."),
                ("Todos os dados originais sem nenhuma alteração.", False, "Incorreto. Usuários não autorizados recebem o valor mascarado."),
                ("O computador do pesquisador é desconectado da rede da empresa.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "Column Masks operam de forma transparente: a consulta SQL executa normalmente, mas os valores exibidos para os usuários não privilegiados são os valores substituídos pela função mascaradora."
        },
        # Q65
        {
            "scenario": "Qual comando SQL lista todas as concessões de privilégios ativas na tabela 'prod.vendas.pedidos'?",
            "options": [
                ("SHOW GRANTS ON TABLE prod.vendas.pedidos;", True, "Correto. A instrução SHOW GRANTS exibe todos os usuários e grupos com privilégios concedidos naquele objeto específico."),
                ("LIST PERMISSIONS IN TABLE prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente."),
                ("SELECT * FROM sys.permissions_table WHERE name = 'prod.vendas.pedidos';", False, "Incorreto. Sintaxe inválida no Databricks."),
                ("DESCRIBE HISTORY prod.vendas.pedidos;", False, "Incorreto. DESCRIBE HISTORY exibe commits de transações do Delta Lake, não concessões de privilégios.")
            ],
            "explanation": "O comando padrão ANSI SQL no Databricks para inspecionar permissões é `SHOW GRANTS ON <securable_type> <securable_name>;`."
        },
        # Q66
        {
            "scenario": "Qual objeto do Unity Catalog é o contêiner de mais alto nível na hierarquia de dados, servindo como agrupador de múltiplos schemas e bancos de dados lógicos?",
            "options": [
                ("Catalog (Catálogo).", True, "Correto. O Catálogo é o primeiro nível da hierarquia de 3 níveis (Catalog -> Schema -> Tabela/View/Volume)."),
                ("Schema.", False, "Incorreto. Schema é o segundo nível, contido dentro de um Catálogo."),
                ("Volume.", False, "Incorreto. Volume é um objeto folha, contido dentro de um Schema."),
                ("Partition.", False, "Incorreto. Partição é uma divisão física de armazenamento dentro de uma tabela.")
            ],
            "explanation": "A hierarquia de dados do Unity Catalog é estritamente: Metastore (nível regional) > Catalog (primeiro nível lógico) > Schema (segundo nível lógico) > Table/View/Volume (terceiro nível)."
        },
        # Q67
        {
            "scenario": "Uma organização multinacional possui cientistas de dados utilizando clusters interativos com Databricks Runtime padrão. Qual modo de acesso ao cluster deve ser configurado para que o cluster respeite 100% as regras de governança do Unity Catalog para um único usuário?",
            "options": [
                ("Modo de acesso 'Single User' associado à identidade Entra ID do cientista de dados.", True, "Correto. Clusters Single User são totalmente compatíveis com o Unity Catalog, suportam todas as linguagens (Python, Scala, R, SQL) e operam com o contexto de segurança daquele usuário específico."),
                ("Modo 'No Isolation Shared' legado.", False, "Incorreto. Desabilita as travas de segurança e não é compatível com governança rigorosa do Unity Catalog."),
                ("Modo 'Driver Only' sem suporte a rede.", False, "Incorreto. Impede a execução de jobs distribuídos."),
                ("Executar sem nenhuma configuração de modo de acesso.", False, "Incorreto. O Databricks exige a seleção do modo de acesso (Single User ou Shared) em clusters com Unity Catalog.")
            ],
            "explanation": "Para desenvolvedores individuais que precisam rodar Python, Scala, R e SQL com suporte completo ao Unity Catalog, o modo 'Single User' é o padrão recomendado."
        },
        # Q68
        {
            "scenario": "Quais DUAS ações são necessárias para que uma aplicação em Python externa conecte-se a uma tabela compartilhada via Delta Sharing sem possuir uma conta no Azure Databricks? (Selecione duas opções)",
            "options": [
                ("O administrador do Databricks cria um Recipient no Delta Sharing e envia o link de ativação seguro para a organização parceira.", True, "Correto. O Recipient gera o token de autenticação e credencial de acesso."),
                ("O parceiro externo utiliza o conector de código aberto 'delta-sharing' (ex: delta_sharing.load_as_pandas()) informando o arquivo de credenciais .share baixado.", True, "Correto. A biblioteca cliente de Delta Sharing lê diretamente os dados autorizados via REST API sem precisar de Databricks."),
                ("O parceiro externo deve pagar uma licença do Microsoft Windows Server para a Databricks.", False, "Incorreto. Delta Sharing é um protocolo aberto de código aberto."),
                ("Os arquivos Parquet devem ser convertidos em planilhas do Microsoft Excel .xls.", False, "Incorreto. Inviável e tecnicamente incorreto."),
                ("O administrador deve liberar acesso irrestrito de escrita em todo o metastore.", False, "Incorreto. Violação crítica de segurança; o compartilhamento é somente leitura.")
            ],
            "type": "multiple",
            "explanation": "No Delta Sharing aberto (Open Sharing), o administrador cria um Recipient que gera um perfil de conexão (.share com bearer token). O parceiro externo utiliza qualquer biblioteca compatível (Python, Power BI, Spark) para ler os dados diretamente."
        },
        # Q69
        {
            "scenario": "Um arquiteto precisa revogar o acesso a uma tabela compartilhada via Delta Sharing para um destinatário parceiro cujo contrato encerrou. Qual comando SQL executa a revogação?",
            "options": [
                ("REVOKE SELECT ON SHARE share_parceiros FROM RECIPIENT recipient_empresa_b;", True, "Correto. Permissões de compartilhamento são revogadas com REVOKE SELECT ON SHARE <share> FROM RECIPIENT <recipient>."),
                ("DELETE STORAGE FROM RECIPIENT recipient_empresa_b;", False, "Incorreto. Sintaxe inexistente."),
                ("ALTER TABLE DROP SHARE;", False, "Incorreto. Sintaxe inválida."),
                ("KILL CONNECTION recipient_empresa_b;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O acesso de um recipient a um share no Unity Catalog é controlado via concessões padrão: `REVOKE SELECT ON SHARE <nome_share> FROM RECIPIENT <nome_recipient>;`."
        },
        # Q70
        {
            "scenario": "Em um schema governado pelo Unity Catalog, um engenheiro cria uma tabela com: CREATE TABLE cat.sch.tbl (id INT);. Onde os dados físicos dessa tabela serão salvos no ADLS Gen2?",
            "options": [
                ("No caminho de armazenamento raiz padrão configurado para o schema 'sch' ou para o catálogo 'cat' associado ao Metastore.", True, "Correto. Managed Tables gravam automaticamente seus dados no local de armazenamento gerenciado definido na hierarquia do schema/catálogo/metastore."),
                ("No desktop do usuário que digitou o comando.", False, "Incorreto. Dados residem na nuvem corporativa."),
                ("Em um pendrive conectado ao servidor da Microsoft.", False, "Incorreto. Resposta fictícia."),
                ("No banco de dados local MySQL do nó Driver.", False, "Incorreto. O Lakehouse utiliza ADLS Gen2.")
            ],
            "explanation": "Managed Tables não exigem cláusula LOCATION; o Unity Catalog armazena seus dados no storage gerenciado definido na criação do Schema, do Catálogo ou do Metastore."
        },
        # Q71
        {
            "scenario": "Qual comando SQL cria um Managed Volume chamado 'raw_logs' dentro do catálogo 'prod' e schema 'telemetria'?",
            "options": [
                ("CREATE VOLUME prod.telemetria.raw_logs;", True, "Correto. A criação de um Managed Volume utiliza a sintaxe direta CREATE VOLUME <catalog>.<schema>.<volume_name>; sem especificar LOCATION."),
                ("CREATE MANAGED FOLDER prod.telemetria.raw_logs;", False, "Incorreto. Sintaxe inexistente; o objeto chama-se VOLUME."),
                ("MKDIR /Volumes/prod/telemetria/raw_logs;", False, "Incorreto. MKDIR é comando de terminal shell, não comando SQL DDL do catálogo."),
                ("MOUNT VOLUME prod.telemetria.raw_logs ON DBFS;", False, "Incorreto. Volumes não utilizam montagem legada DBFS.")
            ],
            "explanation": "Para criar um Managed Volume, a instrução SQL oficial é: `CREATE VOLUME <catalog>.<schema>.<volume_name>;`. Caso fosse um External Volume, adicionaria-se a cláusula `LOCATION '<path>'`."
        },
        # Q72
        {
            "scenario": "Um usuário tenta ler um volume com: SELECT * FROM read_files('/Volumes/prod/raw/dados/*.csv');. Qual permissão mínima ele precisa ter no volume para executar a leitura dos arquivos?",
            "options": [
                ("READ VOLUME (além de USE CATALOG e USE SCHEMA na hierarquia pai).", True, "Correto. A permissão de leitura de arquivos em um Volume é o privilégio READ VOLUME."),
                ("MODIFY", False, "Incorreto. MODIFY é para alterar dados tabulares."),
                ("WRITE VOLUME", False, "Incorreto. WRITE VOLUME é necessário para gravação e upload, não apenas leitura."),
                ("DROP TABLE", False, "Incorreto. Permissão destrutiva de exclusão de tabelas.")
            ],
            "explanation": "A função `read_files()` lê dados de arquivos em volumes e exige o privilégio `READ VOLUME` no volume correspondente, junto com `USE CATALOG` e `USE SCHEMA`."
        },
        # Q73
        {
            "scenario": "Ao consultar o histórico de linhagem de uma tabela Gold no Catalog Explorer, um analista percebe que a linhagem de colunas está disponível. Qual mecanismo produz esses dados de linhagem?",
            "options": [
                ("O Unity Catalog analisa os planos lógicos de execução das queries submetidas no Spark e registra automaticamente as dependências de colunas sem overhead de código.", True, "Correto. A linhagem é gerada de forma automatizada e transparente a partir da instrumentação nativa do Catalyst Optimizer no Unity Catalog."),
                ("O desenvolvedor precisa digitar manualmente a linhagem em um arquivo JSON em cada deploy.", False, "Incorreto. A linhagem é 100% automatizada."),
                ("Um analista da Microsoft verifica as queries manualmente e atualiza o gráfico.", False, "Incorreto. Processo automático de software."),
                ("A linhagem só funciona se os dados forem gravados em formato CSV.", False, "Incorreto. Funciona nativamente com Delta Lake e qualquer formato suportado.")
            ],
            "explanation": "O motor do Unity Catalog intercepta os planos lógicos resolvidos no Spark e extrai as relações de entrada e saída em tempo real, populando as tabelas de linhagem automaticamente."
        },
        # Q74
        {
            "scenario": "Como a governança do Unity Catalog trata permissões concedidas a grupos em comparação com permissões concedidas a usuários individuais?",
            "options": [
                ("Recomenda-se conceder privilégios exclusivamente a Grupos sincronizados via SCIM do Microsoft Entra ID para simplificar a gestão e auditoria, evitando concessões a usuários individuais.", True, "Correto. Conceder acessos a grupos (Role-Based Access Control) é a melhor prática oficial do exame DP-750, evitando privilégios órfãos e complexidade de manutenção."),
                ("O Unity Catalog proíbe o uso de grupos e permite permissões apenas para CPFs individuais.", False, "Incorreto. Grupos são o padrão recomendado."),
                ("Grupos só podem ter privilégios de leitura aos domingos.", False, "Incorreto. Resposta fictícia."),
                ("Conceder privilégios a grupos dobra o consumo de DBUs do workspace.", False, "Incorreto. Governança de catálogo não altera a taxa de DBU de clusters.")
            ],
            "explanation": "A prática recomendada da Microsoft é aplicar RBAC concedendo privilégios a grupos de segurança centralizados gerenciados via Entra ID e propagados pelo SCIM."
        },
        # Q75
        {
            "scenario": "Um engenheiro precisa remover uma External Location chamada 'loc_antiga' do Unity Catalog. Qual comando SQL realiza essa exclusão de metadados?",
            "options": [
                ("DROP EXTERNAL LOCATION loc_antiga;", True, "Correto. A sintaxe oficial para remoção de uma localização externa no catálogo é DROP EXTERNAL LOCATION <nome>;."),
                ("DELETE FROM system.locations WHERE name = 'loc_antiga';", False, "Incorreto. Não se excluem objetos do sistema via comando DELETE."),
                ("UNMOUNT loc_antiga;", False, "Incorreto. UNMOUNT é comando legado do DBFS."),
                ("ALTER LOCATION loc_antiga SET DISABLED;", False, "Incorreto. Sintaxe inválida.")
            ],
            "explanation": "Objetos de infraestrutura de storage no Unity Catalog são removidos com comandos DDL padrão: `DROP EXTERNAL LOCATION <nome>;` e `DROP STORAGE CREDENTIAL <nome>;`."
        },
        # Q76
        {
            "scenario": "Qual função SQL interna do Databricks retorna o endereço de e-mail do usuário autenticado que está executando a consulta no momento, amplamente utilizada em Row Filters?",
            "options": [
                ("current_user()", True, "Correto. A função SQL current_user() retorna o e-mail/identidade do usuário ativo que disparou a consulta."),
                ("get_user_ip()", False, "Incorreto. Retorna endereço IP, não a identidade Entra ID do usuário."),
                ("session_id()", False, "Incorreto. Retorna identificador da sessão Spark."),
                ("who_is_there()", False, "Incorreto. Função fictícia.")
            ],
            "explanation": "Em funções de segurança de linha e coluna, `current_user()` e `is_account_group_member()` são as funções nativas essenciais para autenticação contextual do solicitante."
        }
    ]
    return d2_specs

