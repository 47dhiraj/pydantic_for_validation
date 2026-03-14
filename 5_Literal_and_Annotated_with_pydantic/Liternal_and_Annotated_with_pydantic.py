from datetime import UTC, datetime

from typing import Literal, Annotated

from functools import partial

from pydantic import BaseModel, Field, ValidationError



## Annotated is used to attach extra metadata or validation rules or constraints to a variable(field).

## Literal is used to restrict a field(variable) to a fixed set of exact multiple values.




class User(BaseModel):
    uid: Annotated[int, Field(gt=0)]                                    
    username: Annotated[str, Field(min_length=3, max_length=50, description="username of a user")]
    age: Annotated[int, Field(ge=18, le=120, description="age of a user")]                           
    email: str                                 

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



## initialize user object default value to None
user = None


try:

    # ## First Testing on Invalid User

    # user = User(
    #     uid=0,            
    #     username="JD",
    #     age=17,
    #     bio="King of the World"
    # )

    ## Finally, Testing on a valid user

    user = User(
        uid=1,            
        username="Johndoe",
        age=18,
        email="John.doe@gmail.com",
        bio="King of the World"
    )

except ValidationError as e:
    ## print(e)

    for err in e.errors():
        location = " -> ".join(str(l) for l in err['loc'])
        message = err['msg']
        provided_input = err['input']
        provided_type = type(err['input'])
        valid_type = err['type']
        print(f"\n Field: {location}\n Error: {message}\n Input Data: {provided_input}\n Input Type: {provided_type}\n Valid Type: {valid_type}\n")



if user is not None:

    # user_dict = user.model_dump()
    # print(user_dict)

    user_json = user.model_dump_json(indent=2)
    print('\n', user_json, '\n')





## initialize post object default value to None
post = None


try:

    # ## First Testing on Invalid blog post

    # post = BlogPost(
    #     title="Py",
    #     content="Py",
    #     author_id="One",
    # )


    ## Finally, Testing on a valid blog post

    post = BlogPost(
        title="Getting Started with Python",
        content="This blog post is all about the basics of python ...",
        author_id=1,
        slug="getting-started-with-python",
    )



except ValidationError as e:
    ## print(e)

    for err in e.errors():
        location = " -> ".join(str(l) for l in err['loc'])
        message = err['msg']
        provided_input = err['input']
        provided_type = type(err['input'])
        valid_type = err['type']
        print(f"\n Field: {location}\n Error: {message}\n Input Data: {provided_input}\n Input Type: {provided_type}\n Valid Type: {valid_type}\n")





if post is not None:

    # post_dict = post.model_dump()
    # print(post_dict)


    post_json = post.model_dump_json(indent=2)
    print('\n',post_json,'\n')

