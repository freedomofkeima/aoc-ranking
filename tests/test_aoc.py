# -*- coding: utf-8 -*-
import os

import pytest
import requests
from bs4 import BeautifulSoup
from requests.models import Response

from aoc_ranking.aoc import RankRecord, extract_data_from_line, get_scoreboard

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def mocked_requests(monkeypatch):
    def get(uri, *args, **kwargs):
        r = Response()
        if uri == "https://adventofcode.com/2020/leaderboard/day/1":
            r.status_code = 200
            # Read HTML file (a downloaded copy from real URL above)
            path = os.path.join(SCRIPT_PATH, "files/2020-01.html")
            f = open(path, "r")
            r._content = str.encode(f.read())
        else:
            r.status_code = 400
        return r

    monkeypatch.setattr(requests, "get", get)


def test_get_scoreboard(mocked_requests):
    scoreboard = get_scoreboard(2020, 1)
    assert len(scoreboard) == 200


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
