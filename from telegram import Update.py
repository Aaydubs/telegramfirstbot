from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Token del bot
TELEGRAM_TOKEN = '7661329054:AAGkuVftyzSKkfKAu6qfYJVK4GbCc3jKq2U'  # Reemplaza con tu token

# Listas de palabras clave para clasificación
palabras_positivas = ["amable", "rápido", "atento", "excelente", "cordial", "profesional", "personalizado",
                      "deliciosa", "exquisita", "sabrosa", "fresca", "bien presentada", "casera", "auténtica", "de calidad",
                      "acogedor", "cómodo", "agradable", "limpio", "tranquilo", "elegante", "bonito", "moderno",
                      "razonable", "justo", "económico", "accesible", "buena relación calidad-precio",
                      "memorable", "fantástica", "perfecta", "altamente recomendable", "espectacular", "increíble", "satisfacción",
                      "variedad", "innovador", "ubicación conveniente", "buena decoración", "buen servicio al cliente", "recomendado", "buena atención"]

palabras_negativas = ["lento", "desatento", "grosero", "descortés", "incompetente", "maleducado", "negligente",
                      "insípida", "mala", "fría", "recalentada", "cruda", "mal cocida", "poca calidad", "insatisfactoria",
                      "sucio", "ruidoso", "oscuro", "incómodo", "anticuado", "apretado", "mal ventilado", "desorganizado",
                      "caro", "sobrevalorado", "excesivo", "no vale la pena", "abusivo", "alto",
                      "decepcionante", "mala", "pésima", "no recomendable", "insatisfactoria", "desastrosa", "aburrida",
                      "falta de variedad", "tiempo de espera largo", "falta de higiene", "servicio deficiente", "falta de atención al cliente"]

palabras_neutrales = ["rápido", "eficiente", "regular", "correcto", "normal",
                      "promedio", "simple", "aceptable", "estándar", "típica",
                      "tradicional", "sencillo", "funcional", "pequeño", "básico",
                      "moderado", "intermedio",
                      "común", "habitual", "adecuada", "promedio",
                      "ubicación céntrica", "carta variada", "menú estándar", "ambiente casual"]

# Función para calcular el índice de sentimiento
def clasificar_sentimiento(mensaje):
    mensaje = mensaje.lower()  # Convertir a minúsculas para facilitar la comparación
    
    # Contar palabras positivas, negativas y neutrales
    cuenta_positivas = sum(1 for palabra in palabras_positivas if palabra in mensaje)
    cuenta_negativas = sum(1 for palabra in palabras_negativas if palabra in mensaje)
    cuenta_neutrales = sum(1 for palabra in palabras_neutrales if palabra in mensaje)
    
    # Total de palabras encontradas en las categorías
    total_palabras = cuenta_positivas + cuenta_negativas + cuenta_neutrales
    
    # Calcular el índice de sentimiento en el rango -1 a 1
    if total_palabras > 0:
        indice_sentimiento = (cuenta_positivas - cuenta_negativas) / total_palabras
    else:
        indice_sentimiento = 0  # En caso de que no haya palabras de ninguna categoría
    
    # Determinar la clasificación general basada en el índice
    if indice_sentimiento > 0.2:
        clasificacion = "positivo"
    elif indice_sentimiento < -0.2:
        clasificacion = "negativo"
    else:
        clasificacion = "neutral"
    
    return clasificacion, indice_sentimiento

# Función que maneja el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Envíame una opinión y te diré si es positiva, negativa o neutral.")

# Función para manejar mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    opinion = update.message.text
    clasificacion, indice = clasificar_sentimiento(opinion)
    respuesta = (f"Tu opinión ha sido clasificada como: {clasificacion}.\n"
                 f"Índice de Sentimiento: {indice:.2f}")
    await update.message.reply_text(respuesta)

# Configuración del bot
def main():
    # Inicializamos la aplicación con el token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Añadimos manejadores para los comandos y mensajes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciamos el bot
    application.run_polling()

if __name__ == '__main__':
    main()

