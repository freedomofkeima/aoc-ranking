# -*- coding: utf-8 -*-
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup, element

# Example: "  1) Dec 01 00:10:00 Lupin (AoC++) (Sponsor)"
# There are 2 information that we want to extract, which is:
# - Rank: 1
# - Name: Lupin (AoC++) (Sponsor)
MATCHER = re.compile(
    r"[\s]*([0-9]{1,3})\)[\s]*Dec.+[0-9]{2}[\s]*[0-9]{2}:[0-9]{2}:[0-9]{2}[\s]*(.*)"
)


@dataclass
class RankRecord:
    rank: int
    name: str
    photo: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "name": self.name,
            "photo": self.photo if self.photo else "",
        }


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
    photo = entity.select("span.leaderboard-userphoto")[0].find()
    return RankRecord(int(rank), name, photo)
