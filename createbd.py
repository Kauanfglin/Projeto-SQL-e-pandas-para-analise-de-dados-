import sqlite3

def cria_bancodados():
    con = sqlite3.connect("loja_tech.db")
    cursor = con.cursor()

    cursor.execute("DROP TABLE IF EXISTS clientes")
    cursor.execute("DROP TABLE IF EXISTS produtos")
    cursor.execute("DROP TABLE IF EXISTS pedidos")
    

    cursor.execute("""
    CREATE TABLE if not exists clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        endereco TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE if not exists produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        estoque INTEGER
    )
    """)
    
    cursor.execute("""
    INSERT INTO produtos (nome, preco, estoque) VALUES
    ('Mouse Gamer', 150.00, 10),
    ('Teclado Mecânico', 500.00, 5),
    ('Monitor', 1000.00, 3),
    ('Notebook', 3500.00, 2)
    """)
    
    cursor.execute("""
    CREATE TABLE if not exists pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        produto TEXT,
        quantidade INTEGER,
        preco REAL,
        subtotal REAL
    )
    """)

    con.commit()
    con.close()
