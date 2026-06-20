from fastapi import APIRouter, HTTPException
from app.api.schemas import TenantCreate, CloudAccountCreate
from app.api import crud

router = APIRouter(prefix="/api/v1")

@router.post("/tenants")
async def register_tenant(tenant: TenantCreate):
    try:
        result = crud.create_tenant(tenant)
        return {"message": "Tenant registered successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration Failed: {str(e)}")

@router.post("/accounts")
async def connect_cloud_account(account: CloudAccountCreate):
    try:
        result = crud.create_cloud_account(account)
        return {"message": "AWS Cloud Account linked successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cloud Integration Failed: {str(e)}")
