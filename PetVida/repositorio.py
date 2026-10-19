
import pyodbc
from PetVida.db import conectar, transacao

# TRATAMENTO DE ERROS


def tratar_erro(erro):
    mensagem = str(erro).lower()

    if isinstance(erro, pyodbc.IntegrityError):
        if "2627" in mensagem or "2601" in mensagem:
            return ValueError(
                "Já existe um registro com esses dados únicos "
                "(CPF ou item repetido)."
            )

        if "foreign key" in mensagem or "reference constraint" in mensagem:
            return ValueError(
                "Operação impedida: existem registros relacionados "
                "ou um ID não existe."
            )

        if "check constraint" in mensagem:
            return ValueError(
                "Valor inválido para uma regra do banco "
                "(espécie, peso, status ou quantidade)."
            )

        return ValueError(
            "O banco rejeitou os dados informados."
        )

    if isinstance(erro, pyodbc.OperationalError):
        return ConnectionError(
            "Problema na comunicação com o SQL Server."
        )

    return RuntimeError(
        "Erro ao executar um comando no banco de dados."
    )



# CRUD DE TUTORES


def criar_tutor(nome, cpf, email=None, telefone=None):
    if (
        not isinstance(cpf, str)
        or len(cpf) != 11
        or not cpf.isascii()
        or not cpf.isdigit()
    ):
        raise ValueError(
            "O CPF precisa ter exatamente 11 dígitos numéricos."
        )

    try:
        with transacao() as cursor:
            cursor.execute("""
                INSERT INTO dbo.tutor (nome, cpf, email, telefone)
                OUTPUT INSERTED.id_tutor
                VALUES (?, ?, ?, ?)
            """, (nome, cpf, email, telefone))

            return cursor.fetchone()[0]

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def buscar_tutor(id_tutor):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_tutor, nome, cpf, email, telefone
            FROM dbo.tutor
            WHERE id_tutor = ?
        """, (id_tutor,))

        return cursor.fetchone()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


def listar_tutores(filtro_nome=None):
    conn = conectar()

    try:
        cursor = conn.cursor()

        if filtro_nome:
            cursor.execute("""
                SELECT id_tutor, nome, cpf, email, telefone
                FROM dbo.tutor
                WHERE nome LIKE ?
            """, (f"%{filtro_nome}%",))

        else:
            cursor.execute("""
                SELECT id_tutor, nome, cpf, email, telefone
                FROM dbo.tutor
            """)

        return cursor.fetchall()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


def atualizar_tutor(id_tutor, **campos):
    permitidos = ["nome", "email", "telefone"]

    if not campos:
        raise ValueError(
            "Informe ao menos um campo para atualizar."
        )

    for campo in campos:
        if campo not in permitidos:
            raise ValueError(
                f"Campo não permitido: {campo}"
            )

    atualizacoes = []
    valores = []

    for campo, valor in campos.items():
        atualizacoes.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_tutor)

    query = f"""
        UPDATE dbo.tutor
        SET {', '.join(atualizacoes)}
        WHERE id_tutor = ?
    """

    try:
        with transacao() as cursor:
            cursor.execute(query, valores)
            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def excluir_tutor(id_tutor):
    try:
        with transacao() as cursor:
            cursor.execute("""
                DELETE FROM dbo.tutor
                WHERE id_tutor = ?
            """, (id_tutor,))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro



#  TUTOR E PET 


def criar_pet(
    id_tutor,
    nome,
    especie,
    raca=None,
    data_nascimento=None,
    peso_kg=None
):
    try:
        with transacao() as cursor:
            cursor.execute("""
                INSERT INTO dbo.pet
                    (id_tutor, nome, especie, raca,
                     data_nascimento, peso_kg)
                OUTPUT INSERTED.id_pet
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                id_tutor, nome, especie, raca,
                data_nascimento, peso_kg
            ))

            return cursor.fetchone()[0]

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def atualizar_peso_pet(id_pet, peso_kg):
    try:
        with transacao() as cursor:
            cursor.execute("""
                UPDATE dbo.pet
                SET peso_kg = ?
                WHERE id_pet = ?
            """, (peso_kg, id_pet))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def transferir_pet(id_pet, novo_id_tutor):
    try:
        with transacao() as cursor:
            cursor.execute("""
                UPDATE dbo.pet
                SET id_tutor = ?
                WHERE id_pet = ?
            """, (novo_id_tutor, id_pet))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def excluir_pet(id_pet):
    try:
        with transacao() as cursor:
            cursor.execute("""
                DELETE FROM dbo.pet
                WHERE id_pet = ?
            """, (id_pet,))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def listar_pets_do_tutor(id_tutor):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_pet, nome, especie, raca,
                   data_nascimento, peso_kg
            FROM dbo.pet
            WHERE id_tutor = ?
        """, (id_tutor,))

        return cursor.fetchall()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


def buscar_pet_com_tutor(id_pet):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.id_pet,
                p.nome AS pet,
                p.especie,
                t.id_tutor,
                t.nome AS tutor,
                t.telefone
            FROM dbo.pet AS p
            JOIN dbo.tutor AS t
                ON t.id_tutor = p.id_tutor
            WHERE p.id_pet = ?
        """, (id_pet,))

        return cursor.fetchone()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


# CONSULTAS E PROCEDIMENTOS 

