import asyncio
import threading

from dotenv import load_dotenv
from reactivex import Observable, operators as ops
import reactivex
from reactivex.scheduler import ThreadPoolScheduler

import src.new_repo_processor as repo
import src.language_stats_processor as lang
import src.top_mentioned_projects_processor as top
from src.github_client import fetch_data_as_observable
from src.message import GithubEvent

load_dotenv()


async def main():
    thread_pool_scheduler = ThreadPoolScheduler(max_workers=10)
    keyword = "python"

    repos_storage = dict()
    new_repos = repo.filter_new_repos(repos_storage)
    lang_stat = lang.get_lang_stats(dict())
    top_5 = top.get_top_5_mentioned_projects(keyword)

    fetched_data: Observable[GithubEvent] = await fetch_data_as_observable(keyword)
    fetched_data.pipe(ops.retry(5), ops.share(),
                      lambda src_of_message: reactivex.merge(new_repos(src_of_message),
                                                             lang_stat(src_of_message),
                                                             top_5(src_of_message)),
                      ops.observe_on(thread_pool_scheduler)
                      ).subscribe(
        on_next=lambda event: print(f"New event (Thread: {threading.current_thread().name}): {event}"),
        on_error=print)


if __name__ == "__main__":
    asyncio.run(main())
