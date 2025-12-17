from lib import *

game_modes = ['Tic Tac Toe', 'Connect 4', 'Custom Game']

#Game setup loop
while True:
    print('\n~~ coMNeKt ~~')
    print('\nGAME SETUP\n')

    for i, mode in enumerate(game_modes):
        print(f'{i+1} - {mode}') 
    print('4 - Quit')
    print()

    mode_choice = int_prompt(' game mode', 1, len(game_modes)+1)
    if mode_choice == 1:
        game = TicTacToe()
        board = game.board
    elif mode_choice == 2:
        game = Connect4()
        board = game.board
    elif mode_choice == 3: #custom game setup
        print()
        c = int_prompt(' number of columns', 3, 9)
        r = int_prompt(' number of rows', 3, 9)
        if min(c, r) > 3:
            v = int_prompt(' winning squence length', 3, min(c, r))
        else:
            v = 3
        print('\nDisplay the Y-axis?')
        y = int_prompt('n answer (no/yes)', 0, 1)
        print()
        p = int_prompt(' number of players', 2, 4)
        game = Game(Board(r, c), p, v)
        board = game.board
        board._print_y_rule = y
        tokens = [] #record of player tokens to avoid repetition
        for i in range(game.num_players): #prompt players to choose their game token character
            while True: #error handling
                token = input(f'Player {i+1}, select an alphabet character for your game token: ')
                token = token.upper()
                if token in tokens:
                    print('\nToken already in use - choose again')
                elif not token.isalpha():
                    print('\nToken must be alphabetic - try again')
                    continue
                elif len(token) > 1:
                    print('\nToken must be only 1 character - try again')
                    continue
                else:
                    game.players.append(Player(token)) #add player to game
                    tokens.append(token)
                    break
    else:
        break

    print('\nNEW GAME\n')
    #print game settings
    print(f'Mode: {game_modes[mode_choice-1]}')
    print(f'Victory: get {game.goal} in a row to win')
    print(f'Play order: {', '.join(['Player '+player.token for player in game.players])}')

    #Gameplay loop:
    turn = 1
    while game.winner == None:
        for player in game.players:
            if not board.blank_space(): #if no space left on board, end game with no winner
                print('\nGame over - no spaces left')
                game.winner = 'Draw'
                print(f'Winner: {game.winner}')
                board.display()
                board.wipe()
                break
            else:
                print(f'\nPlayer {player.token}, Turn {turn}')
                board.display()
                game.move(player)
                if game.winner: #end game with winner
                    print(f'\nGame over - Player {game.winner.token} wins!')
                    board.display()
                    board.wipe()
                    break
        turn += 1
    
    #Replay options
    print('1 - New Game')
    print('2 - Quit\n')
    replay = int_prompt('n option', 1, 2)
    if replay == 2:
        break

print('\nGoodbye\n')