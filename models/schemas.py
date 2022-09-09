from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    avatar_url: Optional[str] = None
    shortdesc: Optional[str] = None

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    idea_title: str
    idea_shortdesc: str
    idea_desc: str
    progress: Optional[str]

    class Config:
        orm_mode = True

class TeamNeeds(BaseModel):
    id: int
    need: str

    class Config:
        orm_mode = True
        
class Users(BaseModel):
    id: int
    username: Optional[str]

    class Config:
        orm_mode = True

class Teams(BaseModel):
    id: int
    name: Optional[str]
    idea_title: Optional[str]
    idea_shortdesc: Optional[str]
    role: Optional[str]

    class Config:
        orm_mode = True

class TeamDisplay(BaseModel):
    id: int
    name: str
    idea_title: str
    idea_shortdesc: str
    idea_desc: str
    progress: Optional[str]
    created_at: datetime
    members: Optional[List[Users]]
    team_needs: Optional[List[TeamNeeds]]

    class Config:
        orm_mode = True

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar_url: Optional[str]
    shortdesc: Optional[str]
    teams: Optional[List[Teams]]

    class Config:
        orm_mode = True

class TeamNeedDisplay(BaseModel):
    id: int
    team_id: int
    team_name: str
    team_idea_title: str
    team_idea_shortdesc: str
    need: str
    team_assigned_member: Optional[List[Users]]

    class Config:
        orm_mode = True

class TeamNeedBase(BaseModel):
    team_id: int
    need: str

    class Config:
        orm_mode = True

class AssignNeedToUser(BaseModel):
    team_need_id: int
    user_id: int

    class Config:
        orm_mode = True
