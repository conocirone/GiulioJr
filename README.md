# Tablut Player for AI Competition

This repository contains a Python-based player developed for the **Tablut Competition** held as part of the course *Fundamentals of Artificial Intelligence and Knowledge Representation* at the **University of Bologna**, Academic Year 2024/2025.

The project involves creating an AI player for the game *Tablut*. We implemented an iterative alpha-beta min-max algorithm for decision-making, transposition tables to avoid redundant computations, the history heuristic to optimize move ordering, and various features to evaluate the board and determine game strategies.

---

## Getting Started

### Prerequisites

Before running the player, ensure you have the following:

1. Python 3.x installed.
2. The Tablut Competition server is running. You can find the server repository here:  
   [AGalassi/TablutCompetition](https://github.com/AGalassi/TablutCompetition).

### Setup

1. Clone this repository:  
   ```bash
   git clone https://github.com/conocirone/GiulioJr.git
   cd GiulioJr
   ```

2. Follow the instructions in the [TablutCompetition server repository](https://github.com/AGalassi/TablutCompetition) to start the server.

---

## How to Run the Player

To execute the player, use the following command:

```bash
python main.py --team [WHITE|BLACK] --timeout TIMEOUT --ip IP
```

### Parameters:
- **`--team [WHITE|BLACK]`**: Specifies which side the player will represent.  
- **`--timeout TIMEOUT`**: Time (in seconds) allowed for the player's move decision.  
- **`--ip IP`**: IP address of the running server.

### Example:
If you want to run the player as the WHITE team, with a timeout of 60 seconds, connecting to a server at `127.0.0.1`, the command will be:  
```bash
python main.py --team WHITE --timeout 60 --ip 127.0.0.1
```

---


## Authors

- **Giulio Petrozziello**: [giulioPetroz](https://github.com/giulioPetroz)
- **Gio Formichella**: [Gio-Formichella](https://github.com/Gio-Formichella)
- **Cono Cirone**: [conocirone](https://github.com/conocirone)

---

## License

This project is developed as part of a university competition and is intended for educational purposes.  

