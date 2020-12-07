# -*- coding: utf-8 -*-
import re
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup, element

# Example: "  1) Dec 01 00:10:00 Lupin (AoC++) (Sponsor)"
# There are 2 information that we want to extract, which is:
# - Rank: 1
# - Name: Lupin (AoC++) (Sponsor)
MATCHER = re.compile(
    r"[\s]*([0-9]{1,3})\)[\s]*Dec.+[0-9]{2}[\s]*[0-9]{2}:[0-9]{2}:[0-9]{2}[\s]*(.*)"
)

EXCLUDE_DAY = {
    2020: [1],
    2019: [],
    2018: [6],
    2017: [],
    2016: [],
    2015: [],
}


@dataclass
class RankRecord:
    rank: int
    name: str
    link: Optional[str] = None
    photo_url: Optional[str] = None


@dataclass
class GlobalScoreRecord:
    rank: int
    name: str
    score: int
    link: Optional[str] = None
    photo_url: Optional[str] = None


def get_scoreboard(year: int, day: int) -> List[RankRecord]:
    url = f"https://adventofcode.com/{year}/leaderboard/day/{day}"
    try:
        r = requests.get(url, timeout=30)
    except:
        return []
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.content, "html.parser")
    raw_data = soup.select("div.leaderboard-entry")
    results = []
    for entity in raw_data:
        line = extract_data_from_line(entity)
        results.append(line)
    return results


def extract_data_from_line(entity: element.Tag) -> RankRecord:
    data = MATCHER.match(entity.get_text())
    rank, name = data.group(1), data.group(2)
    href_tags = entity.find_all(href=True)
    link = None
    for a in href_tags:
        if "github" in a["href"] or "twitter" in a["href"]:
            link = a["href"]
    photo_url = entity.select("span.leaderboard-userphoto")[0].find()
    if photo_url:
        photo_url = photo_url.get("src")
    return RankRecord(int(rank), name, link, photo_url)


def tally(results: Dict[Tuple, int], scoreboard: List[RankRecord]) -> Dict[Tuple, int]:
    for i in range(100):
        key = (scoreboard[i].name, scoreboard[i].link, scoreboard[i].photo_url)
        score = 100 - i
        if key in results:
            results[key] += score
        else:
            results[key] = score
    return results


def calculate_global_scoreboard(year: int) -> Dict[Tuple, int]:
    results = {}
    for day in range(1, 26):
        print(f"Processing year {year}, day {day}")
        if day in EXCLUDE_DAY[year]:
            print(f"  Skipping year {year}, day {day} because of technical problem")
            continue
        scoreboard = get_scoreboard(year=year, day=day)
        if not scoreboard:
            print(f"  Skipping year {year}, day {day} because scoreboard is empty")
            continue
        # Two stars
        results = tally(results, scoreboard[:100])
        # One star
        results = tally(results, scoreboard[100:])
    return results


def generate_global_rank(data: Dict[Tuple, int]) -> List[GlobalScoreRecord]:
    # Initialize
    rank = 0
    duplicate = 0
    previous_score = -1
    results = []
    # Process
    for key, score in sorted(data.items(), key=itemgetter(1), reverse=True):
        if previous_score != score:
            rank = rank + duplicate + 1
            duplicate = 0
        else:
            duplicate = duplicate + 1
        results.append(GlobalScoreRecord(rank, key[0], score, key[1], key[2]))
        previous_score = score
    return results
