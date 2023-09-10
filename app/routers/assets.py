from fastapi import Response,status,HTTPException,APIRouter
from ..database import conn,cursor
from pydantic import BaseModel

router=APIRouter(
    prefix="/asset",
    tags=['Employee Assets']
)





class Assets(BaseModel):
    id: int
    assetname: str
    assettype: str



@router.get("/")
def get_assets():
    cursor.execute(""" SELECT * FROM asset""")
    
    asset_details=cursor.fetchall()
    
    return {'data': asset_details }



@router.post("/",status_code=status.HTTP_201_CREATED)
def create_assets(asset:Assets):
    cursor.execute("""INSERT INTO asset (id,assetname,assettype)VALUES(%s,%s,%s) RETURNING *""",
    (asset.id,asset.assetname,asset.assettype))

    new_asset=cursor.fetchone()

    conn.commit()
    
    return {'data':new_asset}


@router.delete("/{assetid}",status_code=status.HTTP_204_NO_CONTENT)
def delete_details(assetid:int):
    
    cursor.execute(""" DELETE FROM asset WHERE assetid=%s returning*""",(str(assetid),))
    deleted_asset=cursor.fetchone()
    conn.commit()


    if deleted_asset ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"asset with id:{assetid} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router .put("/{assetid}")
def update_emp(assetid:int,asset:Assets):

    cursor.execute("""UPDATE asset SET id=%s,assetname=%s,assettype=%s WHERE assetid=%s RETURNING * """,
    (asset.id,asset.assetname,asset.assettype,str(assetid)))

    updated_asset=cursor.fetchone()

    conn.commit()

    if updated_asset ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"asset with id:{assetid} does not exist")

    return{"data": updated_asset}