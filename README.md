# Ejemplo de API usando FastAPI

Repositorio para la evaluación del módulo 2 del Máster en IA, Cloud Computing y DevOps.

## Instalación

1- Clonar el repositorio
```bash
git clone git@github.com:ecorrales1979/pontia-fastapi-practica.git
```
2- Entrar en la nueva carpeta creada
```bash
cd pontia-fastapi-practica
```
3- Crear entorno virtual
```bash
python3 -m venv .venv
```
4- Activar el entorno virtual
```bash
source .venv/bin/activate # o el equivalente según tu Sistema Operativo (ese es para distros de Linux)
```
5- Instalar las dependencias
```bash
pip install -r requirements.txt
```
6- Crear variables de ambiente en el archivo .env a partir del .env.example

## Ejecución

Una vez instalado, ejecutar el comando:

```bash
uvicorn api.main:app
```

Para inicializar en un puerto diferente, por ejemplo en el 8888, adicionar `-p 8888` al final del comando anterior.

## Usando docker

Puedes usar docker para ejecutar la API y la Base de Datos con PostgreSQL

### Requisitos

- Docker instalado
- Docker Compose instalado

### Instalación y ejecución

1- Construir y ejecutar los contenedores
```bash
docker compose up --build -d
```

### Verificar que los servicios están corriendo
```bash
docker compose ps
```

### Ver los logs

Ver todos los logs
```bash
docker compose logs
```

Ver los logs de un servicio específico
```bash
docker compose logs api
docker compose logs data
```

### Detener los contenedores
```bash
docker compose down
```

Detener y eliminar volúmenes
```bash
docker compose down -v
```

## Endpoints de la API

Una vez que la aplicación esté corriendo, estará disponible en `http://localhost:8080`

### Endpoints

- [GET] /notes - Lista de todas las notas
- [GET] /notes/{id} - Obtiene una entidad por ID
- [POST] /notes - Crea una nueva nota
- [PUT] /notes/{id} - Actualiza una nota
- [PATCH] /notes/{id}/status - Cambia el estado de una nota
- [DELETE] /notes/{id} - Elimina una nota

### Documentación interactiva

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

# Estructura del Proyecto

- `docker-compose.yml`: Configuración de servicios y red
- `Dockerfile`: Configuración de la imagen de la aplicación
- `api/main.py`: Código de la aplicación FastAPI
- `requirements.txt`: Dependencias de Python

## Pruebas

Hay un archivo para testar los endpoints usando la biblioteca requests. Para correrlo, ejecutar el comando:

```bash
python tests/test_requests.py
```
