
from fastapi import Response,status,HTTPException,APIRouter
from pydantic import BaseModel,EmailStr
from ..database import conn,cursor


router=APIRouter(
    prefix= "/Emp-details",
    tags=['Employee Details']
)




class Details(BaseModel):
    fname:str
    lname:str
    gender:str
    phone:int
    email:EmailStr
    address:str
    blood:str
    emergency:int




@router.get("/")
def get_details():
    cursor.execute(""" SELECT * FROM details""")
    details=cursor.fetchall()
    return {'data': details }

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_details(det:Details):
    cursor.execute(""" insert into details(fname,lname,gender,phone,email,address,blood,emergency)VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
    (det.fname,det.lname,det.gender,det.phone,det.email,det.address,det.blood,det.emergency))
    
    new_emp=cursor.fetchone()

    conn.commit()
    
    return {'data':new_emp}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_details(id: int):
    cursor.execute(""" DELETE FROM details WHERE id=%s returning *""",(str(id),))
    
    deleted_details=cursor.fetchone()
    
    conn.commit()

    if deleted_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with id:{id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_emp(id:int,details:Details):

    cursor.execute("""UPDATE details SET fname=%s,lname=%s,gender=%s,phone=%s,email=%s,address=%s,blood=%s,emergency=%s WHERE id=%s RETURNING * """,(details.fname,details.lname,details.gender,details.phone,details.email,details.address,details.blood,details.emergency,str(id)))

    updated_emp=cursor.fetchone()

    conn.commit()

    

    if updated_emp ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id:{id} does not exist")

    return{"data": updated_emp}