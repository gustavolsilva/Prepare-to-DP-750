# 🛠️ Guia para Mantenedores e Autores de Conteúdo

Este documento orienta mantenedores e instrutores sobre como evoluir e expandir o currículo da plataforma **Databricks Formation — Prepare to DP-750** garantindo que a suíte de testes (`make verify`) continue passando com 100% de sucesso.

---

## 1. Adicionando ou Editando uma Lição

1. Toda lição deve residir em `lessons/` com a convenção de nomenclatura:
   `XXXX-slug-da-licao.html` (onde `XXXX` é o número com 4 dígitos de `0001` a `9999`).
2. A lição deve obrigatoriamente conter:
   - Seletor de 6 Lentes no topo.
   - Os blocos de conteúdo com os atributos `data-lens="junior"`, `data-lens="pleno"`, `data-lens="senior"`, `data-lens="staff"` e `data-lens="c-level"`.
   - Os 4 canais VARK (`vark-badge-v`, `vark-badge-a`, `vark-badge-r`, `vark-badge-k`).
   - O player sticky de áudio referenciando `../assets/audio/lesson-XXXX-pt.mp3`.
   - O Flash Quiz com a classe `.flash-quiz-box`, opções com `data-correct` e o botão `.btn-shuffle`.
3. Deve existir o arquivo de áudio correspondente em `assets/audio/lesson-XXXX-pt.mp3`.
4. Deve existir o script Python de lab correspondente em `labs/lesson_XXXX_lab.py`.

---

## 2. Adicionando ou Expandindo Questões do Simulado

1. Abra `scripts/expand_exam_bank.py`.
2. Adicione tópicos, cenários ou novos estudos de caso na lista `CASE_STUDIES` ou `DOMAINS_CONFIG`.
3. Execute:
   ```bash
   make build-exam
   ```
4. O script recompilará `assets/exam-questions.js`.

---

## 3. Regras para SVGs (Zero Colisão de Texto)

- O `viewBox` deve ser amplo (mínimo `960x360` ou `960x540`).
- Elementos `<text>` na mesma coluna horizontal devem ter distância vertical no eixo `y` de pelo menos 20px.
- Textos longos devem utilizar `<tspan>` ou blocos de quebra limpos.

---

## 4. Validação Pré-Commit Obrigatória

Antes de qualquer commit ou deploy, execute a suíte de verificação completa:
```bash
make verify
```

Se todos os testes passarem (`✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO`), o projeto está pronto para deploy imediato.

