# 🐍 Python ETL

Pipeline ETL batch desarrollado en **Python**, con estructura por capas (**Extract, Transform, Load**), diseñado para ser mantenible, testeable y fácil de extender.

El proyecto incluye:
- Infraestructura local db con **Docker Compose**
- Script para **generar una estructura general para proyecto ETL**
- Buenas prácticas de organización y separación de responsabilidades

---

## Estructura del proyecto

```text
PYTHON_ETL/
├── etl_project/             
│   ├── config/               
│   │   ├── logging.py        # Configuración de logs (Consola y Archivo)
│   │   ├── settings.py       # Variables
│   │   └── tables.py         # Definiciones de esquemas de tablas
│   ├── logs/                 
│   │   └── etl_process.log   # Registros logs
│   ├── scripts/              
│   │   └── run_etl.py        # Script principal para lanzar el pipeline
│   ├── src/                  
│   │   ├── extract/          # Extracción de datos
│   │   ├── load/             # Carga de datos al destino
│   │   ├── pipelines/        # Orquestación de flujos
│   │   ├── transform/        # Limpieza y transformación
│   │   ├── utils/            # Conectores de DB y helpers
│   │   ├── metadata_manager  # Gestión de checkpoints
│   │   └── extraction_strategies # Uso de Protocols
│   └── tests/                # Pruebas unitarias
├── sql-scripts/              # Scripts para crear tablas src y target en bd con docker
├── docker-compose.yml        # Infraestructura de bases de datos (MySQL/Postgres)
├── requirements.txt          
└── README.md                 
