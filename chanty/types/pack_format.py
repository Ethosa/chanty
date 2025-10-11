from enum import Enum


class PackFormat(int, Enum):
    MC_1_13 = 4
    MC_1_14 = 5
    MC_1_15 = 6
    MC_1_16 = 7
    MC_1_16_2 = 8
    MC_1_16_5 = 9
    MC_1_17 = 10
    MC_1_17_1 = 11
    MC_1_18 = 12
    MC_1_18_2 = 13
    MC_1_19 = 14
    MC_1_19_2 = 15
    MC_1_19_3 = 16
    MC_1_19_4 = 17
    MC_1_20 = 18
    MC_1_20_1 = 48
    MC_1_20_4 = 61
    MC_1_21 = 71

    @classmethod
    def latest(cls) -> 'PackFormat':
        return list(cls)[-1]

    @classmethod
    def from_mc_version(cls, version: str) -> 'PackFormat':
        mapping = {
            "1.13": cls.MC_1_13,
            "1.14": cls.MC_1_14,
            "1.15": cls.MC_1_15,
            "1.16": cls.MC_1_16_5,
            "1.17": cls.MC_1_17_1,
            "1.18": cls.MC_1_18_2,
            "1.19": cls.MC_1_19_4,
            "1.20": cls.MC_1_20_4,
            "1.21": cls.MC_1_21,
            "1.21.5": cls.MC_1_21,
            "1.21.9": cls.MC_1_21,
            "1.21.10": cls.MC_1_21,
        }
        if version not in mapping:
            raise ValueError(f"Unsupported Minecraft version: {version}")
        return mapping[version]
