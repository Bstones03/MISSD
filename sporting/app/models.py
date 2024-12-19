from sqlalchemy import Column, BigInteger, String, Boolean, SmallInteger, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship



class Squad(Base):
    __tablename__ = "squad"

    sqid = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    shooters = relationship("Shooter", back_populates="squad")


class Shooter(Base):
    __tablename__ = "shooter"

    Shid = Column(BigInteger, primary_key=True, autoincrement=True)
    S_Fname = Column(String, nullable=False)
    S_Lname = Column(String, nullable=False)
    Schname = Column(String, nullable=False)
    school_id = Column(BigInteger, ForeignKey('school.school_id'), nullable=False)
    handed = Column(Boolean, nullable=False)
    gender = Column(SmallInteger, nullable=False)
    Still_shooting = Column(Boolean, nullable=False)
    sqid = Column(BigInteger, ForeignKey('squad.sqid'), nullable=False)

    school = relationship("School", back_populates="shooters")    
    squad = relationship("Squad", back_populates="shooters")



class School(Base):
    __tablename__ = 'school'

    school_id = Column(BigInteger, primary_key=True, autoincrement=True)
    Schname = Column(String(255), nullable=False)

    shooters = relationship("Shooter", back_populates="school")


class SportingSSporting(Base):
    __tablename__ = "sporting_s_sporting"

    Score_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    Shid = Column(BigInteger, nullable=False)
    Station_id = Column(BigInteger, nullable=False) 
    super = Column(Boolean, nullable=False)
    #Sqid = Column(BigInteger, nullable=False)
    Shoot_id = Column(SmallInteger, ForeignKey('competition.Shoot_id', ondelete="CASCADE"), primary_key=True)
    total = Column(BigInteger, nullable=False)

    competition = relationship("Competition", back_populates="sporting_entries")


class TargetMenu(Base):
    __tablename__ = "target_menu"

    Station_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    Target_1_type = Column(String, nullable=False)
    Target_1_label = Column(BigInteger, nullable=False)
    Target_2_type = Column(String, nullable=False)
    Target_2_label = Column(BigInteger, nullable=False)


class SportingScore(Base):
    __tablename__ = "sporting_score"

    Station_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    Shot_1 = Column(Boolean, nullable=False)
    Shot_2 = Column(Boolean, nullable=True)
    score_id = Column(BigInteger, nullable=False)
    pair_id = Column(BigInteger, primary_key=True, nullable=False)
    station_num = Column(BigInteger, nullable=False)

class Competition(Base):
    __tablename__ = 'competition'

    Shoot_id = Column(BigInteger, primary_key=True, autoincrement=True)
    Shoot_name = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    is_over = Column(Boolean)

    sporting_entries = relationship("SportingSSporting", back_populates="competition", cascade="all, delete-orphan")
