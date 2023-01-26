MANAGE := poetry run python3 manage.py
.PHONY: shell
shell:
		@$(MANAGE) shell_plus
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
		@$(MANAGE) test --with-coverage --cover-xml
lint:
		flake8 task_manager users statuses labels task