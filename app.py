import streamlit as st

st.set_page_config(
    page_title="🏠 ALUN - Dashboard Financeiro",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

SENHA_CORRETA = "saldosalun2026"

def verificar_autenticacao():
    """Verifica se o usuário está autenticado. Se não, mostra tela de login."""
    
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
            <h1 style="color: #ff6b35; text-align: center;">🔐 Acesso Restrito</h1>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("### Digite a senha para continuar")
            senha = st.text_input("Senha:", type="password")
            
            if st.button("Acessar", use_container_width=True):
                if senha == SENHA_CORRETA:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta!")
        
        st.stop()

verificar_autenticacao()

st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">ALUN</h1>
        <div style="color: #ccc; font-size: 12px; margin-top: 10px;">Dashboard Financeiro</div>
    </div>
""", unsafe_allow_html=True)

st.info("✅ App funcionando! Você tem 2 páginas na barra lateral: **Home** e **Planejamento Estratégico**")
