import chess.pgn
import json
import os

# Convert board to 2D array
def board_to_2d(board):
    board_str = board.board_fen()
    rows = board_str.split('/')
    matrix = []

    for row in rows:
        expanded = ""
        for char in row:
            if char.isdigit():
                expanded += '.' * int(char)
            else:
                expanded += char
        matrix.append(list(expanded))

    return matrix

# Sanitize filename to remove invalid characters
def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')

# Read all games in a single PGN file
def extract_all_games_from_pgn(pgn_path):
    games = []
    with open(pgn_path) as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            games.append(game)
    return games

# Convert PGN to 2D move frames per game
def convert_game_to_move_frames(game):
    board = game.board()
    move_frames = []

    for move in game.mainline_moves():
        board.push(move)
        move_frames.append(board_to_2d(board))

    return move_frames

# Paths
pgn_folder = 'pgn_games/'
output_folder = 'output_moves/'
os.makedirs(output_folder, exist_ok=True)

# Process each PGN file
for filename in os.listdir(pgn_folder):
    if filename.endswith(".pgn"):
        pgn_path = os.path.join(pgn_folder, filename)
        games = extract_all_games_from_pgn(pgn_path)[:1]  # Only take the first game

        for idx, game in enumerate(games):
            move_frames = convert_game_to_move_frames(game)
            event = sanitize_filename(game.headers.get('Event', 'UnknownEvent'))
            output_filename = f"{event}_{filename[:-4]}_Match{idx+1}_moves.json"
            output_path = os.path.join(output_folder, output_filename)

            # Add empty lines between moves for visualization spacing
            spaced_frames = []
            for frame in move_frames:
                spaced_frames.append(frame)
                spaced_frames.append([])

            with open(output_path, 'w') as out_file:
                json.dump(spaced_frames, out_file)

            print(f"Saved: {output_path}")
