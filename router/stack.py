from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database.session import get_db
from models import models, schemas
from typing import List, Union
from models.schemas import StackBase, StackDisplay, Users, Stacks
from models.models import Stack, User , UserStack

router = APIRouter(
    prefix="/stacks",
    tags=["stacks"],
)

@router.get("/", response_model=List[StackDisplay])
def get_all_stacks(db: Session = Depends(get_db)):
    result = (
        db.query(Stack)
        .options(joinedload("user", "rel_user"))
        .all()
    )

    stacks = [
        StackDisplay(
            id=stack.id,
            name=stack.name,
            level=stack.level,
            members=[
                Users(
                    id = member.rel_user.id,
                    username = member.rel_user.username,
                )
                for member in stack.members
            ],
        )
        for stack in result
    ]
    return stacks

@router.get("/{stack_id}", response_model=StackDisplay)
def get_stack(stack_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(Stack)
        .options(joinedload("users", "rel_user"))
        .get(stack_id)
    )

    users = [
        Users(
            id = member.rel_user.id,
            username = member.rel_user.username,
        )
        for member in result.users
    ]

    return StackDisplay(
        id=result.id,
        name=result.name,
        users=users,
    )

@router.post("/", response_model=StackDisplay)
def create_stack(stack: StackBase, db: Session = Depends(get_db)):
    db_stack = Stack(
        name=stack.name,
    )
    db.add(db_stack)
    db.commit()
    db.refresh(db_stack)
    return db_stack

@router.post("/{stack_id}/add/{user_id}")
def add_user_to_stack(stack_id: int, user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).get(user_id)
    db_stack = db.query(Stack).get(stack_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_stack is None:
        raise HTTPException(status_code=404, detail="Stack not found")
    db_user_stack = UserStack(
        user_id = db_user.id,
        stack_id = db_stack.id,
    )
    db.add(db_user_stack)
    db.commit()
    db.refresh(db_user_stack)
    return db_user_stack