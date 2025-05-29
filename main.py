import streamlit as st
from streamlit_option_menu import option_menu
import auth

def main():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "oauth_state" not in st.session_state:
        st.session_state.oauth_state = None

    if not st.session_state.get("token"):
        auth.login_box()
        return

    userinfo = auth.get_user_info()
    if userinfo:
        email = userinfo.get("email")

        if not auth.is_authorized_user(email):
            st.error("🚫 Acceso denegado. Tu cuenta no está autorizada.")
            if st.button("Cerrar sesión"):
                auth.logout()
            return

        role = auth.get_user_role(email)
        st.success(f"Bienvenido, {role} 👋")

        if st.button("Cerrar sesión"):
            auth.logout()
            return

        with st.sidebar:
            menu = option_menu(
                "Menú principal",
                ["Inicio", "Ver Base de Datos", "Generar QR", "Configuración"],
                icons=['house', 'table', 'qr-code', 'gear'],
                menu_icon="cast",
                default_index=0
            )

        if menu == "Inicio":
            vista_datos.mostrar_inicio()
        elif menu == "Ver Base de Datos":
            base_datos.mostrar_base_datos()
        elif menu == "Generar QR":
            generar_qr.generar_qrs()
        elif menu == "Configuración":
            st.info("⚙️ Configuración por implementar.")

if __name__ == "__main__":
    main()