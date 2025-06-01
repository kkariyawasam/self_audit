from fastapi import APIRouter, Depends
from app.utils.deps import require_role
from app.models.user import Role

router = APIRouter(prefix="/client", tags=["client"])

@router.get("/dashboard")
def client_dashboard(user=Depends(require_role(Role.client))):
    return {"message": f"Welcome {user['username']} to the Client Dashboard"}
