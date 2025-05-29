import streamlit as st
from streamlit_auth0_component import login_button

st.set_page_config(page_title="Login CMCH con Google")
st.title("Login CMCH con Google")

# Leer configuración desde st.secrets
auth = st.secrets["auth"]
auth0 = auth["google"]

# Detectar si está en local o en producción
if st.secrets["auth"]["redirect_uri"].startswith("https://cmch-upchic2"):
    redirect_uri = auth["redirect_uri"]
else:
    redirect_uri = auth["redirect_uri_local"]

# Mostrar botón de login
result = login_button(
    domain=auth0["domain"],
    client_id=auth0["client_id"],
    redirect_uri=redirect_uri,
)

# Mostrar resultados
if result:
    st.success("¡Inicio de sesión exitoso!")
    st.subheader("Información del usuario")
    st.json(result)
else:
    st.info("Haz clic en 'Iniciar sesión' para continuar.")

# Botón de logout usando redirección manual
logout_url = f"https://{auth0['domain']}/v2/logout?returnTo={redirect_uri.split('/oauth2callback')[0]}"

if st.button("Cerrar sesión"):
    st.markdown(f'<meta http-equiv="refresh" content="0; url={logout_url}">', unsafe_allow_html=True)
