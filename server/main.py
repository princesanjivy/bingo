from fastapi import FastAPI
from pydantic import BaseModel
import random

class Body(BaseModel):
    name: str

# 0 = not ready
# 1 = ready
# 2 = won

class Bingo:
    def __init__(self):
        self.nums = [num for num in range(1, 51)]
        # self.__nums_str__ = ""
        self.__players__ = {}
        self.started = False
        self.current_number = None
    
    def numbers(self):
        if not self.started:
            return 1, "not started"
        
        if len(self.nums) == 0:
            self.reset()

        if self.current_number is not None:
            return 0, self.current_number

        n = random.choice(self.nums)
        self.nums.remove(n)
        self.current_number = n

        # self.__nums_str__ += str(n) + ","
        
        return 0, self.current_number
    
    def reset(self):
        self.nums = [num for num in range(1, 51)]
        self.__nums_str__ = ""

    def add_player(self, name):
        if name in self.__players__:
            return 1, "player exists"
        self.__players__[name] = 0

        return 0, self.__players__

    def players(self):
        return self.__players__
    
    def can_start(self):
        for p in self.__players__:
            if self.__players__[p] == 0:
                return False
            
        return True
    
    def ready_player(self, name):
        for p in self.__players__:
            if p == name:
                self.__players__[p] = 1 # ready

    def un_ready_player(self, name):
        for p in self.__players__:
            if p == name:
                self.__players__[p] = 0 # not ready

    
    def start(self):
        self.started = True
    
    def __len__(self):
        print(self.__players__)
        return len(self.__players__)
    

    def all_ready(self):
        for p in self.__players__:
            if self.__players__[p] != 1:
                return False
        return True

    def all_not_ready(self):
        for p in self.__players__:
            if self.__players__[p] != 0:
                return False
        return True



app = FastAPI()
bingo = Bingo()

@app.get("/")
def index():
    return {"message": "API for Bingo Game"}

@app.get("/numbers")
def number():
    if not bingo.all_ready():
        return {"message": "not all players are ready"}
    
    s, info = bingo.numbers()
    if s != 0:
        return {"message": info}

    return {"message": {"numbers": info}}

@app.post("/newGame")
def new_game():
    bingo.reset()
    
    return {"message": "success"}

@app.get("/players")
def players():
    info = bingo.players()
    return {"message": {"players": info}}

@app.post("/addPlayer")
def add_player(body: Body):
    status, info = bingo.add_player(body.name)
    if status != 0:
        return {"message": info}
    
    return {"message": {"players": info}}

@app.get("/start")
def start():
    b = bingo.can_start()
    print(b)
    if not b:
        return {"message": bingo.players()}


    bingo.start()
    return {"message": "start"}
    
@app.post("/ready")
def ready(body: Body):
    bingo.ready_player(body.name)

    return {"message": "done"}


@app.post("/next")
def next():
    print("status")
    print(bingo.all_not_ready())
    if  bingo.all_not_ready():
        bingo.current_number = None
        return {"message": "continue"}
    
    return {"message": "wait"}

@app.post("/crossed")
def crossed(body: Body):
    bingo.un_ready_player(body.name)

    return {"message": "done"}








