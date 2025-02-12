PRINT_VERBOSE = False
NUM_ROUNDS = 10000
LOAD_QTABLE = True
SAVE_QTABLE = False
QTABLE_NAME = "qtable_98.pkl"
AGENT_EXPLORING = False

# Game modifiers
MAX_TURNS = 200
AGENT_COUNT = 1
AGENT_ACTIONS_PER_TURN = 4
FLOOR_COUNT = 1
STEALTH_TOKENS = 3
GRID_SIZE = 4 # The grid is a square GRID_SIZE x GRID_SIZE

### NOTE/TODO: 
# - These values do not account for walls
# - These values do not account for tiles that inhibit/impair motion
# - These values do not account for guard positioning/movement
# - These values do not account for other other agent's positioning/movement
WORST_CASE_ACTIONS_TO_FIND_SAFE = (GRID_SIZE**2)-1 # Worst case, it would take (GRID_SIZE^2)-1 actions to find the safe (agent tries every other tile and safe is on the last one)
WORST_CASE_ACTIONS_TO_ESCAPE = (GRID_SIZE-1)*2 # Worst case, it takes (GRID_SIZE-1)*2 actions to return to (safe is at opposite corner as exit)
###

### NOTE/TODO:
# - This value does not account for the "real" safe cracking mechanism
BEST_CASE_ACTIONS_TO_CRACK_SAFE = 1

PUNISHMENT_FOR_MOVING = -1 # The base "reward" for moving must be a slight punishment, else we risk the agent just moving around arbitrarily to gain rewards
PUNISHMENT_FOR_LOSING = -100 # Huge penalty for losing
PUNISHMENT_FOR_BAD_SAFE_CRACK_ACTION_USE = -75  # Punish for trying to crack a safe when not standing on a safe, or for trying to crack a safe that is already cracked

REWARD_FOR_FINDING_SAFE = 20 # Small reward for finding the safe
REWARD_FOR_SAFE_CRACK_ATTEMPT = 30 # Small reward for attempting to crack the safe while standing on it
REWARD_FOR_CRACKING_SAFE = 75 # Medium reward for cracking the safe
REWARD_FOR_WINNING = 100 # Huge reward for winning

# To determine the maximum punishment for losing stealth, we must consider the worst-case scenario, wherein the agent, through bad luck, uses:
# WORST_CASE_ACTIONS_TO_FIND_SAFE and WORST_CASE_ACTIONS_TO_ESCAPE
# Now, with respect to reward/punishment, the "worst" case scenario is actually cracking the safe on the first attempt, because each attempt rewards the agent. 
# We must also consider how much the agent is rewarded for winning.
# We must ensure that if the agent is unlucky, it still receives a net reward for escaping, even if it loses all stealth.
# This allows the agent to learn that it's not necessarily a terrible thing to lose stealth, and stealth can be sacrificed for strategic purposes.
DESIRED_REWARD_IN_WORST_CASE = 10
PUNISHMENT_FOR_LOSING_STEALTH = -1 * (((WORST_CASE_ACTIONS_TO_FIND_SAFE+WORST_CASE_ACTIONS_TO_ESCAPE)*PUNISHMENT_FOR_MOVING + REWARD_FOR_FINDING_SAFE + REWARD_FOR_CRACKING_SAFE + REWARD_FOR_SAFE_CRACK_ATTEMPT + REWARD_FOR_WINNING) - DESIRED_REWARD_IN_WORST_CASE) / STEALTH_TOKENS