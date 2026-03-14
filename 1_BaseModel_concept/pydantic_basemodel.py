from datetime import datetime
from pydantic import BaseModel, ValidationError

import json

from pprint import pprint, pformat




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



user = User(
    uid=1,
    username="john",
    email="john.doe@example.com",
)


# print(type(user))
# print(user)



## Note: Pydantic model's fields are mutable by default, which means you can change their values after instantiation.
## Note: Reassigning a value of an incorrect type to a field will not raise an error immediately.
## But, this issue can be tackled using Pydantic's model configurations or validators if strict type enforcement is desired.


## Reassigning a value of correct type to the 'bio' field.
user.bio = "Software Engineer"                            # This is valid and works fine.


## Reassigning a value of incorrect type to the 'bio' field.
# user.bio = 123456789                                    # This is invalid but does not raise an error immediately.



# ## Accessing the fields of the pydantic User model.
# print(user.uid)
# print(user.username)
# print(user.email)
# print(user.full_name)
# print(user.bio)
# print(user.is_active)
# print(user.joined_at)
# print(user.verified_at)



## To convert pydantic model to a dictionary.
## Note: Type of python dictionary is  <class 'dict'>

## model_dump() is purely pydantic v2 inbuilt method.

user_dict = user.model_dump()

print(type(user_dict))
# print(user_dict)




## To convert pydantic model to a JSON (JavaScript Object Notation).
## Note: Type of JSON is <class 'str'>


## model_dump_json() is purely pydantic v2 inbuilt method.

# user_json = user.model_dump_json()

user_json = user.model_dump_json(indent=2)          ## indent=2 is used for better display when printing.

print(type(user_json))
print(user_json)


