import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# Tus credenciales de Google OAuth, se cargan desde secrets.toml
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]

redirect_uri = "http://localhost:8501"
authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
token_endpoint = "https://oauth2.googleapis.com/token"
userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None
if "token" not in st.session_state:
    st.session_state.token = None

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
    st.title("Login con Google en Streamlit")

    # Si no hay token, mostrar botón para iniciar sesión
    if not st.session_state.token:
        oauth = create_oauth_session()
        authorization_url, state = oauth.create_authorization_url(authorization_endpoint)
        st.session_state.oauth_state = state

        st.markdown(f"[Iniciar sesión con Google]({authorization_url})")

        # Capturar código y estado de los parámetros URL después del login
        query_params = st.query_params
        if "code" in query_params:
            code = query_params["code"][0]
            state = query_params.get("state", [None])[0]

            if state != st.session_state.oauth_state:
                st.error("Error: estado no coincide. Intenta de nuevo.")
                return

            oauth = create_oauth_session(state=state)
            token = oauth.fetch_token(token_endpoint, code=code, client_secret=client_secret)
            st.session_state.token = token
            st.query_params.clear()  # limpiar parámetros de la URL

    # Si ya hay token, mostrar info del usuario
    if st.session_state.token:
        oauth = create_oauth_session(token=st.session_state.token)
        userinfo = oauth.get(userinfo_endpoint).json()
        email = userinfo.get("email")
        name = userinfo.get("name")

        st.success(f"Hola {name} ({email}), has iniciado sesión correctamente! 🎉")

        # Ejemplo de filtro para correos institucionales:
        # if not email.endswith("@cayetano.edu.pe"):
        #     st.error("Solo se permiten correos institucionales")
        #     return

        if st.button("Cerrar sesión"):
            st.session_state.token = None

if __name__ == "__main__":
    main()
