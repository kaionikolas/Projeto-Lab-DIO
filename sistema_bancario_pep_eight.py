from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent


class Cliente:

    def __init__(self, endereco):

        self.endereco = endereco
        self.contas = []

    def fazer_transacao(self, conta, transacao):

        if len(conta.historico.transacoes_diarias()) >= 10:

            print("\n Você excedeu o número de transações diárias! Tente novamente no próximo dia.\n")

            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):

        self.conta.append(conta)


class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):

        super().__init__(endereco)

        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:

        return f"<{self.__class__.__name__}: ('{self.cpf}')>"


class Conta:

    def __init__(self, numero, cliente):

        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):

        return cls(numero, cliente)

    @property
    def saldo(self):

        return self._saldo

    @property
    def numero(self):

        return self._numero

    @property
    def agencia(self):

        return self._agencia

    @property
    def cliente(self):

        return self._cliente

    @property
    def historico(self):

        return self._historico

    def sacar(self, valor):

        saldo = self._saldo

        if valor > saldo:

            print("""\n\t FALHA NA OPERAÇÃO!\n \t \n O valor de saque informado extrapola o saldo em conta. \n""")

        elif valor > 0:

            self._saldo -= valor

            print(f"\n\t OPERAÇÃO REALIZADA COM SUCESSO!\n \t \n Você fez um saque no valor de R$ {valor:.2f} \n")

            return True

        else:

            print("\n \t FALHA NA OPERAÇÃO!\n \t \n O valor de saque informado é inválido. \n")

        return False

    def depositar(self, valor):

        if valor > 0:

            self._saldo += valor

            print(f"\n\t DEPÓSITO REALIZADO!\n \t \n Você fez um depósito no valor de R$ {valor:.2f} \n")

        else:

            print("\n FALHA! O valor inserido não corresponde a uma operação válida.")

            return False

        return True


class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=2):

        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):

        numero_saques = len(

            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]

        )

        if valor > self._limite:

            print("\n\t FALHA NA OPERAÇÃO!\n \t  \n O valor de saque informado extrapola o valor limite.")

        elif numero_saques >= self._limite_saques:

            mensagem_retorno = """

                \t OPERAÇÃO INTERROMPIDA!

        Você atingiu o número máximo de saques diários.

        Tente novamente outro dia.

            """

            print(mensagem_retorno)

        else:

            return super().sacar(valor)

        return False

    def __repr__(self):

        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):

        lista = f"""

        {" CONTA ".center(60, "-")}

                     Agência: {self.agencia}
                     C-C: {self.numero}
                     Cliente: {self.cliente.nome}

        {"=".center(60, "=")}

        """

        return lista


class Historico:

    def __init__(self):

        self._transacoes = []

    @property
    def transacoes(self):

        return self._transacoes

    def adicionar_transacao(self, transacao):

        descricao_transacao = {

            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),

        }

        self._transacoes.append(descricao_transacao)

    def gerador_relatorio(self, tipo_transacao=None):

        for transacao in self._transacoes:

            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():

                yield transacao

    def transacoes_diarias(self):

        dia_atual = datetime.utcnow().date()

        transacoes_do_dia = []

        for transacao in self._transacoes:

            dia_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()

            if dia_atual == dia_transacao:

                transacoes_do_dia.append(transacao)

        return transacoes_do_dia


class Transacao (ABC):

    @property
    @abstractproperty
    def valor(self):

        pass

    @abstractclassmethod
    def registrar(self, conta):

        pass


class Saque(Transacao):

    def __init__(self, valor):

        self._valor = valor

    @property
    def valor(self):

        return self._valor

    def registrar(self, conta):

        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:

            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):

    def __init__(self, valor):

        self._valor = valor

    @property
    def valor(self):

        return self._valor

    def registrar(self, conta):

        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:

            conta.historico.adicionar_transacao(self)


class ContaIterador:

    def __init__(self, contas):

        self.contas = contas

        self._indice = 0

    def __iter__(self):

        return self

    def __next__(self):

        try:

            conta = self.contas[self._indice]

            return f"""
            Agência: {conta.agencia}
            Conta:   {conta.numero}
            Saldo:   R$ {conta.saldo:.2f}
            Cliente: {conta.cliente.nome}

            {"=".center(60, "=")}
        """

        except IndexError:

            raise StopIteration

        finally:

            self._indice += 1


