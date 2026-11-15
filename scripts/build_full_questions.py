#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Compilador Mestre de 184 Questões Estruturadas para scripts/raw_questions_data.py
Garante rotação matemática equilibrada de alternativas (25% A, 25% B, 25% C, 25% D),
estudos de caso vinculados a cada 3 questões e conformidade estrita com o DP-750.
"""

import json
import os
import sys

# Importa os 4 domínios
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.questions_d1 import get_d1_questions
from scripts.questions_d2 import get_d2_questions
from scripts.questions_d3 import get_d3_questions
from scripts.questions_d4 import get_d4_questions

def build_questions():
    d1 = get_d1_questions() # 38 questões
    d2 = get_d2_questions() # 38 questões
    d3 = get_d3_questions() # 54 questões
    d4 = get_d4_questions() # 54 questões

    all_specs = [
        (1, "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)", d1),
        (2, "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)", d2),
        (3, "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)", d3),
        (4, "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)", d4)
    ]

    questions = []
    q_id = 1
    letters = ["A", "B", "C", "D", "E"]

    for dom_id, dom_name, specs in all_specs:
        for spec in specs:
            q_type = spec.get("type", "single")
            opts_raw = spec["options"]
            case_id = f"case-{(q_id % 8) + 1:02d}" if q_id % 3 == 0 else None

            # Rotação cíclica das alternativas para distribuir uniformemente o gabarito
            # A, B, C, D têm distribuição balanceada de 25%
            n_opts = len(opts_raw)
            if q_type == "single":
                shift = (q_id - 1) % n_opts
                # Rotaciona para que o correto caia no índice shift
                rotated_opts = [None] * n_opts
                # O primeiro item de opts_raw é o correto
                rotated_opts[shift] = opts_raw[0]
                # Preenche as outras posições com os distratores
                distractor_idx = 1
                for pos in range(n_opts):
                    if pos != shift:
                        rotated_opts[pos] = opts_raw[distractor_idx]
                        distractor_idx += 1
            else:
                # Para múltipla escolha, rotaciona cíclico simples
                shift = (q_id - 1) % n_opts
                rotated_opts = opts_raw[shift:] + opts_raw[:shift]

            # Monta opções com letras
            options = []
            correct_answers = []
            for idx, opt_tuple in enumerate(rotated_opts):
                let = letters[idx]
                is_corr = opt_tuple[1]
                options.append({
                    "id": let,
                    "text": opt_tuple[0],
                    "correct": is_corr,
                    "explanation": opt_tuple[2]
                })
                if is_corr:
                    correct_answers.append(let)

            questions.append({
                "id": q_id,
                "domain": dom_id,
                "domainName": dom_name,
                "type": q_type,
                "caseStudyId": case_id,
                "question": spec["scenario"],
                "options": options,
                "correctAnswers": correct_answers,
                "overallExplanation": spec["explanation"]
            })
            q_id += 1

    return questions

def main():
    questions = build_questions()
    assert len(questions) == 184, f"Esperado 184 questões, obtido {len(questions)}"
    print(f"Total de Questões validadas: {len(questions)}")
    
    # Estatísticas de Gabarito
    single_q = [q for q in questions if q["type"] == "single"]
    counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for q in single_q:
        counts[q["correctAnswers"][0]] += 1
    print(f"Distribuição do Gabarito em Questões Únicas ({len(single_q)}Q): {counts}")

if __name__ == "__main__":
    main()
