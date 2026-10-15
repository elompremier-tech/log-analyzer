Datacenter Log Analyzer
A modular Python command-line utility designed to parse, validate, and analyze server log files in simulated datacenter environments
Features
- Log parsing and syntax validation
- Global traffic and event statistics
- Security threat and anomaly detection
- Modular architecture with clean separation of concerns
- Automated reporting and export of corrupted log records
Project Structure
├── principal.py # Main entry point (interactive CLI) ├── package/ # Analysis and processing modules │ ├── analyse_avancee.py │ ├── fonctions_analyse.py │ ├── fonctions_affichage.py │ ├── generer_rapport.py │ ├── security_analysis.py │ └── statistique.py ├── log_data/ # Sample log datasets └── README.md
Getting Started
Prerequisites
- Python 3.8 or higher
Installation
Clone the repository:git clone 🔗 https://github.com/elompremier-tech/log-analyzer.git cd log-analyzer
Usage
Run the main script: python principal.py
Follow the on-screen menu to select analysis tasks, generate reports, or inspect invalid entries
Authors
- DZALLO Elom Ezéchiel
- AMEGASHIE
