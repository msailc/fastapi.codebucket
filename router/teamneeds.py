from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database.session import get_db
from models import models, schemas
from typing import List, Union
from models.schemas import TeamNeedBase, TeamNeedDisplay, AssignNeedToUser, Users
from models.models import TeamNeeds, AssignedTeamNeeds

router = APIRouter(
    prefix="/teamneeds",
    tags=["teamneeds"],
)

@router.get("/", response_model=List[TeamNeedDisplay])
def get_all_teamneeds(db: Session = Depends(get_db)):
    result = (
        db.query(TeamNeeds)
        .options(joinedload("team_ideas"))
        .options(joinedload("team_assigned_member", "rel_user"))
        .all()
    )

    teamneeds = [
        TeamNeedDisplay(
            id=teamneed.id,
            team_id=teamneed.team_ideas.id,
            team_name=teamneed.team_ideas.name,
            team_idea_title=teamneed.team_ideas.idea_title,
            team_idea_shortdesc=teamneed.team_ideas.idea_shortdesc,
            need=teamneed.need,
            team_assigned_member=[
                Users(
                    id = member.rel_user.id,
                    username = member.rel_user.username,
                )
                for member in teamneed.team_assigned_member
            ],
        )
        for teamneed in result
    ]
    return teamneeds

@router.post("/", response_model=TeamNeedBase)
def create_teamneed(teamneed: TeamNeedBase, db: Session = Depends(get_db)):
    db_teamneed = TeamNeeds(
        team_id=teamneed.team_id,
        need=teamneed.need,
    )
    db.add(db_teamneed)
    db.commit()
    db.refresh(db_teamneed)
    return db_teamneed

#Assign a team need to a user
@router.post("/assign", response_model=AssignNeedToUser)
def assign_teamneed_to_user(need: AssignNeedToUser, db: Session = Depends(get_db)):
    db_assignedneed = AssignedTeamNeeds(
        team_need_id=need.team_need_id,
        user_id=need.user_id,
    )
    db.add(db_assignedneed)
    db.commit()
    db.refresh(db_assignedneed)
    return db_assignedneed
