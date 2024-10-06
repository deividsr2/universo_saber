import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import os

# Caminho para o diretório das fotos e cadastro
fotos_path = r"C:\Users\deivi\Desktop\projetos\escola"
cadastro_path = r"C:\Users\deivi\Desktop\projetos\escola\cadastro.xlsx"

# Carregar a planilha de usuários
try:
    usuarios_df = pd.read_excel(cadastro_path, usecols=[2, 3], names=["usuario", "senha"])
    st.write("Planilha carregada com sucesso!")
except Exception as e:
    st.write(f"Erro ao carregar a planilha: {e}")

# Função para verificar as credenciais
def validar_login(usuario, senha):
    user_data = usuarios_df[(usuarios_df['usuario'] == usuario) & (usuarios_df['senha'] == str(senha))]
    if not user_data.empty:
        return True
    return False

# Tela de login
if "login_feito" not in st.session_state:
    st.session_state.login_feito = False

if not st.session_state.login_feito:
    st.title("Login")

    usuario_input = st.text_input("Usuário")
    senha_input = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        login_sucesso = validar_login(usuario_input, senha_input)
        if login_sucesso:
            st.session_state.login_feito = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha inválidos. Tente novamente.")
else:
    # Criação da sidebar usando streamlit_option_menu
    with st.sidebar:
        option = option_menu(
            "Menu",
            ["Recados", "Boletos", "Historico", "Galeria"],
            icons=["chat", "credit-card", "clock-history", "images"],
            menu_icon="cast",
            default_index=0
        )

    # Exibe conteúdo com base na opção selecionada
    if option == "Recados":
        st.title("Recados")
        st.write("Aqui você pode visualizar os recados.")

    elif option == "Boletos":
        st.title("Boletos")
        st.write("Aqui você pode visualizar os boletos.")

    elif option == "Historico":
        st.title("Historico")
        st.write("Aqui você pode visualizar o histórico.")

    elif option == "Galeria":
        st.title("Galeria")
        st.write("Aqui você pode visualizar a galeria de imagens.")

        # Verificar se o diretório existe
        if os.path.exists(fotos_path):
            # Listar todas as imagens no diretório
            fotos = [f for f in os.listdir(fotos_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            if fotos:
                st.write(f"Total de fotos encontradas: {len(fotos)}")
                for foto in fotos:
                    img_path = os.path.join(fotos_path, foto)
                    try:
                        img = Image.open(img_path)
                        st.image(img, caption=foto, use_column_width=True)
                    except Exception as e:
                        st.write(f"Erro ao carregar a imagem {foto}: {e}")
            else:
                st.write("Nenhuma foto encontrada no diretório especificado.")
        else:
            st.write("Caminho das fotos não encontrado. Verifique se o caminho está correto.")
