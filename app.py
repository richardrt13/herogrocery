import streamlit as st
from database import (
    create_user, verify_user, save_shopping_list,
    get_user_lists, delete_list
)
from ai_helper import get_shopping_insights

def main():
    st.title("Lista de Compras Inteligente")
    
    # Inicialização do estado da sessão
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    # Sistema de login/registro
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Cadastro"])
        
        with tab1:
            st.header("Login")
            username = st.text_input("Usuário", key="login_username")
            password = st.text_input("Senha", type="password", key="login_password")
            
            if st.button("Entrar"):
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
        
        with tab2:
            st.header("Cadastro")
            new_username = st.text_input("Usuário", key="register_username")
            new_password = st.text_input("Senha", type="password", key="register_password")
            
            if st.button("Cadastrar"):
                if create_user(new_username, new_password):
                    st.success("Cadastro realizado com sucesso!")
                else:
                    st.error("Usuário já existe")
    
    else:
        st.write(f"Bem-vindo, {st.session_state.username}!")
        
        if st.button("Sair"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        tab1, tab2 = st.tabs(["Nova Lista", "Minhas Listas"])
        
        with tab1:
            st.header("Criar Nova Lista")
            
            list_name = st.text_input("Nome da Lista")
            people_count = st.number_input("Número de Pessoas", min_value=1, value=1)
            days = st.number_input("Período (dias)", min_value=1, value=7)
            
            items = []
            st.subheader("Adicionar Itens")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                item = st.text_input("Item")
            with col2:
                quantity = st.number_input("Quantidade", min_value=1, value=1)
            with col3:
                unit = st.selectbox("Unidade", ["unidade(s)", "kg", "g", "L", "ml", "pacote(s)"])
            
            if st.button("Adicionar Item"):
                items.append(f"{quantity} {unit} de {item}")
                st.write("Itens na lista:")
                for item in items:
                    st.write(f"- {item}")
            
            if st.button("Salvar Lista"):
                if list_name and items:
                    save_shopping_list(
                        st.session_state.username,
                        list_name,
                        items,
                        people_count,
                        days
                    )
                    st.success("Lista salva com sucesso!")
                    
                    # Gerar insights
                    insights = get_shopping_insights(items, people_count, days)
                    st.subheader("Análise da Lista")
                    st.write(insights)
                else:
                    st.error("Preencha todos os campos necessários")
        
        with tab2:
            st.header("Minhas Listas")
            
            user_lists = get_user_lists(st.session_state.username)
            
            for shopping_list in user_lists:
                with st.expander(shopping_list["list_name"]):
                    st.write(f"Para {shopping_list['people_count']} pessoas por {shopping_list['days']} dias")
                    st.write("Itens:")
                    for item in shopping_list["items"]:
                        st.write(f"- {item}")
                    
                    if st.button("Excluir Lista", key=f"delete_{shopping_list['list_name']}"):
                        delete_list(st.session_state.username, shopping_list["list_name"])
                        st.success("Lista excluída com sucesso!")
                        st.rerun()
                    
                    if st.button("Analisar Lista", key=f"analyze_{shopping_list['list_name']}"):
                        insights = get_shopping_insights(
                            shopping_list["items"],
                            shopping_list["people_count"],
                            shopping_list["days"]
                        )
                        st.subheader("Análise da Lista")
                        st.write(insights)

if __name__ == "__main__":
    main()
