# 🐍 Python Native ETL

Pipeline ETL batch desarrollado en **Python puro**, con una estructura clara por capas (**Extract, Transform, Load**), diseñado para ser mantenible, testeable y fácil de extender.

El proyecto incluye:
- Infraestructura local con **Docker Compose**
- Script para **generar una estructura general para proyecto ETL**
- Buenas prácticas de organización y separación de responsabilidades

---

## 📂 Estructura del proyecto

```text
python_etl/
├── etl_project/          # Código fuente del ETL
│   ├── extract/          # Extracción de datos (DB, APIs, archivos)
│   ├── transform/        # Limpieza, validación y enriquecimiento
│   ├── load/             # Carga de datos (DB / warehouse)
│   ├── pipelines/        # Orquestación de pipelines
│   ├── utils/            # Utilidades compartidas (DB, fechas, helpers)
│   └── tests/            # Tests unitarios
├── docker-compose.yml    # Infraestructura local (bases de datos)
├── init_etl_project.sh   # Script para crear la estructura base del proyecto
├── requirements.txt      # Dependencias del proyecto
├── .python-version       # Versión de Python (pyenv)
└── README.md
