from classes_sql import *
from sqlmodel import Session, select


def Listar_hospitais_especialidades():
    with Session(engine) as session:
        esp = select(Hospital.nome, Hospital.especialidades)
        result = session.exec(esp).all()
        return result


def Listar_medicos_especialidade():
    with Session(engine) as session:
        esp = select(Medico.nome, Medico.CRM, Medico.especialidade)
        result = session.exec(esp).all()
        return result

def Consultar_consultas_paciente(identificador):
    with Session(engine) as session:
        appointment = select(Consulta).where(Consulta.pacienteID == identificador)
        result = session.exec(appointment).all()
        return result
    
def Consultar_consultas_medico(identificador):
    with Session(engine) as session:
        appointment = select(Consulta).where(Consulta.CRM == identificador)
        result = session.exec(appointment).all()
        return result

def Consultar_consultas_hospital(identificador):
    with Session(engine) as session:
        appointment = select(Consulta).where(Consulta.hospitalID == identificador)
        result = session.exec(appointment).all()
        return result

def Consultar_prescricoes_consulta(identificador):
    with Session(engine) as session:
        prescription = select(Prescricao).where(Prescricao.consultaID == identificador)
        result = session.exec(prescription).all()
        return result
    
def Listar_hospitais():
    with Session(engine) as session:
        hospital = select(Hospital)
        result = session.exec(hospital).all()
        return result

def Listar_medicos():
    with Session(engine) as session:
        medico = select(Medico)
        result = session.exec(medico).all()
        return result

def Listar_pacientes():
    with Session(engine) as session:
        paciente = select(Paciente)
        result = session.exec(paciente).all()
        return result

def Listar_medicos_hospital(IDhospital):
    with Session(engine) as session:
        relacao = select(HospitalMedico.CRM).where(HospitalMedico.hospitalID == IDhospital)
        parcial = session.exec(relacao).all()
        medico = select(Medico).where(Medico.CRM.in_(parcial))
        result = session.exec(medico).all()
        return result


def Listar_medicamentos_farmacia(CNPJ_farmacia):
    with Session(engine) as session:
        relacao = select(FarmaciaMedicamento.medicamentoID).where(FarmaciaMedicamento.CNPJ == CNPJ_farmacia)
        parcial = session.exec(relacao).all()
        medicamento = select(Medicamento).where(Medicamento.medicamentoID.in_(parcial))
        result = session.exec(medicamento).all()
        return result


def Listar_medicos_por_especialidade(speciality):
    with Session(engine) as session:
        doc = select(Medico).where(Medico.especialidade == speciality)
        result = session.exec(doc).all()
        return result

def Consultar_pacientes_consultas_em_hospital(IDhospital):
    with Session(engine) as session:
        appointment = select(Consulta.pacienteID).where(Consulta.hospitalID == IDhospital)
        parcial = session.exec(appointment).all()
        paciente = select(Paciente).where(Paciente.pacienteID.in_(parcial))
        result = session.exec(paciente).all()
        return result

def Consultar_medicamentos_um_paciente(IDpaciente):
    with Session(engine) as session:
        appointment = select(Consulta.consultaID).where(Consulta.pacienteID == IDpaciente)
        parcial = session.exec(appointment).all()
        prescription = select(Prescricao.medicamentoID).where(Prescricao.consultaID.in_(parcial))
        parcial = session.exec(prescription).all()
        drug = select(Medicamento).where(Medicamento.medicamentoID.in_(parcial))
        result = session.exec(drug).all()
        return result

def Listar_farmacias_remedio_especifico(IDremedio):
    with Session(engine) as session:
        relacao = select(FarmaciaMedicamento.CNPJ).where(FarmaciaMedicamento.medicamentoID == IDremedio)
        parcial = session.exec(relacao).all()
        farmacia = select(Farmacia).where(Farmacia.CNPJ.in_(parcial))
        result = session.exec(farmacia).all()
        return result

def Inserir_hospital(ID, nome, endereço, especialidades):
    with Session(engine) as session:
        hospital = Hospital(hospitalID=ID, nome=nome, endereco=endereço, especialidades=especialidades)
        session.add(hospital)
        session.commit()

def Inserir_paciente(ID, nome, nascimento, endereço, historico):
    with Session(engine) as session:
        paciente = Paciente(pacienteID=ID, nome=nome, dataNascimento=nascimento, endereco=endereço, historicoMedico=historico)
        session.add(paciente)
        session.commit()

def Inserir_medico(crm, nome, especialidade, contato):
    with Session(engine) as session:
        doutor = Medico(CRM=crm, nome=nome, especialidade=especialidade, contato=contato)
        session.add(doutor)
        session.commit()

def Inserir_medicamento(ID, nome, fabricante, indicacoes, contraindicacoes):
    with Session(engine) as session:
        medicamento = Medicamento(medicamentoID=ID, nome=nome, fabricante=fabricante, indicacoes=indicacoes, contraIndicacoes=contraindicacoes)
        session.add(medicamento)
        session.commit()

def Inserir_consulta(ID, data, horario, local, diagnostico, IDpaciente, CRM, IDhospital):
    with Session(engine) as session:
        consulta = Consulta(consultaID=ID, dataConsulta=data, horario=horario, local=local, diagnostico=diagnostico, pacienteID=IDpaciente, CRM=CRM, hospitalID=IDhospital)
        session.add(consulta)
        session.commit()

def Listar_medicamentos():
    with Session(engine) as session:
        medicamentos = select(Medicamento)
        result = session.exec(medicamentos).all()
        return result