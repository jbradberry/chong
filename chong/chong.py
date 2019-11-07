import re
import string


class Board(object):
    num_players = 2

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
        cls.positions.update(((r, c), 1 << (r * 8 + c))
                             for r in xrange(8)
                             for c in xrange(8))
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

    def starting_state(self):
        # p1 position, p2 position, p1 placed, p2 placed, player to move, visit number
        return (1 << (0 * 8 + 3), 1 << (7 * 8 + 4), 0, 0, 1, 1)

    def display(self, state, action, _unicode=True):
        pieces = self.unicode_pieces if _unicode else self.str_pieces

        row_sep = "  |" + "-" * (4 * 8 - 1) + "|\n"
        header = "    " + "   ".join(string.lowercase[:8]) + "\n"
        reserve = u"       {0}\u00d7 {1}          {2}\u00d7 {3}\n".format(
            pieces[1], next(x for x in state['unplaced'] if x['player'] == 1)['quantity'],
            pieces[2], next(x for x in state['unplaced'] if x['player'] == 2)['quantity']
        )
        msg = "{0}Player {1} to move.".format(
            "Played: {0}\n".format(
                self.to_notation(self.to_compact_action(action))) if action else '',
            state['player']
        )

        P = [[0 for c in range(8)] for r in xrange(8)]
        for p in state['pieces']:
            P[p['row']][p['column']] = p['player'] * (-1 if p['type'] == 'pawn' else 1)

        board = row_sep.join("%d |" % i + "|".join(pieces[x] for x in row) +
                             "|\n" for i, row in enumerate(P))
        board = ''.join((header, row_sep, board, row_sep, header, reserve, msg))
        return board

    def to_compact_state(self, data):
        state = {(1, 'pawn'): 0, (2, 'pawn'): 0, (1, 'stone'): 0, (2, 'stone'): 0}
        for item in data['pieces']:
            index = 1 << (item['row'] * 8 + item['column'])
            state[(item['player'], item['type'])] += index

        return (
            state[(1, 'pawn')],
            state[(2, 'pawn')],
            state[(1, 'stone')],
            state[(2, 'stone')],
            data['player'],
            data['visit_number'],
        )

    def to_json_state(self, state):
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state

        pieces = []
        for r in range(8):
            for c in range(8):
                index = 1 << (r * 8 + c)
                if index & p1_xy:
                    pieces.append({'type': 'pawn', 'player': 1, 'row': r, 'column': c})
                if index & p2_xy:
                    pieces.append({'type': 'pawn', 'player': 2, 'row': r, 'column': c})
                if index & p1_placed:
                    pieces.append({'type': 'stone', 'player': 1, 'row': r, 'column': c})
                if index & p2_placed:
                    pieces.append({'type': 'stone', 'player': 2, 'row': r, 'column': c})

        return {
            'pieces': pieces,
            'unplaced': [
                {'type': 'stone', 'player': 1,
                 'quantity': 6 - bin(p1_placed).count('1')},
                {'type': 'stone', 'player': 2,
                 'quantity': 7 - bin(p2_placed).count('1')}
            ],
            'player': player,
            'previous_player': 3 - player,
            'visit_number': visit_num,
        }

    def to_compact_action(self, action):
        return (action['row'], action['column'], action['type'] == 'stone')

    def to_json_action(self, action):
        return {'type': 'stone' if action[2] else 'pawn', 'row': action[0], 'column': action[1]}

    def from_notation(self, notation):
        result = self.moveRE.match(notation)
        if result is None:
            return
        s, c, r = result.groups()
        return int(r), 'abcdefgh'.index(c), not(s)

    def to_notation(self, action):
        if action is None:
            return ''
        r, c, s = action
        return ''.join(('P' * (1 - s), 'abcdefgh'[c], str(r)))

    def next_state(self, history, action):
        state = history[-1]
        r, c, s = action
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state

        index = 1 << (r * 8 + c)

        if not s:
            if player == 1:
                p1_xy = index
            else:
                p2_xy = index
        else:
            if player == 1:
                p1_placed += index
            else:
                p2_placed += index

        player = 3 - player
        visit_num = 1 if s else sum(1 for S in history if S[:5] == (p1_xy, p2_xy, p1_placed, p2_placed, player)) + 1
        return (p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num)

    def is_legal(self, history, action):
        return action in self.legal_actions(history)

    def has_legal_action(self, history):
        state = history[-1]
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state

        p1_stones = 6 - bin(p1_placed).count('1')
        p2_stones = 7 - bin(p2_placed).count('1')

        if (player == 1 and p1_stones > 0) or (player == 2 and p2_stones > 0):
            return True

        position = p1_xy if player == 1 else p2_xy
        not_occupied = ~(p1_placed | p2_placed | p1_xy | p2_xy)
        if any(not_occupied & 1 << (r * 8 + c) for r, c in self.pawn_moves[position]):
            return True

        stones = p1_placed if player == 1 else p2_placed
        if not stones:
            return False

        if any(
            stones & 1 << (jr * 8 + jc) and
            not_occupied & 1 << (r * 8 + c)
            for (r, c), (jr, jc) in self.pawn_jumps[position]
        ):
            return True

        return False

    def legal_actions(self, history):
        state = history[-1]
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state

        p1_stones = 6 - bin(p1_placed).count('1')
        p2_stones = 7 - bin(p2_placed).count('1')

        placements = []
        not_occupied = ~(p1_placed | p2_placed | p1_xy | p2_xy)
        if (player == 1 and p1_stones) or (player == 2 and p2_stones):
            placements = [
                (r, c, True)
                for r in xrange(1, 7) for c in xrange(8)
                if not_occupied & 1 << (r * 8 + c)
            ]

        position = p1_xy if player == 1 else p2_xy
        stones = p1_placed if player == 1 else p2_placed

        pawn = [(r, c, False) for r, c in self.pawn_moves[position]
                if not_occupied & 1 << (r * 8 + c)]

        if stones:
            jumps = [(r, c, False) for (r, c), (jr, jc) in self.pawn_jumps[position]
                     if not_occupied & 1 << (r * 8 + c)
                     and stones & 1 << (jr * 8 + jc)]
        else:
            jumps = []

        return jumps + pawn + placements

    def previous_player(self, state):
        return 3 - state[4]

    def current_player(self, state):
        return state[4]

    def is_ended(self, history):
        state = history[-1]
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state

        if p1_xy == 0 or p2_xy == 0:
            return False
        if p1_xy & 0xff00000000000000:
            return True
        if p2_xy & 0x00000000000000ff:
            return True
        if not self.has_legal_action(history):
            return True
        if visit_num >= 3:
            return True
        return False

    def win_values(self, history):
        if not self.is_ended(history):
            return

        state = history[-1]
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state

        if p1_xy & 0xff00000000000000:
            return {1: 1, 2: 0}
        if p2_xy & 0x00000000000000ff:
            return {1: 0, 2: 1}
        if not self.has_legal_action(history):
            return {player: 0, 3 - player: 1}
        if visit_num >= 3:
            return {1: 0.5, 2: 0.5}

    def points_values(self, history):
        if not self.is_ended(history):
            return

        state = history[-1]
        p1_xy, p2_xy, p1_placed, p2_placed, player, visit_num = state
        p1_row = (
            4 * bool(p1_xy & 0xffffffff00000000) +
            2 * bool(p1_xy & 0xffff0000ffff0000) +
            bool(p1_xy & 0xff00ff00ff00ff00)
        )
        p2_row = (
            4 * bool(p2_xy & 0xffffffff00000000) +
            2 * bool(p2_xy & 0xffff0000ffff0000) +
            bool(p2_xy & 0xff00ff00ff00ff00)
        )

        if p1_row == 7:
            return {1: p2_row, 2: -p2_row}
        if p2_row == 0:
            p1_row = 7 - p1_row  # invert the orientation
            return {1: -p1_row, 2: p1_row}
        if not self.has_legal_action(history):
            return {player: -16, 3 - player: 16}
        if visit_num >= 3:
            return {1: 0, 2: 0}

    def winner_message(self, winners):
        winners = sorted((v, k) for k, v in winners.iteritems())
        value, winner = winners[-1]
        if value == 0.5:
            return "Stalemate."
        return "Winner: Player {0}.".format(winner)
