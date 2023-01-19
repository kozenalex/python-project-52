MANAGE := poetry run python3 manage.py
.PHONY: shell
shell:
		@$(MANAGE) shell_plus --ipython
.PHONY: migrate
migrate:
		@$(MANAGE) makemigrations task_manager
		@$(MANAGE) migrate		
.PHONY: install
install:
		@poetry install
.PHONY: run
run:
		@$(MANAGE) runserver
.PHONY: test
test:
		@$(MANAGE) test --with-coverage
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml