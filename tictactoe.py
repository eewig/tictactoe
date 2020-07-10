import random


HELP = '''
TicTacToe
-------------------
| 1 1 | 1 2 | 1 3 |
| 2 1 | 2 2 | 2 3 |
| 3 1 | 3 2 | 3 3 |
-------------------

To put X or O in cell you need type row and column (from 1 to 3).
Like this 1 1 or 2 3, all coordinates you can find above. 
You can play with computer or with your friend.

Game have 4 modes:
-easy, 
-medium, 
-hard,
-user.
To start game enter "<mode> <mode>" (without <>).
Like this "user user" or "user medium".

Have fun.
'''


HUMAN = -1
COMP = 1


class TicTacToe:

    def __init__(self):
        self.grid = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0],
                     ]

    def __str__(self):
        chars = {
                -1: 'O',
                0: ' ',
                +1: 'X'
                }

        string = '---------\n'
        for row in self.grid:
            string += '| '
            for cell in row:
                string += f'{chars[cell]} '
            string += '|\n'
        string += '---------'
        return string

    def new_game(self):
        for x, row in enumerate(self.grid):
            for y in range(len(row)):
                self.grid[x][y] = 0

    def empty_cells(self, state):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def fill(self, string):
        for i in range(9):
            value = 0
            if string[i] == 'X':
                value = 1
            elif string[i] == 'O':
                value = -1
            if i >= 6:
                self.grid[2][i - 6] = value
            elif i >= 3:
                self.grid[1][i - 3] = value
            else:
                self.grid[0][i] = value

    def valid_move(self, x, y):
        # if [x, y] in self.empty_cells(self.grid):
        if self.grid[x][y] == 0:
            return True
        return False

    def add_val(self, x, y, val):
        if self.valid_move(x, y):
            self.grid[x][y] = val
            return True
        return False

    def evaluate(self, state):
        if self.check_win(state, COMP):
            score = +1
        elif self.check_win(state, HUMAN):
            score = -1
        else:
            score = 0

        return score


    def check_win(self, state, player):
        # if all(state[i][i] == player for i in range(0, 3)) or \
        #         all(state[i - 1][-i] == player for i in range(1, 4)):
        #     return True
        # elif any([row.count(player) == 3 for row in self.grid]):
        #     return True
        # else:
        #     for j in range(3):
        #         if all(state[i][j] == player for i in range(3)):
        #             return True
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self, state):
        return self.check_win(state, HUMAN) or self.check_win(state, COMP)

    def easy_level(self, sign):
        while True:
            x, y = random.randint(0, 2), random.randint(0, 2)
            if self.grid[x][y] == 0:
                self.add_val(x, y, sign)
                break

    def medium_level(self, state, sign):
        """By default value equal medium sign(X or O).
        But if value is not None then processor will put medium value
        to block opponent.
        """
        for x, y in self.empty_cells(state):
            state[x][y] = sign
            if self.check_win(state, sign):
                return True
            state[x][y] = -sign
            if self.check_win(state, -sign):
                state[x][y] = sign
                return True
            state[x][y] = 0
        while True:
            x, y = random.randint(0, 2), random.randint(0, 2)
            if self.valid_move(x, y):
                self.add_val(x, y, sign)
                break


# AI part
    def minimax(self, state, depth, player):
        if player == COMP:
            best = [-1, -1, -10000]
        else:
            best = [-1, -1, 10000]

        if depth == 0 or self.game_over(state):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in self.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        return best

    def ai_turn(self, level, sign):
        """
        level: ai level complexity
        sign: X or O
        """
        depth = len(self.empty_cells(self.grid))
        if depth == 0 or self.game_over(self.grid):
            return
        print(f'Making move level "{level}"')
        if level == 'easy':                   # levels
            self.easy_level(sign)
        elif level == 'medium':
            self.medium_level(self.grid, sign)
        elif level == 'hard':
            if depth == 9:
                x = random.randint(0, 2)
                y = random.randint(0, 2)
            else:
                move = self.minimax(self.grid, depth, sign)
                x, y = move[0], move[1]
            self.add_val(x, y, sign)
        print(self)

    def human_turn(self, sign):
        """
        sign: X or O
        """
        depth = len(self.empty_cells(self.grid))
        if depth == 0 or self.game_over(self.grid):
            return
        while True:
            try:
                x, y = [int(c.strip())-1 for c in input('Enter the coordinates: ').split()]
            except (ValueError, TypeError):
                print('You should enter two numbers!')
            if all((3 > x, y >= 0)):
                if self.valid_move(x, y):
                    self.add_val(x, y, sign)  # Need to change later. The placement of hyperskill is really awful.
                    break
                else:
                    print('This cell is occupied! Choose another one!')
            else:
                print('Coordinates should be from 1 to 3!')
        print(self)


    def play(self):
        quit = ''
        print(HELP)
        while quit != 'q':
            self.new_game()
            commands = ('user', 'easy', 'medium', 'hard')
            while True:
                command = [item.strip() for item in input('Start game: ').split()]
                if len(command) == 2 and \
                command[0] in commands and command[1] in commands:
                    player1 = command[0]
                    player2 = command[1]
                    break
                print('Bad parameters!')
            print(self)
            while len(self.empty_cells(self.grid)) > 0 and not self.game_over(self.grid):
                if player1 in ('easy', 'medium', 'hard'):
                    self.ai_turn(player1, 1)
                elif player1 == 'user':
                    self.human_turn(1)
                if player2 in ('easy', 'medium', 'hard'):
                    # self.change_chars()
                    self.ai_turn(player2, -1)
                elif player2 == 'user':
                    self.human_turn(-1)


            if self.check_win(self.grid, 1):
                print('X wins')
            elif self.check_win(self.grid, -1):
                print('O wins')
            else:
                print('Draw')

            quit = input('To play again enter anything. To quit enter "q": ')
        print('\nBye')


if __name__ == '__main__':
    try:
        tic = TicTacToe()
        tic.play()
    except KeyboardInterrupt:
        print('\nBye')
        exit()
