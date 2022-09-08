from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database.session import get_db
from models import models, schemas
from typing import List, Union
from models.schemas import TeamNeedBase, TeamNeedDisplay
from models.models import TeamNeeds

router = APIRouter(
    prefix="/teamneeds",
    tags=["teamneeds"],
)

@router.get("/", response_model=List[TeamNeedDisplay])
def get_all_teamneeds(db: Session = Depends(get_db)):
    result = (
        db.query(TeamNeeds)
        .options(joinedload("team_ideas"))
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
