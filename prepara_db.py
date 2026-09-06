import os
import re

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

load_dotenv()

print("Conectando...")
db_admin_password = os.getenv("ADMIN_SENHA")
db_user = os.getenv("SQL_USUARIO", "flask_app")
db_password = os.getenv("SQL_SENHA")
db_host = os.getenv("DB_HOST", "localhost")

if not db_admin_password or not db_password:
    raise SystemExit("Defina ADMIN_SENHA e SQL_SENHA no arquivo .env")

if not re.fullmatch(r"[A-Za-z0-9_.%-]+", db_user + db_host):
    raise SystemExit("SQL_USUARIO e DB_HOST possuem caracteres inválidos")

account = f"`{db_user}`@`{db_host}`"

try:
    conn = mysql.connector.connect(
        host=db_host,
        user="admin",
        password=db_admin_password,
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Existe algo errado no nome de usuário ou senha")
        raise SystemExit(1) from err
    print(err)
    raise

cursor = conn.cursor(dictionary=True)

cursor.execute(
    f"CREATE USER IF NOT EXISTS {account} IDENTIFIED BY %s",
    (db_password,),
)
cursor.execute(
    f"ALTER USER {account} IDENTIFIED BY %s",
    (db_password,),
)

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")
cursor.execute("CREATE DATABASE `jogoteca`;")
cursor.execute(f"GRANT ALL PRIVILEGES ON `jogoteca`.* TO {account}")
cursor.execute("FLUSH PRIVILEGES;")
cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES["Jogos"] = """
      CREATE TABLE `jogos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""

TABLES["Usuarios"] = """
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print("Criando tabela {}:".format(tabela_nome), end=" ")
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Já existe")
        else:
            print(err.msg)
    else:
        print("OK")

# inserindo usuários
usuario_sql = "INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)"
usuarios = [
    ("Laila", "dog", generate_password_hash(os.getenv("SENHA_DOG")).decode("utf-8")),
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute("select * from jogoteca.usuarios")
print(" -------------  Usuários:  -------------")
for user in cursor.fetchall():
    if isinstance(user, dict):
        print(user["nickname"])
    else:
        print(user[1])

# inserindo jogos
jogos_sql = "INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)"
jogos = [
    ("Tetris", "Puzzle", "Atari 2600"),
    ("Hollow Knight", "Metroidvania", "PS5"),
    ("God of War", "Hack n Slash", "PS2"),
    ("Mortal Kombat", "Luta", "PS2"),
    ("Valorant", "FPS", "PC"),
    ("Crash Bandicoot", "Hack n Slash", "PS2"),
    ("Need for Speed", "Corrida", "PS2"),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute("select * from jogoteca.jogos")
print(" -------------  Jogos:  -------------")
for jogo in cursor.fetchall():
    if isinstance(jogo, dict):
        print(jogo["nome"])
    else:
        print(jogo[1])

# commitando, senão nada tem efeito
conn.commit()

cursor.close()
conn.close()
