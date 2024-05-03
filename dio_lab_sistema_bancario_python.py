# Projeto DIO - Criando um Sistema Bancário com Python

MENU = " MENU "

menu = f"""

{MENU.center(30, "-")}

{"Banco DIO.me".center(30)} 
      
          OPERAÇÕES:

          [1] Depositar
          [2] Sacar
          [3] Extrato
          [0] Sair

{"=".center(30, "=")}      

"""
# Função print para testar o Menu
# print(menu)

#Variáveis:

saldo = 1000
LIMITE = 500
extrato = ""
listagem_deposito = ""
listagem_saque = ""
numero_saques = 0
LIMITE_SAQUES = 3

EXTRATO = " EXTRATO "

while True:

    opcao = int(input(menu))

    if opcao == 1:

        deposito_valor  = float(input("Digite o valor de depósito: "))

        if deposito_valor > 0:

            saldo += deposito_valor

            #extrato
            listagem_deposito += f"\n Você fez um depósito no valor de R$ {deposito_valor:.2f} \n"
        
        else:

            print(f"FALHA! O valor inserido não corresponde a uma operação válida.")

    elif opcao == 2:

        if numero_saques < LIMITE_SAQUES:

            saque_valor = float(input("Digite o valor que deseja sacar de sua conta: "))

            if saque_valor <= saldo and saque_valor <= LIMITE:

                saldo -= saque_valor 

                numero_saques += 1

                #extrato
                listagem_saque += f"\n Você fez um saque no valor de R$ {saque_valor:.2f} \n"

            elif saque_valor > saldo and saque_valor <= LIMITE:

                print(f"FALHA! O valor de saque informado extrapola o saldo em conta.")

            else:

                #saque_valor < LIMITE

                print(f"FALHA! O valor de saque informado extrapola o valor limite.")

        else:

            print(f"Você atingiu o número máximo de saques diários. Tente novamente outro dia.")    
        
    elif opcao == 3:

        extrato = f"""

             {EXTRATO.center(60, "-")}

             {"Listagem de Depósitos:".center(60)}

             {listagem_deposito.center(60)}

             {"Listagem de Saques:".center(60)}

             {listagem_saque.center(60)}

                            "SALDO ATUAL DA CONTA: R$ {saldo:.2f}"

             {"=".center(60, "=")}
        
        """
        print(extrato)

    elif opcao == 0:

        break

    else:

        print("Operação inválida! Por favor, selecione a operação desejada conforme indicado no menu.")  
