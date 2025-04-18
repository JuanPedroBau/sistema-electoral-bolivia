import streamlit as st
import streamlit_authenticator as stauth

# Lista de usuarios
nombres = ['Administrador', 'Invitado']
usuarios = ['admin', 'invitado']

# Contraseñas ya hasheadas con bcrypt
hashed_passwords = [
    '$2b$12$DQynVn1rHUF51izZcQ92pe/ktL95sd9Q6gDhG4H2rRGkiEwU/FQjW',  # admin123
    '$2b$12$qECr7AM8KM2zSGcVPnGZnOug0DrbpBFdvqFMPYo1FrVKY2H0dAnCu'   # inv123
]

# Crear el autenticador
authenticator = stauth.Authenticate(
    names=nombres,
    usernames=usuarios,
    passwords=hashed_passwords,
    cookie_name="control_electoral",
    key="abcdef",
    cookie_expiry_days=1
)

# Login
nombre, autenticado, username = authenticator.login("🔐 Iniciar sesión", "main")

# Validación
if autenticado:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido/a {nombre}")
    st.success("🎉 ¡Login correcto! Aquí empieza tu app...")

elif autenticado is False:
    st.error("❌ Usuario o contraseña incorrectos")

else:
    st.warning("👈 Ingresa tus credenciales para acceder")
