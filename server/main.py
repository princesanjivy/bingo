from fastapi import FastAPI
from pydantic import BaseModel
import random

class Body(BaseModel):
    name: str

# class PlayerStatus:
#     ready: int
#     has_played_once: bool 

# 0 = not ready
# 1 = ready
# 2 = won


class Bingo:
    def __init__(self):
        self.nums = [num for num in range(1, 26)]
        self.__players__ = {}
        self.started = False
        self.current_number = None
        self.all_played_once = False
        self.played = {}

    def numbers(self):
        if not self.started:
            return 1, "not started"
        
        # if self.all_not_ready() and self.is_all_played():
        if self.is_all_played():
            self.all_played_once = True
            self.current_number = None
            # reset all played to 0
            for p in self.played:
                self.played[p] = 0
            # reset all players to ready state
            # for p in self.__players__:
            #     self.__players__[p] = 1
        
        if len(self.nums) == 0:
            self.reset()

        if self.current_number is not None:
            return 0, self.current_number
        
        if self.all_played_once or self.current_number is None:
            print("generating number")
            n = random.choice(self.nums)
            self.nums.remove(n)
            self.current_number = n

        return 0, self.current_number
    
    def reset(self):
        self.nums = [num for num in range(1, 26)]
        self.__players__ = {}
        self.started = False
        self.current_number = None
        self.all_played_once = False

    def add_player(self, name):
        if name in self.__players__:
            return 1, "player exists"
        self.__players__[name] = 0
        self.played[name] = 0 # used for tracking 
        #  when to change current number for all
        return 0, self.__players__

    def players(self):
        return self.__players__
        
    def can_start(self):
        return all(status == 1 for status in self.__players__.values())
    
    def ready_player(self, name):
        if name in self.__players__:
            self.__players__[name] = 1

    def unready_player(self, name):
        if name in self.__players__:
            self.__players__[name] = 0

    def game_played(self, name):
        if name in self.played:
            self.played[name] = 1

    def is_all_played(self):
        return all(status == 1 for status in self.played.values())

    def start(self):
        self.started = True

    # def all_ready(self):
    #     return all(status == 1 for status in self.__players__.values())
        
    def all_not_ready(self):
        return all(status == 0 for status in self.__players__.values())
    
    def get_status(self, name):
        return self.__players__.get(name, None)

app = FastAPI()
bingo = Bingo()

@app.get("/")
def index():
    return {"message": "API for Bingo Game"}

@app.get("/numbers")
def number():
    s, info = bingo.numbers()
    if s != 0:
        return {"message": info}
    return {"message": {"numbers": info}}

@app.get("/players")
def players():
    return {"message": {"players": bingo.players(), "played": bingo.played}}

@app.get("/start")
def start():
    if not bingo.can_start():
        return {"message": bingo.players()}
    bingo.start()
    return {"message": "start"}

@app.get("/playerStatus")
def player_status(name: str):
    status = bingo.get_status(name)
    if status is None:
        return {"message": "player not found"}
    return {"message": {"status": status, "name": name}}

@app.post("/addPlayer")
def add_player(body: Body):
    status, plyr_info = bingo.add_player(body.name)
    if status != 0:
        return {"message": plyr_info}
    return {"message": {"players": plyr_info}}

@app.post("/newGame")
def new_game():
    bingo.reset()
    return {"message": "success"}

@app.post("/ready")
def ready(body: Body):
    bingo.ready_player(body.name)
    return {"message": "done"}

@app.post("/next")
def next(body: Body):
    return {"message": bingo.is_all_played() or bingo.all_played_once}

@app.post("/crossed")
def crossed(body: Body):
    bingo.unready_player(body.name)
    bingo.game_played(body.name)

    return {"message": "done"}



