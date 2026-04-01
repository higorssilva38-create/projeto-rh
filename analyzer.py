from openai import OpenAI
import PyPDF2
import re
import os

# 🔐 pega a API key da variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_curriculo(caminho_pdf):
    texto = ""

    # 📄 leitura do PDF
    with open(caminho_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for pagina in reader.pages:
            texto += pagina.extract_text()

    # ⚠️ limitar tamanho (economiza uso da IA)
    texto = texto[:3000]

    # 🤖 prompt para IA
    prompt = f"""
    Você é um especialista em recrutamento.

    Analise o currículo abaixo e responda EXATAMENTE nesse formato:

    Nome: ...
    Nota: (número de 0 a 10)
    Resumo: ...
    Parecer: ...

    Currículo:
    {texto}
    """

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        analise = resposta.choices[0].message.content

    except Exception as e:
        print("Erro na IA:", e)

        # fallback se IA falhar
        analise = """Nome: Não identificado
Nota: 5
Resumo: Não foi possível analisar com IA.
Parecer: Sistema funcionando em modo básico."""

    # 🔍 extrair dados da resposta
    nome = re.search(r"Nome:\s*(.*)", analise)
    nota = re.search(r"Nota:\s*(\d+)", analise)
    resumo = re.search(r"Resumo:\s*(.*)", analise)
    parecer = re.search(r"Parecer:\s*(.*)", analise)

    return {
        "nome": nome.group(1) if nome else "Não identificado",
        "nota": int(nota.group(1)) if nota else 0,
        "resumo": resumo.group(1) if resumo else analise,
        "parecer": parecer.group(1) if parecer else "Sem parecer"
    }