import chess
import random
import time
from multiprocessing import Process


start = time.time()

def randomfen(piecesCount):
        
    def populate_board(brd, wp):
            piece_amount = wp
            pieces = piece_list
            kingAmount = 0
            while piece_amount != 0:
                piece_rank, piece_file = random.randint(0, 7), random.randint(0, 7)
                piece = random.choice(pieces)
                if piece == 'K':
                    if kingAmount >= 1:
                        continue
                    else:
                        kingAmount += 1
                if brd[piece_rank][piece_file] == " " and pawn_on_promotion_square(piece, piece_rank) == False:
                    brd[piece_rank][piece_file] = piece
                    piece_amount -= 1
    
    def fen_from_board(brd):
        fen = ""
        for x in brd:
            n = 0
            for y in x:
                if y == " ":
                    n += 1
                else:
                    if n != 0:
                        fen += str(n)
                    fen += y
                    n = 0
            if n != 0:
                fen += str(n)
            fen += "/" if fen.count("/") < 7 else ""
        fen += " w - - 0 1"
        return fen
    
    def pawn_on_promotion_square(pc, pr):
        if pc == "P" and pr == 0:
            return True
        elif pc == "p" and pr == 7:
            return True
        return False

    board = [[" " for x in range(8)] for y in range(8)]
    piece_list = ["R", "N", "B", "Q", "P", "K"]
    piece_amount_white = piecesCount
    populate_board(board, piece_amount_white)
    return fen_from_board(board)

def possibleCaptures(board, movedPieces):
    captures = []
    pieces = []
    pieceSquares = []

    for square in range(0, 64):
        piece = board.piece_at(square)
        if piece != None:
            moved = movedPieces.count(square)
            pieces.append({'p': piece, 's': square, 'm': moved})
            pieceSquares.append(square)

    if len(pieces) == 1:
        return False
        
    for piece in pieces:
        if piece['m'] >= 2:
            continue
        attackedSquares = board.attacks(piece['s'])
        for square in attackedSquares:
            if square in pieceSquares:
                attacked = list(filter(lambda piece: piece['s'] == square, pieces))[0]
                if attacked['p'].piece_type == chess.KING:
                    continue
                captures.append({'ag': piece, 'ad': attacked})
    return captures

def find_solution(fen, timeonpos, board):
    timestarted = time.time()
    board.set_fen(fen)
    try:
        solutionFens, solution = calculateMoves(board, [], [], [], timestarted, timeonpos, 1)
    except:
        solutionFens, solution = False, False
    if solution: return solutionFens, solution
    return 'impossible to solve', None

def calculateMoves(board, solution, movedPieces, solutionFens, timestarted, timeonpos, moveN):
    board.turn = False
    captures = possibleCaptures(board, movedPieces)
    if captures == False:
        return solutionFens, solution
    for capture in captures:
        boardBeforecapture = board.copy()
        solutionBeforecapture = solution.copy()
        solutionFensBeforecapture = solutionFens.copy()
        movedPiecesBeforecapture = movedPieces.copy()
        board.remove_piece_at(capture['ag']['s'])

        if capture['ag']['s'] in movedPieces:
            movedPieces.remove(capture['ag']['s'])
            movedPieces.append(capture['ad']['s'])
            movedPieces.append(capture['ad']['s'])
        else: 
            if capture['ad']['s'] not in movedPieces:
                movedPieces.append(capture['ad']['s'])
            else:
                if movedPieces.count(capture['ad']['s']) >= 2:
                    movedPieces.remove(capture['ad']['s'])
                    

        if movedPieces.count(capture['ad']['s']) >= 2:
            capture['ag']['p'].color = 0
        
        board.set_piece_at(capture['ad']['s'], capture['ag']['p'])
        solution.append(chess.square_name(capture['ag']['s']) + '-' + chess.square_name(capture['ad']['s']))
        solutionFens.append(board.fen())
        if time.time() - timestarted > timeonpos:
            return
        solutionFens, solution = calculateMoves(board, solution, movedPieces, solutionFens, timestarted, timestarted, moveN + 1)
        if solutionFens:
            return solutionFens, solution
        
        solution = solutionBeforecapture.copy()
        movedPieces = movedPiecesBeforecapture.copy()
        board = boardBeforecapture.copy()
        solutionFens = solutionFensBeforecapture.copy()

def generate(piecesCount, timeonpos):
    print(piecesCount)
    output = open(f'{piecesCount}.txt', 'a')
    read = open(f'{piecesCount}.txt', 'r')
    x = len(read.readlines())
    board = chess.Board()
    while x < 1250:
        fen = randomfen(piecesCount)
        solutionFens, solution = find_solution(fen, timeonpos, board)
        if solutionFens != 'impossible to solve':
            x += 1
            output.write(f'{fen};{solutionFens};{solution};\n')
            output.flush()

if __name__ == '__main__':
    for _ in range(0, 4):
        Process(target=generate, args=(10, 1)).start()
