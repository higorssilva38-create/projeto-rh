candidatos = []

def adicionar_candidato(dados):
    candidatos.append(dados)
    candidatos.sort(key=lambda x: x["nota"], reverse=True)

def obter_ranking():
    return candidatos

def limpar_ranking():
    candidatos.clear()