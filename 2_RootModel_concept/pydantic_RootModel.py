## Why you actually need RootModel in Pydantic ??


'''

    In a typical API built around your User model, you will most likely need a RootModel when dealing with Bulk Operations or Key-Value lookups.

    sometimes your data isn't a structured object with named keys—it might just be a raw list, a string, or a dictionary with dynamic keys. 
    This is where a RootModel comes in. 

    A RootModel allows you to define a model where the entire data structure is represented by a single field, known as the "root" field.

    '''



from datetime import datetime

from pydantic import BaseModel, RootModel, Field, ValidationError




class User(BaseModel):
    uid: int
    username: str
    email: str
    full_name: str | None = None
    bio: str = ""
    is_active: bool = True
    joined_at: datetime | None = None
    verified_at: datetime | None = None




## single User
single_user_data = {
    "uid": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "joined_at": "2023-01-01T12:00:00"
}


user = User(**single_user_data)
# print(user)






class UserCollection(RootModel):

    root: list[User]


    def __iter__(self):
        return iter(self.root)


    def __getitem__(self, item):
        return self.root[item]


    def __len__(self):
        return len(self.root)






## List of Users (Bulk users, so bulk operation)
bulk_data = [
    {"uid": 1, "username": "alice", "email": "alice@test.com"},
    {"uid": 2, "username": "bob", "email": "bob@test.com", "bio": "Hello world"},
]


## validating bulk users (using RootModel i.e UserCollection)
users = UserCollection(bulk_data)

## users.root gives you access to the underlying list of User objects
# print(f"\nTotal users: {len(users.root)}\n", users.root)




if len(users) > 0:
    print(f"\nfirst user: {users[0]}")


for u in users:
    print(f"\nID: {u.uid}, Username: {u.username}, Email: {u.email}")

