import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def get_shopping_insights(items, people_count, days, total_cost):
    model = genai.GenerativeModel('gemini-pro')
    
    cost_per_person_day = total_cost / (people_count * days)
    
    prompt = f"""
    Analise esta lista de compras para {people_count} pessoas por {days} dias:
    {items}
    
    Custo total: R$ {total_cost:.2f}
    Custo por pessoa/dia: R$ {cost_per_person_day:.2f}
    
    Por favor, forneça:
    1. Se as quantidades parecem adequadas
    2. Sugestões de itens que podem estar faltando
    3. Análise do custo (se está dentro da média, alto ou baixo)
    4. Dicas de economia e otimização dos gastos
    Use português do Brasil na resposta.
    """
    
    response = model.generate_content(prompt)
    return response.text
