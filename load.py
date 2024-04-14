import json

class Load:
    def __init__(self, filename):
        '''Initialize the GameLoader instance with the filename of the JSON file.'''
        self.filename = filename

    def load(self):
        '''Load game records from JSON file.'''
        game_records = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    record = json.loads(line)
                    game_records.append(self.parse_record(record))
                return game_records
        except FileNotFoundError:
            print("File not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return None

    def parse_record(self, record):
        '''Parse a single game record and extract required information.'''
        date = record.get('date')
        winner = record.get('winner')
        moves = [move['column'] for move in record.get('moves', [])]
        return {'date': date, 'winner': winner, 'moves': moves}