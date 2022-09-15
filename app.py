#CONSTANTS:
from sqlalchemy import false, true


BLACK, WHITE =  0, 1 # colors
A, B, C, D, E, F = 0, 1, 2, 3, 4, 5 # sectors
NUM_SECTORS = 6
U, R, L = 0, 1, 2 # directions
S,X,Y,Z = 0, 1, 2, 3
SIZE, OPENINGS = 0, 1

#GLOBAL VARIABLES:
occupied_spots = set()
placeable_spots = {
    (A, 1, 1),(B, 1, 1),(C, 1, 1), (D, 1, 1), (E, 1, 1),(F, 1, 1),
}
monsters = ([
    (1,
     {(A, 1, 1),  (F, 1,1)}
    ),   
    (0,
     {(B, 1, 1),(C, 1, 1), (D, 1, 1), (E, 1, 1),}
    ),  
], [
    (1,
     {(A, 1, 1), (B, 1, 1), (E, 1, 1), (F, 1,1)}
    ),   
    (0,
     {(C, 1, 1), (D, 1, 1)}
    ),  
])

# HELPER FUNCTIONS:
def is_valid_spot(spot):
    if(spot[S] not in range (0,6)):
        return false
    if(spot[Y] > spot[X]):
        return false
    if(spot[Y] <= 0 or spot[X] <= 0):
        return false 
    return true

def get_neighbors(spot):
    s,x,y = spot
    if(spot[X] == 1): # at tip of sector
        return {(s,x+1,y), (s,x+1,y+1), ((s-1)%NUM_SECTORS, 1, 1),((s+1)%NUM_SECTORS, 1, 1), ((s-1)%NUM_SECTORS,2,2)}
    if(spot[Y] == 1): # at beginning of sector
        return {(s,x+1,y), (s,x+1,y+1),(s,x,y+1), (s,x-1,y), ((s-1)%NUM_SECTORS, x, x), ((s-1)%NUM_SECTORS,x+1,x+1)}
    if(spot[Y] == spot[X]): #at end of sector
        return {(s,x+1,y), (s,x+1,y+1), (s,x,y-1),((s+1)%NUM_SECTORS, x, 1), ((s+1)%NUM_SECTORS, x-1, 1), (s,x-1,y-1)}
    # normal case
    return {(s,x+1,y), (s,x+1,y+1), (s,x,y-1),(s,x,y+1), (s,x-1,y), (s,x-1,y-1)}
        
def are_neighbors(spot1,spot2):
    return spot1 in get_neighbors(spot2)
         
def get_possible_first_spots():
    return placeable_spots

def get_possible_second_spots(first_spot):
    return get_neighbors(first_spot) - occupied_spots

def is_won(color):
    return any(map(lambda monster: len(monster[OPENINGS])==0,  monsters[color]))

def is_winnable_in_one_move(color):
    colored_monsters = monsters[color]
    for monster in colored_monsters:
        if len(monster[OPENINGS]) < 2:
            return true
        if len(monster[OPENINGS]) == 2:
            return are_neighbors(monster[OPENINGS][0], monster[OPENINGS][1])
    return any(map(lambda monster: len(monster[OPENINGS])<=2,  monsters[color]))



# UI FUNCTIONS: 
def print_state():
    print("Occupied Spots: ", occupied_spots)
    print("Placeable Spots: ", placeable_spots)
    print("Black Monsters: ", monsters[BLACK])
    print("White Monsters: ", monsters[WHITE])

def main():
    print_state()
    
    
if (__name__ == "__main__"):
    main()
    print(get_possible_second_spots((5,2,2)))
    print(is_won(BLACK))
