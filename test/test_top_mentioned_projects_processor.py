from datetime import datetime, timedelta

from reactivex import from_iterable, Observable

import src.top_mentioned_projects_processor as top
from src.message import GithubEvent


def test_that_processor_works_as_expected():
    # GIVEN
    keyword = "my keyword"
    events = [
        GithubEvent(keyword=keyword, repo_fullname="repo1", found_date=datetime.now() - timedelta(hours=2), stars_cnt=5,
                    langs=["Java"]),
        GithubEvent(keyword=keyword, repo_fullname="repo2", found_date=datetime.now() - timedelta(minutes=5),
                    stars_cnt=4, langs=["Java"]),
        GithubEvent(keyword=keyword, repo_fullname="repo3", found_date=datetime.now() - timedelta(hours=10),
                    stars_cnt=3, langs=["Java"]),
        GithubEvent(keyword=keyword, repo_fullname="repo4", found_date=datetime.now() - timedelta(hours=12),
                    stars_cnt=2, langs=["Java"]),
        GithubEvent(keyword=keyword, repo_fullname="repo5", found_date=datetime.now() - timedelta(hours=23),
                    stars_cnt=2, langs=["Java"]),
        GithubEvent(keyword=keyword, repo_fullname="repo6", found_date=datetime.now() - timedelta(hours=42),
                    stars_cnt=43, langs=["Java"]),
        GithubEvent(keyword="other_keyword", repo_fullname="repo7", found_date=datetime.now() - timedelta(seconds=90),
                    stars_cnt=43, langs=["Java"])
    ]
    expected_repos = ["repo1", "repo2", "repo3", "repo4", "repo5"]
    source: Observable[GithubEvent] = from_iterable(events)
    processor = top.get_top_5_mentioned_projects(keyword)

    # WHEN
    result = []
    processor(source).subscribe(on_next=lambda e: result.append(e))

    # THEN
    assert expected_repos == result
