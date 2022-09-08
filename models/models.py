from datetime import datetime
from turtle import title
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata



class TeamMember(Base):
    __tablename__ = 'team_members'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    team_id = Column(Integer, ForeignKey('team_ideas.id'))
    role = Column(String)
    joined_at = Column(DateTime, default=datetime.utcnow)

    rel_team = relationship("TeamIdea", back_populates="members")
    rel_user = relationship("User", back_populates="teams")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    avatar_url = Column(String)
    shortdesc = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    teams = relationship("TeamMember", back_populates="rel_user")

class TeamIdea(Base):
    __tablename__ = 'team_ideas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    idea_title = Column(String)
    idea_shortdesc = Column(String)
    idea_desc = Column(String)
    progress = Column(String)
    needed_skills = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("TeamMember", back_populates="rel_team")

class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
