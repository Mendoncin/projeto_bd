import streamlit as st
import sqlite3
from template import *  

def conectar_banco():
    return sqlite3.connect("database.db")

def executar_consulta(query, params=None):
    conn = conectar_banco()
    cursor = conn.cursor()

    if isinstance(query, str):
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        resultados = cursor.fetchall()
        conn.commit()
    else:
        resultados = query  

    conn.close()
    return resultados

st.set_page_config(page_title="Consultas", layout="centered")

st.title("Consultas ao Banco de Dados")

consultas = {
    'Listar todos os hospitais': {"func": Listar_hospitais, "param": None},
    'Listar todos os médicos': {"func": Listar_medicos, "param": None},
    'Listar todos os pacientes': {"func": Listar_pacientes, "param": None},
    'LIstar todos os medicamentos': {"func": Listar_medicamentos, "param": None},
    'LIstar todas as consultas': {"func": Listar_consultas, "param": None},
    'LIstar todos os abastecimentos': {"func": Listar_abastecimentos, "param": None},
    'LIstar todas as farmácias': {"func": Listar_farmacias, "param": None},
    'LIstar todas os laboratórios': {"func": Listar_laboratorios, "param": None},
    'LIstar todas as prescrições': {"func": Listar_prescricoes, "param": None},
    'Inserir novo hospital': {"func": Inserir_hospital, "param": ["ID", "nome", "endereço", "especialidades"]},
    'Inserir novo paciente': {"func": Inserir_paciente, "param": ["ID", "nome", "nascimento", "endereço", "historico"]},
    'Inserir novo médico': {"func": Inserir_medico, "param": ["crm", "nome", "especialidade", "contato"]},
    'Inserir novo medicamento': {"func": Inserir_medicamento, "param": ["ID", "nome", "fabricante", 'indicacoes', "contraindicacoes"]},
    'Inserir nova consulta': {"func": Inserir_consulta, "param": ["ID", "data", "horario", 'local', "diagnostico", 'IDpaciente', 'CRM', 'IDhospital']},
    'Remover paciente': {"func": Remover_paciente, "param": ["IDpaciente"]},
    'Listar todos os médicos de um hospital específico': {"func": Listar_medicos_hospital, "param": "ID_Hospital"},
    'Listar medicamentos disponíveis em uma farmácia específica': {"func": Listar_medicamentos_farmacia, "param": "CNPJ_Farmácia"},
    'Listar todos os médicos por especialidade': {"func": Listar_medicos_por_especialidade, "param": "especialidade"},
    'Listar todos os pacientes que passaram por consultas em um hospital específico': {"func": Consultar_pacientes_consultas_em_hospital, "param": "ID_Hospital"},
    'Listar todos os medicamentos prescritos para um paciente específico': {"func": Consultar_medicamentos_um_paciente, "param": "id_paciente"},
    'Listar farmácias que vendem um medicamento específico': {"func": Listar_farmacias_remedio_especifico, "param": "ID_remedio"},
    "Listar todos os hospitais com suas especialidades": {"func": Listar_hospitais_especialidades, "param": None}, 
    "Listar médicos com sua especialidade": {"func": Listar_medicos_especialidade, "param": None},
    "Listar as consultas de um paciente específico": {"func": Consultar_consultas_paciente, "param": "id_paciente"},
    "Listar as consultas de um médico específico": {"func": Consultar_consultas_medico, "param": "CRM"},
    "Listar as consultas de um hospital específico": {"func": Consultar_consultas_hospital, "param": "ID_Hospital"},
    'Listar as prescrições associadas a uma consulta específica': {"func": Consultar_prescricoes_consulta, "param": "ID_Consulta"},
}


escolha = st.selectbox("Escolha uma consulta:", ["Selecione..."] + list(consultas.keys()))

