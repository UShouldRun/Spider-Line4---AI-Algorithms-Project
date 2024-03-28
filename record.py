import json
import datetime

class Record:
    def __init__(self, check_game_status, coordinates, get_turn, check_player_move):
        '''This constructor initializes the attributes of the class instance with functions that are used to manage and track the state of a game. 
        Each function is passed as an argument to the constructor and is expected to perform a specific role related to the game mechanics.
        chek_game_status, coordinates and get_turn, return integer values. check_player_move returns a boolean value ''' 
        
        self.current_game = None 
        
        #functions
        self.check_game_status = check_game_status 
        self.coordinates = coordinates 
        self.get_turn = get_turn 
        self.check_player_move = check_player_move 

    def set_current_game(self, game): self.current_game = game
    def get_current_game(self): return self.current_game

    def save_game_record(self, game_record):
        '''Function to save game record to a JSON file'''
        with open('game_records.json', 'a') as f:
            json.dump(game_record, f)
            f.write('\n')

    def new_game(self):
        '''Function to start a new game'''
        return {
            'date': str(datetime.date.today()),
            'winner': None,
            'moves': []
        }

    def record_move(self, game_record, player, coordinates: str, move_time):
        '''Function to record a move in the game'''
        game_record['moves'].append({'player': player, 'column': coordinates, 'time': move_time})


    def end_game(self, game_record, winner):
        '''Function to end the game and record the winner'''
        game_record['winner'] = winner

    def record(self):
        ''' Function responsible for managing the progression of the game: starting a new game if needed, 
        recording moves if the game is ongoing and the player has made a move, 
        and ending the game if it's over or if the player hasn't made a move. '''
        if self.get_current_game() is None and self.check_game_status() == 0:        
            self.set_current_game(self.new_game()) 
        if self.set_current_game() is not None:  
            if self.check_game_status() == 0 and self.check_player_move():  
                self.record_move(self.current_game, player = f'Player {self.get_turn()}' , coordinates = self.coordinates(), move_time = datetime.datetime.now())
            else:
                self.end_game(self.get_current_game(), winner = f'Player {self.get_turn()}') 
                self.set_current_game(None) 
