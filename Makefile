# Variables
PYTHON=venv/bin/python3
PIP=venv/bin/pip
SRC_DIR=src
DATA_DIR=data
FILTERED_PGN=$(DATA_DIR)/filtered_ruy_lopez.pgn

# Reglas
.PHONY: all run filter visualize install clean

all: install filter run

install:
	@echo "Instalando dependencias..."
	$(PYTHON) -m pip install -r requirements.txt

filter:
	@echo "Filtrando dataset para Ruy López..."
	$(PYTHON) $(SRC_DIR)/data_processing.py

run:
	@echo "Ejecutando el programa..."
	$(PYTHON) $(SRC_DIR)/main.py

visualize:
	@echo "Visualizando la matriz de transición..."
	$(PYTHON) -c "from src.visualization import plot_transition_matrix; from src.markov_model import MarkovModel; plot_transition_matrix(MarkovModel('$(FILTERED_PGN)').transition_matrix)"

clean:
	@echo "Limpiando archivos temporales..."
	rm -f $(FILTERED_PGN)
