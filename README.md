# Game Selector

Find good and bad games

## Help

```
usage: game-selector [-h] --input INPUT --output-good OUTPUT_GOOD --output-bad
                     OUTPUT_BAD --engine ENGINE [--hash HASH] [--threads THREADS]      
                     [--move-time-sec MOVE_TIME_SEC] [--score-margin SCORE_MARGIN] [-v]

Separate good and bad games

options:
  -h, --help            show this help message and exit
  --input INPUT         Input pgn filename (required=True).
  --output-good OUTPUT_GOOD
                        Output filename for good games (required=True).
  --output-bad OUTPUT_BAD
                        Output filename for bad games (required=True).
  --engine ENGINE       engine filename (required=True).
  --hash HASH           engine hash size (required=False, default=128).
  --threads THREADS     engine threads to use (required=False, default=1).
  --move-time-sec MOVE_TIME_SEC
                        movetime in seconds (required=False, default=1).
  --score-margin SCORE_MARGIN
                        score margin in pawn unit (required=False, default=7.0).       
  -v, --version         show program's version number and exit
```

## Command line

```
python main.py --input mypgn.pgn --output-good good.pgn --output-bad bad.pgn --engine stockfish_15_modern.exe --hash 128 --threads 1 --move-time-sec 2
```

## Clone the repository

Copy all files in this repository.

```
git clone https://github.com/fsmosca/gameselector.git
```


