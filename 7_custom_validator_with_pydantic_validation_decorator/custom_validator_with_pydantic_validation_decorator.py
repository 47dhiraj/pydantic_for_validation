from datetime import UTC, datetime

from typing import Literal, Annotated

from functools import partial

 
from pydantic import (

    BaseModel, 
    Field, 
    ValidationError,
    HttpUrl,                                        ## HttpUrl is al network type(validated type)
    SecretStr,                                      ## SecretStr is al pydantic type(validated type)
    ValidationError, 
    ValidationInfo, 
    field_validator,                                ## decorator for creating custom validator function for a specific field inside pydantic model.
    model_validator,                                ## decorator for creating custom validator function for a pydantic model.
)

from uuid import UUID, uuid4


from pydantic import EmailStr                       ## EmailStr is al pydantic type(validated type)






class User(BaseModel):

    
    uid: UUID = Field(default_factory=uuid4)     

    username: Annotated[str, Field(min_length=3, max_length=50, description="username of a user")]
    age: Annotated[int, Field(ge=18, le=120, description="age of a user")]                           
   
   
    email: EmailStr                                 ## EmailStr is a pydantic type(validated type)

    password : SecretStr                            ## SecretStr is a pydantic type(validated type)

    website: HttpUrl | None = None                  ## HttpUrl is a network type(validated type)        

    verified_at: datetime | None = None         
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None
    

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:          ## This is how we create a custom validator inside pydantic class using pydantic decorators @.
        if not v.replace("_","").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()








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
        username="John-Doe123",
        age=18,
        email="John.doe@gmail.com",
        password = "jhon123",
        website = "https://www.google.com",
        bio="King of the World"
    )

    #print(User.validate_username(user.username))
    #print(user.validate_username(user.username))

except ValidationError as e:
    print(e)


if user is not None:
    user_json = user.model_dump_json(indent=2)
    print('\n', user_json, '\n')

    



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
    print('\n',post_json,'\n')




