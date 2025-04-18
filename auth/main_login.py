import streamlit as st
import yaml
import streamlit_authenticator as stauth

# Cargar configuración desde YAML
with open("auth/config.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Pantalla de inicio de sesión
nombre, autenticado, username = authenticator.login("Iniciar sesión", "main")

if autenticado:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido/a {nombre}")
    st.success("Acceso concedido. Continúa desarrollando tu app aquí...")

elif autenticado is False:
    st.error("Usuario o contraseña incorrectos")

else:
    st.warning("Por favor, ingresa tus credenciales")
