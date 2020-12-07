# -*- coding: utf-8 -*-
import logging
import sys

from aoc_ranking.aoc import calculate_global_scoreboard, generate_global_rank


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # TODO:
    data = calculate_global_scoreboard(2020)
    results = generate_global_rank(data)
    for entity in results:
        print(entity.rank, entity.name, entity.score, entity.photo_url)


if __name__ == "__main__":
    main()
