import re

from pydantic import BaseModel, Field, validator, SecretStr, BaseSettings


class KeySkills(BaseModel):
    name: str | None = None

class Experience(BaseModel):
    name: str | None = None

class Snippet(BaseModel):
    requirement: str | None = None
    responsibility: str | None = None


class Employer(BaseModel):
    name: str
    alternate_url: str

class Salary(BaseModel):
    from_: int = Field(None, alias='from')
    to: int | None = None
    currency: str


    class Config:
        allow_population_by_field_name = True


class Area(BaseModel):
    name: str

    class Config:
        allow_population_by_field_name = True

class Items(BaseModel):
    name: str
    url: str
    alternate_url: str
    published_at: str
    # area: Area | None = None
    # salary: Salary | None = None
    # employer: Employer | None = None
    # snippet: Snippet | None = None
    # experience: Experience | None = None
    # description : str | None = None

    class Config:
        allow_population_by_field_name = True

class GetUrlVacancy(BaseModel):
    items: list[Items] | None = None


    class Config:
        allow_population_by_field_name = True


class DetailVacancyResponse(BaseModel):
    name: str | None = None
    # url: str
    # alternate_url: str
    description: str | None = None
    area: Area | None = None
    salary: Salary | None = None
    employer: Employer | None = None
    snippet: Snippet | None = None
    experience: Experience | None = None
    key_skills: list[KeySkills] | None = None
    alternate_url: str | None = None


    class Config:
        allow_population_by_field_name = True

