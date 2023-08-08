from pydantic import BaseModel, Field, constr, validator
from docker_functions import search_image
from enums import ProgrammingLanguage
import re


class JobInput(BaseModel):
    code: constr(min_length=1)
    scheduling: str = Field(None, nullable=True)
    base_image: str
    environments: dict
    language: ProgrammingLanguage = Field(
        ..., description="Programming language of the code"
    )

    @validator("scheduling")
    def validate_scheduling(cls, value):
        if value is not None:
            pattern = r"^\*|^(\*\/[1-9]|[0-9]|[0-5][0-9]) (\*\/[1-9]|[0-9]|1[0-9]|2[0-3]) (\*\/[1-9]|[1-9]|[1-2][0-9]|3[0-1]) (\*\/[1-9]|1[0-2]|0[1-9]) (\*\/[1-9]|1[0-9]|2[0-3])$"
            if not re.match(pattern, value):
                raise ValueError("Invalid scheduling format")
        return value

    @validator("base_image")
    def validate_base_image(cls, value):
        # Search for the base image
        images = search_image(value)
        if not any(image["name"] == value for image in images):
            raise ValueError("Base image does not exist in the Docker repository")

        return value
