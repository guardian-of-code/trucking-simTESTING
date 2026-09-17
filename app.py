import streamlit as st
import anthropic

st.set_page_config(page_title="Simulador Trucking Insurance", page_icon="🚛")
st.title("🚛 Entrenamiento de Ventas: Manejo de Objeciones")

# Configurar API Key
api_key = st.sidebar.text_input("Pega tu API Key de Anthropic aquí:", type="password")

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

        # Configuración de personalidad de Claude
        system_prompt = (
            "Eres Rigoberto, un camionero/dueño-operador difícil e impaciente. "
            "Rechaza las propuestas por precio, enganche o papeleo. "
            "Si el asesor escribe '/evaluar', sal del personaje y dale una calificación "
            "del 1 al 10 en manejo de objeciones con una sugerencia concreta de mejora."
        )

        with st.chat_message("assistant"):
            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=300,
                system=system_prompt,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            reply = response.content[0].text
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.warning("Ingresa tu API Key en el menú de la izquierda para comenzar el entrenamiento.")
