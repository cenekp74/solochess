from re import X
import chess
import random

def randomfen(piecesCount):
        
    def populate_board(brd, wp):
            piece_amount = wp
            pieces = piece_list

            while piece_amount != 0:
                piece_rank, piece_file = random.randint(0, 7), random.randint(0, 7)
                piece = random.choice(pieces)
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


def validate(fen):
    board = chess.Board(fen)
    solution = calculateMoves(board, [], [])
    if solution: return solution
    return 'impossible to solve'

def calculateMoves(board, solution, movedPieces):
    board.turn = False
    captures = possibleCaptures(board, movedPieces)
    if captures == False:
        return solution

    for capture in captures:
        boardBeforecapture = board.copy()
        solutionBeforecapture = solution.copy()
        movedPiecesBeforecapture = movedPieces.copy()
        board.remove_piece_at(capture['ag']['s'])

        if capture['ag']['s'] in movedPieces:
            movedPieces.remove(capture['ag']['s'])
            movedPieces.append(capture['ad']['s'])
            movedPieces.append(capture['ad']['s'])
        else: 
            movedPieces.append(capture['ad']['s'])

        board.set_piece_at(capture['ad']['s'], capture['ag']['p'])
        solution.append(str(capture['ag']['p'].symbol()) + chess.square_name(capture['ad']['s']))
        solution = calculateMoves(board, solution, movedPieces)
        if solution: return solution
        solution = solutionBeforecapture.copy()
        movedPieces = movedPiecesBeforecapture.copy()
        board = boardBeforecapture.copy()

def generate(piecesCount):
    clear = open('output.txt', 'w')
    clear.write('')
    output = open('output.txt', 'a')

    while True:
        fen = randomfen(piecesCount)
        moves = validate(fen)
        if moves!= 'impossible to solve':
            output.write(f'{fen}    ;   {moves}\n')

if __name__ == '__main__':
    print(validate('8/8/8/8/8/8/8/8 w - - 0 1'))
    generate(6)
