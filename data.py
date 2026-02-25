game_data = {
    1: {
        "cutscenes": {
            1:"game graphics/cutscenes/DAY 1/Day1_cut1.png",
            2:"game graphics/cutscenes/DAY 1/Day1_cut2.png",
            3:"game graphics/cutscenes/DAY 1/Day1_cut3.png",
            4:"game graphics/cutscenes/DAY 1/Day1_cut4.png",
            5:"game graphics/cutscenes/DAY 1/Day1_cut5.png",
            6:"game graphics/cutscenes/DAY 1/Day1_cut6.png",
            7:"game graphics/cutscenes/DAY 1/Day1_cut7.png",
        },
        "next_day": 2
    },
    2: {
        "first_map": "D2",
        "maps": {
            "D2": {
                "map": "game graphics/maps/D2.png",
                "first_spawn": (18, 8),
                "cutscenes": {
                    "intro_cutscene": {
                        1: "game graphics/cutscenes/DAY2/DAY2.png"},
                    "HouseA": {
                        1: "game graphics/cutscenes/DAY2/BuildingA.png",
                    },
                    "HouseC": {
                        1: "game graphics/cutscenes/DAY2/BuildingC.png",
                    },
                },
                "collision": [
                    '11111111111111111111',
                    '11111111111111111141',
                    '11111111111111111101',
                    '11111111111111111101',
                    '10AAA010BBB010CCC001',
                    '11100000001000000001',
                    '11100000004000000101',
                    '17440000000000000071',
                    '17000000000000000071',
                    '17000000000000000071',
                    '10000000000000444401',
                    '100440440666004114P1',
                    '10011011000000000001',
                    '11111111111111111151',
                    '11111111111111111111',
                ],
                "dialog": [
                    "You can't go there",
                    "Thank you for delivering the package! \nI hope you have a great day!"
                ]
            }
        },
        "next_day": 3
    },
    3: {
        "first_map": "D3-1",
        "maps": {
            "D3-1": {
                "map": "game graphics/maps/D3-1.png",
                "first_spawn": (18, 8),
                "cutscenes": {
                    "intro_cutscene": {
                        1: "game graphics/cutscenes/DAY3/DAY3.png"},
                },
                "collision": [
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    'a0000000000000000071',
                    'a0000000000000000071',
                    'a0000000000000000071',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                    '11111111111111111111',
                ],
                "dialog": [
                    "You can't go there"
                ],
                "exits": {
                    "a": {"target_map": "D3-2", "spawn_at": (18, 7)} # Exit 'a' leads to D3-2
                }
            },
            "D3-2": {
                "map": "game graphics/maps/D3-2.png",
                "cutscenes": {
                    "HouseD": {
                        1: "game graphics/cutscenes/DAY3/HouseD/Day3_HouseD_1.png",
                        2: "game graphics/cutscenes/DAY3/HouseD/Day3_HouseD_2.png",
                        3: "game graphics/cutscenes/DAY3/HouseD/Day3_HouseD_3.png",
                        4: "game graphics/cutscenes/DAY3/HouseD/Day3_HouseD_4.png",
                        5: "game graphics/cutscenes/DAY3/HouseD/Day3_HouseD_5.png",
                    },
                },
                "dialog": [
                    "This house looks abandoned. \nI don't think anyone lives here.",
                ],
                "collision": [
                '11111111111111111111',
                '11111111111111111111',
                '11111111111311111111',
                '110DDDD0003311113331',
                '11000000003311113111',
                '11111111113311113111',
                'b000000000333333333a',
                'b000000000000000000a',
                'b000000000000000033a',
                '13330000000000000311',
                '11130000111111111311',
                '1113000E111111111111',
                '1113000E111111111111',
                '1111000E111111111111',
                '11111111111111111111',
            ],
                "exits": {
                    "b": {"target_map": "D3-3", "spawn_at": (18, 8)}, # Leads to Map 3
                    "a": {"target_map": "D3-1", "spawn_at": (1, 8)}  # Leads back to Map 1
                }
            },
            "D3-3": {
                "map": "game graphics/maps/D3-3.png",
                "cutscenes": {
                    "HouseG": {
                        1: "game graphics/cutscenes/DAY3/HouseG/Day3_HouseG.png"
                    },
                    "HouseH": {
                        1: "game graphics/cutscenes/DAY3/HouseH/Day3_HouseH_1.png",
                        2: "game graphics/cutscenes/DAY3/HouseH/Day3_HouseH_2.png",
                    },
                    "HouseI": {
                        1: "game graphics/cutscenes/DAY3/HouseI/Day3_HouseI_1.png",
                        2: "game graphics/cutscenes/DAY3/HouseI/Day3_HouseI_2.png",
                    }
                },
                "dialog": [
                    "You can't go there",
                    "Thank you for delivering the package! \nI hope you have a great day!"
                ],
                "collision": [
                '11111111111111111111',
                '11111111111111111111',
                '11111111111111111111',
                '11111113311111111111',
                '11111110001111113331',
                '111111103130GG000001',
                '100FF000333000000001',
                '1700000000000000000b',
                '1700000000000000000b',
                '1700000000000000000b',
                '1HHHHHHHHHHH00000001',
                '111111111111000II001',
                '11111111111111111111',
                '11111111111111111111',
                '11111111111111111111',
            ],
                "exits": {
                    "b": {"target_map": "D3-2", "spawn_at": (1, 7)} # Leads back to Map 2
                }
            }
        },
        "next_day": 4,
    },
    4: {
        "first_map": "D4-1",
        "maps": {
            "D4-1": {
                "map": "game graphics/maps/D4-1.png",
                "first_spawn": (2, 8),
                "cutscenes": {
                    "intro_cutscene": {
                        1: "game graphics/cutscenes/DAY4/DAY4.png"},
                },
                "dialog": [
                    "You can't go there",
                    "A massive tree blocks the way. \nIt doesn't look like you can get past it.",
                ],
                "collision": [
                    '11111111111111111111',
                    '11011110000000000001',
                    '11011110000000000001',
                    '10000000000000000001',
                    '11110000001111110001',
                    '11110000001111110001',
                    '11110000001111110001',
                    '1700000000000111000c',
                    '1700000000000111000c',
                    '1700000000001111100c',
                    '10011011100011111111',
                    '10000011100000000111',
                    '11110011100000001111',
                    '11110000000008881111',
                    '11111111111111111111',
                ],
                "exits": {
                    "c": {"target_map": "D4-2", "spawn_at": (1, 8)} # Exit 'c' leads to D4-2
                }
            },
            "D4-2": {
                "map": "game graphics/maps/D4-2.png",
                "collision": [
                '11111111111111111111',
                '11100000001000000001',
                '11101011111011111101',
                '1110101111100000010d',
                '11101010001011111101',
                '11101110101000001101',
                '11101010101111101111',
                'c0101010100000100001',
                'c0001010111010111101',
                'c0101010101010100001',
                '11100010001010101111',
                '11101010101010100001',
                '11101110101011111101',
                '11100000101000000001',
                '11111111111111111111',
            ],
                "exits": {
                    "c": {"target_map": "D4-1", "spawn_at": (18, 8)}, # Leads back to Map 1
                    "d": {"target_map": "D4-3", "spawn_at": (2, 8)}  # Leads to Map 3
                }
            },
            "D4-3": {
                "map": "game graphics/maps/D4-3.png",
                "cutscenes": {
                    "HouseJ":{
                        1: "game graphics/cutscenes/DAY4/red_house.png",
                        2: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_0.png",
                        3: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_1.png",
                        4: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_2.png",
                        5: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_3.png",
                        6: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_4.png",
                        7: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_5.png",
                        8: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_6.png",
                        9: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_7.png",
                        10: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_8.png",
                        11: "game graphics/cutscenes/DAY4/DAY4_Sent/DAY4_Sent_9.png"
                    }
                },
                "collision": [
                '11111111111111111111',
                '11100001111011111111',
                '11100111111011111111',
                '11100111100011111111',
                '10000001100000JJJ011',
                '10111001110000000001',
                '10111001110000000001',
                '1d000000110000000001',
                '1d000000110000000001',
                '1d000000111110000011',
                '10000000011111100111',
                '11100000000011100111',
                '11100000000000000001',
                '10000000000000000111',
                '11111111111111111111',
            ],
                "exits": {
                    "d": {"target_map": "D4-2", "spawn_at": (18, 3)} # Leads back to Map 2
                }
            }
        },
        "next_day": 5,
    },
    5: {
        "first_map": "D5-1",
        "maps": {
            "D5-1": {
                "map": "game graphics/maps/D5-1.png",
                "first_spawn": (1, 8),
                "cutscenes": {
                    "intro_cutscene": {
                        1: "game graphics/cutscenes/DAY5/DAY5.png"},
                },
                "dialog": [
                    "A massive tree blocks the way. \nIt doesn't look like you can get past it.",
                ],
                "collision": [
                    '11111111111111111111',
                    '11101118811001111111',
                    '11100011000000001111',
                    '11111011111111101111',
                    '11111000111111100011',
                    '11100000000111101111',
                    '11100111100000001111',
                    '11100110011111111111',
                    '10000000000000011111',
                    '11011100110011011111',
                    '11011111110000000111',
                    '11111111001111010111',
                    '10000011001100110111',
                    '10000000000000000111',
                    '1e111111111111111111',
                ],
                "exits": {
                    "e": {"target_map": "D5-2", "spawn_at": (1, 1)} # Exit 'e' leads to D5-2
                }
            },
            "D5-2": {
                "map": "game graphics/maps/D5-2.png",
                "dialog": [
                    "A massive tree blocks the way. \nIt doesn't look like you can get past it.",
                ],
                "collision": [
                '1e111111111111111111',
                '10000000111110000001',
                '11100110111110110111',
                '11111110000000110111',
                '10011010001111110001',
                '11011010111101110111',
                '11000001110000000111',
                '11001101110111011001',
                '11111101110111000081',
                '11110000000111001101',
                '11110111111111111111',
                '11100110011111111111',
                '11100000000111111111',
                '11111001100001111111',
                '1111111111f111111111',
            ],
                "exits": {
                    "e": {"target_map": "D5-1", "spawn_at": (1, 13)}, # Leads back to Map 1
                    "f": {"target_map": "D5-3", "spawn_at": (10, 1)}  # Leads to Map 3
                }
            },
            "D5-3": {
                "map": "game graphics/maps/D5-3.png",
                "cutscenes": {
                    "End":{
                        1: "game graphics/cutscenes/DAY5/DAY5_altar_1.png",
                        2: "game graphics/cutscenes/DAY5/DAY5_altar_2.png",
                        3: "game graphics/cutscenes/DAY5/DAY5_altar_3.png",
                        4: "game graphics/cutscenes/DAY5/THE END.png",
                    }
                },
                "collision": [
                '1111111111f111111111',
                '11011100110111111111',
                '10011100110100000111',
                '11000000000101100111',
                '11011111001101100111',
                '11011000111100010011',
                '11011000000100010011',
                '11011000110101110001',
                '1101101111010111000g',
                '11000011000101111111',
                '11111111100100000011',
                '11110000000111111011',
                '11110111111111111011',
                '11110000000000000001',
                '11111111111111111111',
            ],
                "exits": {
                    "f": {"target_map": "D5-2", "spawn_at": (10, 13)} # Leads back to Map 2
                }
            }
        }
    }
}