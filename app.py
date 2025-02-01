import streamlit as st
from database import (
    create_user, verify_user, save_shopping_list,
    get_user_lists, delete_list
)
from ai_helper import get_shopping_insights

def format_currency(value):
    return f"R$ {value:.2f}"

def main():
    st.title("Lista de Compras Inteligente")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_items = []
        st.session_state.total_cost = 0.0

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
                    st.session_state.current_items = []
                    st.session_state.total_cost = 0.0
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
            st.session_state.current_items = []
            st.session_state.total_cost = 0.0
            st.rerun()
        
        tab1, tab2 = st.tabs(["Nova Lista", "Minhas Listas"])
        
        with tab1:
            st.header("Criar Nova Lista")
            
            list_name = st.text_input("Nome da Lista")
            people_count = st.number_input("Número de Pessoas", min_value=1, value=1)
            days = st.number_input("Período (dias)", min_value=1, value=7)
            
            st.subheader("Adicionar Itens")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                item = st.text_input("Item")
            with col2:
                quantity = st.number_input("Quantidade", min_value=0.1, value=1.0, step=0.1)
            with col3:
                unit = st.selectbox("Unidade", ["unidade(s)", "kg", "g", "L", "ml", "pacote(s)"])
            with col4:
                price = st.number_input("Preço (R$)", min_value=0.01, value=1.00, step=0.01)
            
            if st.button("Adicionar Item"):
                item_total = price * quantity
                item_data = {
                    "name": item,
                    "quantity": quantity,
                    "unit": unit,
                    "price": price,
                    "total": item_total
                }
                st.session_state.current_items.append(item_data)
                st.session_state.total_cost += item_total
            
            # Mostrar itens atuais
            if st.session_state.current_items:
                st.write("Itens na lista:")
                for idx, item in enumerate(st.session_state.current_items):
                    st.write(f"- {item['quantity']} {item['unit']} de {item['name']} - {format_currency(item['price'])} cada = {format_currency(item['total'])}")
                
                st.write(f"**Custo Total: {format_currency(st.session_state.total_cost)}**")
                st.write(f"**Custo por pessoa/dia: {format_currency(st.session_state.total_cost / (people_count * days))}**")
            
            if st.button("Salvar Lista"):
                if list_name and st.session_state.current_items:
                    formatted_items = [
                        f"{item['quantity']} {item['unit']} de {item['name']} ({format_currency(item['price'])} cada)"
                        for item in st.session_state.current_items
                    ]
                    formatted_items
                    
                    save_shopping_list(
                        st.session_state.username,
                        list_name,
                        formatted_items,
                        people_count,
                        days,
                        st.session_state.total_cost
                    )
                    
                    # Gerar insights
                    insights = get_shopping_insights(
                        formatted_items,
                        people_count,
                        days,
                        st.session_state.total_cost
                    )
                    
                    st.success("Lista salva com sucesso!")
                    st.subheader("Análise da Lista")
                    st.write(insights)
                    
                    # Limpar lista atual
                    st.session_state.current_items = []
                    st.session_state.total_cost = 0.0
                    st.rerun()
                else:
                    st.error("Preencha todos os campos necessários")
        
        with tab2:
            st.header("Minhas Listas")
            
            user_lists = get_user_lists(st.session_state.username)
            
            for shopping_list in user_lists:
                with st.expander(shopping_list["list_name"]):
                    st.write(f"Para {shopping_list['people_count']} pessoas por {shopping_list['days']} dias")
                    st.write(f"**Custo Total: {format_currency(shopping_list['total_cost'])}**")
                    st.write(f"**Custo por pessoa/dia: {format_currency(shopping_list['total_cost'] / (shopping_list['people_count'] * shopping_list['days']))}**")
                    
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
                            shopping_list["days"],
                            shopping_list["total_cost"]
                        )
                        st.subheader("Análise da Lista")
                        st.write(insights)

if __name__ == "__main__":
    main()
