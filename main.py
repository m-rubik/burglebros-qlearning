"""
TODO:
- Implement walls
- Implement traps + alarms
- Implement losing stealth is guard moves THROUGH a tile with an agent
- Implement 2nd floor (utilize stairs, add their location to state space and action to move up/down)
- Implement n floors with n safes?
- What happens on turn 0? What if the safe is underneath the agent at 0,0 ?
- Add a second agent

- Re-condider the definition of a hallway
"""


import pickle
import numpy as np
from burglebros.modules.game import Game
from burglebros.configs.configs import *

# Q-learning setup
# State space: (agent_x, agent_y, can_move_up, can_move_down, can_move_left, can_move_right, guard_x, guard_y, guard_target_x, guard_target_y, safe_x, safe_y, safe_cracked, action)
if LOAD_QTABLE:
    with open(QTABLE_NAME, 'rb') as file:
        q_table = pickle.load(file)
else:
    q_table = np.zeros((GRID_SIZE, 
                        GRID_SIZE,
                        2,
                        2,
                        2,
                        2,
                        GRID_SIZE, 
                        GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE, 
                        2, 
                        5))


win_counter = [0]
loss_counter = [0]
counter_loss_from_stealth = 0
counter_loss_from_turns = 0
counter_batch_wins = 0
counter_batch_losses = 0
avg_connectivities = []
BATCH_SIZE = 10000

for episode in range(NUM_ROUNDS):
    game = Game(max_turns=MAX_TURNS, agent_count=AGENT_COUNT, floor_count=FLOOR_COUNT)
    game.setup_game()
    
    for agent in game.agents:
        agent.add_q_table(q_table)

    # for floor in game.floors:
    #     avg_connectivities.append(round(floor.gu.avg_connectivity*100))

    ret_val = game.play_game()

    if ret_val == "LOSS_FROM_STEALTH":
        loss_counter.append(loss_counter[-1]+1)
        win_counter.append(win_counter[-1])
        counter_loss_from_stealth += 1
        counter_batch_losses +=1
    elif ret_val == "LOSS_FROM_TIME":
        loss_counter.append(loss_counter[-1]+1)
        win_counter.append(win_counter[-1])
        counter_loss_from_turns += 1
        counter_batch_losses += 1
    elif ret_val == "WIN":
        win_counter.append(win_counter[-1]+1)
        loss_counter.append(loss_counter[-1])
        counter_batch_wins += 1
    else:
        print("What happened?")

    
    if episode % BATCH_SIZE == 0:
        print(f"Episode {episode}")
    if episode % BATCH_SIZE == 0:
        print(f"WINS: {counter_batch_wins}, LOSSES: {counter_batch_losses} (Stealth: {counter_loss_from_stealth}, Turns: {counter_loss_from_turns})")
        counter_loss_from_stealth = 0
        counter_loss_from_turns = 0
        counter_batch_wins = 0
        counter_batch_losses = 0
        # print(sum(avg_connectivities)/len(avg_connectivities))

print("Training Complete!")
print("TOTAL WINS:", win_counter[-1], "TOTAL LOSSES:", loss_counter[-1])

if SAVE_QTABLE:
    with open(QTABLE_NAME, 'wb') as file:
        pickle.dump(q_table, file)

if not PRINT_VERBOSE:
    # PLOT STUFF
    import matplotlib.pyplot as plt

    x = [i for i in range(NUM_ROUNDS+1)]

    x_np = np.array(x)
    y_np = np.array(win_counter)

    plt.plot(x, win_counter, label="Wins", marker='o')  # Wins

    # Perform linear fit (forcing intercept to 0)
    slope, _ = np.polyfit(x_np, y_np, 1, full=False)  # Fit without intercept
    trendline = slope * x_np  # Use slope and force intercept to 0

    # Plot trendline
    plt.plot(x, trendline, label="Trendline", color="red", linestyle="--")

    # Add text with the slope value
    plt.text(x[0], trendline[0], f"Slope: {slope:.2f}", fontsize=12, color="red", verticalalignment="top")

    plt.xlabel("Episode")
    plt.ylabel("Count")
    plt.title("Total Win Count v.s Episode Number")
    plt.legend()  # Show legend
    plt.grid(True)  # Add grid for better visibility
    plt.show()