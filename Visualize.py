import json
import os
import pygame
import time

pygame.init()

PIECE_IMAGES = {
    'r': pygame.image.load("PNG/ROCK BLACK.png"),
    'n': pygame.image.load("PNG/KNIGHT BLACK.png"),
    'b': pygame.image.load("PNG/BISHOP BLACK.png"),
    'q': pygame.image.load("PNG/QUEEN BLACK.png"),
    'k': pygame.image.load("PNG/KING BLACK.png"),
    'p': pygame.image.load("PNG/PAWN BLACK.png"),
    'R': pygame.image.load("PNG/ROCK WHITE.png"),
    'N': pygame.image.load("PNG/KNIGHT WHITE.png"),
    'B': pygame.image.load("PNG/BISHOP WHITE.png"),
    'Q': pygame.image.load("PNG/QUEEN WHITE.png"),
    'K': pygame.image.load("PNG/KING WHITE.png"),
    'P': pygame.image.load("PNG/PAWN WHITE.png"),
}

infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

GRID_ROWS = 3
GRID_COLS = 5

# Calculate cell width and height based on the screen size and grid dimensions
CELL_WIDTH = SCREEN_WIDTH // GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT // GRID_ROWS

# Force square cell (use the smaller dimension)
SQUARE_SIZE = min(CELL_WIDTH, CELL_HEIGHT)

# Calculate margins to center the grid
x_margin = (SCREEN_WIDTH - (SQUARE_SIZE * GRID_COLS)) // 2
y_margin = (SCREEN_HEIGHT - (SQUARE_SIZE * GRID_ROWS)) // 2

# Force square cell (use the smaller dimension)
SQUARE_SIZE = min(CELL_WIDTH, CELL_HEIGHT)
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

def visualize_board(surface, board_2d, x_offset, y_offset):
    square_width = CELL_WIDTH // 8
    square_height = CELL_HEIGHT // 8
    scale_factor = 0.9  # 90% of the square size

    for i, row in enumerate(board_2d):
        for j, piece in enumerate(row):
            square_x = x_offset + j * square_width
            square_y = y_offset + i * square_height

            # Alternate square color for checkerboard pattern
            color = WHITE if (i + j) % 2 == 0 else GRAY
            pygame.draw.rect(surface, color, (square_x, square_y, square_width, square_height))

            if piece != '.':
                img = PIECE_IMAGES.get(piece)
                if img:
                    new_width = int(square_width * scale_factor)
                    new_height = int(square_height * scale_factor)
                    img_scaled = pygame.transform.scale(img, (new_width, new_height))

                    # Center the image within the square
                    img_x = square_x + (square_width - new_width) // 2
                    img_y = square_y + (square_height - new_height) // 2
                    surface.blit(img_scaled, (img_x, img_y))

    pygame.draw.rect(surface, BLACK, (x_offset, y_offset, CELL_WIDTH, CELL_HEIGHT), 1)

# Show 15 games on screen
def display_matches(games, match_start_idx, move_index):
    match_limit = 15
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

        # Display the current board states
        display_matches(games, match_start_idx, move_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move to the next game move after some duration
        if time.time() - last_move_time >= move_duration:
            move_index += 1
            max_moves = get_max_moves_for_current_matches()  # Get max moves for the current 15 games

            # Check if all moves in the current game are finished
            if move_index >= max_moves:
                move_index = 0  # Reset move index for the next batch of games
                match_start_idx += 15  # Move to the next set of 15 games
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
