import json
import sys

if len(sys.argv) <= 1:
    print("Usar: python mt.py [MT].json \"[Palavra]\" ")
    sys.exit(0)
    
with open(sys.argv[1], 'r') as file:
    mt_json = json.loads(file.read())
    if len(sys.argv) == 2:
        sys.argv.append("_")
        palavra = sys.argv[2]
    else:    
        palavra = sys.argv[2]

M = mt_json["mt"]
estados = M[0]
alfabeto_entrada = M[1]
alfabeto_fita = M[2]
cabeca = M[3]
vazio = M[4]
transicoes = M[5]
estado_inicial = M[6]
estados_finais = M[7]

historico_transicoes = ["@","@"]
historico_indices = ["@","@"]


def fn_trans(estado, fita_principal, transicoes, finais, fita_mutavel, i_fita_mutavel):
    
    #print(f'Atual: {estado}, fita: {fita_mutavel}, i: {i_fita_mutavel} ({fita_mutavel[i_fita_mutavel]})') # Depuração

    trans = [i for i in transicoes if i[0] == estado and i[1] == fita_mutavel[i_fita_mutavel]]
    
    if len(trans) == 0:
        #print("não foi achada transição para esse caso") # Depuração
        if estado in finais:
            return True
        historico_transicoes.pop()
        historico_indices.pop()
        return False  

    for t in trans:

        #print(f'Atual: {estado}, fita: {fita_mutavel}, i: {i_fita_mutavel} ({fita_mutavel[i_fita_mutavel]})') # Depuração
        #print(f"TENTANDO TRANSICAO DE {t[0]} para {t[2]}") # Depuração

        flag = False

        for hi in historico_indices:

            #print(f"--com indice {hi}--") # Depuração

            for ht in historico_transicoes:

                #print(f"{t} x {ht}") # Depuração

                if t == ht and fita_principal == fita_mutavel and hi == i_fita_mutavel:
                    flag = True
                    
            if flag: break
        if flag: break
        
        if flag == False:

            fita_mutavel_aux = list(fita_mutavel)
            

            # Troca caracter
            
            fita_mutavel_aux[i_fita_mutavel] = t[3]
            fita_mutavel_aux = ''.join(fita_mutavel_aux)
            
            historico_transicoes.append(t)
            historico_indices.append(i_fita_mutavel)

            if len(historico_transicoes) > 2:
                historico_transicoes.pop(0)
            if len(historico_indices) > 2:
                historico_indices.pop(0)

            # Move referencia
            i_fita_mutavel_aux = i_fita_mutavel

            if t[4] == "<":
                i_fita_mutavel_aux -= 1
            elif t[4] == ">":
                i_fita_mutavel_aux += 1

            # Chamar transicao
            if fn_trans(t[2], fita_principal, transicoes, finais, fita_mutavel_aux, i_fita_mutavel_aux):
                return True


            
    return False
            



def mt():

    fita_principal_inicial = cabeca + palavra + vazio
    i_fita_principal_inicial = 1

    fita_mutavel_incial = fita_principal_inicial
    i_fita_mutavel_inicial = i_fita_principal_inicial

    tem_transicao_inicial = False

    for t in transicoes:
        if t[0] == estado_inicial and t[1] == fita_principal_inicial[i_fita_principal_inicial]:
            tem_transicao_inicial = True
            break
    
    if(tem_transicao_inicial == True):# Caso tenha transição inicial válida para o primeiro elemento da palavra

        if fn_trans(estado_inicial, fita_principal_inicial, transicoes, estados_finais, fita_mutavel_incial, i_fita_mutavel_inicial):
            print("Sim")
        else:
            print("Não")

    else:# Caso não tenha transição inicial válida para o primeiro elemento da palavra
        if(len(transicoes) == 0 and palavra[0] == "_"):# O unico caso que da certo é o quando o automato é somente um estado sem transiçoes, ou seja, só reconhece lambda.
            print("Sim")
        else:
            print("Não")



mt()