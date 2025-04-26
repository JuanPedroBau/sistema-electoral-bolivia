import streamlit as st
import yaml
import streamlit_authenticator as stauth

st.set_page_config(page_title="Análisis Electoral Bolivia", layout="wide")

# ========================
# Cargar configuración
# ========================
with open("auth/config.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    expiry_days=config["cookie"]["expiry_days"]
)

# ========================
# ESTILO VISUAL LOGIN
# ========================
st.markdown("""
<style>
.login-container {
    max-width: 420px;
    margin: 0 auto;
    padding: 2rem;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.login-container h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ========================
# LOGIN
# ========================
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown("<h1>🔐 Sistema Electoral Bolivia</h1>", unsafe_allow_html=True)

# Usar login sin descomprimir nada
authenticator.login("main")

st.markdown("</div>", unsafe_allow_html=True)

# ========================
# VERIFICACIÓN DE LOGIN
# ========================
if "authentication_status" in st.session_state:

    if st.session_state["authentication_status"] is True:
        authenticator.logout("Cerrar sesión", "sidebar")
        st.session_state["usuario"] = st.session_state["username"]

        # Solo mostramos app si el login fue exitoso
        import app
        app.run_app()

    elif st.session_state["authentication_status"] is False:
        st.error("❌ Usuario o contraseña incorrectos")

else:
    st.info("🔐 Por favor, ingresa tus credenciales")
