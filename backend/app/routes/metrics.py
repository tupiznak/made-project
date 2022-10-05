from fastapi import Request
from prometheus_client import Gauge
from starlette_exporter import handle_metrics

from .database.author import author_operations
from .database.paper import paper_operations
from .database.venue import venue_operations

papers_count = Gauge('papers_count', 'Count of papers')
author_count = Gauge('author_count', 'Count of author')
venue_count = Gauge('venue_count', 'Count of venue')


def metric_request(request: Request):
    papers_count.set(paper_operations.total_size())
    author_count.set(author_operations.total_size())
    venue_count.set(venue_operations.total_size())
    return handle_metrics(request)
