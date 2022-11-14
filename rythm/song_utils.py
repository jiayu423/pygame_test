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


class KingOfKings(Songs):

    def __int__(self):
        Songs.__init__(self)
        self.bpm = 70
        self.beatsRatio = 4
        self.ignoredNotes = [26, 31]
        self.beats = [
            np.ones((8,)) * 2,
            np.ones((4,)) * 4,
            np.ones((8,)) * 2,
            np.ones((3,)) * 4, np.array([1, 2, 1, 1]),
            np.array([3, 1, 2, 1, 1]),
            np.array([3, 1, 2, 1]),
        ]


class BecauseYouWalkWithMe:

    def __init__(self):
        # self.bpm = 93
        self.beatsRatio = 4
        self.ignoredNotes = np.array([24, 31, 38, 45, 52, 59, 74, 82, 90, 97, 104, 111, 118, 133, 134, 135, 136]) - 18
        self.bpm = np.concatenate((np.ones(74, ) * 98, np.ones(199 - 74, ) * 99, np.ones(254 - 199, ) * 99.2))
        self.introEndPoint = 17
        self.beats = [
            np.ones((2,)) * 2,  # 处处
            np.ones((3,)) * 4,  # 留  下
            np.array([2, 2, 4, 4]),  # 有你同在
            np.array([2, 2, 4, 4]),  # 的恩典痕
            np.ones((3,)) * 4,  # 迹 - -

            # 16
            np.array([4, 4, 2, 2]),  # - - 因你
            np.ones((3,)) * 4,  # 与我同
            np.array([4, 4, 2, 2]),  # 行 - 我就
            np.ones((3,)) * 4,  # 不会孤
            np.array([4, 4, 2, 2]),  # 寂 - 欢笑
            np.ones((3,)) * 4,  # 时你同
            np.array([4, 4, 2, 2]),  # 喜 - 悲伤
            np.ones((3,)) * 4,  # 时你共
            np.array([4]),  # 泣

            # 45
            np.array([4, 2, 2]),  # - 因你
            np.ones((3,)) * 4,  # 是我力
            np.array([4, 4, 2, 2]),  # 量 - 我就
            np.ones((3,)) * 4,  # 不会绝
            np.array([4, 4, 2, 2]),  # 望 - 困乏
            np.ones((3,)) * 4,  # 软弱中
            np.array([2, 2, 4, 4]),  # 有你赐恩
            np.array([2, 2, 6, 2]),  # 我就得刚
            np.array([4]),  # 强

            # 74
            np.array([4, 2, 2]),     # - 经风
            np.array([6, 2, 2, 2]),  # 暴 过黑
            np.array([4, 4, 2, 2]),  # 夜 - 度阡
            np.array([6, 2, 2, 2]),  # 陌 越洋
            np.array([4, 4, 2, 2]),  # 海 - 有你
            np.ones((3,)) * 4,       # 手牵引
            np.array([4, 4, 2, 2]),  # 我 - 我就
            np.ones((3,)) * 4,       # 勇往向
            np.array([4]),           # 前

            # 106
            np.array([4, 2, 2]),  # - 愿我
            np.ones((3,)) * 4,  # 所行路
            np.array([4, 4, 2, 2]),  # 径 - 愿我
            np.ones((3,)) * 4,  # 所历际
            np.array([4, 4, 2, 2]),  # 遇 - 处处
            np.ones((3,)) * 4,  # 留 下
            np.array([2, 2, 4, 4]),  # 有你同在
            np.array([2, 2, 4, 4]),  # 的恩典痕
            np.ones((3,)) * 4,  # 迹 - -

            # 141
            np.array([4, 4, 2, 2]),  # - - 因你
            np.ones((3,)) * 4,  # 与我同
            np.array([4, 4, 2, 2]),  # 行 - 我就
            np.ones((3,)) * 4,  # 不会孤
            np.array([4, 4, 2, 2]),  # 寂 - 欢笑
            np.ones((3,)) * 4,  # 时你同
            np.array([4, 4, 2, 2]),  # 喜 - 悲伤
            np.ones((3,)) * 4,  # 时你共
            np.array([4]),  # 泣

            # 170
            np.array([4, 2, 2]),  # - 因你
            np.ones((3,)) * 4,  # 是我力
            np.array([4, 4, 2, 2]),  # 量 - 我就
            np.ones((3,)) * 4,  # 不会绝
            np.array([4, 4, 2, 2]),  # 望 - 困乏
            np.ones((3,)) * 4,  # 软弱中
            np.array([2, 2, 4, 4]),  # 有你赐恩
            np.array([2, 2, 6, 2]),  # 我就得刚
            np.array([4]),  # 强

            # 199
            np.array([4, 2, 2]),  # - 经风
            np.array([6, 2, 2, 2]),  # 暴 过黑
            np.array([4, 4, 2, 2]),  # 夜 - 度阡
            np.array([6, 2, 2, 2]),  # 陌 越洋
            np.array([4, 4, 2, 2]),  # 海 - 有你
            np.ones((3,)) * 4,  # 手牵引
            np.array([4, 4, 2, 2]),  # 我 - 我就
            np.ones((3,)) * 4,  # 勇往向
            np.array([4]),  # 前

            np.array([4, 2, 2]),  # - 愿我
            np.ones((3,)) * 4,  # 所行路
            np.array([4, 4, 2, 2]),  # 径 - 愿我
            np.ones((3,)) * 4,  # 所历际
            np.array([4, 4, 2, 2]),  # 遇 - 处处
            np.ones((3,)) * 4,  # 留 下
            np.array([2, 2, 4, 4]),  # 有你同在
            np.array([2, 2, 4, 4]),  # 的恩典痕
            np.ones((1,)) * 4,  # 迹 - -

        ]
        self.beatsPosX = np.array([1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 2, 3,
                                   2, 1, 2, 3, 2, 1, 2, 2,  # 我就得刚强
                                   1, 2, 2, 1, 3.2, 2.4, 1.6,
                                   0.8, 1, 2, 2, 3, 0.8, 1.6, 2.4,
                                   3.2, 1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 2, 3,
                                   2, 1, 2, 3, 2, 1, 2, 2, 1, 1, 1, 1,
                                   1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 2, 3,
                                   2, 1, 2, 3, 2, 1, 2, 2,  # 我就得刚强
                                   1, 2, 2, 1, 3.2, 2.4, 1.6,
                                   0.8, 1, 2, 2, 3, 0.8, 1.6, 2.4,
                                   3.2, 1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 3, 2,
                                   1, 1, 2, 1, 2, 3, 2,
                                   1, 1, 1, 1, 2, 2, 3,
                                   2, 1, 2, 3, 2, 1, 2, 2,
                                   ])
        # self.beatsPosX = None


def convertXY(song: object, note_size: int, top_player: int) -> list:
    """
    Convert counts to x and y position in the windows
    :param note_size: height of notes
    :param top_player: top y position of player
    :param song: contains all counts for a song
    :return: a list of notes x and y positions
    """

    raw_beats = song.beats
    beats = np.concatenate(raw_beats)
    multiplier = np.zeros((len(beats),))

    for i in range(len(beats) - 1):
        multiplier[i + 1] = beats[i] + multiplier[i]

    pos_y = [(top_player - 1 * note_size) - multiplier[i] * note_size for i in range(len(beats))]

    if song.beatsPosX is not None:
        pos_x = (song.beatsPosX * 100).astype(int)
        return pos_x, pos_y[song.introEndPoint + 1:]
    else:
        pos_x = (np.ones(beats.shape) * 200).astype(int)
        # pos_x = np.zeros(beats.shape)
        # for i in range(len(pos_x)):
        #     x_ = [100, 200, 300]
        #     if i == 0:
        #         pos_x[i] = choice(x_)
        #     else:
        #         x_.remove(pos_x[i - 1])
        #         pos_x[i] = choice(x_)

        return pos_x[song.introEndPoint + 1:], pos_y[song.introEndPoint + 1:]
