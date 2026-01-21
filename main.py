import pandas as pd
import numpy as np
from funcoes import SalvaUsers, SalvaCarrinho, Listarprodutos, conecta_bd, listarClientes, ListasPedidos, ListasPedidos_produtos, AddProd,Remove,AttCli,AttProd
from createbd import cria_bancodados
from tratamento import ChamaTratamento, aplicandomerge, faturamento_total, media_gastos_cliente

cria_bancodados()
print("=== SISTEMA DA LOJA TECHs ===")

Prod = {
    "1": {"nome": "Notebook", "preco": 3500.00},
    "2": {"nome": "Mouse Gamer", "preco": 150.00},
    "3": {"nome": "Teclado Mecânico", "preco": 500.00},
    "4": {"nome": "Monitor", "preco": 1000.00}
}

while True:
    carrinho = []

    print("\n1 - Acessar Loja")
    print("2 - Admin")
    print("0 - Sair")

    opc = input("Escolha: ")

    if opc == "1":
        while True:
            print("\n--- PRODUTOS DE TECNOLOGIA ---")
            for key, value in Prod.items():
                print(f"{key} - {value['nome']} | Preço: R$ {value['preco']:.2f}")
            print("0 - Finalizar compra")

            prod = input("Escolha o produto: ")

            if prod == "0":
                break

            if prod not in Prod:
                print("Produto inválido!")
                continue

            qtd = int(input("Digite a quantidade: "))

            carrinho.append({
                "id": prod,
                "nome": Prod[prod]["nome"],
                "quantidade": qtd,
                "preco": Prod[prod]["preco"]
            })

            print("\n--- CARRINHO ---")
            for item in carrinho:
                subtotal = item["quantidade"] * item["preco"]
                print(
                    f"Nome: {item['nome']} | "
                    f"Quantidade: {item['quantidade']} | "
                    f"Preço Unitário: R$ {item['preco']:.2f} | "
                    f"Subtotal: R$ {subtotal:.2f}"
                )
            print("Seu Carrinho foi Salvo!")

        if carrinho:
            print("\n--- CHECKOUT ---")
            nome = input("Digite seu nome: ")
            email = input("Digite seu email: ")
            endereco = input("Digite seu endereço: ")

            SalvaUsers(nome, email, endereco)
            SalvaCarrinho(carrinho, nome)

            print("\n--- DADOS CADASTRADOS ---")
            print(f"Nome: {nome}")
            print(f"Email: {email}")
            print(f"Endereço: {endereco}")
            print("\nPedido salvo com sucesso!")

    # ================== ADMIN ==================
    elif opc == "2":
        while True:
            print("\n=== ADMIN ===")
            print("1 - Listar dados")
            print("2 - Remover dados")
            print("3 - Atualizar dados")
            print("4 - Tratamento de dados")
            print("5 - Adicionar Produtos")
            print("0 - Voltar")

            adm = input("Escolha: ")

            # Pré-tratamento com Pandas
            clientes = pd.read_sql("SELECT * FROM clientes", conecta_bd())
            produtos = pd.read_sql("SELECT * FROM produtos", conecta_bd())
            pedidos = pd.read_sql("SELECT * FROM pedidos", conecta_bd())

            clientes = ChamaTratamento(clientes)
            produtos = ChamaTratamento(produtos)
            pedidos = ChamaTratamento(pedidos)

            # -------- LISTAR --------
            if adm == "1":
                print("\nQual dados deseja listar?")
                print("1 - Produtos")
                print("2 - Clientes")
                print("3 - Pedidos")
                print("0 - Voltar")

                tabela = input("Escolha: ")

                if tabela == "1":
                    print("\n--- PRODUTOS ---")
                    print(produtos.to_string(index=False))

                elif tabela == "2":
                    print("\n--- CLIENTES ---")
                    print(clientes.to_string(index=False))

                elif tabela == "3":
                    print("\n--- PEDIDOS ---")
                    print(pedidos.to_string(index=False))

            # -------- REMOVER --------
            elif adm == "2":
                print("\nQual dados deseja remover?")
                print("1 - Produtos")
                print("2 - Clientes")
                print("3 - Pedidos")
                print("0 - Voltar")

                remover = input("Escolha: ")

                if remover == "1":
                    Remove(input("ID do produto: "), "produtos")
                elif remover == "2":
                    Remove(input("ID do cliente: "), "clientes")
                elif remover == "3":
                    Remove(input("ID do pedido: "), "pedidos")

            # -------- ATUALIZAR --------
            elif adm == "3":
                print("\nQual dados deseja atualizar?")
                print("1 - Produtos")
                print("2 - Clientes")
                print("0 - Voltar")
                atualizar = input("Escolha: ")

                if atualizar == "1":
                    idprod = input("Digite o ID do produto para procurar ele: ")
                    nome = input("Digite novo nome: ")
                    val = input("Digite novo valor: ")
                    AttProd(idprod,nome,val)

                elif atualizar == "2":
                    idd = input("Digite o ID do cliente: ")
                    nome =  input("Digite novo nome: ")
                    email = input("Digite novo email: ")
                    end = input("Digite novo endereço: ")
                    AttCli(idd,nome,email,end)


                elif atualizar == "0":
                    continue

            # -------- TRATAMENTO --------
            elif adm == "4":
                print("\n--- TRATAMENTOS ---")
                print("Ao escolher uma das opções abaixo, os dados serão tratados e exibidos, conforme a opção escolhida,inclusive eles ja passaram pelo tratamento de limpeza, conversão e formatação.")
                print("1 - Junção Pedido + Cliente")
                print("2 - Média de valor gasto por cliente")
                print("3 - Faturamento total da loja")
                t = input("Escolha: ")

                if t == "1":
                    print("Junção Pedido + Cliente")
                    res = aplicandomerge(pedidos,clientes)
                    print(res.to_string(index=False))    
                elif t == "2":
                    print("Gastos por cliente") #Usar o merge para juntar pedidos e clientes, agrupar por cliente e calcular a média dos gastos
                    Media = media_gastos_cliente()
                    print(Media.to_string(index=False)) 
                elif t == "3":
                    print("Faturamento total da loja")
                    res = faturamento_total()
                    print(res)

            # -------- ADICIONAR PRODUTOS --------
            elif adm == "5":
                print("\n--- ADICIONAR PRODUTOS ---")
                nome_prod = input("Nome do produto: ")
                preco_prod = float(input("Preço do produto: "))
                estoque_prod = int(input("Estoque do produto: "))
          
                AddProd(nome_prod, preco_prod, estoque_prod)
                print(f"Produto {nome_prod} adicionado com sucesso!")

            elif adm == "0":
                break

    elif opc == "0":
        print("Encerrando sistema...")
        break