def agendar_consulta(
    id_pet,
    id_vet,
    data_hora,
    motivo,
    procedimentos
):

    try:
        with transacao() as cursor:

            cursor.execute("""
                INSERT INTO dbo.consulta
                    (id_pet, id_veterinario, data_hora, motivo)
                OUTPUT INSERTED.id_consulta
                VALUES (?, ?, ?, ?)
            """, (id_pet, id_vet, data_hora, motivo))

            id_consulta = cursor.fetchone()[0]

            for id_procedimento, quantidade in procedimentos:
                if not isinstance(quantidade, int) or quantidade <= 0:
                    raise ValueError(
                        "Quantidade deve ser um inteiro maior que zero."
                    )

                cursor.execute("""
                    SELECT preco_base
                    FROM dbo.procedimento
                    WHERE id_procedimento = ?
                """, (id_procedimento,))

                linha = cursor.fetchone()

                if linha is None:
                    raise ValueError(
                        f"Procedimento {id_procedimento} não existe."
                    )

                cursor.execute("""
                    INSERT INTO dbo.consulta_procedimento
                        (id_consulta, id_procedimento,
                         quantidade, valor_cobrado)
                    VALUES (?, ?, ?, ?)
                """, (
                    id_consulta, id_procedimento,
                    quantidade, linha[0]
                ))

            return id_consulta

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def adicionar_procedimento(
    id_consulta,
    id_procedimento,
    quantidade=1
):
    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError(
            "Quantidade deve ser um inteiro maior que zero."
        )

    try:
        with transacao() as cursor:

            cursor.execute("""
                SELECT status
                FROM dbo.consulta
                WHERE id_consulta = ?
            """, (id_consulta,))

            consulta = cursor.fetchone()

            if consulta is None:
                raise ValueError(
                    "Consulta não encontrada."
                )

            if consulta[0] == "CANCELADA":
                raise ValueError(
                    "Consulta cancelada não aceita procedimentos."
                )

            cursor.execute("""
                SELECT preco_base
                FROM dbo.procedimento
                WHERE id_procedimento = ?
            """, (id_procedimento,))

            procedimento = cursor.fetchone()

            if procedimento is None:
                raise ValueError(
                    "Procedimento não encontrado."
                )

            cursor.execute("""
                INSERT INTO dbo.consulta_procedimento
                    (id_consulta, id_procedimento,
                     quantidade, valor_cobrado)
                VALUES (?, ?, ?, ?)
            """, (
                id_consulta, id_procedimento,
                quantidade, procedimento[0]
            ))

            return True

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def remover_procedimento(id_consulta, id_procedimento):
    try:
        with transacao() as cursor:

            cursor.execute("""
                SELECT status
                FROM dbo.consulta
                WHERE id_consulta = ?
            """, (id_consulta,))

            consulta = cursor.fetchone()

            if consulta is None:
                raise ValueError(
                    "Consulta não encontrada."
                )

            if consulta[0] == "CANCELADA":
                raise ValueError(
                    "Consulta cancelada não pode ser alterada."
                )

            cursor.execute("""
                DELETE FROM dbo.consulta_procedimento
                WHERE id_consulta = ?
                  AND id_procedimento = ?
            """, (id_consulta, id_procedimento))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def listar_procedimentos_da_consulta(id_consulta):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.id_procedimento,
                p.descricao,
                cp.quantidade,
                cp.valor_cobrado,
                cp.quantidade * cp.valor_cobrado AS subtotal
            FROM dbo.consulta_procedimento AS cp
            JOIN dbo.procedimento AS p
                ON p.id_procedimento = cp.id_procedimento
            WHERE cp.id_consulta = ?
        """, (id_consulta,))

        return cursor.fetchall()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


def listar_consultas_por_procedimento(id_procedimento):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.id_consulta,
                c.data_hora,
                c.status,
                p.nome AS pet,
                cp.quantidade,
                cp.valor_cobrado
            FROM dbo.consulta_procedimento AS cp
            JOIN dbo.consulta AS c
                ON c.id_consulta = cp.id_consulta
            JOIN dbo.pet AS p
                ON p.id_pet = c.id_pet
            WHERE cp.id_procedimento = ?
        """, (id_procedimento,))

        return cursor.fetchall()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


def total_da_consulta(id_consulta):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ISNULL(
                SUM(quantidade * valor_cobrado), 0
            )
            FROM dbo.consulta_procedimento
            WHERE id_consulta = ?
        """, (id_consulta,))

        return cursor.fetchone()[0]

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()


def atualizar_status_consulta(id_consulta, status):
    if status not in (
        "AGENDADA", "REALIZADA", "CANCELADA"
    ):
        raise ValueError("Status inválido.")

    try:
        with transacao() as cursor:
            cursor.execute("""
                UPDATE dbo.consulta
                SET status = ?
                WHERE id_consulta = ?
            """, (status, id_consulta))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


def excluir_consulta(id_consulta):
    try:
        with transacao() as cursor:
            cursor.execute("""
                DELETE FROM dbo.consulta
                WHERE id_consulta = ?
            """, (id_consulta,))

            return cursor.rowcount > 0

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro


# HISTÓRICO DO PET

def historico_do_pet(id_pet):
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                v.id_consulta,
                v.data_hora,
                v.status,
                v.pet,
                v.tutor,
                v.veterinario,
                v.qtd_itens,
                v.valor_total
            FROM dbo.vw_resumo_consulta AS v
            JOIN dbo.consulta AS c
                ON c.id_consulta = v.id_consulta
            WHERE c.id_pet = ?
            ORDER BY v.data_hora
        """, (id_pet,))

        return cursor.fetchall()

    except pyodbc.Error as erro:
        raise tratar_erro(erro) from erro

    finally:
        conn.close()
