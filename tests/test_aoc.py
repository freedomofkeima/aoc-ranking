# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup

from aoc_ranking.aoc import RankRecord, extract_data_from_line


@pytest.mark.parametrize(
    "entity, expected",
    [
        (
            """
<div class="leaderboard-entry">
  <span class="leaderboard-position">  1)</span>
  <span class="leaderboard-time">Dec 01  00:10:00</span>
  <span class="leaderboard-userphoto"><img height="20" src="https://lh3.googleusercontent.com/a-/fake"/></span>
  Lupin
  <a class="supporter-badge" href="/2020/support" title="Advent of Code Supporter">(AoC++)</a>
  <a class="sponsor-badge" href="https://www.fake.com/" onclick="if(ga)ga('send','event','sponsor','badge',this.href);" target="_blank" title="Member of sponsor: Fake">(Sponsor)</a>
</div>
            """,
            RankRecord(1, "Lupin", "https://lh3.googleusercontent.com/a-/fake"),
        ),
        (
            """
<div class="leaderboard-entry">
  <span class="leaderboard-position">100)</span>
  <span class="leaderboard-time">Dec 01  01:00:00</span>
  <span class="leaderboard-userphoto"></span>
  Lupin
</div>
            """,
            RankRecord(100, "Lupin", None),
        ),
    ],
)
def test_extract_data_from_line(entity, expected):
    soup = BeautifulSoup(entity, "html.parser")
    line = extract_data_from_line(soup.select("div.leaderboard-entry")[0])
    assert line.rank == expected.rank
    assert line.name == expected.name
    assert line.photo_tag == expected.photo_tag
