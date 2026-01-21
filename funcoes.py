import sqlite3 as lite
import pandas as pd
import numpy as np

def conecta_bd():
    return lite.connect("loja_tech.db")

def SalvaUsers(nome, email, endereco):
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, email, endereco) VALUES (?,?,?)",
            (nome, email, endereco)
        )
        con.commit()
        print("Cliente salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar cliente: {e}")
    finally:
        con.close()

def listarClientes():
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM clientes")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar clientes: {e}")
        return []
    finally:
        con.close()

def AttCli(id, nome, email, endereco):
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute(
            "UPDATE clientes SET nome = ?, email = ?, endereco = ? WHERE id = ?",
            (nome, email, endereco, id)
        )
        con.commit()
        print("Cliente atualizado!")
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")
    finally:
        con.close()

def AddProd(nome, preco, estoque):
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, preco, estoque) VALUES (?,?,?)",
            (nome, preco, estoque)
        )
        con.commit()
        print("Produto adicionado!")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
    finally:
        con.close()

def Listarprodutos():
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []
    finally:
        con.close()

def AttProd(idProd, nome, valor):
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = ?, preco = ? WHERE id = ?",
            (nome, valor, idProd)
        )
        con.commit()
        print("Produto atualizado!")
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        con.close()

def SalvaCarrinho(carrinho, nome):
    try:
        if not carrinho:
            print("Carrinho vazio. Nada para salvar.")
            return

        con = conecta_bd()
        dados = []

        for item in carrinho:
            dados.append({
                "nome": nome,
                "produto": item["nome"],
                "quantidade": item["quantidade"],
                "preco": item["preco"],
                "subtotal": item["quantidade"] * item["preco"]
            })

        df = pd.DataFrame(dados)
        df.to_sql("pedidos", con, if_exists="append", index=False)
        con.commit()
        print("Carrinho salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar carrinho: {e}")
    finally:
        con.close()

def ListasPedidos():
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM pedidos")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar pedidos: {e}")
        return []
    finally:
        con.close()

def ListasPedidos_produtos():
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM pedidos_produtos")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar pedidos_produtos: {e}")
        return []
    finally:
        con.close()

def Remove(id, tabela):
    try:
        con = conecta_bd()
        cursor = con.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (id,))
        con.commit()
        print("Registro removido!")
    except Exception as e:
        print(f"Erro ao remover registro: {e}")
    finally:
        con.close()


