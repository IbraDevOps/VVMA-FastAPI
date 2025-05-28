from fastapi import FastAPI
from app.routes import user
from app.routes import auth
from app.routes import ssrf
from app.routes import reset
app = FastAPI()

app.include_router(user.router,prefix="/api")
app.include_router(auth.router,prefix="/api")
app.include_router(ssrf.router,prefix="/api")
app.include_router(reset.router,prefix="/api")
@app.get("/")
def read_root():
    return {"Hello": "World"}
