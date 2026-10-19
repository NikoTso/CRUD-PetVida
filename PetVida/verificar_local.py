
from PetVida.db import testar_conexao

from PetVida.repositorio import (
    buscar_tutor,
    listar_tutores,
    listar_pets_do_tutor,
    buscar_pet_com_tutor,
    listar_procedimentos_da_consulta,
    listar_consultas_por_procedimento,
    total_da_consulta,
    historico_do_pet
)


def verificar(nome, funcao):
    try:
        resultado = funcao()
        print(f"[OK] {nome}: {resultado}")

    except Exception as erro:
        print(f"[ERRO] {nome}: {erro}")


print("========== TESTES PETVIDA ==========")

verificar(
    "Conexão com SQL Server",
    lambda: testar_conexao()[:2]
)

verificar(
    "Listar tutores",
    lambda: len(listar_tutores())
)

verificar(
    "Buscar tutor",
    lambda: buscar_tutor(1)
)

verificar(
    "Pesquisar tutores por nome",
    lambda: listar_tutores("Ana")
)

verificar(
    "Listar pets de um tutor",
    lambda: listar_pets_do_tutor(1)
)

verificar(
    "Buscar pet com tutor",
    lambda: buscar_pet_com_tutor(1)
)

verificar(
    "Procedimentos da consulta",
    lambda: listar_procedimentos_da_consulta(1)
)

verificar(
    "Consultas por procedimento",
    lambda: listar_consultas_por_procedimento(1)
)

verificar(
    "Total da consulta",
    lambda: total_da_consulta(1)
)

verificar(
    "Histórico do pet",
    lambda: historico_do_pet(1)
)

print("========== FIM DOS TESTES ==========")
