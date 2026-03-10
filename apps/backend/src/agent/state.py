import operator
from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict, total=False):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    plan: str
    search_results: str
    next_step: str
    retrieval_sources: list[dict]
