# -*- coding: utf-8 -*-
import datetime
import logging
import sys

from aoc_ranking.aoc import calculate_global_scoreboard, generate_global_rank
from aoc_ranking.util import write_global_rank_to_file


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # Generate cache
    now = datetime.datetime.now()
    for year in range(2015, now.year + (now.month == 12)):
        data = calculate_global_scoreboard(year)
        results = generate_global_rank(data)
        write_global_rank_to_file(year, results)


if __name__ == "__main__":
    main()
