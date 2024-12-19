from pydantic import BaseModel
from typing import Optional, List

class ShooterBase(BaseModel):
    S_Fname: str
    S_Lname: str
    Schname: str
    school_id: int
    handed: bool
    gender: int
    Still_shooting: bool
    sqid: int


class ShooterCreate(ShooterBase):
    pass


class ShooterResponse(ShooterBase):
    Shid: int

    class Config:
        orm_mode = True


# School Schema
class SchoolBase(BaseModel):
    Schname: str


class SchoolCreate(SchoolBase):
    pass


class SchoolResponse(SchoolBase):
    school_id: int

    class Config:
        orm_mode = True


class CompetitionBase(BaseModel):
    Shoot_name: str
    city: str
    state: str
    is_over: bool


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionResponse(CompetitionBase):
    Shoot_id: int

    class Config:
        orm_mode = True


class SportingSSportingBase(BaseModel):
    Shoot_id: int
    Station_id: int
    super: bool
    #Sqid: int
    total: int


class SportingSSportingCreate(SportingSSportingBase):
    score_id: int


class SportingSSportingResponse(SportingSSportingBase):
    Shid: int

    class Config:
        orm_mode = True


class TargetMenuBase(BaseModel):
    Target_1_type: str
    Target_1_label: int
    Target_2_type: str
    Target_2_label: int


class TargetMenuCreate(TargetMenuBase):
    pass


class TargetMenuResponse(TargetMenuBase):
    Station_id: int

    class Config:
        orm_mode = True


class SportingScoreBase(BaseModel):
    Shot_1: bool
    Shot_2: Optional[bool] = None
    score_id: int
    station_num: int


class SportingScoreCreate(SportingScoreBase):
    pair_id: int


class SportingScoreResponse(SportingScoreBase):
    Station_id: int
    pair_id: int

    class Config:
        orm_mode = True


