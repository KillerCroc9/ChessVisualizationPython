import json
import os
import pygame
import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 800
GRID_ROWS, GRID_COLS = 3, 3
CELL_WIDTH = SCREEN_WIDTH // GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT // GRID_ROWS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Matches Visualization")

output_folder = 'output_moves/'

# Load games from JSON files
def load_all_games():
    games = []
    for filename in os.listdir(output_folder):
        if filename.endswith("_moves.json"):
            json_path = os.path.join(output_folder, filename)
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    games.append(data)
            except Exception as e:
                print(f"Error with file {filename}: {e}")
    return games

# Draw a single board
def visualize_board(surface, board_2d, x_offset, y_offset):
    piece_colors = {
        'r': BLACK, 'n': BLACK, 'b': BLACK, 'q': BLACK, 'k': BLACK, 'p': BLACK,
        'R': WHITE, 'N': WHITE, 'B': WHITE, 'Q': WHITE, 'K': WHITE, 'P': WHITE,
        '.': GRAY
    }
    font = pygame.font.SysFont("Arial", min(CELL_WIDTH, CELL_HEIGHT) // 8)

    for i, row in enumerate(board_2d):
        for j, piece in enumerate(row):
            rect_color = BLACK if piece.islower() else WHITE if piece.isupper() else GRAY
            pygame.draw.rect(surface, rect_color,
                             (x_offset + j * (CELL_WIDTH // 8), y_offset + i * (CELL_HEIGHT // 8),
                              CELL_WIDTH // 8, CELL_HEIGHT // 8))
            if piece != '.':
                text = font.render(piece.lower(), True, "Red")
                text_rect = text.get_rect(center=(x_offset + j * (CELL_WIDTH // 8) + CELL_WIDTH // 16,
                                                  y_offset + i * (CELL_HEIGHT // 8) + CELL_HEIGHT // 16))
                surface.blit(text, text_rect)

    pygame.draw.rect(surface, BLUE, (x_offset, y_offset, CELL_WIDTH, CELL_HEIGHT), 5)

# Show 9 games on screen
def display_matches(games, match_start_idx, move_index):
    match_limit = 9
    match_count = 0
    game_idx = match_start_idx

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if game_idx < len(games) and match_count < match_limit:
                game_data = games[game_idx]
                game_moves = game_data
                if game_moves:
                    move = game_moves[min(move_index, len(game_moves) - 1)]
                    x_offset = col * CELL_WIDTH
                    y_offset = row * CELL_HEIGHT
                    visualize_board(WINDOW, move, x_offset, y_offset)
                    match_count += 1
                game_idx += 1
    pygame.display.update()


def display_winners(games, match_start_idx):
    font = pygame.font.SysFont("Arial", 100, bold=True)  # Large font for the word "Finished"
    text = font.render("Finished", True, "Red")
    
    # Get the center of the window
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Draw the background to cover the entire screen (optional)
    WINDOW.fill(WHITE)  # Optional: You can choose a color for the background
    
    # Draw the "Finished" text in the center of the screen
    WINDOW.blit(text, text_rect)
    
    pygame.display.update()
    time.sleep(5)  # Show the text for 5 seconds



def main():
    running = True
    games = load_all_games()
    match_start_idx = 0
    move_index = 0
    move_duration = 0.05
    last_move_time = time.time()

    # Calculate move counts for only the current 9 games
    def get_max_moves_for_current_matches():
        current_games = games[match_start_idx:match_start_idx + 9]
        return max(len(game) for game in current_games)

    while running:
        # Draw the grid once at the beginning (or when necessary)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x_offset = col * CELL_WIDTH
                y_offset = row * CELL_HEIGHT
                pygame.draw.rect(WINDOW, BLUE, (x_offset, y_offset, CELL_WIDTH, CELL_HEIGHT), 5)

        # Display the current board states
        display_matches(games, match_start_idx, move_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move to the next game move after some duration
        if time.time() - last_move_time >= move_duration:
            move_index += 1
            max_moves = get_max_moves_for_current_matches()  # Get max moves for the current 9 games

            # Check if all moves in the current game are finished
            if move_index >= max_moves:
                move_index = 0  # Reset move index for the next batch of games
                match_start_idx += 9  # Move to the next set of 9 games
                if match_start_idx >= len(games):
                    match_start_idx = 0  # Reset to start if we've reached the end of all games

                # After finishing all moves in the current set, display the winners
                display_winners(games, match_start_idx)

            last_move_time = time.time()

        # Small delay for smoother animation
        time.sleep(0.1)

    pygame.quit()

if __name__ == "__main__":
    main()
