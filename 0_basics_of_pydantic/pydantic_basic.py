from pydantic import BaseModel

## Basemodel is pydantic's core class that turns type hints into runtime validated, parsed and serializable objects.


## Only that class should inherit from BaseModel, in which untrusted data enters your code/system.
class User(BaseModel):
    username: str
    email: str
    age: int



user1 = User(username="John Doe", email="john.doe@example.com", age=29)
print(user1)


## This below line of code will raise a validation error due to invalid email type and age type.
user2 = User(username="Jane Doe", email=None, age='Twenty Five')
print(user2)
