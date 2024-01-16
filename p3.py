from pulp import GLPK, LpInteger, LpMaximize, LpProblem, LpVariable, lpSum, value

def ler_dados_producao():
    linhas = []
    while True:
        try:
            linha = input()
            if linha:  # Verifica se a linha não está vazia
                linhas.append(linha)
            else:  # Se a linha estiver vazia, para de ler
                break
        except EOFError:  # Encerra a leitura se chegar ao fim do arquivo
            break

    n, p, prod_maxima = map(int, linhas[0].split())
    brinquedos = [processar_brinquedo(linha) for linha in linhas[1:n + 1]]
    pacotes = [processar_pacote(linha) for linha in linhas[n + 1:]]
    return n, p, prod_maxima, brinquedos, pacotes

def processar_brinquedo(linha_brinquedo):
    lucro, capacidade = map(int, linha_brinquedo.split())
    return {'lucro': lucro, 'capacidade': capacidade}

def processar_pacote(linha_pacote):
    partes = linha_pacote.split()
    produtos, lucro = tuple(map(int, partes[:-1])), int(partes[-1])
    return {'produtos': produtos, 'lucro': lucro}

def criar_problema_otimizacao(n, p, prod_maxima, brinquedos, pacotes):
    problema_otimizacao = LpProblem("Maximizar_Lucro", LpMaximize)
    variaveis_brinquedos = {i + 1: LpVariable(f"Brinquedo_{i + 1}", 0, brinquedos[i]['capacidade'], LpInteger) for i in range(n)}
    variaveis_pacotes = {i + 1: LpVariable(f"Pacote_{i + 1}", 0, None, LpInteger) for i in range(p)}
    adicionar_restricoes(problema_otimizacao, variaveis_brinquedos, variaveis_pacotes, brinquedos, pacotes)
    adicionar_objetivo(problema_otimizacao, variaveis_brinquedos, variaveis_pacotes, brinquedos, pacotes)
    return problema_otimizacao

def adicionar_restricoes(problema_otimizacao, variaveis_brinquedos, variaveis_pacotes, brinquedos, pacotes):
    brinquedos_nos_pacotes = {i: [] for i in range(1, n + 1)}

    for indice_pacote, pacote in enumerate(pacotes, start=1):
        for brinquedo in pacote['produtos']:
            brinquedos_nos_pacotes[brinquedo].append(indice_pacote)

    for i in range(1, n + 1):
        problema_otimizacao += variaveis_brinquedos[i] + lpSum(variaveis_pacotes[j] for j in brinquedos_nos_pacotes[i]) <= brinquedos[i-1]['capacidade']
    problema_otimizacao += lpSum(variaveis_brinquedos.values()) + lpSum(3 * variaveis_pacotes[j] for j in range(1, p + 1)) <= prod_maxima

def adicionar_objetivo(problema_otimizacao, variaveis_brinquedos, variaveis_pacotes, brinquedos, pacotes):
    problema_otimizacao += lpSum(brinquedos[i-1]['lucro'] * variaveis_brinquedos[i] for i in range(1, n + 1)) + lpSum(pacotes[j-1]['lucro'] * variaveis_pacotes[j] for j in range(1, p + 1))

def otimizar_lucro(problema_otimizacao):
    problema_otimizacao.solve(GLPK(msg=0))
    return value(problema_otimizacao.objective)

# Executa o programa e imprime o lucro máximo
n, p, prod_maxima, brinquedos, pacotes = ler_dados_producao()
problema_otimizacao = criar_problema_otimizacao(n, p, prod_maxima, brinquedos, pacotes)
lucro_maximo = otimizar_lucro(problema_otimizacao)
print(lucro_maximo)