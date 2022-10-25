from functools import cache

from sqlalchemy import Boolean, Column, ForeignKey, Integer, MetaData, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@cache
def get_db_metadata() -> MetaData:
    return Base.metadata  # type: ignore


class Constituency(Base):  # type: ignore
    __tablename__ = "constituency"
    name = Column(Text, primary_key=True)


class ConstituencyResult(Base):  # type: ignore
    __tablename__ = "constituency_result"
    constituency = Column(
        Text,
        ForeignKey(
            f"{Constituency.__tablename__}.name",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        primary_key=True,
    )
    candidate = Column(Text, nullable=False, primary_key=True)
    party = Column(Text, nullable=False, primary_key=True)
    votes = Column(Integer, nullable=False, primary_key=True)
    elected = Column(Boolean, nullable=False, primary_key=True)


class ConstituencySummary(Base):  # type: ignore
    __tablename__ = "constituency_summary"
    constituency = Column(
        Text,
        ForeignKey(
            f"{Constituency.__tablename__}.name",
            ondelete="NO ACTION",
            onupdate="NO ACTION",
        ),
        primary_key=True,
    )
    seats = Column(Integer, nullable=False)
    valid_votes = Column(Integer, nullable=False)
    electorate = Column(Integer, nullable=False)
    rejected_ballots = Column(Integer, nullable=True)
