from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.routes.users import get_current_user
from app.authorization import check_permission

router = APIRouter(prefix="/rbac", tags=["RBAC"])

@router.post("/assign-role")
def assign_role(user_id: int, role: str, 
                db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):


    allowed_roles = ["admin", "user"]

    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role '{role}'. Allowed roles: {', '.join(allowed_roles)}")


    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied. Only admins can assign roles.")


    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    if current_user.id == user_id:
        raise HTTPException(status_code=403, detail="You cannot change your own role.")


    user.role = role
    db.commit()
    
    return {"message": f"Role '{role}' assigned to user {user_id}"}
