# -*- coding: utf-8 -*-
import csv
import os
from typing import List

from aoc_ranking.aoc import GlobalScoreRecord

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


def write_global_rank_to_file(year: int, data: List[GlobalScoreRecord]):
    dst_path = os.path.join(SCRIPT_PATH, "..", "data", f"{year}.txt")
    with open(dst_path, "w", newline="", encoding="utf-8") as fobj:
        writer = csv.writer(fobj)
        writer.writerow(
            [
                "Rank",
                "Name",
                "Score",
                "Avatar",
            ]
        )
        for entity in data:
            writer.writerow(
                [
                    entity.rank,
                    entity.name,
                    entity.score,
                    entity.photo_url if entity.photo_url else "",
                ]
            )
