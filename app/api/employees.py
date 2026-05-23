from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "employees router up"}
