# Yatzy 🎲

## How to play

1. Run `app.py` in a terminal
2. When prompted, enter how many players that will play

### Roll dice

After entering how many players, the screen will show something like this:

```
=== Round 1/15 | Player 1 | Roll 1/3
Available score boxes: 
1 Ones
2 Twos
3 Threes
4 Fours
5 Fives
6 Sixes
7 One pair
8 Two pairs
9 Three of a kind
10 Four of a kind
11 Small straight
12 Large straight
13 Full house
14 Chance
15 Yatzy

Rolled dice: 2 2 3 5 6
Enter the dice you want to keep (eg: 123): 
```

The first line tells which round it is, which player's turn it is and how many rolls the player has left in the current round.

The numbered rows below the line "Available score boxes" shows which boxes the player still has left to fill.

The penultimate line show which dice the player got. When the player has selected one or more dice from a previous turn, the selected dice will show up within parentheses like this:

```
Rolled dice: 2 2 3 (5 6)
```

On the last row the player will enter the dice they want to save (including the ones they have already saved from a previous turn). If a player want to re-roll all dice they simply leave the input empty and press enter.

### Save score

When a player is done rolling the dice they will see something like this:

```
=== Round 1/15 | Player 1 | Roll 3/3
Rolled dice: 2 4 (5 6 6)
Your final dice: 2 4 5 6 6

1 Ones 0p
2 Twos 2p
3 Threes 0p
4 Fours 4p
5 Fives 5p
6 Sixes 12p
7 One pair 12p
8 Two pairs 0p
9 Three of a kind 0p
10 Four of a kind 0p
11 Small straight 0p
12 Large straight 0p
13 Full house 0p
14 Chance 23p
15 Yatzy 0p

Select where to save your score (2-4-5-6-6): 
```

The numbered rows show the player which score boxes are available to fill and also how many points each box is worth based on the final dice.

To select a score box enter its corresponding number. For example; To add 12 points to “One pair” the player would enter `7`

When the player has selected a score box, the turn goes to the next player.