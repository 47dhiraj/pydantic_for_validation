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
)

from uuid import UUID, uuid4


from pydantic import EmailStr                      






class User(BaseModel):

    
    uid: UUID = Field(default_factory=uuid4)     

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


    ## This is useful for fields that are computed from other fields, or for fields that are expensive to compute and should be cached.
    
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





class BlogPost(BaseModel):
    
    title: Annotated[str, Field(min_length=2, max_length=100, description="title of the blog post")]                          
    content: Annotated[str, Field(min_length=5, description="content of the blog post")]                            
    author_id: Annotated[int, Field(gt=0)]                   

    view_count: int = 0                   
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))

    status: Literal["draft", "published", "archived"] = "draft"     
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]







user = None

try:
    user = User(         
        username="John_Doe123",
        age=18,
        email="John.doe@gmail.com",
        password = "jhon123",
        website = "www.google",
        bio="King of the World",
        first_name = "John",
        last_name="Doe",
        follower_count = 10000

        
        
    )

    #print(user)


except ValidationError as e:
    print(e)


if user is not None:
    user_json = user.model_dump_json(indent=2)
    print('\n', user_json, '\n')

    



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

    post = BlogPost(
        title="Getting Started with Python",
        content="This blog post is all about the basics of python ...",
        author_id=1,
        slug="getting-started-with-python",
    )

except ValidationError as e:

    print(e)



if post is not None:

    post_json = post.model_dump_json(indent=2)
   # print('\n',post_json,'\n')




