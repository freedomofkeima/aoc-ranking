# -*- coding: utf-8 -*-
import logging
import sys

from aoc_ranking.aoc import get_scoreboard


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # TODO:
    scoreboard = get_scoreboard(year=2020, day=1)
    for entity in scoreboard:
        print(entity.to_dict())


if __name__ == "__main__":
    main()
