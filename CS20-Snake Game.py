##############################
# Hyder Shahzaib Ahmed
# Major Project
# Snake Game
##############################

# Importing all the necessary modules
import pygame
import random
import easygui_qt as ez
# Initialize Pygame
pygame.init()
# This initializes the music module
pygame.mixer.init()

# All variables
level_choices = ["Level 1", "Level 2", "Level "
                                       "3", "Level 4", "Extreme"]
shape_choices = ["Circular", "Rectangular"]
user_choices = open("users.txt", "r").read().split()
new_user_name = ""
user_highscore = []
width, height = 1000, 800
speed = 15
snake_size = 40
score = 0
cause = None
game_over = False
food_spawn = True
paused = False
black = pygame.Color("black")
white = pygame.Color("white")
red = pygame.Color("red")

# Load the background image
background = pygame.image.load("background.png")
# Load the sound effect for food
bite = pygame.mixer.Sound("foodbite_effect.mp3")
# Setting up initial snake position and direction
snake_head = [120, 80]
snake_body = [[160, 80], [120, 80], [120, 80]]
direction = "RIGHT"
# Setting up the game window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
# Setting up the game clock to use for fps
clock = pygame.time.Clock()
# Set up initial food position
food_pos = [random.randrange(1, (width // snake_size)) * snake_size, random.randrange(1, (height // snake_size)) * snake_size]


# The following code pops the last object in the list because python is weird and adds nothing as a choice
if user_choices[-1] == "":
    user_choices.pop()

# Getting who is playing today
user = ez.get_choice("Who is playing today?", "User", user_choices)
# Exits if user cancels to choose
if user is None:
    exit()

# Creating a new user and updating the list
elif user == "NewUser":
    new_user_name = ez.get_string("What is your name?", "New User", "No Numbers, only letters")
    if new_user_name is None:
        exit()

    # Before doing anything, explaining to user how to play
    ez.show_message("Controlling the snake: \'ARROW KEYS\'             "
                    "Pausing the game: \'SPACEBAR\'", "How to control")

    open(f"{new_user_name}.txt", 'x')

# Gets the chosen user's data
else:
    user_highscore = open(f"{user}.txt", "r").read().split("=")

# Ask important questions regarding the game
level_choice = ez.get_choice("What level would you like to play on?", "Choose your level", level_choices)
# Exits if user cancels to choose
if level_choice is None:
    exit()

# The following bit sets the levels of difficulty for the player to their choice
elif level_choice == "Level 1":
    snake_size = 40
    speed = 10
    music = pygame.mixer.music.load("level1_music.mp3")
elif level_choice == "Level 2":
    snake_size = 40
    speed = 15
    music = pygame.mixer.music.load("level2_music.mp3")
elif level_choice == "Level 3":
    snake_size = 20
    speed = 20
    music = pygame.mixer.music.load("level3_music.mp3")
elif level_choice == "Level 4":
    snake_size = 20
    speed = 25
    music = pygame.mixer.music.load("level4_music.mp3")
elif level_choice == "Extreme":
    snake_size = 20
    speed = 35
    music = pygame.mixer.music.load("extreme_music.mp3")

# Ask the user to choose the shape of the snake
shape_choice = ez.get_choice("What shape would you like the snake to be?", "Choose snake shape", shape_choices)
# Exits if user cancels to choose
if shape_choice is None:
    exit()
# Set the snake shape based on user choice
elif shape_choice == "Circular":
    is_circular = True
else:
    is_circular = False


# Function to display score on the screen
def display_score(score_type, score_value, score_alignment):
    font = pygame.font.SysFont('Arial', 24)
    score_surface = font.render(f"{score_type}: {score_value}", True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (width / score_alignment, 10)
    win.blit(score_surface, score_rect)


# The little popup screen for when the game ends
def end_game():
    ez.show_message(f"Your final score was {score} and the cause was {cause.lower()}", "Game Over")


# The following bit allows the music to loop forever
pygame.mixer.music.play(-1)

# The actual code that runs the game
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_SPACE:  # Added pause functionality with the SPACE key
                paused = not paused

    if not paused:  # Only update the game state if not paused
        # Update snake position based on the direction
        if direction == "RIGHT":
            snake_head[0] += snake_size
        elif direction == "LEFT":
            snake_head[0] -= snake_size
        elif direction == "UP":
            snake_head[1] -= snake_size
        elif direction == "DOWN":
            snake_head[1] += snake_size

        # Check if the snake ate the food
        if snake_head == food_pos:
            bite.play()
            score += 1
            food_spawn = False
        else:
            if snake_body:
                snake_body.pop(0)

        # Spawn new food if necessary
        if not food_spawn:
            food_pos = [random.randrange(1, (width // snake_size)) * snake_size, random.randrange(1, (height // snake_size)) * snake_size]
            food_spawn = True

        # Check for collision with the boundaries of the window
        if snake_head[0] >= width or snake_head[0] < 0 or snake_head[1] >= height or snake_head[1] < 0:
            game_over = True
            cause = "The snake collided with the boundaries."

        # Check for collision with the snake's body
        for block in snake_body[1:]:
            if snake_head == block:
                game_over = True
                cause = "The snake head hit the body."

        # Add new head to the snake's body
        snake_body.append(list(snake_head))

    # Set the background image
    win.blit(background, (0, 0))

    # Draw the snake
    for pos in snake_body:
        if is_circular:
            pygame.draw.circle(win, white, (pos[0] + snake_size // 2, pos[1] + snake_size // 2), snake_size // 2)
        else:
            pygame.draw.rect(win, white, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    # Draw the food
    if is_circular:
        pygame.draw.circle(win, red, (food_pos[0] + snake_size // 2, food_pos[1] + snake_size // 2), snake_size // 2)
    else:
        pygame.draw.rect(win, red, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

    # Display the score
    display_score("Score", score, 2)
    if user != "NewUser":
        if user_highscore[1] == level_choice:
            if score > int(user_highscore[2]):
                display_score(f"Highest score ({level_choice})", score, 4)
            else:
                display_score(f"Highest score ({level_choice})", int(user_highscore[2]), 4)

        elif user_highscore[3] == level_choice:
            if score > int(user_highscore[4]):
                display_score(f"Highest score ({level_choice})", score, 4)
            else:
                display_score(f"Highest score ({level_choice})", int(user_highscore[4]), 4)

        elif user_highscore[5] == level_choice:
            if score > int(user_highscore[6]):
                display_score(f"Highest score ({level_choice})", score, 4)
            else:
                display_score(f"Highest score ({level_choice})", int(user_highscore[6]), 4)

        elif user_highscore[7] == level_choice:
            if score > int(user_highscore[8]):
                display_score(f"Highest score ({level_choice})", score, 4)
            else:
                display_score(f"Highest score ({level_choice})", int(user_highscore[8]), 4)
        elif user_highscore[9] == level_choice:
            if score > int(user_highscore[10]):
                display_score(f"Highest score ({level_choice})", score, 4)
            else:
                display_score(f"Highest score ({level_choice})", int(user_highscore[10]), 4)

    # Update the game display
    pygame.display.update()

    # Set the game's FPS
    clock.tick(speed)

# Creates a new user text file and appends the current game details
if user == "NewUser":
    with open("users.txt", 'a') as f:
        f.write(f"\n{new_user_name}")
    if level_choice == "Level 1":
        with open(f"{new_user_name}.txt", 'w') as f:
            f.write(f"Highscore=Level 1={score}=Level 2=0=Level 3=0=Level 4=0=Extreme=0")
    elif level_choice == "Level 2":
        with open(f"{new_user_name}.txt", 'w') as f:
            f.write(f"Highscore=Level 1=0=Level 2={score}=Level 3=0=Level 4=0=Extreme=0")
    elif level_choice == "Level 3":
        with open(f"{new_user_name}.txt", 'w') as f:
            f.write(f"Highscore=Level 1=0=Level 2=0=Level 3={score}=Level 4=0=Extreme=0")
    elif level_choice == "Level 4":
        with open(f"{new_user_name}.txt", 'w') as f:
            f.write(f"Highscore=Level 1=0=Level 2=0=Level 3=0=Level 4={score}=Extreme=0")
    elif level_choice == "Extreme":
        with open(f"{new_user_name}.txt", 'w') as f:
            f.write(f"Highscore=Level 1=0=Level 2=0=Level 3=0=Level 4=0=Extreme={score}")

# Appends an already existing user file to save the user game data
if user != "NewUser":
    if user_highscore[1] == level_choice:
        if score > int(user_highscore[2]):
            with open(f"{user}.txt", 'w') as f:
                f.write(f"Highscore=Level 1={score}=Level 2={user_highscore[4]}=Level 3={user_highscore[6]}=Level 4={user_highscore[8]}=Extreme={user_highscore[10]}")

    elif user_highscore[3] == level_choice:
        if score > int(user_highscore[4]):
            with open(f"{user}.txt", 'w') as f:
                f.write(f"Highscore=Level 1={user_highscore[2]}=Level 2={score}=Level 3={user_highscore[6]}=Level 4={user_highscore[8]}=Extreme={user_highscore[10]}")

    elif user_highscore[5] == level_choice\
            :
        if score > int(user_highscore[6]):
            with open(f"{user}.txt", 'w') as f:
                f.write(f"Highscore=Level 1={user_highscore[2]}=Level 2={user_highscore[4]}=Level 3={score}=Level 4={user_highscore[8]}=Extreme={user_highscore[10]}")

    elif user_highscore[7] == level_choice:
        if score > int(user_highscore[8]):
            with open(f"{user}.txt", 'w') as f:
                f.write(f"Highscore=Level 1={user_highscore[2]}=Level 2={user_highscore[4]}=Level 3={user_highscore[6]}=Level 4={score}=Extreme={user_highscore[10]}")

    elif user_highscore[9] == level_choice:
        if score > int(user_highscore[10]):
            with open(f"{user}.txt", 'w') as f:
                f.write(f"Highscore=Level 1={user_highscore[2]}=Level 2={user_highscore[4]}=Level 3={user_highscore[6]}=Level 4={user_highscore[8]}=Extreme={score}")

# Stops music
pygame.mixer.music.pause()

# Display the end game message
end_game()

# Quit Pygame
pygame.quit()
