help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Setup
setup:
	chmod +x docker/run.sh

# Testing and linting
lint:
	poetry run tasks/lint.sh

test:
	PYTHONPATH=. poetry run pytest -s .


# Tmp
data_pipeline:
	PYTHONPATH=. poetry run python src/data_downloader/run.py

chat:
	PYTHONPATH=. poetry run '--' streamlit run src/app/app.py '--' --temperature 1
# PYTHONPATH=. poetry run python src/app/app.py  --temperature=1

chat_db:
	PYTHONPATH=. poetry run '--' streamlit run src/app/app.py '--' --delete_persisted_db