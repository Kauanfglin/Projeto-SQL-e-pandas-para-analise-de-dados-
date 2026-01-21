import pandas as pd 
import numpy as np

from funcoes import conecta_bd
def limpando(df):
    try:
        df_analise = df.copy()
        df_analise = df_analise.dropna()
        df_analise = df_analise.drop_duplicates()
        df_analise = df_analise.reset_index(drop=True)
        return df_analise
    except Exception as e:
        print(f"Erro na limpeza dos dados: {e}")
def conversao(df):
    try:
        df_conv = df.copy()

        if 'quantidade' in df_conv.columns:
            df_conv['quantidade'] = pd.to_numeric(df_conv['quantidade'], errors='coerce')

        if 'preco' in df_conv.columns:
            df_conv['preco'] = pd.to_numeric(df_conv['preco'], errors='coerce')

        if 'subtotal' in df_conv.columns:
            df_conv['subtotal'] = pd.to_numeric(df_conv['subtotal'], errors='coerce')

        return df_conv

    except Exception as e:
        print(f"Erro na conversão de tipos: {e}")
        return df  

def Formatacao(df):
    try:
        df_format = df.copy()

        if 'preco' in df_format.columns:
            df_format['preco'] = df_format['preco'].map('R$ {:,.2f}'.format)

        if 'subtotal' in df_format.columns:
            df_format['subtotal'] = df_format['subtotal'].map('R$ {:,.2f}'.format)

        if 'nome' in df_format.columns:
            df_format['nome'] = df_format['nome'].str.title()

        if 'produto' in df_format.columns:
            df_format['produto'] = df_format['produto'].str.title()

        return df_format

    except Exception as e:
        print(f"Erro na formatação dos dados: {e}")
        return df   

def ChamaTratamento(df):
    Resultado = limpando(df)
    Resultado = conversao(Resultado)
    Resultado = Formatacao(Resultado)
    return Resultado
 # CRIAR AS FUNCOES PARA TRATAR E VISUALIZAR OS DADOS DOS CLIENTES E PRODUTOS
 # Junção Pedido + Cliente
def aplicandomerge(df1,df2):
        try:
            con = conecta_bd()
            Pedidos = pd.read_sql_query("SELECT * FROM pedidos", con)
            Clientes = pd.read_sql_query("SELECT * FROM clientes", con)
            df_marged = pd.merge(Pedidos,Clientes, left_on='nome', right_on='nome', how='inner')  #o left é o primeiro df e o right o segundo
            return df_marged
        except Exception as e:
            print(f"Erro na junção dos dados: {e}")
        finally:
            con.close()    


def media_gastos_cliente():
    try:
        con = conecta_bd()
        pd_Pedidos = pd.read_sql_query("SELECT * FROM pedidos", con)
        pd_Clientes = pd.read_sql_query("SELECT * FROM clientes", con)
        df_merged = pd.merge(pd_Pedidos, pd_Clientes, left_on='nome', right_on='nome', how='inner')#AGORA ELAS ESTAO JUNTADAS AO POSSO AGRUDAR
        agrupamaneto = df_merged.groupby('nome')['subtotal'].mean().reset_index()
        agrupamaneto.rename(columns={'subtotal': 'media_gastos'}, inplace=True)
        return agrupamaneto
    except Exception as e:
        print(f"Erro ao calcular média de gastos por cliente: {e}")     
    finally:
        con.close()    



def faturamento_total():
    try:
        con = conecta_bd() 
        pdd = pd.read_sql_query("SELECT * FROM pedidos", con)
        tot = pdd['subtotal'].sum()
        return tot
       
    except Exception as e:
        print(f"Erro ao calcular faturamento total: {e}")     
    finally:
        con.close()