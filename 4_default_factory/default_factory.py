from datetime import UTC, datetime
from pydantic import BaseModel, Field, ValidationError
from functools import partial




class User(BaseModel):
    uid: int
    username: str
    email: str
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None
    



class BlogPost(BaseModel):
    title: str
    content: str
    view_count: int = 0
    is_published: bool = False

    '''
        Pydantic's default_factory, allows to store a callable function(a function that can be called whenever needed(not when .py file is run)) rather than storing a fixed value.
    '''
    tags: list[str] = Field(default_factory=list)


    '''
        here, lamda is just a python anonymous function, which will only gets executed, when default_factory _factory() is called.
    '''
    # created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC)) 
    

    created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    '''

        here, partial() creates a new callable function by pre-filling arguments of an existing function
        partial() is not only a function, it is also a python class
        partial works on OOP aaproach rather than functional approach

        Behind the scene, this happens : 

        p = partial(datetime.now, tz=UTC)

        when, a object like p is created, internally python do these below things, as we all know, it is basic python obj creation concept.

            partial.__new__(partial, datetime.now, tz=UTC) → returns a new partial instance

            partial.__init__(instance, datetime.now, tz=UTC) → initializes func, args, keywords

                So, inside __init__ or constructor this happends

                    self.func = datetime.now
                    self.args = ()
                    self.keywords = {'tz': UTC}
        

        Now, the partial object is being called like this p(), behind the scene this happens

            p.__call__()

            and the above line call this definition internally

            def __call__(self, *args, **kwargs):
            
                new_args = self.args + args
                new_kwargs = {**self.keywords, **kwargs}

                return self.func(*new_args, **new_kwargs)

            
    '''