# Cadenas-de-Markov
### Cadenas de Markov - Ajedrez

Este proyecto implementa un modelo de Cadenas de Markov para jugar al ajedrez. Utiliza un conjunto de partidas de la apertura Ruy López para construir una matriz de transición, lo que permite a la máquina tomar decisiones basadas en jugadas reales. La interfaz gráfica permite a los usuarios jugar contra la máquina.

### Requisitos

Antes de comenzar
Asegúrate de tener instalado:

Python 3.10 o superior
Git
Sistema operativo compatible:
macOS, Linux o Windows
Instalación

1. Clona este repositorio
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
2. Crea un entorno virtual
python3 -m venv venv
source venv/bin/activate  # Para macOS/Linux
venv\Scripts\activate     # Para Windows
3. Instala las dependencias
make install
Esto instalará las bibliotecas necesarias como python-chess, PyQt5, matplotlib, y seaborn.

4. Filtra las partidas de Ruy López
make filter
Este comando procesa el archivo RuyLopezClassical.pgn y genera el archivo filtrado filtered_ruy_lopez.pgn.

5. Ejecuta el programa
make run
Esto abrirá una ventana gráfica donde podrás jugar al ajedrez contra el modelo.