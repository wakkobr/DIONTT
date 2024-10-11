# Sistema Bancário em Python
# Autor: Gabriel Pessine
# Data: 10/10/2024
# Descrição: Atualização do Sistema Bancário criado anteriormente, adicionando POO
# Parte do desafio do DIO/NTT - Modulo Trabalhando com Coleções em Pyhton

import textwrap
import re
from datetime import datetime
from abc import ABC, abstractmethod

#----------------------------------------
# CLASSE: Conta
#----------------------------------------
#
# UML: 1 Conta - N Historico
#
# - saldo: float
# - numero: int
# - agencia: str - senpre 0001
# - cliente: Cliente
# - historico: Historico
#
# + saldo(): float
# + nova_conta(cliente: Cliente, numero: int): Conta
# + sacar(valor: float): bool
# + depositar(valor: floar): bool
#

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

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

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

#
# MÉTODO sacar
#
# Realiza saque da conta.
#
# Args:
#    valor (float): valor do saque.
# Retorna:
#    bool: T ou F, dependendo do sucesso ou não da operação
#

    @property
    def sacar(self, valor):

      saldo = self.saldo
      excedeu_saldo = valor > saldo

      if excedeu_saldo:
        print("\n==================================================")
        print(f"Saldo insuficiente. Seu saldo atual é de R$ {saldo:.2f}.")
        print("==================================================")

      elif valor > 0:
        self._saldo -= valor
        print("\n==================================================")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        print("==================================================")
        return True

      else:
        print("\n==================================================")
        print("Valor inválido, deve ser maior que zero.")
        print("==================================================")

      return False

#
# MÉTODO depositar
#
# Realiza depósito na conta.
#
# Args:
#    valor (float): valor do depósito.
# Retorna:
#    bool: T ou F, dependendo do sucesso ou não da operação
#

    def depositar(self, valor):

      if valor > 0:
        self._saldo += valor
        print("\n==================================================")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        print("==================================================")

      else:
        print("\n==================================================")
        print("Valor inválido, deve ser maior que zero.")
        print("==================================================")
        return False

      return True

#----------------------------------------
# CLASSE: ContaCorrente
# Estende: Conta
#----------------------------------------
#
# - limite: float - 500
# - limite_saques: int - 3
#

class ContaCorrente (Conta):
  def __init__(self, numero, cliente, limite=500, limite_saques=3):
    super().__init__(numero, cliente)
    self.limite = limite
    self.limite_saques = limite_saques

# sobrescreve o método SACAR, para fazer validações
  def sacar(self, valor):

    # percorre o Historico (transacoes) para contar os que sejam do tipo "Saque"
    cont_saques = 0
    for transacao in self.historico.transacoes:
        if transacao["tipo"] == "Saque":
            cont_saques += 1

    excedeu_limite = valor > self.limite                  # T or F
    excedeu_saques = cont_saques >= self.limite_saques    # T or F

    if excedeu_limite:
      print("\n==================================================")
      print("O valor do saque excede o limite máximo por operação, que é de R$ 500.")
      print("==================================================")

    elif excedeu_saques:
      print("\n==================================================")
      print("Você atingiu o limite máximo de 3 saques diários.")
      print("==================================================")

    # se deu tudo certo, chama o método pai SACAR
    else:
      return super().sacar(valor)

    # se não entrou no else, siginifica que entrou em alguma das excessÕes acima
    return False

# método STR, que representa a classe ContaCorrente
  def __str__(self):
    return f"""\
      Agência:\t{self.agencia}
      C/C:\t\t{self.numero}
      Titular:\t{self.cliente.nome}
    """

#----------------------------------------
# CLASSE: Historico
#----------------------------------------
#
# UML: 1 Conta - N Historico
#
# + adicionar_transacao (transacao: Transacao)

class Historico:

# lista de transacoes
  def __init__(self):
    self.transacoes = []

  @property
  def transacoes(self):
    return self._transacoes

#
# MÉTODO adicionar_transacao
#
# Adiciona transação à lista de transações (dicionário)
#
# Dicionário:
# - tipo: str - nome da transação - "Saque" ou "Deposito"
# - valor: float - valor da transação
#

  def adicionar_transacao(self, transacao):
    self._transacoes.append
    {
      "tipo": transacao.__class__.__name__,
      "valor": transacao.valor,
    }

