from pydantic import BaseModel
from datetime import date

#utilizado en: PERSONAS_ou
class PersonasOUInModel(BaseModel):
    Id: int

class PersonasOUOutModel(BaseModel):
    Id: str  # ajustar tipo real
    Tipo_Documento: str  # ajustar tipo real
    Persona_Tipo_Institucion_Id: str  # ajustar tipo real
    codigo_interno_institucional: str  # ajustar tipo real
    Documento: str  # ajustar tipo real
    Apellido: str  # ajustar tipo real
    Nombre: str  # ajustar tipo real
    Fecha_Nacimiento: str  # ajustar tipo real
    CUIL: str  # ajustar tipo real
    Sexo: str  # ajustar tipo real
    Estado_Civil: str  # ajustar tipo real
    Activo: str  # ajustar tipo real
    Validado: str  # ajustar tipo real
    ULTIMA_MODIFICACION_: str  # ajustar tipo real
    BORRADO_: str  # ajustar tipo real

#Utilizado en: PERSONAS_IN    
class PersonasINModel(BaseModel):
    Tipo_Documento: int
    Persona_Tipo_Institucion_Id: int
    codigo_interno_institucional: str
    Documento: str
    Apellido: str
    Nombre: str
    Fecha_Nacimiento: date
    CUIL: str
    Sexo: str
    Estado_Civil: str
    Activo: bool
    Validado: bool
    
#Utilizado en: PERSONAS_cbu
class PersonasCbuModel(BaseModel):
    Persona_Id: int
    cbu: str
    
