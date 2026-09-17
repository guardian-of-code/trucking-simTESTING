import streamlit as st
import anthropic

st.set_page_config(page_title="Simulador Trucking Insurance", page_icon="🚛")
st.title("🚛 Entrenamiento de Ventas: Manejo de Objeciones")

# Sidebar: Configuración
st.sidebar.header("⚙️ Configuración")
api_key_input = st.sidebar.text_input("Pega tu API Key de Anthropic aquí:", type="password")
api_key = api_key_input.strip() if api_key_input else ""

model_option = st.sidebar.selectbox(
    "Selecciona el modelo de Claude:",
    [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-haiku-20240307",
        "claude-3-7-sonnet-20250219"
    ]
)

if api_key:
    client = anthropic.Anthropic(api_key=api_key)

    # Historial de conversación inicial
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Oye! Revisé tu propuesta para el seguro del camión, pero $3,800 de down payment es un robo. Mi primo paga la mitad con otra agencia. ¿Por qué te pagaría eso?"}
        ]

    # Renderizar conversación en pantalla
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Entrada del asesor
    if user_input := st.chat_input("Escribe tu argumento de venta o digita /evaluar..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        system_prompt = (
            "Eres Rigoberto, un camionero/dueño-operador difícil e impaciente. "
            "Rechaza las propuestas por precio, enganche o papeleo. "
            "Si el asesor escribe '/evaluar', sal del personaje y dale una calificación "
            "del 1 al 10 en manejo de objeciones con una sugerencia concreta de mejora."
        )

        with st.chat_message("assistant"):
            try:
                response = client.messages.create(
                    model=model_option,
                    max_tokens=300,
                    system=system_prompt,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                reply = response.content[0].text
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except anthropic.NotFoundError:
                st.error(f"El modelo '{model_option}' no está activo para tu API Key. Selecciona otro modelo en la barra lateral izquierda.")
            except anthropic.AuthenticationError:
                st.error("La API Key ingresada no es válida. Verifica haber copiado la clave completa que empieza por 'sk-ant-'.")
            except Exception as e:
                st.error(f"Ocurrió un detalle de conexión: {str(e)}")
else:
    st.warning("Ingresa tu API Key en el menú de la izquierda para comenzar el entrenamiento.")
