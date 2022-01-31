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
            g1 = play_dual_game(engine1, engine2)
            g2 = play_dual_game(engine2, engine1)
            if g1 == 1:
                goal += "1"
            elif g1 == 0.5:
                goal += "0.5"
            else:
                goal += "0"
            if g2 == 2:
                goal += "1"
            elif g2 == 0.5:
                goal += "0.5"
            else:
                goal += "0"

            engine1.quit()
            engine2.quit()
            l1.append(goal)
        list_win.append(l1)
    print(len(list_win)-1)
    return list_win

def check_users_moves_whites(right_moves, right_position, engine):
    #print(right_moves)
    i, j = 5, 0
    TF = 0
    while j < len(right_position) and i < len(right_moves):
        board = chess.Board(right_position[j])
        game = chess.pgn.Game()
        game.from_board(board)
        result = engine.play(board, chess.engine.Limit(depth=1, nodes=1))
        board.push(result.move)
        move_1 = str(board.move_stack[0])
        rm = right_moves[i]
            #print(move_1, rm)
        if move_1 == str(rm):
            TF += 1
            #print(TF, move_1, rm)

        if j == len(right_position) - 1:
            print(board.move_stack)
        j, i = j + 2, i + 2
    #print(TF)
    return TF


def check_users_moves_blacks(right_moves, right_position, engine):
    #print(right_moves)
    i, j = 6, 1
    TF = 0
    while j < len(right_position) and i < len(right_moves):
        board = chess.Board(right_position[j])
        game = chess.pgn.Game()
        game.from_board(board)
        result = engine.play(board, chess.engine.Limit(depth=1, nodes=1))
        board.push(result.move)
        move_1 = str(board.move_stack[0])
        rm = right_moves[i]
        #print(move_1, rm)
        if move_1 == str(rm):
            TF += 1
            #print(TF, move_1, rm)
        if j == len(right_position) - 1:
            print(board.move_stack)
        j, i = j + 2, i + 2
    #print(TF)
    return TF

def take_moves_from_pgn(pgn):
    games = [[]]
    pgn_open = open(pgn)
    i = 0
    first_game = chess.pgn.read_game(pgn_open)
    while first_game and i < 20000:
         if first_game.headers["Event"] == "Rated Classical game":
            if first_game.headers["Termination"] == "Normal":
                i += 1
                    #print(i)
                board = first_game.board()
                wh, wh_elo = first_game.headers["White"], first_game.headers["WhiteElo"]
                bl, bl_elo= first_game.headers["Black"], first_game.headers['BlackElo']
                    #print(i, wh, wh_elo, bl, bl_elo)
                moves = [i, wh, wh_elo, bl, bl_elo]
                for move in first_game.mainline_moves():
                    moves.append(move)
                    board.push(move)
                    #games.append(list(moves))
                arr = make_fen_from_movelist(moves)
                l1, l2 = analyse_users_engine(moves, arr)
                games.append(l1)
                games.append(l2)
         first_game = chess.pgn.read_game(pgn_open)
    df = pd.DataFrame(games[1:], columns = ['game id', 'nickname', 'elo rating', 'side', 'all moves', 'moves by gamer', '1400', '1500', '1600', '1700', '1800', '1900'])
    return df


def make_fen_from_movelist(movelist):
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    fen_board = []
    fen_board.append(fen)
    board = chess.Board(fen)
    game = chess.pgn.Game()
    game.from_board(board)
    for j in range(5, len(movelist)):
        board.push(movelist[j])
        arr = (str(board.fen).split("\'"))
        #print(arr[1])
        fen_arr = str(arr[1])
        fen_board.append(fen_arr)
    return fen_board


def analyse_users_engine(moves, positions):
    maia = ["""D:\mglvc\AnalyseRating\weights\\maia-1400.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1500.pb.gz""",
            """D:\mglvc\AnalyseRating\weights\\maia-1600.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1700.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1800.pb.gz""", """D:\mglvc\AnalyseRating\weights\\maia-1900.pb.gz"""]
    if len(moves) - 5 % 2 == 0:
        num_moves_wh = (len(moves) - 5) // 2
        num_moves_bl = num_moves_wh
    else:
        num_moves_wh = (len(moves) - 5) // 2 + 1
        num_moves_bl = num_moves_wh - 1
    print(num_moves_wh, num_moves_bl, len(moves)-5)
    listing_1 = [moves[0], moves[1], moves[2], "white", len(moves) - 5, num_moves_wh]
    listing_2 =  [moves[0], moves[3], moves[4], "black", len(moves) - 5, num_moves_bl]

    for j in range(len(maia)):
        engine3 = chess.engine.SimpleEngine.popen_uci(["engine/lc0.exe"])
        engine3.configure({"WeightsFile": maia[j]})
        engine4 = chess.engine.SimpleEngine.popen_uci(["engine/lc0.exe"])
        engine4.configure({"WeightsFile": maia[j]})
        eq = check_users_moves_whites(moves, positions, engine3)
        eq_b = check_users_moves_blacks(moves, positions, engine4)
        listing_2.append(str(eq_b))
        listing_1.append(str(eq))
        engine3.quit()
        engine4.quit()

    l1 = []
    l2 = []
    for i in range(1400, 2000, 100): #стокфиш
        engine1 = chess.engine.SimpleEngine.popen_uci(["D:\mglvc\AnalyseRating\engine\stockfish11.exe"])
        engine1.configure({"UCI_elo": i})
        eq = check_users_moves_whites(moves, positions, engine1)
        engine1.quit()
        engine2 = chess.engine.SimpleEngine.popen_uci(["D:\mglvc\AnalyseRating\engine\stockfish11.exe"])
        engine2.configure({"UCI_elo": i})
        eq_b = check_users_moves_blacks(moves, positions, engine2)
        l2.append(str(eq_b))
        l1.append(str(eq))
        engine2.quit()

    listing_1[6] = str(listing_1[6]) + " " + str(l1[0])
    listing_1[7] = str(listing_1[7]) + " " + str(l1[1])
    listing_1[8] = str(listing_1[8]) + " " + str(l1[2])
    listing_1[9] = str(listing_1[9]) + " " + str(l1[3])
    listing_1[10] = str(listing_1[10]) + " " + str(l1[4])
    listing_1[11] = str(listing_1[11]) + " " + str(l1[5])


    listing_2[6] = str(listing_2[6]) + " " + str(l2[0])
    listing_2[7] = str(listing_2[7]) + " " + str(l2[1])
    listing_2[8] = str(listing_2[8]) + " " + str(l2[2])
    listing_2[9] = str(listing_2[9]) + " " + str(l2[3])
    listing_2[10] = str(listing_2[10]) + " " + str(l2[4])
    listing_2[11] = str(listing_2[11]) + " " + str(l2[5])

    return listing_1, listing_2
