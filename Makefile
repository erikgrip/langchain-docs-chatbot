help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Setup
setup:
	chmod +x docker/build.sh
	sudo apt install -y g++-11


# Training
train-help:
	PYTHONPATH=. python training/run_experiment.py --help

train-overfit:
	PYTHONPATH=. python training/run_experiment.py --max_epochs=300 --data_class=MotionsDataModule --model_class=MT5 --overfit_batches=1 --lr=0.001 --early_stopping=50

train-dev-run:
	PYTHONPATH=. python training/run_experiment.py --max_epochs=2 --data_class=MotionsDataModule --model_class=MT5 --fast_dev_run=True  --data_frac=0.001

tensorboard:
	tensorboard --logdir training/logs/lightning_logs

# Testing and linting
lint:
	poetry run tasks/lint.sh

test:
	PYTHONPATH=. poetry run pytest -s .


# Tmp
data_pipeline:
	PYTHONPATH=. poetry run python src/data_downloader/run.py

chat:
	PYTHONPATH=. poetry run python src/chat.py