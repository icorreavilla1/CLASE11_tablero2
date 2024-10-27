import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image, ImageOps
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Configurar la página de Streamlit
st.set_page_config(page_title='🎨 Tablero Inteligente')

# Personalizar el título y descripción
st.title('🎨 Tablero de Dibujo Inteligente')
st.markdown("### ¡Bienvenido al tablero donde tu creatividad se despliega y puedes analizar tus dibujos! 😎✨")

# Barra lateral con configuraciones
with st.sidebar:
    st.title("🖌️ Configuraciones de Dibujo")
    st.write("Personaliza tu experiencia de dibujo.")

    # Configurar ancho de línea, herramienta de dibujo y color del trazo
    stroke_width = st.slider('Selecciona el ancho de línea', 1, 30, 5)
    drawing_mode = st.selectbox("Herramienta de dibujo:", ["freedraw", "line", "rect", "circle", "transform"])
    st.write("### 🎨 Selecciona el color de trazo")
    stroke_color = st.color_picker("Escoge el color", "#000000")

    # Ingresar clave de OpenAI
    ke = st.text_input('🔑 Ingresa tu Clave de API de OpenAI', type="password")
    os.environ['OPENAI_API_KEY'] = ke

# Configuración del lienzo
st.write("### 🖼️ Tu Lienzo de Arte")
canvas_result = st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#F0F8FF",  # Fondo azul claro
    height=600,
    width=800,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Botón para analizar el dibujo
analyze_button = st.button("Analiza el dibujo 🧠", type="secondary")

# Codificación de imagen a base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# Verificar la API key y analizar la imagen si se presiona el botón
if canvas_result.image_data is not None and ke and analyze_button:
    st.write("🖌️ **Procesando tu dibujo...**")
    
    # Convertir el lienzo en imagen
    input_numpy_array = np.array(canvas_result.image_data)
    input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
    input_image.save('img.png')

    # Codificar la imagen en base64
    base64_image = encode_image_to_base64("img.png")
    
    # Preparar el prompt para la API
    prompt_text = "Describe brevemente la imagen en español."

    # Crear el mensaje de la API
    try:
        with st.spinner("Analizando ..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt_text},
                    {"role": "user", "content": f"data:image/png;base64,{base64_image}"}
                ],
                max_tokens=500,
            )

            # Mostrar la respuesta en la aplicación
            full_response = response.choices[0].message["content"]
            st.write("### 🧩 Análisis de la imagen:")
            st.write(full_response)
    except Exception as e:
        st.error(f"Error durante el análisis: {e}")
else:
    # Mensajes de advertencia para el usuario
    if not ke:
        st.warning("Por favor ingresa tu clave de API de OpenAI.")

# Estilos adicionales: fondo de la aplicación y barra lateral
st.markdown("""
<style>
    .reportview-container {
        background-color: #FAF3E0;
        padding: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #FFEDCC;
    }
</style>
""", unsafe_allow_html=True)
