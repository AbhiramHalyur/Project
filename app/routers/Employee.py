
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
    return {'Message':'Employees Data Successfully Fetched','data': details }

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_details(det:Details):
    cursor.execute(""" insert into details(fname,lname,gender,phone,email,address,blood,emergency)VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
    (det.fname,det.lname,det.gender,det.phone,det.email,det.address,det.blood,det.emergency))
    
    new_emp=cursor.fetchone()

    conn.commit()
    
    return {'Message':'Employee Successfully Created','data':new_emp}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_details(id: int):
    cursor.execute(""" DELETE FROM details WHERE id=%s returning *""",(str(id),))
    
    deleted_details=cursor.fetchone()
    
    conn.commit()

    if deleted_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with id:{id} does not exist")
    
    return {'Message':'Employee Details Deleted Successfully'}

@router.put("/{id}")
def update_emp(id:int,details:Details):

    cursor.execute("""UPDATE details SET phone=%s,email=%s,emergency=%s WHERE id=%s RETURNING * """,
    (details.phone,details.email,details.emergency,str(id)))

    updated_emp=cursor.fetchone()

    conn.commit()

    

    if updated_emp ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id:{id} does not exist")

    return{'Message':'Details Updated Successfully',"data": updated_emp}
