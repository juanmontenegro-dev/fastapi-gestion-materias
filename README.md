# Materias API

API REST simple que permite gestionar distintas materias de la facultad, permitiendo agregar, consultar, actualizar y eliminar materias.

---

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## Instalación y ejecución

### 1- Clonar el repositorio

git clone https://github.com/juanmontenegro-dev/fastapi-gestion-materias.git
cd fastapi-gestion-materias

### 2- Crear entorno virtual

python -m venv venv

### 3- Activar entorno virtual

Windows:
    venv\Scripts\activate

Linux/macOS:
    source venv/bin/activate

### 4- Instalar dependencias

pip install -r requirements.txt

### 5- Ejecutar la aplicación

uvicorn main:app --reload

API:
    http://127.0.0.1:8000

Documentación interactiva:

    Swagger UI:
        http://127.0.0.1:8000/docs
    
    Redoc:
        http://127.0.0.1:8000/redoc

---

#### Endpoints disponibles

- GET "/materias": Obtiene todas las materias

- GET "/materias/{id}": Obtiene una materia por ID

- POST "/materias": Agrega una materia

- PUT "/materias/{id}": Actualiza una materia ya existente

- DELETE "/materias/{id}": Elimina una materia ya existente

---

#### Modelo de Materia

- nombre: Indica el nombre de la materia

- anio: El año en el que se cursa la materia

- modalidad: Anual o cuatrimestral

- correlativas: Lista de IDs de materias correlativas

---

#### Estado del proyecto

Proyecto en desarrollo con fines meramente educativos. Actualmente utiliza almacenamiento en memoria, careciendo de una base de datos

---

#### Proximos pasos

- Persistencia en base de datos

- Implementación de tests automatizados

- Mejoras en validaciones

- Autenticación y autorización

---

#### Autor

Juan Ignacio Montenegro
Estudiante de segundo año de Ingeniería en Sistemas de Información - UTN Facultad Regional Buenos Aires