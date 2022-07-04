import numpy as np
from random import choice


class Songs:

    def __init__(self):
        """
        each song contains a list of beat counts and its time sig,
        each bar (measure) is separated by common in the list, so that their y position can be randomized
        beatRatio = 4 means that each note height = 1/4 beat
        the last item are the locations of suspended notes
        """

        # time signature: 4/4
        self.kingOfKings = [
                            {'bpm': 70, 'beatRatio': 4},
                            np.ones((8,)) * 2,
                            np.ones((4,)) * 4,
                            np.ones((8,)) * 2,
                            np.ones((3,)) * 4, np.array([1, 2, 1, 1]),
                            np.array([3, 1, 2, 1, 1]),
                            np.array([3, 1, 2, 1]),
                            [26, 31]
                            ]

        self.SYMSLL = [{'bpm': 110, 'beatRatio': 2},
                       ]

        self.names = ['King of Kings', 'SYMSLL']
        self.nSongs = len(self.names)


def convertXY(song: Songs, note_size: int, top_player: int) -> list:
    """
    Convert counts to x and y position in the windows
    :param note_size: height of notes
    :param top_player: top y position of player
    :param song: contains all counts for a song
    :return: a list of notes x and y positions
    """

    raw_beats = song[1:]
    beats = np.concatenate(raw_beats)
    multiplier = np.zeros((len(beats),))

    for i in range(len(beats) - 1):
        multiplier[i + 1] = beats[i] + multiplier[i]

    pos_y = [(top_player - 2 * note_size) - multiplier[i] * note_size for i in range(len(beats))]

    pos_x = np.zeros(beats.shape)
    for i in range(len(pos_x)):
        x_ = [100, 200, 300]
        if i == 0:
            pos_x[i] = choice(x_)
        else:
            x_.remove(pos_x[i-1])
            pos_x[i] = choice(x_)

    # # generate note pos by cycling through [100, 200, 300]
    # pos_x = np.zeros(beats.shape)
    # col_ = 100
    # start_ = 0
    # for bar in raw_beats:
    #     temp_note_len = len(bar)
    #     pos_x[start_:start_ + temp_note_len] = np.ones((temp_note_len,)) * col_
    #     start_ += temp_note_len
    #     col_ += 100
    #     if col_ > 300: col_ = 100

    return pos_x, pos_y



