import requests

base_url = "http://localhost:8000/notes"

# Crear nota
note_data = {
    "title": "Nueva nota",
    "content": "Contenido de la nueva nota"
}
response = requests.post(base_url, json=note_data)
print(response.status_code) # Debe retornar 201
print(response.json()) # Contenido de la nota creada

# Crear nota con deadline
note_data = {
    "title": "Nueva nota",
    "content": "Contenido de la nueva nota",
    "deadline": "2027-01-01"
}
response = requests.post(base_url, json=note_data)
print(response.status_code) # Debe retornar 201
print(response.json()) # Contenido de la nota creada

# Error al crear nota sin título
note_data = {
    "content": "Contenido de la nueva nota"
}
response = requests.post(base_url, json=note_data)
print(response.status_code) # Debe retornar 422
print(response.json()) # Error de validación por falta de título

# Error al crear nota sin contenido
note_data = {
    "title": "Nueva nota"
}
response = requests.post(base_url, json=note_data)
print(response.status_code) # Debe retornar 422
print(response.json()) # Error de validación por falta de contenido

# Error al crear nota con deadline en el pasado
note_data = {
    "title": "Nueva nota",
    "content": "Contenido de la nueva nota",
    "deadline": "2025-01-01"
}
response = requests.post(base_url, json=note_data)
print(response.status_code) # Debe retornar 209
print(response.json()) # Error indicando que el deadline no puede estar en el pasado

# Listar todas las notas
response = requests.get(base_url)
print(response.status_code) # Debe retornar 200
print(response.json()) # Lista de todas las notas

# Obtener una nota específica
note_id = 1
response = requests.get(f"{base_url}/{note_id}")
print(response.status_code) # Debe retornar 200
print(response.json()) # Contenido de la nota específica

# Error al obtener una nota que no existe
note_id = 99
response = requests.get(f"{base_url}/{note_id}")
print(response.status_code) # Debe retornar 404
print(response.json()) # Error indicando que la nota no fue encontrada

# Actualizar una nota existente
note_id = 1
update_data = {
    "title": "Nota actualizada",
    "content": "Contenido actualizado de la nota"
}
response = requests.put(f"{base_url}/{note_id}", json=update_data)
print(response.status_code) # Debe retornar 200
print(response.json()) # Contenido de la nota actualizada

# Definir que la nota fue conpletada
note_id = 1
complete_data = {
    "is_done": True
}
response = requests.patch(f"{base_url}/{note_id}/done", json=complete_data)
print(response.status_code) # Debe retornar 200
print(response.json()) # Contenido de la nota con el estado actualizado

# Eliminar una nota existente
note_id = 2
response = requests.delete(f"{base_url}/{note_id}")
print(response.status_code) # Debe retornar 204
