# Bowling Simulator
This project simulates bowling games, allowing the user to compute bowling scores.

## Interactive game
To launch an interactive prompt to compute the score of a bowling game as it is being played, just launch the 
`main_game` file as following (The user must be located at the root of the project too do so.):

`python main_game [player_name]...`

If the user provides no name, a single-player game will be launched, using the default name.
 
## Compute score
To compute the score of an already played bowling game, just launch the `main_score` file with the number of
knocked down pins at each throwing (The user must be located at the root of the project too do so):

`python main_score [throwing_result]...`

For example, to compute the score of a spare, followed by a hole, one can compute the score as following:

`python main_score 3 7 5 1`

And the script will display the resulting score (21)

## Unit tests
To launch the unit tests, just launch the unittest module on the test folder.
The user must be located at the root of the project too do so.

`python -m unittest discover test`