if escolha != "Selecione...":
    info_consulta = consultas[escolha]
    parametro_nome = info_consulta["param"]

    if escolha == "Inserir novo hospital":
        id_hospital = st.text_input("Digite o ID do hospital:")
        nome_hospital = st.text_input("Digite o nome do hospital:")
        endereco_hospital = st.text_input("Digite o endereço do hospital:")
        especialidades_hospital = st.text_input("Digite as especialidades do hospital (separadas por vírgula):")

        if st.button("Inserir Hospital"):
            if not id_hospital.isdigit():
                st.warning("O ID do hospital deve ser um número válido.")
            elif not nome_hospital.strip() or not endereco_hospital.strip() or not especialidades_hospital.strip():
                st.warning("Por favor, preencha todos os campos corretamente.")
            else:
                resultado = Inserir_hospital(int(id_hospital), nome_hospital, endereco_hospital, especialidades_hospital)
                st.success("Hospital inserido com sucesso!")

    elif escolha == "Inserir novo paciente":
        id_paciente = st.text_input("Digite o ID do paciente:")
        nome_paciente = st.text_input("Digite o nome do paciente:")
        nascimento_paciente = st.text_input("Digite a data de nascimento (YYYY-MM-DD):")
        endereco_paciente = st.text_input("Digite o endereço do paciente:")
        historico_paciente = st.text_area("Digite o histórico médico do paciente:")

        if st.button("Inserir Paciente"):
            if not id_paciente.isdigit():
                st.warning("O ID do paciente deve ser um número válido.")
            elif not nome_paciente.strip() or not nascimento_paciente.strip() or not endereco_paciente.strip() or not historico_paciente.strip():
                st.warning("Por favor, preencha todos os campos corretamente.")
            else:
                resultado = Inserir_paciente(int(id_paciente), nome_paciente, nascimento_paciente, endereco_paciente, historico_paciente)
                st.success("Paciente inserido com sucesso!")

    elif escolha == "Inserir novo médico":
        crm_medico = st.text_input("Digite o CRM do médico:")
        nome_medico = st.text_input("Digite o nome do médico:")
        especialidade_medico = st.text_input("Digite a especialidade do médico:")
        contato_medico = st.text_input("Digite o contato do médico:")

        if st.button("Inserir Médico"):
            if not crm_medico.isdigit():
                st.warning("O CRM deve ser um número válido.")
            elif not nome_medico.strip() or not especialidade_medico.strip() or not contato_medico.strip():
                st.warning("Por favor, preencha todos os campos corretamente.")
            else:
                resultado = Inserir_medico(int(crm_medico), nome_medico, especialidade_medico, contato_medico)
                st.success("Médico inserido com sucesso!")
    
    elif escolha == "Inserir novo medicamento":
        id_medicamento = st.text_input("Digite o ID do medicamento:")
        nome_medicamento = st.text_input("Digite o nome do medicamento:")
        fabricante_medicamento = st.text_input("Digite o fabricante do medicamento:")
        indicacoes_medicamento = st.text_area("Digite as indicações do medicamento:")
        contraindicacoes_medicamento = st.text_area("Digite as contraindicações do medicamento:")

        if st.button("Inserir Medicamento"):
            if not id_medicamento.isdigit():
                st.warning("O ID do medicamento deve ser um número válido.")
            elif not nome_medicamento.strip() or not fabricante_medicamento.strip() or not indicacoes_medicamento.strip() or not contraindicacoes_medicamento.strip():
                st.warning("Por favor, preencha todos os campos corretamente.")
            else:
                resultado = Inserir_medicamento(int(id_medicamento), nome_medicamento, fabricante_medicamento, indicacoes_medicamento, contraindicacoes_medicamento)
                st.success("Medicamento inserido com sucesso!")

    elif escolha == "Inserir nova consulta":
        id_consulta = st.text_input("Digite o ID da consulta:")
        data_consulta = st.text_input("Digite a data da consulta (YYYY-MM-DD):")
        horario_consulta = st.text_input("Digite o horário da consulta (HH:MM):")
        local_consulta = st.text_input("Digite o local da consulta:")
        diagnostico_consulta = st.text_area("Digite o diagnóstico da consulta:")
        id_paciente = st.text_input("Digite o ID do paciente:")
        crm_medico = st.text_input("Digite o CRM do médico:")
        id_hospital = st.text_input("Digite o ID do hospital:")

        if st.button("Inserir Consulta"):
            if not (id_consulta.isdigit() and id_paciente.isdigit() and crm_medico.isdigit() and id_hospital.isdigit()):
                st.warning("IDs e CRM devem ser números válidos.")
            elif not data_consulta.strip() or not horario_consulta.strip() or not local_consulta.strip() or not diagnostico_consulta.strip():
                st.warning("Por favor, preencha todos os campos corretamente.")
            else:
                resultado = Inserir_consulta(int(id_consulta), data_consulta, horario_consulta, local_consulta, diagnostico_consulta, int(id_paciente), int(crm_medico), int(id_hospital))
                st.success("Consulta inserida com sucesso!")

    else:
        parametro = None  
        if parametro_nome:  
            entrada_parametro = st.text_input(f"Digite o valor para {parametro_nome}:")
            if entrada_parametro.strip():  
                if parametro_nome in ["id_paciente", 'CRM', 'ID_Hospital', 'ID_Consulta', 'ID_remedio']:
                    try:
                        parametro = int(entrada_parametro)
                    except ValueError:
                        st.warning(f"Por favor, insira um número válido para {parametro_nome}.")
                        parametro = None
                else:
                    parametro = entrada_parametro  

        if parametro is not None or parametro_nome is None:
            query_func = consultas[escolha]["func"]
            query = query_func(parametro) if parametro is not None else query_func()
            resultados = executar_consulta(query)

            st.write("### Resultados")
            if resultados:
                if isinstance(resultados[0], tuple):
                    colunas = [f"coluna_{i}" for i in range(len(resultados[0]))]
                    dados_corrigidos = {coluna: [] for coluna in colunas}

                    for linha in resultados:
                        for i, valor in enumerate(linha):
                            dados_corrigidos[f"coluna_{i}"].append(valor)

                elif hasattr(resultados[0], "__table__"):
                    colunas = [c.name for c in resultados[0].__table__.columns]
                    dados_corrigidos = {coluna: [] for coluna in colunas}

                    for obj in resultados:
                        for coluna in colunas:
                            dados_corrigidos[coluna].append(getattr(obj, coluna))

                else:
                    colunas = resultados[0]._fields
                    dados_corrigidos = {coluna: [] for coluna in colunas}

                    for row in resultados:
                        for coluna in colunas:
                            dados_corrigidos[coluna].append(getattr(row, coluna))

                st.table(dados_corrigidos)


            else:
                st.warning("Nenhum resultado encontrado.")