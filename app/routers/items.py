import re
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

router = APIRouter()
items: list[dict] = []


class ItemCreate(BaseModel):
    # TODO: name must have 1-100 characters; description has at most 500.
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length= 500) 

    @field_validator("name", "description", mode= "before") #before: strips html tags and whitespace first, then pydantic check length
    @classmethod
    def sanitize_html_and_white_spaces(cls, value: str) -> str:
        if not isinstance(value, str): #Guards against non-string inputs so re.sub() doesn't crash before pydantic raises a clean validation error.
            raise ValueError ("Field must be a string")

        #Remove HTML tags to prevent store XSS, then strip outer whitespace
        cleaned = re.sub(r"<[^>]*>", "", value).strip()
        return cleaned

@router.get("/")
def list_items():
    """TODO: return items and explain why parameterized SQL treats input as data."""
    
    #Parameterized queries keep the SQL code separate from the user's input. The database treats user input stricktly as plain text, not as runnable commands so special characters cannot  change the query
   
    #VULNERABLE (String formatting)
    #cursor.execute(f"SElECT * FROM items WHERE name = '{name}'")
    
    #SAFE (Parameterized query with placeholders)
    #cursor.execute("SELECT *FROM items WHERE name = ?", (name,))

    return items


@router.post("/", status_code=201)
def create_item(item: ItemCreate):
    """TODO: assign an id, append validated item data, and return the new item."""

    new_item = {
        "id": len(items) + 1, #generates the next sequential integer ID - 1,2,3
        "name": item.name,
        "description": item.description,
    }
    items.append(new_item )
    return new_item