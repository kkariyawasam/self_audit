from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Audit platform backend running"}


from app.routers import auth
from app.routers import client
from app.routers import upload
from app.routers import audit
from app.routers import admin



app.include_router(auth.router)
app.include_router(client.router)
app.include_router(upload.router)
app.include_router(audit.router)
app.include_router(admin.router)
