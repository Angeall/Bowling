[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6adf93bec91a4ce9ae80b0d61b4052c7)](https://www.codacy.com/app/angeal1105/Bowling?utm_source=github.com&utm_medium=referral&utm_content=Angeall/Bowling&utm_campaign=badger)
[![Build Status](https://travis-ci.org/Angeall/Bowling.svg?branch=master)](https://travis-ci.org/Angeall/Bowling)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6adf93bec91a4ce9ae80b0d61b4052c7)](https://www.codacy.com/app/angeal1105/Bowling?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Angeall/Bowling&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/Angeall/Bowling/badge.png?branch=master)](https://coveralls.io/github/Angeall/Bowling?branch=master)

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
