In an environment witout walls, traps, multiple floors, multiple agents, etc, etc...
It is not only possible for the win rate to be nearly 100%, but likely (if it were a human playing).
In this state, the game is quite trivial. You always know where the guard will ends its turn, and you also know where you are.
In that simplified environment, much of the challenge of the game simply isn't present.

So, as a benchmark, it would be beneficial to see how well an agent can perform in such an environment, to show that the agents are capable of learning how to exploit the environment before more features get added.

In this environment, the agent was trained on 300,000 iterations at a fixed epsilon of 0.2.
Then, the agent played another 300,000 iterations with the epislon set to 0 (purely exploiting, no exploring).
The benchmark win rate achieved was: 93%
(TOTAL WINS: 278783 TOTAL LOSSES: 21217)