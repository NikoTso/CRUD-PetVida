
from db import testar_conexao

from repositorio import (
    criar_tutor,
    buscar_tutor,
    listar_tutores,
    atualizar_tutor,
    excluir_tutor,
    criar_pet,
    listar_pets_do_tutor,
    buscar_pet_com_tutor,
    atualizar_peso_pet,
    transferir_pet,
    excluir_pet,
    agendar_consulta,
    adicionar_procedimento,
    remover_procedimento,
    listar_procedimentos_da_consulta,
    listar_consultas_por_procedimento,
    total_da_consulta,
    atualizar_status_consulta,
    excluir_consulta,
    historico_do_pet
)


def mostrar_resultados(resultados):
    if not resultados:
        print("Nenhum registro encontrado.")
    else:
        for resultado in resultados:
            print(resultado)


def menu():
    while True:
        print("\n========== PETVIDA ==========")
        print("1  - Testar conexão")
        print("2  - Listar tutores")
        print("3  - Buscar tutor")
        print("4  - Cadastrar tutor")
        print("5  - Atualizar tutor")
        print("6  - Excluir tutor")
        print("7  - Listar pets de um tutor")
        print("8  - Buscar pet com tutor")
        print("9  - Cadastrar pet")
        print("10 - Atualizar peso do pet")
        print("11 - Transferir pet")
        print("12 - Excluir pet")
        print("13 - Agendar consulta")
        print("14 - Adicionar procedimento")
        print("15 - Remover procedimento")
        print("16 - Listar procedimentos da consulta")
        print("17 - Listar consultas por procedimento")
        print("18 - Total da consulta")
        print("19 - Atualizar status da consulta")
        print("20 - Excluir consulta")
        print("21 - Histórico do pet")
        print("0  - Sair")
        print("=============================")

        opcao = input("Escolha uma opção: ")

        try:
            if opcao == "1":
                print(testar_conexao())

            elif opcao == "2":
                nome = input("Filtrar por nome (Enter para todos): ")
                mostrar_resultados(listar_tutores(nome or None))

            elif opcao == "3":
                id_tutor = int(input("ID do tutor: "))
                print(buscar_tutor(id_tutor))

            elif opcao == "4":
                nome = input("Nome: ")
                cpf = input("CPF: ")
                email = input("Email: ") or None
                telefone = input("Telefone: ") or None

                id_tutor = criar_tutor(
                    nome, cpf, email, telefone
                )

                print("Tutor cadastrado! ID:", id_tutor)

            elif opcao == "5":
                id_tutor = int(input("ID do tutor: "))
                campo = input(
                    "Campo (nome, email ou telefone): "
                )
                valor = input("Novo valor: ")

                resultado = atualizar_tutor(
                    id_tutor, **{campo: valor}
                )

                print("Atualizado:", resultado)

            elif opcao == "6":
                id_tutor = int(input("ID do tutor: "))
                confirmar = input("Confirmar exclusão? (s/n): ")

                if confirmar.lower() == "s":
                    print("Excluído:", excluir_tutor(id_tutor))

            elif opcao == "7":
                id_tutor = int(input("ID do tutor: "))
                mostrar_resultados(
                    listar_pets_do_tutor(id_tutor)
                )

            elif opcao == "8":
                id_pet = int(input("ID do pet: "))
                print(buscar_pet_com_tutor(id_pet))

            elif opcao == "9":
                id_tutor = int(input("ID do tutor: "))
                nome = input("Nome do pet: ")
                especie = input("Espécie: ")
                raca = input("Raça: ") or None

                id_pet = criar_pet(
                    id_tutor, nome, especie, raca
                )

                print("Pet cadastrado! ID:", id_pet)

            elif opcao == "10":
                id_pet = int(input("ID do pet: "))
                peso = float(input("Novo peso: "))
                print("Atualizado:", atualizar_peso_pet(id_pet, peso))

            elif opcao == "11":
                id_pet = int(input("ID do pet: "))
                id_tutor = int(input("ID do novo tutor: "))

                print(
                    "Transferido:",
                    transferir_pet(id_pet, id_tutor)
                )

            elif opcao == "12":
                id_pet = int(input("ID do pet: "))
                confirmar = input("Confirmar exclusão? (s/n): ")

                if confirmar.lower() == "s":
                    print("Excluído:", excluir_pet(id_pet))

            elif opcao == "13":
                id_pet = int(input("ID do pet: "))
                id_vet = int(input("ID do veterinário: "))
                data = input("Data e hora (AAAA-MM-DD HH:MM): ")
                motivo = input("Motivo: ")

                procedimentos = []

                while True:
                    id_proc = int(
                        input("ID do procedimento (0 para terminar): ")
                    )

                    if id_proc == 0:
                        break

                    quantidade = int(input("Quantidade: "))
                    procedimentos.append((id_proc, quantidade))

                id_consulta = agendar_consulta(
                    id_pet, id_vet, data, motivo, procedimentos
                )

                print("Consulta agendada! ID:", id_consulta)

            elif opcao == "14":
                id_consulta = int(input("ID da consulta: "))
                id_proc = int(input("ID do procedimento: "))
                quantidade = int(input("Quantidade: "))

                print(
                    "Adicionado:",
                    adicionar_procedimento(
                        id_consulta, id_proc, quantidade
                    )
                )

            elif opcao == "15":
                id_consulta = int(input("ID da consulta: "))
                id_proc = int(input("ID do procedimento: "))

                print(
                    "Removido:",
                    remover_procedimento(id_consulta, id_proc)
                )

            elif opcao == "16":
                id_consulta = int(input("ID da consulta: "))
                mostrar_resultados(
                    listar_procedimentos_da_consulta(id_consulta)
                )

            elif opcao == "17":
                id_proc = int(input("ID do procedimento: "))
                mostrar_resultados(
                    listar_consultas_por_procedimento(id_proc)
                )

            elif opcao == "18":
                id_consulta = int(input("ID da consulta: "))
                print(
                    "Total: R$",
                    total_da_consulta(id_consulta)
                )

            elif opcao == "19":
                id_consulta = int(input("ID da consulta: "))
                status = input(
                    "Status (AGENDADA, REALIZADA ou CANCELADA): "
                )

                print(
                    "Atualizado:",
                    atualizar_status_consulta(id_consulta, status)
                )

            elif opcao == "20":
                id_consulta = int(input("ID da consulta: "))
                confirmar = input("Confirmar exclusão? (s/n): ")

                if confirmar.lower() == "s":
                    print(
                        "Excluída:",
                        excluir_consulta(id_consulta)
                    )

            elif opcao == "21":
                id_pet = int(input("ID do pet: "))
                mostrar_resultados(historico_do_pet(id_pet))

            elif opcao == "0":
                print("Encerrando PetVida...")
                break

            else:
                print("Opção inválida.")

        except Exception as erro:
            print("Erro:", erro)


if __name__ == "__main__":
    menu()
