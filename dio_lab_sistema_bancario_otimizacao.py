# Projeto DIO - Criando um Sistema Bancário com Python - Otimização

def menu():
    
    MENU = " MENU "

    menu = f"""

    {MENU.center(30, "-")}

    {"Banco DIO.me".center(30)} 
      
              OPERAÇÕES:

              [1] Novo Usuário
              [2] Nova Conta
              [3] Listar Contas
              [4] Depositar
              [5] Sacar
              [6] Extrato
              [0] Sair

    {"=".center(30, "=")}      

    """

    return int(input(menu))

def filtro_usuario(cpf, usuarios):

    listagem_usuario = []

    for usuario in usuarios:

        if usuario["cpf"] == cpf:

            listagem_usuario.append(usuario)

            print("\n Esse CPF está cadastrado por um cliente! \n")

            return listagem_usuario[0]

        else:
            
            None

    else:

        None        

def criar_usuario(usuarios):

    cpf = input("\n Informe o número do seu CPF: ")

    cliente = filtro_usuario(cpf, usuarios)

    if bool(cliente) == False:

        print("\n Novo Usuário! Faça seu cadastro. \n")

        nome = input("\n Informe o seu nome completo: ")

        data_nascimento = input("\n Informe sua data de nascimento no formato dd/mm/aaaa: ")

        endereco = input("\n Informe o seu endereço no formato 'rua, nº - bairro - cidade/UF': ")

        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

        print("""
        
        \n Usuário cadastrado com sucesso!
        
        """.center(60))

def criar_conta(agencia, numero_conta, usuarios):

    cpf = input("\n Informe o número do seu CPF: ")

    cliente = filtro_usuario(cpf, usuarios)

    if bool(cliente) == True:

        conta_cliente = {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}

        print("\n Sua conta foi criada com sucesso! \n".center(60))

        return conta_cliente

    else:

        print("\n Não foi possível criar a conta. Usuário não encontrado! \n")

def listagem_contas(contas):

    LISTAGEM_CONTA = " LISTAGEM - CONTA "

    for conta in contas:

        lista = f"""

        {LISTAGEM_CONTA.center(60, "-")}

                     Agência: {conta['agencia']}
                     Nº Conta: {conta['numero_conta']}
                     Cliente: {conta['cliente']['nome']}
                    
        {"=".center(60, "=")}
        
        """

        print(lista)

    #return lista


       

def depositar( saldo, deposito_valor, listagem_deposito, /):

    if deposito_valor > 0:

        saldo += deposito_valor

        #extrato
        listagem_deposito += f"\n Você fez um depósito no valor de R$ {deposito_valor:.2f} \n"
        
    else:

        print(f"FALHA! O valor inserido não corresponde a uma operação válida.")

    return saldo, listagem_deposito

def sacar( *, saldo, saque_valor, listagem_saque, limite, numero_saques, limite_saques):

    if numero_saques < limite_saques:

        if saque_valor <= saldo and saque_valor <= limite:

            saldo -= saque_valor 

            numero_saques += 1

            #extrato
            listagem_saque += f"\n Você fez um saque no valor de R$ {saque_valor:.2f} \n"

        elif saque_valor > saldo and saque_valor <= limite:

            print(f"FALHA! O valor de saque informado extrapola o saldo em conta.")

        else:

            #saque_valor < LIMITE

            print(f"FALHA! O valor de saque informado extrapola o valor limite.")

    else:

        print(f"Você atingiu o número máximo de saques diários. Tente novamente outro dia.")    

    return saldo, listagem_saque 

def listagem_extrato( saldo, /, *, listagem_deposito, listagem_saque):

    EXTRATO = " EXTRATO "

    extrato = f"""

         {EXTRATO.center(60, "-")}

         {"Listagem de Depósitos:".center(60)}

         {listagem_deposito.center(60)}

         {"Listagem de Saques:".center(60)}

         {listagem_saque.center(60)}

                        "SALDO ATUAL DA CONTA: R$ {saldo:.2f}"

         {"=".center(60, "=")}
        
    """
    #print(extrato)
    return extrato

def main():

    #Variáveis:

    saldo = 1000
    LIMITE = 500
    extrato = ""
    listagem_deposito = ""
    listagem_saque = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == 1:

            criar_usuario(usuarios)

        elif opcao == 2:

            numero_conta = len(contas) + 1

            conta = criar_conta( AGENCIA, numero_conta, usuarios)

            if bool(conta) == True:

               contas.append(conta) 

            else:

                None
            
        elif opcao == 3:

            contas_sistema = listagem_contas(contas)

            #print(contas_sistema)

        elif opcao == 4:

            deposito_valor  = float(input("Digite o valor de depósito: "))

            saldo, listagem_deposito = depositar( saldo, deposito_valor, listagem_deposito)

        elif opcao == 5:

            saque_valor = float(input("Digite o valor que deseja sacar de sua conta: "))

            saldo, listagem_saque = sacar( saldo = saldo, saque_valor = saque_valor, listagem_saque = listagem_saque, limite = LIMITE, numero_saques = numero_saques, limite_saques = LIMITE_SAQUES)

        elif opcao == 6:

            lista_extrato = listagem_extrato( saldo, listagem_deposito = listagem_deposito, listagem_saque = listagem_saque)

            print(lista_extrato)
        
        elif opcao == 0:

            break

        else:

            print("Operação inválida! Por favor, selecione a operação desejada conforme indicado no menu.")  

main()