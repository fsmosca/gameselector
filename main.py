"""
Decisive games by "... wins on time" or "Error ..." or
"polyglot: resign (illegal engine move by ..." or "Xboard: Forfeit due to invalid move: ..."
where the losing side has > -7.00 according to latest SF.
"""


__script_name__ = 'game-selector'
__goal__ = 'Separate good and bad games'
__version__ = '0.2.1'


import argparse

import chess.pgn
import chess.engine


def main():
    parser = argparse.ArgumentParser(
        prog='%s' % __script_name__,
        description=__goal__, epilog='%(prog)s')
    parser.add_argument('--input', required=True, type=str,
                        help='Input pgn filename (required=True).')
    parser.add_argument('--output-good', required=True, type=str,
                        help='Output filename for good games, append mode (required=True).')
    parser.add_argument('--output-bad', required=True, type=str,
                        help='Output filename for bad games, append mode (required=True).')
    parser.add_argument('--engine', required=True, type=str,
                        help='engine filename (required=True).')
    parser.add_argument('--hash', required=False, type=int, default=128,
                        help='engine hash size (required=False, default=128).')
    parser.add_argument('--threads', required=False, type=int, default=1,
                        help='engine threads to use (required=False, default=1).')
    parser.add_argument('--move-time-sec', required=False, type=int, default=1,
                        help='movetime in seconds (required=False, default=1).')
    parser.add_argument('--score-margin', required=False, type=float, default=7.0,
                        help='score margin in pawn unit (required=False, default=7.0).')
    parser.add_argument('-v', '--version', action='version',
                        version=f'{__version__}')                        

    args = parser.parse_args()
    output_goodfn = args.output_good
    output_badfn = args.output_bad
    fn = args.input
    movetimesec = args.move_time_sec
    score_margin = args.score_margin
    enginefn = args.engine
    cnt = 0

    engine = chess.engine.SimpleEngine.popen_uci(enginefn)

    with open(fn) as h:
        while True:
            game = chess.pgn.read_game(h)
            if game is None:
                break
            cnt += 1

            result = game.headers['Result']
            is_bad = False
            is_save = True

            for node in game.mainline():
                parent_node = node.parent
                # board = parent_node.board()
                comment = node.comment                

                if 'polyglot: resign (illegal engine move' in comment:
                    is_bad = True

                elif 'Forfeit due to invalid move' in comment:
                    is_bad = True

                elif 'wins on time' in comment:
                    is_bad = True

                elif 'exited unexpectedly' in comment:
                    is_bad = True
                    
                if is_bad:
                    fen = node.board().fen()  # pos after move
                    print(f'game_num: {cnt}, result: {result}, commnent: {comment}, fen: {fen}')

                    board = chess.Board(fen)
                    info = engine.analyse(board, chess.engine.Limit(time=movetimesec))
                    score_wpov = info['score'].white().score(mate_score=32000)

                    # white loses
                    if result == '0-1' and score_wpov > -score_margin*100:
                        print(f'do not save this game, eval: {score_wpov/100} wpov')
                        is_save = False
                    # black loses
                    if result == '1-0' and score_wpov < score_margin*100:
                        print(f'do not save this game, eval: {score_wpov/100} wpov')
                        is_save = False

                    break

            if is_save:
                with open(output_goodfn, 'a') as f:
                    f.write(f'{game}\n\n')
            else:
                with open(output_badfn, 'a') as f:
                    f.write(f'{game}\n\n')                

    engine.quit()


if __name__ == '__main__':
    main()
