from fastapi import status,HTTPException,APIRouter

from ..database import conn

router=APIRouter(
    prefix="/dashboard",
    tags=['Dashboard']
)



@router.get("/{id}")
def get_dashboard(id: int):
    cursor = conn.cursor()
    cursor.execute(
        """SELECT D.id, D.fname, D.lname, D.gender, D.phone, D.email, D.address, D.blood, D.emergency, COUNT (A.assetid),STRING_AGG(A.AssetName, ', ') AS asset_name
        FROM details D 
        LEFT JOIN Asset A ON D.id = A.id 
        WHERE D.id = %s 
        GROUP BY D.id;""",
        (str(id),)
    )
    
    dashboard = cursor.fetchone()

    if not dashboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found")
    
    return {'data':dashboard}