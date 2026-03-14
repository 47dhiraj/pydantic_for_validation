from datetime import datetime
from pydantic import BaseModel, ValidationError





## User class is a Pydantic BaseModel which defines the structure and data types for user information.
class User(BaseModel):
    uid: int
    username: str
    email: str
    full_name: str | None = None
    bio: str = ""
    is_active: bool = True
    joined_at: datetime | None = None
    verified_at: datetime | None = None




## Exception Handling
try:
    user = User(
        uid="1",                    
        username=None,
        email=456789123,
        bio="King of the World"
    )

except ValidationError as e:

    # print(e)

    for err in e.errors():
        # print(err)
        location = " -> ".join(str(l) for l in err['loc'])
        message = err['msg']
        provided_input = err['input']
        provided_type = type(err['input'])
        valid_type = err['type']
        print(f"\n Field: {location}\n Error: {message}\n Input Data: {provided_input}\n Input Type: {provided_type}\n Valid Type: {valid_type}\n")



# print(user.model_dump_json(indent=2))

# user_json = user.model_dump_json(indent=2)         
