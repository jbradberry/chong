import re
import string


class Board(object):
    num_players = 2
    rows = cols = 8
    p1_starting_stones = 6
    p2_starting_stones = 7

    # Valid pawn move offsets
    DIRECTIONS = (        (-1, 0),
                  ( 0,-1),        ( 0, 1),
                          ( 1, 0),)

    JUMP_DIRECTIONS = (  #Jump destination, jumped over
        ((-2,-2), (-1,-1)), #UL
        ((-2, 0), (-1, 0)), #U
        ((-2, 2), (-1, 1)), #UR
        (( 0,-2), ( 0,-1)), #L
        (( 0, 2), ( 0, 1)), #R
        (( 2,-2), ( 1,-1)), #BL
        (( 2, 0), ( 1, 0)), #B
        (( 2, 2), ( 1, 1)), #BR
    )

    positions = {(None, None): 0}
    inv_positions = {}

    pawn_moves = {}
    pawn_jumps = {}

    str_pieces = {0: "   ", 1: " x ", 2: " o ",
                  -1: "PX ", -2: "PO "}
    unicode_pieces = {0: "   ", 1: u" \u25cb ", 2: u" \u25cf ",
                      -1: u" \u2659 ", -2: u" \u265f "}

    moveRE = re.compile(r'([Pp]?)([a-h])([0-7])')


    def __init__(self):
        if not self.pawn_moves:
            self.initialize()

    @classmethod
    def initialize(cls):
        cls.positions.update(((r, c), 1 << (cls.cols * r + c))
                             for r in xrange(cls.rows)
                             for c in xrange(cls.cols))
        cls.inv_positions.update((b, a)
                                 for a, b in cls.positions.iteritems())

        cls.pawn_moves.update((v, tuple((r+dr, c+dc)
                                        for dr, dc in cls.DIRECTIONS
                                        if (r+dr, c+dc) in cls.positions))
                              for (r, c), v in cls.positions.iteritems()
                              if v)
        cls.pawn_jumps.update((v, tuple(((r+dr, c+dc), (r+jr, c+jc))
                                        for (dr, dc), (jr, jc)
                                        in cls.JUMP_DIRECTIONS
                                        if (r+dr, c+dc) in cls.positions))
                              for (r, c), v in cls.positions.iteritems()
                              if v)

    def start(self):
        # p1 position, p2 position, p1 placed, p2 placed, player to move
        return (self.positions[(0,3)], self.positions[(7,4)], 0, 0, 1)

    def display(self, state, _unicode=True):
        pieces = self.unicode_pieces if _unicode else self.str_pieces

        p1_xy, p2_xy, p1_placed, p2_placed, player = state

        row_sep = "  |" + "-"*(4*self.cols - 1) + "|\n"
        header = " "*4 + "   ".join(string.lowercase[:self.cols]) + "\n"
        msg = "Player {0} to move.\n".format(player)

        P = [[0 for c in xrange(self.cols)] for r in xrange(self.rows)]
        if p1_xy:
            r, c = self.inv_positions[p1_xy]
            P[r][c] = -1
        if p2_xy:
            r, c = self.inv_positions[p2_xy]
            P[r][c] = -2
        for v, (r, c) in self.inv_positions.iteritems():
            if v & p1_placed:
                P[r][c] = 1
            elif v & p2_placed:
                P[r][c] = 2

        board = row_sep.join("%d |"%i + "|".join(pieces[x] for x in row) +
                             "|\n" for i, row in enumerate(P))
        board = ''.join((header, row_sep, board, row_sep, header, msg))
        return board

    def parse(self, play):
        s, c, r = self.moveRE.match(play).groups()
        return int(r), 'abcdefgh'.index(c), not(s)

    def pack(self, play):
        r, c, s = play
        return ''.join(('P' * s, 'abcdefgh'[c], str(r)))

    def play(self, state, play):
        r, c, s = play
        p1_xy, p2_xy, p1_placed, p2_placed, player = state

        if not s:
            if player == 1:
                p1_xy = self.positions[(r, c)]
            else:
                p2_xy = self.positions[(r, c)]
        else:
            if player == 1:
                p1_placed += self.positions[(r, c)]
            else:
                p2_placed += self.positions[(r, c)]

        player = 3 - player
        return (p1_xy, p2_xy, p1_placed, p2_placed, player)

    def is_legal(self, state, play):
        plays = set(self.legal_plays(state))
        return play in plays

    def legal_plays(self, state):
        p1_xy, p2_xy, p1_placed, p2_placed, player = state

        if player == 1 and p1_xy == 0:
            return [(0, x, False) for x in xrange(self.cols)]
        if player == 2 and p2_xy == 0:
            return [(self.rows-1, x, False) for x in xrange(self.cols)]

        p1_stones = self.p1_starting_stones - bin(p1_placed).count('1')
        p2_stones = self.p2_starting_stones - bin(p2_placed).count('1')

        placements = []
        occupied = p1_placed | p2_placed | p1_xy | p2_xy
        if (player == 1 and p1_stones) or (player == 2 and p2_stones):
            placements = [(r, c, True)
                          for v, (r, c) in self.inv_positions.iteritems()
                          if not (not r or r == self.rows-1 or (v & occupied))]

        position = p1_xy if player == 1 else p2_xy
        stones = p1_placed if player == 1 else p2_placed

        pawn = [(r, c, False) for r, c in self.pawn_moves[position]
                if not (self.positions[(r, c)] & occupied)]

        jumps = [(r, c, False) for (r,c), (jr,jc) in self.pawn_jumps[position]
                 if not (self.positions[(r, c)] & occupied)
                 and (self.positions[(jr, jc)] & stones)]

        return jumps + pawn + placements

    def winner(self, state_lst):
        state = state_lst[-1]
        p1_xy, p2_xy, p1_placed, p2_placed, player = state

        if p1_xy == 0 or p2_xy == 0:
            return 0
        if self.inv_positions[p1_xy][0] == self.rows - 1:
            return 1
        if self.inv_positions[p2_xy][0] == 0:
            return 2
        if not self.legal_plays(state):
            return 3 - player
        if state_lst.count(state) >= 3:
            return 3
        return 0

    def winner_message(self, winner):
        if winner == 3:
            return "Stalemate."
        return "Winner: Player {0}.".format(winner)
