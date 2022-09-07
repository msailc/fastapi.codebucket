from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database.session import get_db
from models import models, schemas
from typing import List, Union
from models.schemas import TeamBase, TeamDisplay, Users
from models.models import TeamIdea, User

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)

@router.get("/", response_model=List[TeamDisplay])
def get_all_teams(db: Session = Depends(get_db)):
    result = (
        db.query(TeamIdea)
        .options(joinedload("members", "rel_user"))
        .all()
    )

    teams = [
        TeamDisplay(
            id=team.id,
            name=team.name,
            idea_title=team.idea_title,
            idea_shortdesc=team.idea_shortdesc,
            idea_desc=team.idea_desc,
            progress=team.progress,
            needed_skills=team.needed_skills,
            created_at=team.created_at,
            team_members=[
                Users(
                    id = member.rel_user.id,
                    username = member.rel_user.username,
                    title = member.role,
                )
                for member in team.members
            ]
        )
        for team in result
    ]
    return teams


@router.get("/{team_id}", response_model=TeamDisplay)
def get_team(team_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(TeamIdea)
        .options(joinedload("members", "rel_user"))
        .get(team_id)
    )

    members = [
        Users(
            id = user.rel_user.id,
            username = user.rel_user.username,
            title = user.role,
        )
        for user in result.members
    ]

    return TeamDisplay(
        id=result.id,
        name=result.name,
        idea_title=result.idea_title,
        idea_shortdesc=result.idea_shortdesc,
        idea_desc=result.idea_desc,
        progress=result.progress,
        needed_skills=result.needed_skills,
        created_at=result.created_at,
        members=members,
    )


@router.post("/", response_model=TeamDisplay)
def create_team(team: TeamBase, db: Session = Depends(get_db)):
    new_team = models.TeamIdea(name=team.name, idea_title=team.idea_title, idea_shortdesc=team.idea_shortdesc, idea_desc=team.idea_desc, progress=team.progress, needed_skills=team.needed_skills)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


