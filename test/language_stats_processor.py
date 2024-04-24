from datetime import datetime
from reactivex import from_iterable

import src.language_stats_processor as lang
from src.message import GithubEvent


def test_that_language_stats_are_calculated_as_expected():
    # GIVEN
    events = [
        GithubEvent(keyword="keyword1", repo_fullname="repo1", found_date=datetime.now(), stars_cnt=1,
                    langs=["Java", "C++"]),
        GithubEvent(keyword="keyword2", repo_fullname="repo2", found_date=datetime.now(), stars_cnt=1,
                    langs=["Java", "Go"]),
        GithubEvent(keyword="keyword2", repo_fullname="repo4", found_date=datetime.now(), stars_cnt=1, langs=["Java"]),
        GithubEvent(keyword="keyword1", repo_fullname="repo3", found_date=datetime.now(), stars_cnt=1,
                    langs=["Java", "Python"])
    ]
    storage = {}
    expected_storage = {
        "keyword1": {
            "Java": 2,
            "C++": 1,
            "Python": 1
        },
        "keyword2": {
            "Java": 2,
            "Go": 1
        }
    }

    # WHEN
    lang.get_lang_stats(storage)(from_iterable(events)).subscribe(on_next=print)

    # THEN
    assert storage == expected_storage
