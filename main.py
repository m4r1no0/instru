from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import (
    pago, users, auth, instructor, contrato,
    direccion, contacto, proceso, programa,
    poliza, rol, supervisor, area_formacion, informe, InformeDos,informeTres,cesion
)

from app.router.email_router import router as email_router

app = FastAPI()

# CORS (solo uno)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción pon dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/access", tags=["auth"])
app.include_router(instructor.router, prefix="/instructores", tags=["instructores"])
app.include_router(contrato.router, prefix="/contrato", tags=["contrato"])
app.include_router(direccion.router, prefix="/direccion", tags=["direccion"])
app.include_router(pago.router, prefix="/pago", tags=["pago"])
app.include_router(proceso.router, prefix="/proceso", tags=["proceso"])
app.include_router(programa.router, prefix="/programa", tags=["programa"])
app.include_router(poliza.router, prefix="/poliza", tags=["poliza"])
app.include_router(rol.router, prefix="/rol", tags=["rol"])
app.include_router(contacto.router, prefix="/contacto", tags=["contacto"])
app.include_router(supervisor.router, prefix="/supervisor", tags=["supervisor"])
app.include_router(area_formacion.router, prefix="/area_formacion", tags=["area_formacion"])
app.include_router(informe.router, tags=["informes"])
app.include_router(InformeDos.router, tags=["informes"])
app.include_router(informeTres.router, tags=["informes"])
app.include_router(cesion.router, prefix="/cesion", tags=["cesion"])
app.include_router(email_router)

@app.get("/")
def read_root():
    return {
        "message": "ok",
        "autor": "Marino A Osorio D 2026"
    }
# print("Rutas disponibles:")
# for route in app.routes:
#     print(f"{route.methods} {route.path}")