import streamlit as st

st.title("Login CMCH con Google")

if st.button("Ingresar"):
    st.login("google")

st.json(st.experimental_user())  # Mostrar información del usuario autenticado
st.image(st.experimental_user().picture, width=100)  # Mostrar la foto de perfil del usuario
st.logout("Cerrar sesión")  # Botón para cerrar sesión