def decorador_transacao(func):

    def envelope_transacao(*args, **kwargs):

        retorno = func(*args, **kwargs)

        data_hora = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        with open(ROOT_PATH / "log.txt", "a") as documento:

            documento.write(

                f"[{data_hora}] Função '{func.__name__}' argumentada com {args} e {kwargs}. O retorno é: {retorno}.\n"

            )

        return retorno

    return envelope_transacao


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


@decorador_transacao
def criar_cliente(clientes):

    cpf = input("\n Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:

        print("\n Existe no sistema um cliente cadastrado com esse CPF!")

        return

    print("\n Novo Usuário! Faça seu cadastro. \n")

    nome = input("\n Informe o seu nome completo: ")

    data_nascimento = input("\n Informe sua data de nascimento no formato dd/mm/aaaa: ")

    endereco = input("\n Informe o seu endereço no formato 'rua, nº - bairro - cidade/UF': ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("""

        \n Usuário cadastrado com sucesso!

        """.center(60))


@decorador_transacao
def criar_conta(numero_conta, clientes, contas):

    cpf = input("\n Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:

        print("\n Não foi possível criar a conta. Usuário não encontrado! \n")

        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

    contas.append(conta)

    cliente.contas.append(conta)

    print("\n Sua conta foi criada com sucesso! \n".center(60))


@decorador_transacao
def listar_contas(contas):

    for conta in ContaIterador(contas):

        print(f"""

        {str(conta).center(60)}

        """)


def filtrar_cliente(cpf, clientes):

    listagem_usuario = [cliente for cliente in clientes if cliente.cpf == cpf]

    return listagem_usuario[0] if listagem_usuario else None


def recuperar_conta_cliente(cliente):

    if not cliente.contas:

        print("\n O Cliente não possui conta no presente momento!")

    return cliente.contas[0]


@decorador_transacao
def depositar(clientes):

    cpf = input("\n Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:

        print("\n Esse não é um CPF cadastrado por cliente! \n")

        return

    valor = float(input("\n Insira o valor do depósito: "))

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:

        return

    cliente.fazer_transacao(conta, transacao)


@decorador_transacao
def sacar(clientes):

    cpf = input("\n Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:

        print("\n Esse não é um CPF cadastrado por cliente! \n")

        return

    valor = float(input("\n Informe o valor do saque: "))

    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:

        return

    cliente.fazer_transacao(conta, transacao)


@decorador_transacao
def listagem_extrato(clientes):

    cpf = input("\n Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:

        print("\n Esse CPF está cadastrado por um cliente! \n")

        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:

        return

    extrato = ""

    transacao_existencia = False

    variavel_transacao = input("\n Entre com o tipo de transação => 'Deposito', 'Saque', 'Ambos': ")

    print("\n ")

    print(" EXTRATO ".center(60, "-"))

    if variavel_transacao == "Ambos":

        variavel_transacao = None

    for transacao in conta.historico.gerador_relatorio(tipo_transacao=variavel_transacao):

        transacao_existencia = True

        extrato += f"\n {transacao['data']} \n {transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n"

    if not transacao_existencia:

        extrato = "Não foram realizadas transações até o momento."

    print(extrato)
    print(f"\n SALDO ATUAL DA CONTA:\n\tR$ {conta.saldo:.2f}".center(60))
    print("=".center(60, "="))


def main():

    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == 1:

            criar_cliente(clientes)

        elif opcao == 2:

            numero_conta = len(contas) + 1

            criar_conta(numero_conta, clientes, contas)

        elif opcao == 3:

            listar_contas(contas)

        elif opcao == 4:

            depositar(clientes)

        elif opcao == 5:

            sacar(clientes)

        elif opcao == 6:

            listagem_extrato(clientes)

        elif opcao == 0:

            break

        else:

            print("Operação inválida! Por favor, selecione a operação desejada conforme indicado no menu.")


main()
