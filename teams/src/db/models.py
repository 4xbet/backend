from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    founded_year: Mapped[int] = mapped_column(nullable=False)
    logo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    
    athletes: Mapped[list["Athlete"]] = relationship(back_populates="team", cascade="all, delete-orphan")

class Athlete(Base):
    __tablename__ = "athletes"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    position: Mapped[str] = mapped_column(String(50), nullable=False, quote=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    
    team: Mapped["Team"] = relationship(back_populates="athletes")