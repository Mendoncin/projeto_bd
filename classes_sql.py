from sqlmodel import SQLModel, Relationship, Field, create_engine
from typing import Optional, List



class Hospital(SQLModel, table=True):
    hospitalID: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    endereco: str = Field(max_length=200)
    especialidades: Optional[str] = Field(default=None, max_length=200)
    medicos: List["HospitalMedico"] = Relationship(back_populates="hospital")
    consultas: List["Consulta"] = Relationship(back_populates="hospital")

class Medico(SQLModel, table=True):
    CRM: int = Field(primary_key=True)
    nome: str = Field(max_length=100)
    especialidade: str = Field(max_length=100)
    contato: Optional[str] = Field(default=None, max_length=100)
    hospitais: List["HospitalMedico"] = Relationship(back_populates="medico")
    consultas: List["Consulta"] = Relationship(back_populates="medico")

class HospitalMedico(SQLModel, table=True):
    hospitalID: int = Field(foreign_key="hospital.hospitalID", primary_key=True)
    CRM: int = Field(foreign_key="medico.CRM", primary_key=True)
    hospital: Hospital = Relationship(back_populates="medicos")
    medico: Medico = Relationship(back_populates="hospitais")

class Paciente(SQLModel, table=True):
    pacienteID: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    dataNascimento: Optional[str] = Field(default=None)
    endereco: Optional[str] = Field(default=None, max_length=200)
    historicoMedico: Optional[str] = Field(default=None, max_length=500)
    consultas: List["Consulta"] = Relationship(back_populates="paciente")

class Consulta(SQLModel, table=True):
    consultaID: Optional[int] = Field(default=None, primary_key=True)
    dataConsulta: str
    horario: str
    local: Optional[str] = Field(default=None, max_length=100)
    diagnostico: Optional[str] = Field(default=None, max_length=500)
    pacienteID: int = Field(foreign_key="paciente.pacienteID")
    CRM: int = Field(foreign_key="medico.CRM")
    hospitalID: int = Field(foreign_key="hospital.hospitalID")
    paciente: Paciente = Relationship(back_populates="consultas")
    medico: Medico = Relationship(back_populates="consultas")
    hospital: Hospital = Relationship(back_populates="consultas")
    prescricoes: List["Prescricao"] = Relationship(back_populates="consulta")

class Medicamento(SQLModel, table=True):
    medicamentoID: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    fabricante: Optional[str] = Field(default=None, max_length=100)
    indicacoes: Optional[str] = Field(default=None, max_length=200)
    contraIndicacoes: Optional[str] = Field(default=None, max_length=200)
    prescricoes: List["Prescricao"] = Relationship(back_populates="medicamento")

class Prescricao(SQLModel, table=True):
    prescricaoID: Optional[int] = Field(default=None, primary_key=True)
    consultaID: int = Field(foreign_key="consulta.consultaID")
    medicamentoID: int = Field(foreign_key="medicamento.medicamentoID")
    dosagem: Optional[str] = Field(default=None, max_length=50)
    frequencia: Optional[str] = Field(default=None, max_length=50)
    duracao: Optional[str] = Field(default=None, max_length=50)
    consulta: Consulta = Relationship(back_populates="prescricoes")
    medicamento: Medicamento = Relationship(back_populates="prescricoes")

class Farmacia(SQLModel, table=True):
    CNPJ: str = Field(primary_key=True, max_length=20)
    nome: str = Field(max_length=100)
    endereco: Optional[str] = Field(default=None, max_length=200)
    medicamentos: List["FarmaciaMedicamento"] = Relationship(back_populates="farmacia")
    funcionarios: List["FuncionarioFarmacia"] = Relationship(back_populates="farmacia")
    abastecimentos: List["Abastecimento"] = Relationship(back_populates="farmacia")

class FarmaciaMedicamento(SQLModel, table=True):
    CNPJ: str = Field(foreign_key="farmacia.CNPJ", primary_key=True)
    medicamentoID: int = Field(foreign_key="medicamento.medicamentoID", primary_key=True)
    farmacia: Farmacia = Relationship(back_populates="medicamentos")
    medicamento: Medicamento = Relationship()

class FuncionarioFarmacia(SQLModel, table=True):
    funcionarioID: Optional[int] = Field(default=None, primary_key=True)
    CNPJ: str = Field(foreign_key="farmacia.CNPJ")
    nome: str = Field(max_length=100)
    cargo: Optional[str] = Field(default=None, max_length=50)
    numeroCaixa: Optional[int] = Field(default=None)
    setor: Optional[str] = Field(default=None, max_length=50)
    registro: Optional[str] = Field(default=None, max_length=50)
    farmacia: Farmacia = Relationship(back_populates="funcionarios")

class Laboratorio(SQLModel, table=True):
    laboratorioID: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    especialidade: Optional[str] = Field(default=None, max_length=100)
    endereco: Optional[str] = Field(default=None, max_length=200)
    abastecimentos: List["Abastecimento"] = Relationship(back_populates="laboratorio")

class Abastecimento(SQLModel, table=True):
    abastecimentoID: Optional[int] = Field(default=None, primary_key=True)
    laboratorioID: int = Field(foreign_key="laboratorio.laboratorioID")
    CNPJ: str = Field(foreign_key="farmacia.CNPJ")
    dataAbastecimento: Optional[str] = Field(default=None)
    quantidade: Optional[int] = Field(default=None)
    laboratorio: Laboratorio = Relationship(back_populates="abastecimentos")
    farmacia: Farmacia = Relationship(back_populates="abastecimentos")

sqlite_file_name = "database.db"
connection_string = f'sqlite:///{sqlite_file_name}'

engine = create_engine(connection_string, echo=False)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)