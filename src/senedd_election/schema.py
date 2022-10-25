from typing import Optional

from pydantic import BaseModel


class Constituency(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ConstituencyResult(BaseModel):
    constituency: str
    candidate: str
    party: str
    votes: int
    elected: bool

    class Config:
        orm_mode = True


class ConstituencySummary(BaseModel):
    constituency: str
    seats: int
    valid_votes: int
    electorate: int
    rejected_ballots: Optional[int]

    class Config:
        orm_mode = True
