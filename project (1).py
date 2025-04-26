import streamlit as st
import json
import os
from uuid import uuid4

# ====== FUNCIONES DE UTILIDAD ======

def cargar_preguntas(codigo_sesion):
    archivo = f"preguntas_{codigo_sesion}.json"
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def guardar_preguntas(codigo_sesion, preguntas):
    archivo = f"preguntas_{codigo_sesion}.json"
    with open(archivo, "w", encoding="utf-8") as file:
        json.dump(preguntas, file, ensure_ascii=False, indent=4)

def generar_codigo_sesion():
    return ''.join([str(uuid4().hex[i]) for i in range(6)])  # Código corto

def agregar_pregunta(codigo_sesion, texto, opciones, correcta):
    preguntas = cargar_preguntas(codigo_sesion)
    nueva = {
        "id": str(uuid4()),
        "texto": texto,
        "opciones": opciones,
        "correcta": correcta
    }
    preguntas.append(nueva)
    guardar_preguntas(codigo_sesion, preguntas)

def obtener_pregunta_aleatoria(codigo_sesion):
    import random
    preguntas = cargar_preguntas(codigo_sesion)
    if preguntas:
        return random.choice(preguntas)
    return None

def verificar_respuesta(pregunta, seleccion):
    # Mapeo de "A", "B", "C" a índices 0, 1, 2
    indices = {"A": 0, "B": 1, "C": 2}
    if seleccion in indices:
        # Compara la respuesta seleccionada con la correcta
        return pregunta["opciones"][indices[seleccion]] == pregunta["correcta"]
    return False


# ====== MODO PROFESOR ======

def modo_profesor():
    # Crear nuevo código de sesión solo si es una nueva sesión
    if 'codigo_sesion' not in st.session_state:
        st.session_state.codigo_sesion = generar_codigo_sesion()

    codigo_sesion = st.session_state.codigo_sesion
    st.header("👩‍🏫 Diseña tus preguntas")
    st.markdown(f"**Código de sesión:** {codigo_sesion}")

    texto = st.text_input("Escribe la pregunta")
    opcion1 = st.text_input("Opción A")
    opcion2 = st.text_input("Opción B")
    opcion3 = st.text_input("Opción C")
    correcta = st.selectbox("¿Cuál es la respuesta correcta?", ("A", "B", "C"))

    if st.button("Guardar pregunta"):
        if texto and opcion1 and opcion2 and opcion3:
            opciones = [opcion1, opcion2, opcion3]
            indice = {"A": 0, "B": 1, "C": 2}[correcta]
            agregar_pregunta(codigo_sesion, texto, opciones, opciones[indice])
            st.success("✅ Pregunta guardada")
        else:
            st.error("❌ Rellena todos los campos")

    st.markdown("---")
    st.subheader("📋 Preguntas actuales")
    for p in cargar_preguntas(codigo_sesion):
        st.write(f"❓ {p['texto']}")
        for i, op in enumerate(p["opciones"]):
            st.write(f"{chr(65+i)}. {op}")
        st.markdown("---")

    if st.button("He terminado"):
        # Mostrar el código de sesión
        codigo_actual = st.session_state.codigo_sesion
        st.session_state.codigo_sesion = generar_codigo_sesion()
        st.success(f"✅ Has terminado. Código de sesión creado: {codigo_actual}")

# ====== MODO ESTUDIANTE ======

def modo_estudiante():
    st.header("🎓 ¡Responde la pregunta!")

    # Obtener el código de sesión del alumno
    codigo_sesion = st.text_input("Introduce el código de la sesión:", "")

    # Si el código ha cambiado desde el anterior, reiniciar el estado
    if 'codigo_anterior' not in st.session_state:
        st.session_state.codigo_anterior = ""

    if codigo_sesion and codigo_sesion != st.session_state.codigo_anterior:
        st.session_state.pregunta_actual = 0
        st.session_state.respuestas = {}
        st.session_state.codigo_anterior = codigo_sesion
        st.rerun()  # reinicia todo desde cero

    if codigo_sesion:
        preguntas = cargar_preguntas(codigo_sesion)
        if not preguntas:
            st.warning("⚠️ No hay preguntas disponibles para este código.")
            return

        # Estado inicial
        if 'pregunta_actual' not in st.session_state:
            st.session_state.pregunta_actual = 0

        if 'respuestas' not in st.session_state:
            st.session_state.respuestas = {}

        pregunta_actual = st.session_state.pregunta_actual

        # SI YA TERMINÓ TODAS LAS PREGUNTAS
        if pregunta_actual >= len(preguntas):
            st.markdown("---")
            st.header("📊 Resultados finales")
            for pregunta in preguntas:
                seleccion = st.session_state.respuestas.get(pregunta['id'])
                if seleccion == pregunta['correcta']:
                    st.success(f"❓ {pregunta['texto']} - ✅ Correcto")
                else:
                    st.error(f"❓ {pregunta['texto']} - ❌ Incorrecto. La correcta era: {pregunta['correcta']}")
            return  # Fin

        # MOSTRAR PREGUNTA ACTUAL
        pregunta = preguntas[pregunta_actual]
        st.write(f"❓ {pregunta['texto']}")

        # Usamos una clave única
        seleccion = st.radio(
            "Selecciona una opción",
            pregunta["opciones"],
            key=f"seleccion_{pregunta['id']}"
        )

        if st.button("Siguiente pregunta"):
            # Guardamos la respuesta
            st.session_state.respuestas[pregunta["id"]] = seleccion

            # Avanzamos 
            st.session_state.pregunta_actual += 1
            st.rerun()

    else:
        st.warning("⚠️ Ingresa el código de sesión para empezar")



# ====== MAIN ======

def main():
    st.title("🧠 Tus ejercicios")

    modo = st.sidebar.selectbox("Selecciona tu rol", ["Profesor/a", "Estudiante"])

    if modo == "Profesor/a":
        modo_profesor()
    else:
        modo_estudiante()

if __name__ == "__main__":
    main()