#----------------------------------------
# CLASSE: Cliente
#----------------------------------------
#
# UML: 1 Cliente - N Contas
#
# - endereco: str
# - contas: lista
#
# + realizar_transacao(conta: Conta, transacao: Transacao)
# + adicionar_conta(conta: Conta)
#

class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao ):
    transacao.registrar(conta)

  def adicionar_conta(self, conta):
    self.contas.append(conta)

#
# CLASS: PessoaFisice
# Estende: Cliente
#
# - cpf: str
# - nome: str
# - data_nascimento: date
#

class PessoaFisica (Cliente):
  def __init__(self, nome, data_nascimento, cpf, endereco):
    super().__init__(endereco)
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf

#
# CLASS: <<interface>>Transacao
#
# Estende ABC (classe abstrata)
#

class Transacao(ABC):

  @property
  @abstractmethod
  def valor(self):
    pass

#
# MÉTODO registrar
#
# Recebe a conta
#

  @classmethod
  @abstractmethod
  def registrar(self, conta):
    pass

#----------------------------------------
# CLASSE: Saque
# Estende: Transacao
#----------------------------------------
#

class Saque(Transacao):

  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    resultado_operacao = conta.sacar(self.valor)

# se retornou TRUE - operação bem-sucedida
    if resultado_operacao:
      conta.historico.adicionar_transacao(self)

#----------------------------------------
# CLASSE: Deposito
# Estende: Transacao
#----------------------------------------
#

class Deposito(Transacao):

  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor

  def registrar(self, conta):
    resultado_operacao = conta.depositar(self.valor)

#se retornou TRUE - operação bem-sucedida
    if resultado_operacao:
      conta.historico.adicionar_transacao(self)


#====================================================================
# Desafio Extra - Atualizar os métodos que tratam as opções do Menu, 
# para funcionar com as classes acima
#====================================================================
#
# Eliminação das variaveis (limite, etc), que são atributos da classe Conta
# Ajuste de nomenclatura: usuario virou cliente
#                                          


###############
# Função MENU #
###############
#                                          
# Cria o menu principal do programa, retornando a opção escolhida
#

def menu():

    print("======================================")
    print("     Sistema Bancário em Python")
    print("======================================")

    menu = """
    ===== Escolha a operação desejada ====

    [D]  Depósito
    [S]  Saque
    [E]  Extrato
    [N]  Novo cliente
    [C]  Criar conta corrente
    [L]  Listar contas
    [X]  Sair\n
    => """
    return input(textwrap.dedent(menu))

######################
# Função VALIDAR_CPF #
######################
#                                          
# Valida o CPF informado
#
# Args:
#    cpf (str): cpf do cliente
# Retorna:
#    bool: T ou F - cpf válido ou não
#

def validar_cpf(cpf):

    # Remove pontos e traços do CPF e valida
    cpf = limpar_cpf(cpf)

    # Verifica se possui os 11 dígitos esperados
    if len(cpf) != 11:
      return False

    # Verifica se todos os caracteres são dígitos
    elif not cpf.isdigit():
      return False

    return True

######################
# Função LIMPAR_CPF #
######################
#                                          
# Transforma o CPF em apenas numeros
#
# Args:
#    cpf (str): cpf do cliente
# Retorna:
#    cpf (str): cpf 'limpo'
#

def limpar_cpf(cpf):

    # Remove pontos e traços do CPF e valida
    cpf = cpf.replace('.', '').replace('-', '')

    return cpf
                                                                                    
##########################
# Função VALIDAR_CLIENTE #
##########################
#                                          
# Valida se o cliente ja existe ou não
#
# Args:
#    cpf (float): cpf a ser pesquisado
#    clientes (list): lista de clientes
#

def validar_cliente(cpf, clientes):

    cliente_existente = None
                  
    # percorre a lista, comparando o cpf
    # se existir, retorna o cliente
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_existente = cliente
            break  # para o for quando o cliente é encontrado

#######################
# Função BUSCAR_CONTA #
#######################
#                                          
# Busca e retorna a conta do cliente
#
# Args:
#    cliente: lista de clientes
#

def buscar_conta(cliente):

    # caso a conta não exista
    if not cliente.contas:
        print("\n==================================================")
        print("Cliente não possui conta corrente, favor verificar")
        print("==================================================")
        return
                                          
    # retorna a primeira conta do cliente
    return cliente.contas[0]
                                                                                    
