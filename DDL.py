import sqlite3

conn = sqlite3.connect('ProjetoHTTP.db')

cursor = conn.cursor()

cursor.execute("""
    create table tb_curso(
        id_curso integer primary key autoincrement not null,
        nome varchar(45) not null
        );
""")
print ("Tabela tb_curso criada com sucesso")

cursor.execute("""
    create table tb_aluno(
        id_aluno integer primary key  autoincrement not null,
        nome varchar(45) not null,
        matricula varchar(12) not null,
        cpf varchar(11) not null,
        nascimento date not null,
        fk_id_curso integer not null
        );
""")
print ("Tabela tb_aluno criada com sucesso")

