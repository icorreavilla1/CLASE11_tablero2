import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas


st.set_page_config(page_title="✨ Lienzo Creativo AI ✨")


st.title("🖍️ Bienvenido al Lienzo Creativo con Inteligencia Artificial 🎉")
st.markdown("#### Despierta tu creatividad y permite que la IA analice tus trazos únicos! 🚀")


with st.sidebar:
    st.title("🎨 Opciones de Personalización")
    st.write("Ajusta las herramientas para crear tu obra maestra.")

    
    stroke_width = st.slider("🎚️ Ancho de Línea", 1, 50, 8)
    drawing_mode = st.selectbox("✏️ Herramienta:", ["freedraw", "line", "rect", "circle", "transform"])
    st.write("### 🌈 Color de Trazo")
    stroke_color = st.color_picker("Elige un color", "#FF5733")

   
    ke = st.text_input("🔑 API Key de OpenAI", type="password")
    os.environ['OPENAI_API_KEY'] = ke


st.write("### 🎉 Tu Espacio Creativo sin Límites")
canvas_result = st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFF8DC", 
    height=700,  
    width=1200,  
    drawing_mode=drawing_mode,
    key="canvas",
)


analyze_button = st.button("🔍 Analizar Dibujo con IA 🧠", type="primary")


def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."


if canvas_result.image_data is not None and ke and analyze_button:
    st.write("🔄 **Procesando tu obra de arte...**")

   
    input_numpy_array = np.array(canvas_result.image_data)
    input_image = Image.fromarray(input_numpy_array.astype("uint8"), "RGBA")
    input_image.save("img.png")

    
    base64_image = encode_image_to_base64("img.png")
    
    
    prompt_text = "Describe de forma breve y en español esta imagen."

    try:
        with st.spinner("Analizando..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt_text},
                    {"role": "user", "content": f"data:image/png;base64,{base64_image}"}
                ],
                max_tokens=500,
            )

            
            full_response = response.choices[0].message["content"]
            st.write("### 🔍 Resultado del Análisis:")
            st.write(full_response)
    except Exception as e:
        st.error(f"Error durante el análisis: {e}")
else:
    
    if not ke:
        st.warning("Por favor, ingresa tu API Key de OpenAI.")


st.markdown("""
<style>
    .reportview-container {
        background-color: #FFF8DC;  /* Fondo en amarillo suave */
        padding: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #FFE4B5;  /* Fondo lateral en tono melón */
    }
</style>
""", unsafe_allow_html=True)
