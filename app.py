#CONSTANTS:
BLACK, WHITE =  "black", "white" # colors
A, B, C, D, E, F = 0, 1, 2, 3, 4, 5 # sectors
ORIGIN = (0,0,0)
NUM_SECTORS = 6
U, R, L = 0, 1, 2 # directions
S,X,Y,Z = 0, 1, 2, 3 # coordinates
SIZE, OPENINGS = 0, 1 # monster parts
OPENING_SPOT, DIRECTION_OF_NEIGHBOR = 0, 1 #opening parts

#GLOBAL VARIABLES:
class Palago:
    def __init__(self):
        self.occupied_spots = {ORIGIN}
        self.placeable_spots = {
            (A, 1, 1),(B, 1, 1),(C, 1, 1), (D, 1, 1), (E, 1, 1),(F, 1, 1),
        }
        # format is (size, openings). format of opening is (spot, direction of neighbor)--where the black tip is)
        self.monsters = {BLACK: [ #black starting monsters
            (0,
            {((A, 1, 1), L),  ((F, 1,1), R)}
            ),   
            (1,
            {((B, 1, 1), L),((C, 1, 1), U), ((D, 1, 1),U), ((E, 1, 1), R),}
            ),  
        ], WHITE:  [#white starting monsters
            (1,
            {((A, 1, 1), U), ((B, 1, 1), R), ((E, 1, 1),L), ((F, 1,1),U)}
            ),   
            (0,
            {((C, 1, 1), R), ((D, 1, 1), L)}
            ),  
        ]}
    # HELPER FUNCTIONS:
    def is_valid_spot(self, spot):
        if(spot[S] not in range (0,6)):
            return False
        if(spot[Y] > spot[X]):
            return False
        if(spot[Y] <= 0 or spot[X] <= 0):
            return False 
        return True

    def get_neighbors(self, spot):
        s,x,y = spot
        if(spot[X] == 1): # at tip of sector, in clockwise order starting at origin
            return {ORIGIN, ((s-1)%NUM_SECTORS, 1, 1), ((s-1)%NUM_SECTORS,2,2), (s,x+1,y), (s,x+1,y+1), ((s+1)%NUM_SECTORS, 1, 1)}
        if(spot[Y] == 1): # at beginning of sector, in clockwise order starting at origin
            return {(s,x-1,y), ((s-1)%NUM_SECTORS, x, x), ((s-1)%NUM_SECTORS,x+1,x+1), (s,x+1,y), (s,x+1,y+1),(s,x,y+1)}
        if(spot[Y] == spot[X]): #at end of sector
            return {(s,x+1,y), (s,x+1,y+1), (s,x,y-1),((s+1)%NUM_SECTORS, x, 1), ((s+1)%NUM_SECTORS, x-1, 1), (s,x-1,y-1)}
        # normal case
        return {(s,x+1,y), (s,x+1,y+1), (s,x,y-1),(s,x,y+1), (s,x-1,y), (s,x-1,y-1)}
            
    def are_neighbors(self, spot1,spot2):
        return spot1 in self.get_neighbors(spot2)
            
    def get_possible_first_spots(self):
        return self.placeable_spots

    def get_possible_second_spots(self, first_spot):
        self.get_open_neighbors(first_spot)

    def get_open_neighbors(self, spot):
        return self.get_neighbors(spot) - self.occupied_spots

    def is_won(self, color):
        return any(map(lambda monster: len(monster[OPENINGS])==0,  self.monsters[color]))

    def is_closable_in_one_move(self, color): #TODO: this should return the closable monsters really
        colored_monsters = self.monsters[color]
        for monster in colored_monsters:
            if len(monster[OPENINGS]) < 2:
                return monster[SIZE] >= 1
            if len(monster[OPENINGS]) == 2:
                pair = list(monster[OPENINGS])
                return self.are_neighbors(pair[0][OPENING_SPOT], pair[1][OPENING_SPOT]) and monster[SIZE] >= 1
        return False
    
    #gets two neighbors in the direction requested based on tip of color
    def get_two_openings_in_direction(self, color, spot, direction):
        s,x,y = spot
        if(spot[X] == 1): # at tip of sector, in clockwise order starting at origin
            neighbors_list = [ORIGIN, ((s-1)%NUM_SECTORS, 1, 1), ((s-1)%NUM_SECTORS,2,2), (s,x+1,y), (s,x+1,y+1), ((s+1)%NUM_SECTORS, 1, 1)]
        elif(spot[Y] == 1): # at beginning of sector, in clockwise order starting at origin
            neighbors_list = [(s,x-1,y), ((s-1)%NUM_SECTORS, x, x), ((s-1)%NUM_SECTORS,x+1,x+1), (s,x+1,y), (s,x+1,y+1),(s,x,y+1)]
        elif(spot[Y] == spot[X]): #at end of sector, in clockwise order
            neighbors_list = [((s+1)%NUM_SECTORS, x-1, 1), (s,x-1,y-1), (s,x,y-1), (s,x+1,y), (s,x+1,y+1),((s+1)%NUM_SECTORS, x, 1)]
        else:# normal case
            neighbors_list = [(s,x-1,y), (s,x-1,y-1),  (s,x,y-1), (s,x+1,y), (s,x+1,y+1),(s,x,y+1)]
        if(color==BLACK):
            if(direction == U):
                return {(neighbors_list[2-s], R),(neighbors_list[3-s], L)}
            if(direction == R):
                return {(neighbors_list[4-s], L),(neighbors_list[5-s], U)}
            if(direction == L):
                return {(neighbors_list[0-s], U),(neighbors_list[1-s], R)}
        if(color==WHITE):
            if(direction == U):
                return {(neighbors_list[5-s],R),(neighbors_list[0-s],L)}
            if(direction == R):
                return {(neighbors_list[1-s],L),(neighbors_list[2-s],U)}
            if(direction == L):
                return {(neighbors_list[3-s],U),(neighbors_list[4-s],R)}

    def update_monsters_on_placement(self, spot, direction):
        tip_attached_flag = {BLACK: False, WHITE: False}
        for color in [BLACK, WHITE]:
            for monster in self.monsters[color]:
                if((spot,direction) in monster[OPENINGS]): # black tip of a monster placed attached
                    monster[OPENINGS].remove((spot,direction))
                    tip_attached_flag[color] = True
            if(not tip_attached_flag[color]): # a new tip is formed
                openings = self.get_two_openings_in_direction(color, spot, direction)
                monster = (0, openings)
                self.monsters[color].append(monster)
                
        # TODO: handle the bridge case
                
    def place_tile(self, spot, direction):
        self.update_monsters_on_placement(spot, direction)
        self.occupied_spots.add(spot)
        new_placable_spots = self.get_open_neighbors(spot) - self.occupied_spots
        self.placeable_spots.remove(spot)
        self.placeable_spots = self.placeable_spots.union(new_placable_spots)

    def make_move(self, spot1, spot2, direction1, direction2):
        # TODO: check validity of move 
        self.place_tile(spot1, direction1)
        self.place_tile(spot2, direction2)





# UI FUNCTIONS: 
def print_monster(monster):
    print("Size: ", monster[SIZE], " : ")
    for opening in list(monster[OPENINGS]):
        spot = opening[OPENING_SPOT]
        sector = ["A","B","C","D","E","F"][spot[S]]
        direction = ["U","R","L"][opening[DIRECTION_OF_NEIGHBOR]]
        print(sector, spot[X], spot[Y], "-", direction)

def print_state(game):
    print("Occupied Spots: ", game.occupied_spots)
    print("Placeable Spots: ", game.placeable_spots)
    print("Black Monsters: ")
    for monster in game.monsters[BLACK]:
        print_monster(monster)
    print("White Monsters: ")
    for monster in game.monsters[WHITE]:
        print_monster(monster)
def main():
    game = Palago()
    print_state(game)
    game.place_tile((B,1,1), L)
    print_state(game)
    
    
if (__name__ == "__main__"):
    main()
    
