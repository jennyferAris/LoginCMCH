import streamlit as st
from streamlit_option_menu import option_menu
import auth  # módulo de autenticación


def main():
    # Asegurar estados iniciales
    if "token" not in st.session_state:
        st.session_state.token = None
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = None

    # Mostrar login si no hay token
    if not st.session_state.get("token"):
        auth.login_box()
        return

    # Obtener datos del usuario
    userinfo = auth.get_user_info()
    if userinfo:
        name = userinfo.get("name")
        email = userinfo.get("email")
        st.success(f"Bienvenida, {name} ({email}) ")

        if st.button("Cerrar sesión"):
            auth.logout()
            return

    # Sidebar de navegación
    with st.sidebar:
        menu = option_menu(
            "Menú principal",
            ["Inicio", "Ver Base de Datos", "Generar QR", "Configuración"],
            icons=['house', 'table', 'qr-code', 'gear'],
            menu_icon="cast",
            default_index=0
        )

    # Navegación
    if menu == "Inicio":
        vista_datos.mostrar_inicio()
    elif menu == "Ver Base de Datos":
        base_datos.mostrar_base_datos()
    elif menu == "Generar QR":
        generar_qr.generar_qrs()
    elif menu == "Configuración":
        st.info("⚙️ Configuración por implementar.")

if name == "main":
    main()