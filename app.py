import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]

# Configuración OAuth
redirect_uri = "http://localhost:8501"
authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
token_endpoint = "https://oauth2.googleapis.com/token"
userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

# Estado
if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None
if "token" not in st.session_state:
    st.session_state.token = None

# CSS limpio y centrado
st.markdown("""
    <style>
    body, .stApp {
        background-color: #ffffff !important;
    }
    .login-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 80px;
    }
    .logo {
        width: 160px;
        margin-bottom: 30px;
    }
    .title {
        font-size: 22px;
        font-weight: normal;
        color: #000;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 26px;
        font-weight: bold;
        color: #000;
        margin-bottom: 40px;
    }
    .google-button {
        background-color: #FFD60A;
        color: #000;
        padding: 12px 24px;
        border-radius: 30px;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        transition: background-color 0.3s ease;
    }
    .google-button:hover {
        background-color: #e6c000;
    }
    </style>
""", unsafe_allow_html=True)

# Crear sesión
def create_oauth_session(state=None, token=None):
    return OAuth2Session(
        client_id,
        client_secret,
        scope="openid email profile",
        redirect_uri=redirect_uri,
        state=state,
        token=token,
    )

def main():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.image("https://asdf.amerins.com/uploads/Logo_CMCH_9cb2a11816.png", width=160)

    st.markdown("<div class='title'>Ingreso</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Departamento de Ingeniería Clínica</div>", unsafe_allow_html=True)

    if not st.session_state.token:
        oauth = create_oauth_session()
        auth_url, state = oauth.create_authorization_url(authorization_endpoint)
        st.session_state.oauth_state = state

        st.markdown(f"<a class='google-button' href='{auth_url}'>Iniciar sesión con Google</a>", unsafe_allow_html=True)

        query_params = st.query_params
        if "code" in query_params:
            code = query_params["code"][0]
            state = query_params.get("state", [None])[0]

            if state != st.session_state.oauth_state:
                st.error("Error de autenticación. Inténtalo de nuevo.")
                return

            oauth = create_oauth_session(state=state)
            token = oauth.fetch_token(token_endpoint, code=code, client_secret=client_secret)
            st.session_state.token = token
            st.query_params.clear()

    if st.session_state.token:
        oauth = create_oauth_session(token=st.session_state.token)
        userinfo = oauth.get(userinfo_endpoint).json()
        name = userinfo.get("name")
        email = userinfo.get("email")

        st.success(f"Bienvenida, **{name}** ({email}) 👋")

        if st.button("Cerrar sesión"):
            st.session_state.token = None

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