####################
# Função DEPOSITAR #
####################
#                                          
# Recebe: lista de CLIENTES
#
# Possivel melhoria: pedir em qual conta do cliente quer depositar                                          

def depositar(clientes):

    cpf = input("\nInforme o CPF do cliente (somente números): ")

    # cpf inválido
    if not validar_cpf(cpf):
        print("\n===================================")
        print("CPF inválido, favor verificar")
        print("===================================")
        return

    else:
        cpf = limpar_cpf(cpf)

        cliente = validar_cliente(cpf, clientes)

        # cliente não existe
        if not cliente:
            print("\n=========================================================")
            print(f"Cliente CPF {cpf} não encontrado, depósito não realizado")
            print("=========================================================")
            return

        valor = float(input("\nDigite o valor que quer depositar: "))

        if valor <= 0:
            print("\n==================================================")
            print("Valor inválido, deve ser maior que zero.")
            print("==================================================")
            return
                  
        # cliente existe          
        else:      
            # cria uma transacao de Deposito      
            transacao = Deposito(valor)

            conta = buscar_conta(cliente)

            # cliente nao tem conta
            if not conta:
                  return

            cliente.realizar_transacao(conta, transacao)

################
# Função SACAR #
################
#
# Recebe: lista de CLIENTES
#

def sacar(clientes):

    cpf = input("\nInforme o CPF do cliente (somente números): ")

    # cpf inválido
    if not validar_cpf(cpf):
        print("\n===================================")
        print("CPF inválido, favor verificar")
        print("===================================")
        return

    else:
        cpf = limpar_cpf(cpf)          

        cliente = validar_cliente(cpf, clientes)

        # cliente não existe
        if not cliente:
            print("\n=========================================================")
            print(f"Cliente CPF {cpf} não encontrado, depósito não realizado")
            print("=========================================================")
            return

        valor = float(input("\nDigite o valor que quer sacar: "))

        if valor <= 0:
            print("\n==================================================")
            print("Valor inválido, deve ser maior que zero.")
            print("==================================================")
            return
                  
        # cliente existe          
        else:      
            # cria uma transacao de Saque      
            transacao = Saque(valor)

            conta = buscar_conta(cliente)

            # cliente nao tem conta       
            if not conta:
                  return

            cliente.realizar_transacao(conta, transacao)
                  
#########################
# Função MOSTRA_EXTRATO #
#########################
#                  
# Mostra o extrato completo da conta
#
# Recebe: lista de CLIENTES
#

def mostra_extrato(clientes):

    cpf = input("\nInforme o CPF do cliente (somente números): ")

    # cpf inválido
    if not validar_cpf(cpf):
        print("\n===================================")
        print("CPF inválido, favor verificar")
        print("===================================")
        return

    else:
        cpf = limpar_cpf(cpf)         

        cliente = validar_cliente(cpf, clientes)

        # cliente não existe
        if not cliente:
            print("\n=========================================================")
            print(f"Cliente CPF {cpf} não encontrado, depósito não realizado")
            print("=========================================================")
            return

        conta = buscar_conta(cliente)

        # cliente nao tem conta
        if not conta:
              return

        # cliente existe e tem conta                                 
        print("\n==================================================")
        print("Extrato:")
        print("==================================================\n")

        transacoes = conta.historico.transacoes

        extrato = ""

        # nao ha transacoes para a conta
        if not transacoes:
            print("\n==================================================")
            print("Não foram realizadas movimentações nessa conta.")
            print("==================================================")

        # ha trasacoes para a conta              
        else:
            print("\n=========================")
            for transacao in transacoes:
                  extrato += f"Data: {transacao['data']}\n"
                  extrato += f"Tipo: {transacao['tipo']}\n"
                  extrato += f"Valor: {transacao['valor']}\n"

        print(extrato)
        print("\n=========================")
        print(f"Saldo atual: R$ {conta.saldo:.2f}")
        print("=========================")

######################                  
# Função CRIAR_CONTA #
######################                  
#
# Cria uma conta corrente
#
# Args:
#    numero_conta (valor incremental)
#    clientes
#    contas                  
#

