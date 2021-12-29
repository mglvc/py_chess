import chess
import chess.engine
import chess.pgn
import pandas as pd
import csv
import xlsxwriter

def print_pgn(moves_list):
    if len(moves_list)% 2 == 0:
        i = 0
        j = 1
        while i + 1 < len(moves_list):
            print(str(j) + ".", moves_list[i], moves_list[i + 1])
            i += 2
            j += 1
    else:
        i = 0
        j = 1
        while i + 2 < len(moves_list):
            print(str(j)+".", moves_list[i], moves_list[i + 1])
            i += 2
            j += 1
        print(str(j)+".", moves_list[i])

def play_dual_game(engine1, engine2, first_starts=True):
    board = chess.Board()
    game = chess.pgn.Game()
    game.from_board(board)
    moves_list = []
    while not board.is_game_over():
        result = (engine1 if first_starts else engine2).play(board, chess.engine.Limit(depth=1, nodes=1))
        moves_list.append(board.san(result.move))
        board.push(result.move)
        first_starts = not first_starts
    #moves_list.append(result.move)
    mov_list_rev = moves_list[::-1]
    if str(moves_list[-1])[-1] != "#" or str(moves_list[-1])[::-1][:2] != "++" or (mov_list_rev[0] == mov_list_rev[4] == mov_list_rev[8] and
        mov_list_rev[1] == mov_list_rev[5] == mov_list_rev[9] and
         mov_list_rev[2] == mov_list_rev[6] == mov_list_rev[10] and
         mov_list_rev[3] == mov_list_rev[7] == mov_list_rev[11]):

        winner = 0.5
    elif first_starts:
        winner = 2
    else:
        winner = 1
    print_pgn(moves_list)
    return winner

  
def check_move(right_moves, right_position, engine):
    T_F_moves = []
    i, j = 0, 0
    while j < len(right_position):
        board = chess.Board(right_position[j])
        game = chess.pgn.Game()
        game.from_board(board)
        while not board.is_game_over():
            result = engine.play(board, chess.engine.Limit(depth=1, nodes=1))
            board.push(result.move)
            move_1 = str(board.move_stack[0])
            if move_1 == right_moves[i]:
                T_F_moves.append("True")
            else:
                T_F_moves.append("False")
            break
        if j == len(right_position) - 1:
            print(board.move_stack)
        j, i = j + 1, i + 1
    print(T_F_moves)
    return T_F_moves
  
 def play_game(engine):
    board = chess.Board("3R4/2r2N2/K1kprn2/7R/3P4/8/8/8 w - - 0 1")
    game = chess.pgn.Game()
    game.from_board(board)
    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(depth=1, nodes=1))
        board.push(result.move)
    moves_list = []
    for i in range(len(board.move_stack)):
        k = (board.move_stack[i])
        #print("k=", str(k))
        moves_list.append(str(k))
    return moves_list
  
  
def test_engine():
    maia = ["""D:\mglvc\AnalyseRating\weights\\maia-1100.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1200.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1300.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1400.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1500.pb.gz""",
            """D:\mglvc\AnalyseRating\weights\\maia-1600.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1700.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1800.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1900.pb.gz"""]
    list_win = [[]]
    for i in range(1350, 2900, 50): #стокфиш
        text = 'stockfish ' + str(i)
        l1 = []
        l1.append(text)
        for j in range(9): #майя
            engine1 = chess.engine.SimpleEngine.popen_uci(["D:\mglvc\AnalyseRating\engine\stockfish11.exe"])
            engine1.configure({"UCI_elo": i})
            engine2 = chess.engine.SimpleEngine.popen_uci(["engine/lc0.exe"])
            engine2.configure({"WeightsFile": maia[j]})
            goal = ''
            if play_dual_game(engine1, engine2) == 1:
                goal += "1"
            else:
                goal += "0"
            if play_dual_game(engine2, engine1) == 2:
                goal += "1"
            else:
                goal += "0"

            engine1.quit()
            engine2.quit()
            l1.append(goal)
        list_win.append(l1)
    print(len(list_win)-1)
    return list_win
