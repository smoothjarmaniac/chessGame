
# Handles user input.
# Displays current GameStatus object.


import pygame as p
from itertools import cycle
import Engine
import chessAI
import sys
import Theme

BOARD_WIDTH = BOARD_HEIGHT = 768
MOVE_LOG_PANEL_WIDTH = 300
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8

SQUARE_SIZE = (BOARD_HEIGHT // DIMENSION)

MAX_FPS = 120
IMAGES = {}
# global piece_sound
# piece_sound = p.mixer.Sound("sounds/main.wav")
# global basic_sound
# basic_sound = p.mixer.Sound("sounds/basic.wav")


# only to initialize IMAGES
# later add themes
def loadImages():
    pieces_white, pieces_black = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ'], ['bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    pieces = pieces_white + pieces_black

    for piece in pieces:
        if piece == 'wp' or piece == 'bp':
            IMAGES[piece] = p.transform.smoothscale(p.image.load("new/" + piece + ".png"), (60, 70))
        else:
            IMAGES[piece] = p.transform.smoothscale(p.image.load("new/" + piece + ".png"), (88, 88))


# driver code
# handles user input
# renders/updates the graphics
def main():
    # init pygame
    p.init()
    # p.mixer.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT), 0, 32)
    p.display.set_caption("Chess Basic")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = Engine.GameState()
    valid_moves = game_state.getValidMoves()
    global theme_value
    value = cycle([0, 1, 2, 3, 4])
    theme_value = next(value)
    move_made = False
    animate = False
    loadImages()

    init_font = p.font.SysFont("Cambria", 15, False, False)
    end_font = p.font.SysFont("Cambria", 43, False, False)

    running = True
    square_selected = ()  # keeps track of last selected square, used in event handling
    player_clicks = []   # [initial position, final position] of a piece
    game_over = False

    white_did_check = ""
    black_did_check = ""
    last_move_printed = False
    moves_list = []
    move_log_font = p.font.SysFont("Cambria", 18, False, False)

    turn = 1

    player_one = True
    player_two = False

    # event handling
    while running:

        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            # handling mouse inputs
            elif e.type == p.MOUSEBUTTONDOWN:  # later add functionality to drag pieces
                if not game_over and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if square_selected == (row, col) or col >= 8:  # to handle multiple clicks
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:  # if all happens as expected, two squares clicked
                        move = Engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # handling keyboard inputs
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # if 'Z' is pressed, undo
                    if game_state.white_to_move:
                        if turn > 1:
                            turn -= 1
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    last_move_printed = False

                if e.key == p.K_r:  # if 'R' is pressed, reset the board
                    game_state = Engine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    turn = 1
                    last_move_printed = False
                    moves_list = []

                if e.key == p.K_t:
                    theme_value = next(value)

        if not game_over and not human_turn:
            AI_move = chessAI.findBestMoveNegaMaxAlphaBeta(game_state, valid_moves)
            if AI_move is None:
                AI_move = chessAI.findRandomMove(valid_moves)
            game_state.makeMove(AI_move, True)
            move_made = True
            animate = True

        if move_made:
            if game_state.checkForPinsAndChecks()[0]:
                if not game_state.white_to_move:
                    white_did_check = "+"
                else:
                    black_did_check = "+"
            if game_state.white_to_move:
                try:
                    moves_list.append(
                        f"\n{turn}. {game_state.move_log[-2].getChessNotation()}{white_did_check} {game_state.move_log[-1].getChessNotation()}{black_did_check}")
                    print(
                        f"\n{turn}. {game_state.move_log[-2].getChessNotation()}{white_did_check} {game_state.move_log[-1].getChessNotation()}{black_did_check}",
                        end="")
                    turn += 1
                    white_did_check = ""
                    black_did_check = ""
                except:
                    pass

            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False

        drawGameState(screen, game_state, valid_moves, square_selected, move_log_font, theme_value)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)
            drawInitial(screen,  init_font)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate", end_font)
                if not last_move_printed:
                    moves_list[-1] += "+"
                    moves_list.append("result: 0-1")
                    print("+")
                    print("result: 0-1")
                    last_move_printed = True
                    saveGame(moves_list)

            else:
                drawEndGameText(screen, "White wins by checkmate", end_font)
                if not last_move_printed:
                    moves_list.append(f"\n{turn}. {game_state.move_log[-1].getChessNotation()}++")
                    moves_list.append("result: 1-0")
                    print(f"\n{turn}. {game_state.move_log[-1].getChessNotation()}++")
                    print("result: 1-0")
                    last_move_printed = True
                    saveGame(moves_list)

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate", end_font)
            if not last_move_printed:
                if not game_state.white_to_move:
                    moves_list.append(f"\n{turn}. {game_state.move_log[-1].getChessNotation()}")
                    moves_list.append("result: 1/2-1/2")
                    print(f"\n{turn}. {game_state.move_log[-1].getChessNotation()}")
                    print("result: 1/2-1/2")
                    last_move_printed = True
                    saveGame(moves_list)

        clock.tick(MAX_FPS)
        p.display.update()


def drawGameState(screen, game_state, valid_moves, square_selected, move_log_font, theme_value):
    drawBoard(screen, theme_value)
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)

# **************************** USED BY drawGameState ****************************
# called by drawGameState, draws the squares
def drawBoard(screen, theme_value):
    global colors
    theme = Theme.boardTheme()
    colors = theme.getTheme(theme_value)
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]  # if color is even then white, black == odd
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# called by drawGameState, shows possible moves
def highlightSquares(screen, game_state, valid_moves, square_selected):
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

# called by drawGameState, draws the pieces
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece == 'wp' or piece == 'bp':
                screen.blit(IMAGES[piece], p.Rect((column * SQUARE_SIZE)+ 19, (row * SQUARE_SIZE )+ 14, SQUARE_SIZE, SQUARE_SIZE))
            elif piece != "--":
                screen.blit(IMAGES[piece], p.Rect((column * SQUARE_SIZE)+ 6, (row * SQUARE_SIZE )+ 6, SQUARE_SIZE, SQUARE_SIZE))
#  The term blit stands for Block Transfer, and .blit() is how you copy the contents of one Surface to another.

# called in event handling, explicitly
def drawMoveLog(screen, game_state, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


# not in use as of now
def saveGame(moves_list):
    result = moves_list.pop()
    turns_dict = {}
    for i in range(len(moves_list) - 1, -1, -1):
        try:
            int(moves_list[i][1])
            if moves_list[i][1] not in turns_dict:
                turns_dict[moves_list[i][1]] = moves_list[i][1:] + "\n"
        except:
            pass
    file = open("last_game_logs.txt", "w")
    for turn in sorted(turns_dict.keys()):
        file.write(turns_dict[turn])
    file.write(result)
    file.close()


# called in event handling, explicitly
def drawEndGameText(screen, text, end_font):
    text_object = end_font.render(text, False, p.Color("black"), p.Color("gray"))
    text_rect = text_object.get_rect()
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    # screen.blit(text_object, text_rect.move(BOARD_WIDTH//2 - MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT//2))
    screen.blit(text_object, text_location)
    # text_object = font.render(text, False, p.Color('black'), p.Color("dark green"))
    # screen.blit(text_object, text_rect.move(2, 2))


def animateMove(move, screen, board, clock):

    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 6
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen, theme_value)
        drawPieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


# called in event handling, explicitly
def drawInitial(screen,  init_font):
    hints = "Z: Undo |" + " R: Reset |" " T: Theme"

    text_object = init_font.render(hints, False, p.Color("green"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH + 20,
                                                                 BOARD_HEIGHT - 20)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