def criar_conta(numero_conta, clientes, contas):

    cpf = input("\nInforme o CPF do cliente (somente números): ")

    # cpf inválido
    if not validar_cpf(cpf):
        print("\n===================================")
        print("CPF inválido, favor verificar")
        print("===================================")
        return

    else:
        cpf = limpar_cpf(cpf)          

        cliente = validar_cliente(cpf, clientes)

        # cliente não existe
        if not cliente:
            print("\n=========================================================")
            print(f"Cliente CPF {cpf} não encontrado, criação de conta não realizada")
            print("=========================================================")
            return

        # chama o construtor da conta
        conta = ContaCorrente.nova_conta(cliente = cliente,
                                         numero = numero_conta)
        
        # atualiza a lista de contas          
        contas.append(conta)

        # atualiza a lista de contas do cliente                            
        cliente.adicionar_conta(conta)
                  
        print("\n=========================")
        print(f"Conta número {numero_conta} criada com sucesso para o cliente {cpf}")
        print("=========================")

########################
# Função LISTAR_CONTAS #
########################
#                      
# Lista as conta correntes existentes
#
# Args:
#    contas (list): lista com as contas existentes
#

def listar_contas(contas):

    print("\n==================================================")
    print("Listagem de Contas")
    print("==================================================\n")

    # repete até listar todas as contas
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
                  
########################                
# Função CRIAR_cliente #
########################                  
#
# Cria um cliente
#
# Args:
#    clientes (list): Lista com todos os clientes
#

def criar_cliente(clientes):

#---------------------        
# CPF
#---------------------   
              
    cpf = input("\nInforme o CPF do cliente (somente números): ")

    # cpf inválido
    if not validar_cpf(cpf):
        print("\n===================================")
        print("CPF inválido, favor verificar")
        print("===================================")
        return

    else:
        cpf = limpar_cpf(cpf)

        cliente = validar_cliente(cpf, clientes)

        # cliente já existe
        if cliente:
            print("\n=====================================")
            print(f"Cliente CPF {cpf} já existe!")
            print("=====================================")
            return

  
#---------------------
# Nome Completo
#---------------------

    print("\n=========================")
    nome = input("Informe o nome completo (nome + sobrenome): ")
    print("=========================")

    # Verifica se um nome foi informado
    if not nome:
        print("\n=========================")
        print("O nome não pode ser vazio.")
        print("=========================")
        return

    # Verifica se o nome é composto de Nome e Sobrenome
    else:
        if len(nome.split()) < 2:
            print("\n=========================")
            print("O nome deve conter pelo menos duas palavras (nome e sobrenome).")
            print("=========================")
            return

#---------------------
# Data de Nascimento
#---------------------

    print("\n=========================")
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
    print("=========================")

    # Verifica se a data de nascimento foi informada
    if not data_nascimento:
        print("\n=========================")
        print("A data de nascimento não pode ser vazia.")
        print("=========================")
        return

    # Validação da data de nascimento
    try:
        datetime.strptime(data_nascimento, '%d/%m/%Y')
    except ValueError:
        print("\n=========================")
        print("Data de nascimento inválida. Utilize o formato DD/MM/AAAA.")
        print("=========================")
        return

#---------------------
# Endereço
#---------------------

    endereco = input("Informe o endereço (Logradouro - Num - Bairro - Cidade/Sigla do estado): ")

    # Verifica se o endereço foi informado
    if not endereco:
        print("\n=========================")
        print("O endereço não pode ser vazio.")
        print("=========================")
        return
    
    # Passou em todas as validações
    else:

        # cria pessoa fisica (instancia)              
        cliente = PessoaFisica (nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco)

        # adiciona o cliente à lista              
        clientes.append(cliente)    

        print("\n=======================================================")
        print(f"Cliente {cpf} cadastrado com sucesso!")
        print("=======================================================")
        return

#==================================
# PROGRAMA PRINCIPAL
#==================================

def main():

    # listas
    clientes = []
    contas = []

    while True:
        opcao = menu()

# DEPOSITAR
        if opcao == "D" or opcao == "d":
            depositar(clientes)

# SACAR
        elif opcao == "s" or opcao == "S":
            sacar(clientes)

# EXTRATO
        elif opcao == "e" or opcao == "E":
            mostra_extrato(clientes)

# CRIAR cliente
        elif opcao == "n" or opcao == "N":
            criar_cliente(clientes)

# CRIAR CC
        elif opcao == "C" or opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

# LISTAR CC
        elif opcao == "L" or opcao == "l":
            listar_contas(contas)

# SAIR
        elif opcao == "x" or opcao == "X":
            break

# OP INVÁLIDA
        else:
            print("\n=========================")
            print("Opção inválida.")
            print("=========================")

main()