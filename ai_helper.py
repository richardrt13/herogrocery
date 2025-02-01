import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def get_shopping_insights(items, people_count, days, total_cost):
    model = genai.GenerativeModel('gemini-pro')
    
    cost_per_person_day = total_cost / (people_count * days)
    
    # Criar uma lista formatada com itens por categoria
    items_text = "\n".join(items)
    
    prompt = f"""Você é um nutricionista e especialista em planejamento de compras muito crítico e detalhista.
    Analise criticamente esta lista de compras para {people_count} pessoas por {days} dias:

    {items_text}

    Custo total: R$ {total_cost:.2f}
    Custo por pessoa/dia: R$ {cost_per_person_day:.2f}

    Forneça uma análise detalhada e crítica considerando:

    1. ANÁLISE NUTRICIONAL:
    - Verifique se há proteínas suficientes (considere ~100g/pessoa/dia)
    - Avalie se há vegetais e frutas adequados (mínimo 400g/pessoa/dia)
    - Verifique carboidratos e grãos
    - Identifique grupos alimentares ausentes ou insuficientes
    
    2. ANÁLISE QUANTITATIVA:
    - Compare com o consumo médio esperado por pessoa
    - Calcule se as quantidades durarão pelo período especificado
    - Identifique itens com quantidades potencialmente insuficientes
    - Alerte sobre quantidades excessivas que podem estragar
    
    3. ITENS ESSENCIAIS FALTANTES:
    - Liste itens básicos ausentes por categoria (proteínas, vegetais, etc.)
    - Sugira itens complementares importantes
    - Aponte condimentos e ingredientes básicos que possam estar faltando
    
    4. ANÁLISE DE CUSTOS:
    - Compare com o custo médio de R$ 20-30 por pessoa/dia
    - Identifique itens com preços acima da média
    - Sugira substituições mais econômicas
    - Aponte onde é possível economizar
    
    5. RECOMENDAÇÕES PRÁTICAS:
    - Sugira ajustes específicos nas quantidades
    - Recomende itens adicionais com quantidades específicas
    - Proponha alternativas mais econômicas
    - Dê dicas de armazenamento para evitar desperdício

    IMPORTANTE:
    - Seja extremamente crítico e detalhista
    - Aponte claramente as deficiências
    - Use dados numéricos e comparações específicas
    - Não hesite em apontar problemas graves
    - Indique se a lista é realmente inadequada quando for o caso
    - Liste problemas em ordem de gravidade

    Use português do Brasil na resposta e seja direto e objetivo.
    """
    
    response = model.generate_content(prompt)
    return response.text
