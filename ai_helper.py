import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def get_shopping_insights(items, people_count, days):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Analise esta lista de compras para {people_count} pessoas por {days} dias:
    {items}
    
    Por favor, forneça:
    1. Se as quantidades parecem adequadas
    2. Sugestões de itens que podem estar faltando
    3. Dicas de economia
    Use português do Brasil na resposta.
    """
    
    response = model.generate_content(prompt)
    return response.text
