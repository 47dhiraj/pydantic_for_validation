from datetime import UTC, datetime

from typing import Literal, Annotated

from functools import partial

 
from pydantic import (

    BaseModel, 
    Field, 
    ValidationError,
    HttpUrl,                                        
    SecretStr,                                      
    ValidationError, 
    ValidationInfo, 
    field_validator,                                
    model_validator,      
    computed_field,      
    ConfigDict,                    
)

from uuid import UUID, uuid4


from pydantic import EmailStr                      






class User(BaseModel):

    ## validate_by_alias,validate_by_name  --> allows to use alias to the field properly.
    
    model_config = ConfigDict(validate_by_name=False, validate_by_alias=True, serialize_by_alias = True)

 
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




### Model Validator
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    

    @model_validator(mode='after')
    def passwords_match(self) -> 'UserRegistration':
        
        
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')

        return self




class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0





class BlogPost(BaseModel):
    
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=False, serialize_by_alias=True)

    
    title: Annotated[str, Field(alias="heading", min_length=2, max_length=100, description="title of the blog post")]                          
    content: Annotated[str, Field(alias="description", min_length=5, description="content of the blog post")]                            
    author: User                

    view_count: int = 0                   
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))

    status: Literal["draft", "published", "archived"] = "draft"     
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]


    comments: list[Comment] = Field(default_factory=list)







user = None

try:
   

    ### User Dictionary
    user_data = {
        "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
        "username": "John_Doe123",
        "email": "John.doe@gmail.com",
        "age": "39",
        "password": "secret123",
    }


    user = User.model_validate(user_data)
   



except ValidationError as e:
    print(e)


if user is not None:

    user_json = user.model_dump_json(indent=2)       
          
   # print('\n', user_json, '\n')

    



registration = None

try:

    registration = UserRegistration(
        email="CoreyMSchafer@gmail.com",
        password="secret123",
        confirm_password="secret123"
    )
    
    #print(registration, type(registration))


except ValidationError as e:
    print(e)







post = None

try:

    
    ### BlogPost Dictionary
    post_data = {
        "heading": "Getting Started with Pydantic",
        "description": "This blog post is all about the basics of pydantic ...",
        "slug": "understanding-pydantic",
        "author": {
            "username": "JohnDoe",
            "email": "john123@gmail.com",
            "age": 39,
            "password": "secret123",
        },
        "comments": [
            {
                "content": "I think I understand nested models now!",
                "author_email": "student@example.com",
                "likes": 25,
            },
            {
                "content": "Can you cover FastAPI next?",
                "author_email": "viewer@example.com",
                "likes": 15,
            },
        ],
    }


    ## model_validate() --> takes raw input as python dictionary and validate it through pydantic-core.
    post = BlogPost.model_validate(post_data) 


except ValidationError as e:

    print(e)



if post is not None:


    post_json = post.model_dump_json(indent=2)
    print('\n',post_json,'\n')




