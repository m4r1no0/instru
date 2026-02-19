from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import pago
from app.router import users
from app.router import auth
from app.router import instructor
from app.router import contrato
from app.router import direccion
from app.router import contacto
from app.router import proceso
from app.router import programa
from app.router import poliza
from app.router import rol
from app.router import supervisor
from app.router import area_formacion

app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/access", tags=["login"])
app.include_router(instructor.router, prefix="/instructores", tags=["Instructores"])
app.include_router(contrato.router, prefix="/contrato", tags=["Contrato"])
app.include_router(direccion.router, prefix="/direccion", tags=["direccion"])
app.include_router(pago.router, prefix="/pago", tags=["pago"])
app.include_router(proceso.router, prefix="/proceso", tags=["proceso"])
app.include_router(programa.router, prefix="/programa", tags=["programa"])
app.include_router(poliza.router, prefix="/poliza", tags=["poliza"])
app.include_router(rol.router, prefix="/rol", tags=["rol"])
app.include_router(contacto.router, prefix="/contacto", tags=["contacto"])
app.include_router(supervisor.router, prefix="/supervisor", tags=["supervisor"])
app.include_router(area_formacion.router, prefix="/area_formacion", tags=["area_formacion"])

app.include_router(auth.router, prefix="/access", tags=["Auth"])


# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "ok",
                "autor": "Marino A Osorio D"
            }