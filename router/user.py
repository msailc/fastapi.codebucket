from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database.session import get_db
from models import models, schemas
from typing import List, Union
from models.schemas import TeamBase, TeamDisplay, UserDisplay, Teams
from models.models import TeamIdea, User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[schemas.UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    result = (
        db.query(User)
        .options(joinedload("teams", "rel_team"))
        .all()
    )

    users = [
        UserDisplay(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            avatar_url=user.avatar_url,
            shortdesc=user.shortdesc,
            teams=[
                Teams(
                    id = team.rel_team.id,
                    idea_title = team.rel_team.idea_title,
                    idea_shortdesc = team.rel_team.idea_shortdesc,
                    role = team.role,
                )
                for team in user.teams
            ]
        )
        for user in result
    ]
    return users

@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(User)
        .options(joinedload("teams", "rel_team"))
        .get(user_id)
    )

    teams = [
        Teams(
            id = team.rel_team.id,
            name = team.rel_team.name,
            idea_title = team.rel_team.idea_title,
            idea_shortdesc = team.rel_team.idea_shortdesc,
            role = team.role,
        )
        for team in result.teams
    ]
    return UserDisplay(
        id=result.id,
        username=result.username,
        email=result.email,
        created_at=result.created_at,
        avatar_url=result.avatar_url,
        shortdesc=result.shortdesc,
        teams=teams
    )

@router.post("/create", response_model=schemas.UserDisplay)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username, email=user.email, avatar_url=user.avatar_url, shortdesc=user.shortdesc)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user