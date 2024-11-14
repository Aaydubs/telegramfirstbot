import googlemaps

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyD1j50wtFU8tLtaPXqNXkEc5b5XenxmKBE')

# Search for a place by name
place_name = "VivaGym, Granada"
place_search = gmaps.find_place(place_name, 'textquery')

# Get the place ID
place_id = place_search['candidates'][0]['place_id']
print(f"The place ID for '{place_name}' is: {place_id}")

import requests

def obtener_comentarios_restaurante(api_key, place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,reviews&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "reviews" in data["result"]:
            print(f"Nombre del lugar: {data['result']['name']}")
            print(f"Calificación general: {data['result']['rating']}")
            print("\nComentarios recientes:")
            for comentario in data["result"]["reviews"]:
                print("Autor:", comentario["author_name"])
                print("Calificación:", comentario["rating"])
                print("Comentario:", comentario["text"])
                print("Hace:", comentario["relative_time_description"])
                print("-" * 20)
        else:
            print("No hay comentarios disponibles para este lugar.")
    else:
        print("Error en la solicitud:", response.status_code)

# Ejemplo de uso
api_key = "AIzaSyD1j50wtFU8tLtaPXqNXkEc5b5XenxmKBE"  # Coloca aquí tu clave de API
place_id = "ChIJpftiipL8cQ0RoMKghYTgcBU"  # Reemplaza con el place_id del lugar en Granada
obtener_comentarios_restaurante(api_key, place_id)

