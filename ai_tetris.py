import pygame
import random
import numpy as np
import copy

pygame.font.init()

# GLOBALS VARS
w_width = 800
w_height = 700

play_width = 300
play_height = 600
block_size = 30

top_left_x = (w_width - play_width) // 2
top_left_y = w_height - play_height - 50

# SHAPE FORMATS
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '.....',
      '0000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '0....',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '..000',
      '....0',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '..0..',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '..000',
      '..0 ..',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '.0...',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '..000',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]

shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


class TetrisGame:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.board = self.create_grid()
        self.piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.fall_time = 0
        self.level_time = 0
        self.fall_speed = 0.27
        self.level = 0
        self.timedelta = 0
        self.win = pygame.display.set_mode((w_width, w_height))

    def create_grid(self, locked_positions={}):
        grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if (x, y) in locked_positions:
                    c = locked_positions[(x, y)]
                    grid[y][x] = c
        return grid

    def convert_shape_format(self, piece):
        positions = []
        shape_format = piece.shape[piece.rotation % len(piece.shape)]
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((piece.x + j, piece.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions

    def valid_space(self, piece):
        accepted_pos = [[(j, i) for j in range(
            10) if self.board[i][j] == (0, 0, 0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = self.convert_shape_format(piece)
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape(self):
        return Piece(5, 0, random.choice(shapes))

    def draw_text_middle(self, text, size, color, surface):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                     top_left_y + play_height/2 - label.get_height()/2))

    def draw_grid(self, surface, grid):
        sx = top_left_x
        sy = top_left_y
        for i in range(len(grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx,
                             sy+i*block_size), (sx+play_width, sy+i*block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx+j *
                                 block_size, sy), (sx+j*block_size, sy+play_height))

    def clear_rows(self, grid, locked):
        inc = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
        return inc

    def draw_next_shape(self, piece, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100
        format = piece.shape[piece.rotation % len(piece.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, piece.color, (sx + j*block_size,
                                     sy + i*block_size, block_size, block_size), 0)
        surface.blit(label, (sx + 10, sy - 30))

    def draw_window(self, surface, grid, score=0, last_score=0):
        surface.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))
        surface.blit(label, (top_left_x + play_width /
                     2 - (label.get_width()/2), 30))
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255, 255, 255))
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100
        surface.blit(label, (sx + 20, sy + 160))
        label = font.render(
            'High Score: ' + str(last_score), 1, (255, 255, 255))
        sx = top_left_x - 200
        sy = top_left_y + 200
        surface.blit(label, (sx + 20, sy + 160))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (
                    top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
        pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                         top_left_y, play_width, play_height), 5)
        self.draw_grid(surface, grid)

    def max_score(self):
        try:
            with open('scores.txt', 'r') as f:
                lines = f.readlines()
                if lines:
                    score = lines[0].strip()
                else:
                    score = "0"
        except FileNotFoundError:
            score = "0"
        return score

    def main_menu(self):
        run = True
        self.win.fill((0, 0, 0))
        self.draw_text_middle('Press any key to begin.',
                              60, (255, 255, 255), self.win)
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    print("start")
                    self.manual_main()

    def manual_main(self):
        self.draw_window(self.win, self.board)
        pygame.display.update()
        last_score = self.max_score()
        locked_positions = {}
        grid = self.create_grid(locked_positions)
        change_piece = False
        run = True
        current_piece = self.get_shape()
        next_piece = self.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        while run:
            grid = self.create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick()
            if level_time/1000 > 5:
                level_time = 0
                if fall_speed > 0.12:
                    fall_speed -= 0.005
            if fall_time/1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not (self.valid_space(current_piece)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not (self.valid_space(current_piece)):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not (self.valid_space(current_piece)):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not (self.valid_space(current_piece)):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotation = current_piece.rotation + \
                            1 % len(current_piece.shape)
                        if not (self.valid_space(current_piece)):
                            current_piece.rotation = current_piece.rotation - \
                                1 % len(current_piece.shape)
            shape_pos = self.convert_shape_format(current_piece)
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color
            if next_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = self.get_shape()
                change_piece = False
                self.score += self.clear_rows(grid, locked_positions) * 10
            self.draw_window(self.win, grid)
            self.draw_next_shape(next_piece, self.win)
            pygame.display.update()

    def reset(self):
        self.__init__()

    def get_state(self):
        return np.array(self.board), self.score, self.game_over

    def get_action_space(self):
        return 4  # Move left,right,rotate, or do nothing

    def take_action(self, action):
        old_grid = copy.deepcopy(self.board)
        if action == 0:  # move left
            self.piece.x -= 1
            if not self.valid_space(self.piece, self.board):
                self.piece.x += 1
        elif action == 1:  # move right
            self.piece.x += 1
            if not self.valid_space(self.piece, self.board):
                self.piece.x -= 1
        elif action == 2:  # rotate
            self.piece.rotation = (
                self.piece.rotation + 1) % len(self.piece.shape)
            if not self.valid_space(self.piece, self.board):
                self.piece.rotation = (
                    self.piece.rotation - 1) % len(self.piece.shape)
        elif action == 3:  # do nothing
            pass
        # Falling and level time
        self.fall_time += self.timedelta
        self.level_time += self.timedelta
        if self.level_time/1000 > 5:
            self.level_time = 0
            if self.fall_speed > 0.12:
                self.fall_speed -= 0.005
        if self.fall_time/1000 > self.fall_speed:
            self.fall_time = 0
            self.piece.y += 1
            if not (self.valid_space(self.piece, self.board)) and self.piece.y > 0:
                self.piece.y -= 1
                self.change_piece = True
        # Check for cleared lines
        cleared_lines = 0
        for i in range(len(self.board)-1, -1, -1):
            row = self.board[i]
            if (0, 0, 0) not in row:
                cleared_lines += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except:
                        continue
        if cleared_lines > 0:
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y+cleared_lines)
                    self.locked_positions[newKey] = self.locked_positions.pop(
                        key)
        # Check for game over
        new_grid = self.create_grid(self.locked_positions)
        if self.piece.y < 1:
            self.game_over = True
        # Check for change piece
        reward = self.get_reward(
            self, old_grid, new_grid, cleared_lines, self.game_over)
        return self.get_state(), reward

    def get_max_height(self, grid):
        max_height = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != (0, 0, 0):
                    max_height = max(max_height, i)
                    break
        return max_height

    def get_holes(self, grid):
        holes = 0
        for i in range(len(grid[0])):
            block_found = False
            for j in range(len(grid)):
                if grid[j][i] != (0, 0, 0):
                    block_found = True
                elif grid[j][i] == (0, 0, 0) and block_found:

                    holes += 1
        return holes

    def get_bumpiness(self, grid):
        bumpiness = 0
        for i in range(len(grid[0])-1):
            bumpiness += abs(self.get_max_height(grid[:]
                             [i]) - self.get_max_height(grid[:][i+1]))
        return bumpiness

    def get_reward(self, old_grid, new_grid, lines_cleared, game_over):
        reward = 0
        # Lines cleared
        reward += lines_cleared ** 2
        # Height increase
        old_max_height = self.get_max_height(old_grid)
        new_max_height = self.get_max_height(new_grid)
        reward -= max(0, new_max_height - old_max_height)
        # Creating holes
        old_holes = self.get_holes(old_grid)
        new_holes = self.get_holes(new_grid)
        reward -= max(0, new_holes - old_holes)
        # Bumpiness
        old_bumpiness = self.get_bumpiness(old_grid)
        new_bumpiness = self.get_bumpiness(new_grid)
        reward -= max(0, new_bumpiness - old_bumpiness)
        # Losing game
        if game_over:
            reward -= 1000
        return reward


if __name__ == "__main__":
    game = TetrisGame()
    game.main_menu()
