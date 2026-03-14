from datetime import datetime

from typing import Annotated

 
from pydantic import (
    BaseModel, 
    Field, 
    ValidationError,
    HttpUrl,                                        
    SecretStr,                                      
    field_validator,                                     
    computed_field,      
    ConfigDict,                    
)


from uuid import UUID, uuid4

from pydantic import EmailStr                      

import json



## 'from_attributes=True' option in ConfigDict in pydantic v2 to enable ORM like behavior.



class UserTable:

    def __init__(self, id: UUID | str, username: str, email: str, age: int, password: str) -> None:

        self.id: UUID | str = id

        self.username: str = username

        self.email: str = email

        self.age: int = age

        self.password: str = password





db_user_record = UserTable(
    id="3bc4bf25-1b73-44da-9078-f2bb310c7374",
    username="Jane123",
    email="jane@example.com",
    age=29,
    password="jane_secret123"
)


## print(type(db_user_record))                 ## <class '__main__.UserTable'>




class User(BaseModel):

    model_config = ConfigDict(
        
        from_attributes=True,         
        
        # from_attributes = False,            
        
        validate_by_name=False, 
        validate_by_alias=True, 
        serialize_by_alias = True
    )

 
    uid: UUID = Field(alias="id", default_factory=uuid4)     

    username: Annotated[str, Field(min_length=3, max_length=50, description="username of a user")]
    age: Annotated[int, Field(ge=18, le=120, description="age of a user")]                           
   
    email: EmailStr                                 

    password : SecretStr

    website: HttpUrl | None = None                         

    verified_at: datetime | None = None         
    bio: str = ""
    is_active: bool = True
    
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0


    @field_validator("username")    
    @classmethod
    def validate_username(cls, v: str) -> str:           
        if not v.replace("_","").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()


    @field_validator("website", mode="before")
    @classmethod
    def add_https(cls, v: str | None) -> str | None:
        if v and (not v.startswith(("http://", "https://")) or not v.endswith(".com")):

            scheme = "" if v.startswith(("http://", "https://")) else "https://"
            domain = "" if v.endswith(".com") else ".com"

            return f"{scheme}{v}{domain}"

        return v


    @computed_field
    @property
    def display_name(self) -> str:

        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        
        return self.username


    @computed_field
    @property
    def is_influencer(self) -> bool:

        return self.follower_count >= 10000








user = None


try:

    # ## simulating data received from client side or from API endpoint as JSON.

    # user_data = {
    #     "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    #     "username": "John_Doe123",
    #     "email": "John.doe@gmail.com",
    #     "age": "29",
    #     "password": "secret123",
    # }

    # user = User.model_validate_json(json.dumps(user_data))



    ## simulating data received from ORM like SQLAlchemy as an object.
    ## using from_attributes=True in ConfigDict enables us to use ORM like objects directly in pydantic model_validate() method.
    user = User.model_validate(db_user_record)


except ValidationError as e:

    print(e)




if user is not None:

    user_json = user.model_dump_json(indent=2)       
          
    print('\n', user_json, '\n')

