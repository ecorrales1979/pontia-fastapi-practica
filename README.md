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

## Ejecución

Una vez instalado, ejecutar el comando:

```bash
uvicorn api.main:app
```

Para inicializar en un puerto diferente, por ejemplo en el 8888, adicionar `-p 8888` al final del comando anterior.

## Pruebas

Hay un archivo para testar los endpoints usando la biblioteca requests. Para correrlo, ejecutar el comando:

```bash
python tests/test_requests.py
```
