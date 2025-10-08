from enum import Enum


class PackFormat(int, Enum):
    V4 = 4
    V5 = 5
    V6 = 6
    V7 = 7
    V8 = 8
    V9 = 9
    V10 = 10
    V11 = 11
    V12 = 12
    V13 = 13
    V14 = 14
    V15 = 15
    V16 = 16
    V17 = 17
    V18 = 18
    V48 = 48
    V61 = 61
    V71 = 71

    @classmethod
    def latest(cls) -> 'PackFormat':
        return list(PackFormat)[-1]
