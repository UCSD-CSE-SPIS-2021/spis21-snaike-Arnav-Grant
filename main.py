from snake import *

# Food variables
f = Food(grid_width, grid_height)
f.relocate()

# Player variables
player = Snake(10, 10, f)

play_game(player)
