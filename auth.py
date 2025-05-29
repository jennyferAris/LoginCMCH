import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# Configuración OAuth
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_uri = "https://cmch-upchic2.streamlit.app/"
authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
token_endpoint = "https://oauth2.googleapis.com/token"
userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

# Usuarios autorizados
AUTHORIZED_USERS = {
    "jear142003@gmail.com": "Ingeniero Clínico"
}

def is_authorized_user(email):
    return email in AUTHORIZED_USERS

def get_user_role(email):
    return AUTHORIZED_USERS.get(email, None)

def create_oauth_session(state=None, token=None):
    return OAuth2Session(
        client_id,
        client_secret,
        scope="openid email profile",
        redirect_uri=redirect_uri,
        state=state,
        token=token,
    )

def login_box():
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = None
    if "token" not in st.session_state:
        st.session_state.token = None

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.image("https://asdf.amerins.com/uploads/Logo_CMCH_9cb2a11816.png", width=160)
    st.markdown("<div class='title'>Ingreso</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Departamento de Ingeniería Clínica</div>", unsafe_allow_html=True)

    oauth = create_oauth_session()
    auth_url, state = oauth.create_authorization_url(authorization_endpoint)
    st.session_state.oauth_state = state

    st.markdown(f"<a class='google-button' href='{auth_url}'>Iniciar sesión con Google</a>", unsafe_allow_html=True)

    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"][0]
        returned_state = query_params.get("state", [None])[0]

        if returned_state != st.session_state.oauth_state:
            st.error("Error de autenticación. Inténtalo de nuevo.")
            return

        oauth = create_oauth_session(state=returned_state)
        token = oauth.fetch_token(token_endpoint, code=code, client_secret=client_secret)
        st.session_state.token = token
        st.query_params.clear()

    st.markdown("</div>", unsafe_allow_html=True)

def get_user_info():
    if not st.session_state.get("token"):
        return None
    oauth = create_oauth_session(token=st.session_state.token)
    return oauth.get(userinfo_endpoint).json()

def logout():
    st.session_state.token = None
    st.query_params.clear()