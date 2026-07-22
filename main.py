from fastapi import FastAPI

from database import Base, engine

from routes.auth import router as auth_router
from routes.houses import router as house_router
from routes.tenants import router as tenant_router
from routes.payments import router as payment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="House Rental & Tenant Management System"
)

app.include_router(auth_router)
app.include_router(house_router)
app.include_router(tenant_router)
app.include_router(payment_router)


@app.get("/")
def home():
    return {
        "message": "House Rental & Tenant Management System API"
    }
