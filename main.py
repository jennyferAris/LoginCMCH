import streamlit as st
from streamlit_option_menu import option_menu
import auth  # <--- Importa el módulo de autenticación

def main():
    if not st.session_state.token:
        auth.login_box()
        return

    userinfo = auth.get_user_info()
    if userinfo:
        name = userinfo.get("name")
        email = userinfo.get("email")
        st.success(f"Bienvenida, {name} ({email}) 👋")

        if st.button("Cerrar sesión"):
            auth.logout()
            return

    # Sidebar
    with st.sidebar:
        menu = option_menu(
            "Menú principal",
            ["Inicio", "Ver Base de Datos", "Generar QR", "Configuración"],
            icons=['house', 'table', 'qr-code', 'gear'],
            menu_icon="cast",
            default_index=0
        )

    # Rutas
    if menu == "Inicio":
        vista_datos.mostrar_inicio()
    elif menu == "Ver Base de Datos":
        base_datos.mostrar_base_datos()
    elif menu == "Generar QR":
        generar_qr.generar_qrs()
    elif menu == "Configuración":
        st.info("⚙️ Configuración por implementar.")

if __name__ == "main":
    main()