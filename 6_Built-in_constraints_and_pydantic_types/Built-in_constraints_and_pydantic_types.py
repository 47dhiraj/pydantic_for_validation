from datetime import UTC, datetime

from typing import Literal, Annotated

from functools import partial

from pydantic import BaseModel, Field, ValidationError, HttpUrl, SecretStr   
from uuid import UUID, uuid4

from pydantic import EmailStr




class User(BaseModel):

    ## uid is generated automatically by uuid. So, no need to pass when creating instance.
    uid: UUID = Field(default_factory=uuid4)     

    username: Annotated[str, Field(min_length=3, max_length=50, description="username of a user")]
    age: Annotated[int, Field(ge=18, le=120, description="age of a user")]                           
   
    ## EmailStr validates email syntax.
    email: EmailStr     

    ## SecretStr used for password masking.
    password : SecretStr

    ## Guarantee that you’re dealing with a real HTTP(S) URL
    website: HttpUrl | None = None                            

    verified_at: datetime | None = None         
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None
    



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
        username="Johndoe",
        age=18,
        email="John.doe@gmail.com",
        password = "jhon123",
        website = "https://www.google.com",
        bio="King of the World"
    )

except ValidationError as e:
    print(e)


if user is not None:
    user_json = user.model_dump_json(indent=2)
    print('\n', user_json, '\n')

    ## get_secret_value() method is used to display the password('**********') into plain text. 
    print(user.password.get_secret_value()) 




## initialize post object default value to None
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

