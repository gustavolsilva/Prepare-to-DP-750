.PHONY: help setup test test-labs verify serve build-exam clean

PYTHON := python3

help:
	@echo "======================================================================"
	@echo " Databricks Formation — Prepare to DP-750 Automation Makefile"
	@echo "======================================================================"
	@echo " make setup       : Configura o ambiente virtual Python (.venv)"
	@echo " make test        : Executa testes de integridade de currículo"
	@echo " make test-labs   : Executa todos os 15 labs Python de engenharia"
	@echo " make build-exam  : Regenera o banco de +180 questões do exame"
	@echo " make verify      : Executa a bateria completa de validação (Zero Regressões)"
	@echo " make serve       : Inicia servidor HTTP local para desenvolvimento na porta 8000"
	@echo " make clean       : Limpa arquivos temporários e caches"
	@echo "======================================================================"

setup:
	@echo "==> Configurando ambiente Python..."
	@if [ ! -d ".venv" ]; then $(PYTHON) -m venv --without-pip .venv; fi
	@echo "==> Ambiente configurado com sucesso."

build-exam:
	@echo "==> Compilando banco de questões (+180 questões e 8 estudos de caso)..."
	@$(PYTHON) scripts/expand_exam_bank.py

test:
	@echo "==> Executando testes de integridade do currículo..."
	@$(PYTHON) -m unittest discover -s tests -p "test_*.py" -v

test-labs:
	@echo "==> Executando os 15 Labs Python..."
	@for lab in labs/lesson_*_lab.py; do \
		echo "--> Executando $$lab..."; \
		$(PYTHON) $$lab || exit 1; \
	done
	@echo "==> Todos os 15 labs foram executados com sucesso!"

verify: build-exam test-labs test
	@echo "======================================================================"
	@echo " ✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO: CURRÍCULO 100% ÍNTEGRO!"
	@echo "======================================================================"

serve:
	@echo "==> Iniciando Databricks Formation em http://localhost:8000..."
	@$(PYTHON) -m http.server 8000

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "==> Limpeza concluída."

