from pydantic import Field
from beanie import Document
from .user_schema import User

class Item(Document):

    """
        Schema design for Item with attributes
        1. name
        2. description
        3. rate
        4. isAvailable
        5. createdBy
        6. updatedBy

    """

    name: str = Field(
        ...,
        title="User Name", 
        description="Enter your user name",
        min_length=1
    )
    description: str = Field(
        None,
        title="Item description",
    )
    rate: float = Field(
        ...,
        ge=0,
        title="Rate",
        description="Item's rate"
    )
    isAvailable: bool = Field(
        default=False,
    )
    createdBy: User 
    updatedBy: User

    class Config:
        schema_extra = {
            "example": {
                "name": "Lasagne",
                "description": """In a mixing bowl, combine ricotta cheese with egg, remaining 2 tablespoons parsley, 1/2 teaspoon salt, and nutmeg. Refrigerate until ready to assemble lasagna. Preheat oven to 375 degrees. Lightly grease a deep 9x13 pan. To assemble, spread about 1 cup of meat sauce in the bottom of the prepared pan.""",
                "rate": "1.1",
                "isAvailable": True
            }
        }

    