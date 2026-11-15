# 🏛️ Arquitetura do Sistema: Databricks Formation DP-750

Este documento descreve a arquitetura de engenharia de software, os pilares pedagógicos e os padrões de design da plataforma **"Databricks Formation — Prepare to DP-750"**.

---

## 1. Visão Geral da Arquitetura

A plataforma foi concebida sob os princípios de:
- **Zero Dependências Pesadas em Runtime:** HTML5 semântico puro, CSS modular e Vanilla JavaScript moderno sem bundlers pesados ou frameworks lentos.
- **Alta Densidade de Informação (Padrão Edward Tufte):** Uso de sidenotes, tabelas de alta densidade, tipografia serifada de alta legibilidade e diagramas amplos.
- **Portabilidade Total:** Compatível com hospedagem estática direta (Vercel, GitHub Pages, Azure Static Web Apps ou servidor local Python).

```
.
├── assets/
│   ├── tufte.css              # Tipografia Tufte, sidenotes e tabelas densas
│   ├── vark.css               # Design System Databricks (Lava Red, Navy Dark, Teal)
│   ├── lens.js                # Motor de 6 Lentes, Audio Player Sticky e Fisher-Yates
│   ├── exam-simulator.js      # Motor Pearson VUE com Split-Screen e cronômetro
│   ├── exam-questions.js      # Banco de +180 questões e 8 estudos de caso
│   └── audio/                 # 15 Áudios neurais PT-BR das lições
├── lessons/                   # 15 Lições completas com 6 Lentes e VARK
├── labs/                      # 15 Labs executáveis em Python sem deps
├── reference/                 # 6 Folhas de referência rápida
├── simulados/                 # Centro Pearson VUE com Split-Screen
├── scripts/                   # Scripts de automação e compilação
├── tests/                     # Testes automatizados de integridade
├── docs/                      # Documentação de arquitetura e manutenção
├── Makefile                   # Automação de testes e verificação
└── vercel.json                # Configuração de deploy estático Vercel
```

---

## 2. Metodologia Multi-Lente (6 Níveis de Profundidade)

Cada lição implementa marcação de atributos `data-lens-block` e `data-lens`:
1. `all`: Exibe todas as camadas integradas.
2. `junior`: Conceitos elementares e analogias do cotidiano.
3. `pleno`: Detalhes de implementação em PySpark e Spark SQL.
4. `senior`: Matrizes de decisão arquitetural e análise de pegadinhas do DP-750.
5. `staff`: Análise de código-fonte, otimizações de baixo nível e algoritmos de execução interna.
6. `c-level`: Estratégia FinOps, dimensionamento de DBUs, governança e TCO.

O script `assets/lens.js` intercepta a seleção do usuário, persiste no `localStorage` via chave `dp750_active_lens` e escuta os atalhos de teclado `[0..5]`.

---

## 3. Os 4 Canais Sensoriais VARK

- **[A] Auditivo:** Narração de alta precisão técnica com player sticky fixado na base.
- **[V] Visual:** Diagrama arquitetural SVG (`viewBox="0 0 960 360"`) com hotspots e Dark UI simulando o portal Azure Databricks.
- **[R] Leitura/Escrita:** Textos aprofundados com sidenotes Tufte e tabelas comparativas.
- **[K] Cinestésico:**
  - Simulador interativo browser-side para cálculo de DBUs e particionamento.
  - Lab prático Python local em `labs/`.
  - Desafio Flash DP-750 com embaralhamento dinâmico Fisher-Yates a cada abertura de página.

---

## 4. Motor de Simulado Pearson VUE

O motor em `assets/exam-simulator.js` fornece:
- **8 Estudos de Caso Corporativos Split-Screen** divididos em 5 abas (`Visão Geral`, `Arquitetura Atual`, `Requisitos de Dados`, `Segurança/Unity Catalog`, `Problemas de Pipeline`).
- **6 Modos de Exame:** Padrão Oficial (55Q/100m/corte 700), Maratona (90Q), Banco Completo (184Q), Domínio Específico, Estudos de Caso e Revisão Rápida.
- **Embaralhamento Total Fisher-Yates:** Questões e alternativas são reembaralhadas a cada tentativa, recalculando o mapeamento das letras corretas para evitar vício cognitivo na mesma opção.

