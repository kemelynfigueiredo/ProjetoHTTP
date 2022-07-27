from flask import Flask, request, jsonify
import sqlite3
import logging
from flask_json_schema import JsonSchema, JsonValidationError

app = Flask(__name__)
schema = JsonSchema(app)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("projetohtml.log")

handler.setFormatter(formatter)
logger = app.logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

curso_schema = {
    'required': ['nome'],
    'properties': {
        'nome': {
            'type': 'string'
        },
    }
}

aluno_schema = {
    'required': ['nome', 'matricula', 'cpf', 'nascimento', 'fk_id_curso'],
    'properties': {
        'nome': {
            'type': 'string'
        },
        'matricula': {
            'type': 'string'
        },
        'cpf': {
            'type': 'string'
        },
        'nascimento': {
            'type': 'string'
        },
        'fk_id_curso': {
            'type': 'string'
        }
    }
}


@app.route("/cursos", methods=['GET'])
def getCursos():

    logger.info("Listando cursos.")
    try:
        conn = sqlite3.connect('ProjetoHTTP.db')
        cursor = conn.cursor()

        cursor.execute("""
                select * from tb_curso;
        """)
        curso = []

        for linha in cursor.fetchall():

            curso.append(dict_factory(linha, cursor))

        conn.close()

    except (sqlite3.Error):
        logger.error("Aconteceu um erro.")
        logger.error(sqlite3.Error)

    return (jsonify(curso))


@app.route("/curso/<int:id>", methods=['GET'])
def getCursoById(id):

    logger.info("Listando curso pelo seu Id.")
    try:
        conn = sqlite3.connect('ProjetoHTTP.db')

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM tb_curso WHERE id_curso = ?;
        """, (id))

        linha = cursor.fetchone()
        curso = []
        curso.append(dict_factory(linha, cursor))

        conn.close()
    except (sqlite3.Error):
        logger.error("Ops, aconteceu um erro.")
        logger.error(sqlite3.Error)

    return (jsonify(curso))


@app.route("/curso", methods=['POST'])
@schema.validate(curso_schema)
def setCurso():

    logger.info("Buscando dados do curso.")

    cursoJson = request.get_json()
    nome = cursoJson['nome']

    try:
        conn = sqlite3.connect('ProjetoHTTP.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tb_curso(nome)
            VALUES(?);
        """, (nome))
        conn.commit()
        conn.close()

    except (sqlite3.Error):
        logger.error("Ops,aconteceu um erro.")
        logger.error(sqlite3.Error)

    id = cursor.lastrowid
    cursoJson["id_curso"] = id

    return jsonify(cursoJson)


@app.route("/cursos/<int:id>", methods=['PUT'])
def updateCurso():

    logger.info("Atualizando dados do curso.")

    cursoJson = request.get_json()
    nome = cursoJson['nome']
    curso = Curso(nome)
    try:
        conn = sqlite3.connect('ProjetoHTTP.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tb_curso WHERE id_curso = ?;
        """, (id, ))

        data = cursor.fetchone()

        if data is not None:

            cursor.execute(
                """
              UPDATE tb_curso SET nome=? WHERE id_curso=?;
            """, (nome))

            conn.commit()

        else:

            cursor.execute(
                """
                INSERT INTO tb_curso(nome)
                VALUES(?)
            """, (nome, ))

            conn.commit()
            id = cursor.lastrowid
            curso['id_curso'] = id

        conn.close()
    except (sqlite3.Error):
        logger.error("Ops, Aconteceu um erro.")
        logger.error(sqlite3.Error)

    return (jsonify(cursoJson))


@app.route("/alunos", methods=['GET'])
def getAlunos():

    logger.info("Listando alunos.")
    try:
        conn = sqlite3.connect('ProjetoHTTP.db')
        cursor = conn.cursor()

        cursor.execute("""
                select * from tb_aluno;
        """)
        aluno = []

        for linha in cursor.fetchall():

            aluno.append(dict_factory(linha, cursor))

        conn.close()

    except (sqlite3.Error):
        logger.error("Aconteceu um erro.")
        logger.error(sqlite3.Error)

    return (jsonify(aluno))


@app.route("/aluno/<int:id>", methods=['GET'])
def getAlunoById(id):

    logger.info("Listando aluno pelo seu Id.")
    try:
        conn = sqlite3.connect('ProjetoHTTP.db')

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM tb_aluno WHERE id_aluno = ?;
        """, (id, ))

        linha = cursor.fetchone()
        aluno = []
        aluno.append(dict_factory(linha, cursor))

        conn.close()
    except (sqlite3.Error):
        logger.error("Ops, aconteceu um erro.")
        logger.error(sqlite3.Error)

    return (jsonify(aluno))


@app.route("/aluno", methods=['POST'])
@schema.validate(aluno_schema)
def setAluno():

    logger.info("Buscando dados do aluno.")

    alunoJson = request.get_json()
    nome = alunoJson['nome']
    matricula = alunoJson['matricula']
    cpf = alunoJson['cpf']
    nascimento = alunoJson['nascimento']
    fk_id_curso = alunoJson['fk_id_curso']

    try:
        conn = sqlite3.connect('ProjetoHTTP.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tb_aluno(nome, matricula, cpf, nascimento, fk_id_curso)
            VALUES(?,?,?,?,?);
        """, (nome, matricula, cpf, nascimento, fk_id_curso))
        conn.commit()
        conn.close()

    except (sqlite3.Error):
        logger.error("Ops,aconteceu um erro.")
        logger.error(sqlite3.Error)

    id = cursor.lastrowid
    alunoJson["id_aluno"] = id

    return jsonify(alunoJson)


@app.route("/alunos/<int:id>", methods=['PUT'])
def updateAluno():

    logger.info("Atualizando dados do aluno.")

    alunoJson = request.get_json()
    nome = alunoJson['nome']
    matricula = alunoJson['matricula']
    cpf = alunoJson['cpf']
    nascimento = alunoJson['nascimento']
    fk_id_curso = alunoJson['fk_id_curso']
    try:
        conn = sqlite3.connect('ProjetoHTTP.db')
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tb_aluno WHERE id_aluno = ?;
        """, (id, ))

        data = cursor.fetchone()

        if data is not None:

            cursor.execute(
                """
                UPDATE tb_aluno SET nome=?, matricula=?, cpf=?, nascimento=?, fk_id_curso WHERE id_aluno=?;
            """, (nome, matricula, cpf, nascimento, fk_id_curso, id))

            conn.commit()

        else:

            cursor.execute(
                """
            
                INSERT INTO tb_aluno (nome, matricula, cpf, nascimento, fk_id_curso)
                VALUES(?,?,?,?,?)
            """, (nome, matricula, cpf, nascimento, fk_id_curso))

            conn.commit()
            id = cursor.lastrowid
            alunoJson['id_aluno'] = id

        conn.close()
    except (sqlite3.Error):
        logger.error("Ops, Aconteceu um erro.")
        logger.error(sqlite3.Error)

    return (jsonify(alunoJson))


def dict_factory(linha, cursor):
    dicionario = {}
    for idx, col in enumerate(cursor.description):
        dicionario[col[0]] = linha[idx]
    return dicionario


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({
        'error':
        e.message,
        'errors': [validation_error.message for validation_error in e.errors]
    })

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
