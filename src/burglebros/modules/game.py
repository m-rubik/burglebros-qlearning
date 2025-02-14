"""
"""

from burglebros.modules.floor import Floor
from burglebros.modules.agent import Agent
from burglebros.configs.configs import *
from burglebros.utilities.vprint import vprint

class Game():
    def __init__(self, max_turns=200, agent_count=1, floor_count=1):
        self.max_turns = max_turns
        self.agent_count = agent_count
        self.floor_count = floor_count

        self.floors = []
        self.agents = []

    def setup_game(self):
        for i in range(self.agent_count):
            self.agents.append(Agent(agent_number=i, stealth=STEALTH_TOKENS, actions_per_turn=AGENT_ACTIONS_PER_TURN))

        for i in range(self.floor_count):
            self.floors.append(Floor(floor_number=i, grid_size=GRID_SIZE))

        for floor in self.floors:
            floor.generate_random_layout()
            if PRINT_VERBOSE:
                vprint(f"Average Reachability: {round(floor.gu.avg_reachability*100)}%")
                floor.gu.plot_network()

        for agent in self.agents:
            agent.add_floor(self.floors[0])

    def play_game(self):
        game_over = False
        escaped_agents = []
        for _ in range(self.max_turns):
            if len(escaped_agents) == self.agent_count:
                game_over = "WIN"
                break
            for agent in self.agents:
                if not agent.escaped:

                    # Agent takes their turn, using all of their actions
                    agent.take_turn()
                    if agent.stealth == -1:
                        game_over = "LOSS_FROM_STEALTH"
                        break
                    
                    # Then the guard on the floor where the agent ended its turn takes a turn
                    agent.floor.guard.take_turn()

                    # This system doesn't actually punish agents for ending their turn somewhere and then having another agents turn cause the guard to move into their spot
                    # We actually would have to wait until all agents have taken their turn, then apply the reward from the last action each agent took
                    for agent_i in self.agents:
                        if agent_i.floor.number == agent.floor.number: # If agent is on the same floor as the guard that just moved
                            if (agent_i.x, agent_i.y) == (agent.floor.guard.x, agent.floor.guard.y): # Check if the guard has ended its turn on an agent
                                agent_i.stealth -= 1 # Lose a stealth token
                                agent_i.reward += PUNISHMENT_FOR_LOSING_STEALTH # Punish for losing stealth
                                agent_i.stats['counter_guard_move_into_agent'] += 1
                                if agent_i.stealth == -1: # Game is over if agent loses stealth when they have no spare tokens
                                    agent_i.reward += PUNISHMENT_FOR_LOSING
                                    game_over = "LOSS_FROM_STEALTH"
                                    break
                    agent.resolve_end_of_guards_turn()

            for agent in self.agents:
                if agent.escaped:
                    escaped_agents.append(agent)
            if game_over:
                break
        for agent in self.agents:
            vprint(f"{agent.stats}")
        if game_over:
            return game_over
        else:
            return "LOSS_FROM_TIME"
            