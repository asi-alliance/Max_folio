#!/usr/bin/env python3
"""Web search tool using DuckDuckGo (ddgs)."""

DESCRIPTION = "Search the web. Returns JSON array of results with title, url, snippet."

from ddgs import DDGS
import json

def run(query, max_results=10):
    """
    query: str - search query
    max_results: str or int - max number of results (default 10)
    returns: str - JSON array of results
    """
    max_results = int(max_results)
    with DDGS() as ddgs:
        results = [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            }
            for r in ddgs.text(query, max_results=max_results)
        ]
    return json.dumps(results, indent=2)
