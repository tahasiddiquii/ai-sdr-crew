.DEFAULT_GOAL := help
.PHONY: help install web lint test eval demo serve dev build ci clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install the backend (dev extras)
	cd backend && pip install -e ".[dev]"

web: ## Install the frontend
	cd frontend && npm install

lint: ## Ruff the backend
	cd backend && ruff check .

test: ## Run the backend test suite
	cd backend && pytest

eval: ## Qualification accuracy + no-fabrication / no-auto-send gates
	cd backend && sdr eval --report reports/eval_report.md

demo: ## Narrated run incl. the fabrication block
	cd backend && sdr demo

serve: ## Run the FastAPI backend on :8000
	cd backend && sdr serve --host 0.0.0.0 --port 8000 --reload

dev: ## Run the Next.js console on :3000
	cd frontend && npm run dev

build: ## Build the frontend
	cd frontend && npm run build

ci: lint test eval ## Everything the backend CI runs

clean: ## Remove caches and build artifacts
	rm -rf backend/.ruff_cache backend/.pytest_cache backend/**/__pycache__ frontend/.next frontend/node_modules
