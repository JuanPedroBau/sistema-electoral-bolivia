import streamlit as st
import streamlit_authenticator as stauth
import yaml

# Simular archivo config.yaml como diccionario directamente (evita errores de lectura)
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Administrador',
                'password': '$2b$12$DQynVn1rHUF51izZcQ92pe/ktL95sd9Q6gDhG4H2rRGkiEwU/FQjW'  # admin123
            },
            'invitado': {
                'name': 'Invitado',
                'password': '$2b$12$qECr7AM8KM2zSGcVPnGZnOug0DrbpBFdvqFMPYo1FrVKY2H0dAnCu'  # inv123
            }
        }
    },
    'cookie': {
        'name': 'control_electoral',
        'key': 'abcdef',
        'expiry_days': 1
    }
}

# Crear autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# LOGIN
nombre, autenticado, username = authenticator.login("🔐 Iniciar sesión", "main")

if autenticado:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido/a {nombre}")
    st.success("✔️ Acceso concedido. Ya estás dentro.")
elif autenticado is False:
    st.error("❌ Usuario o contraseña incorrectos")
else:
    st.warning("👈 Por favor, ingresa tus credenciales.")
