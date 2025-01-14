from fastapi import APIRouter

from app.llm.anthropic_service import AnthropicService
from app.llm.openai_service import OpenAIService
from app.models import (
    CompareResponsesRequest,
    GenerateTestCodeRequest,
    ReEvaluateResponsesRequest,
    RewriteRequest,
    SolveTaskRequest,
    TranslateCodeRequest,
)


router = APIRouter(prefix="/llm")

anthropic = AnthropicService()
openai = OpenAIService()


@router.post("/translation/solve")
async def solve(body: SolveTaskRequest):
    """
    Solve a task
    """
    # return {"examples":[{"input":[{"var_name":"nums","value":"[1, 2, 3, 4, 5, 6, 7]"},{"var_name":"k","value":"3"}],"output":"[5, 6, 7, 1, 2, 3, 4]","explanation":"The list is rotated 3 positions to the right: [5, 6, 7, 1, 2, 3, 4]. Each segment is rotated in parallel threads."},{"input":[{"var_name":"nums","value":"[10, 20, 30, 40, 50]"},{"var_name":"k","value":"1"}],"output":"[50, 10, 20, 30, 40]","explanation":"The list is rotated 1 position to the right: [50, 10, 20, 30, 40]."},{"input":[{"var_name":"nums","value":"[7, 8, 9, 1, 2]"},{"var_name":"k","value":"2"}],"output":"[1, 2, 7, 8, 9]","explanation":"The list is rotated 2 positions to the right: [1, 2, 7, 8, 9]."}],"solution":"To rotate the list to the right by k positions using multiple threads, start by calculating the effective rotation k as k mod len(nums). Given that calculating each rotation can be thought of independently, split the list into segments that can be processed concurrently by threads. Each thread will rotate its segment individually, and then results are combined. The default rotate_segment function shifts items in `segment` based on provided `k` its length.","python_code":"from threading import Thread\n\ndef rotate_segment(segment: list, k: int) -> list:\n    n = len(segment)\n    k = k % n  # Effective rotation\n    return segment[-k:] + segment[:-k]\n\n\ndef rotate_list(nums: list, k: int) -> list:\n    n = len(nums)\n    if n == 0:\n        return []\n    k = k % n  # Effective rotation\n\n    num_threads = min(4, n)  # Use up to 4 threads\n    step = n // num_threads\n    segments = [nums[i:i + step] for i in range(0, n, step)]\n\n    # Handles the last segment if splitting doesn't divide evenly\n    if len(segments) > num_threads:\n        segments[-2].extend(segments[-1])\n        segments.pop()\n\n    rotated_segments = [None] * len(segments)\n\n    def rotate_and_store(segment_id):\n        rotated_segments[segment_id] = rotate_segment(segments[segment_id], k)\n\n    threads = []\n    for i in range(len(segments)):\n        thread = Thread(target=rotate_and_store, args=(i,))\n        threads.append(thread)\n        thread.start()\n\n    for thread in threads:\n        thread.join()\n\n    # Concatenate segments to form final rotated list\n    rotated_list = [item for segment in rotated_segments for item in segment]\n\n    # Rotate back the concatenated result\n    return rotated_list[-k:] + rotated_list[:-k]\n\n# Example usage:\nassert rotate_list([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]  # Test rotation of 3\nassert rotate_list([10, 20, 30, 40, 50], 1) == [50, 10, 20, 30, 40]  # Test rotation of 1\nassert rotate_list([7, 8, 9, 1, 2], 2) == [1, 2, 7, 8, 9]  # Test rotation of 2\nassert rotate_list([], 5) == []  # Edge case: empty list\nassert rotate_list([1], 0) == [1]  # Edge case: single element\n"}
    res = openai.solve_task(body.prompt)
    print(res)
    return res


@router.post("/translation/rewrite")
async def rewrite(body: RewriteRequest):
    """
    rewrite a text
    """
    res = openai.rewrite_text(body.text)
    print(res)
    return res


@router.post("/translation/translate")
async def translate(body: TranslateCodeRequest):
    """
    Translate from Swift to Python
    """
    # return {"code":"from typing import List, Tuple\n\n\ndef find_parallel_topological_order(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:\n    \"\"\"\n    Finds a valid topological order of tasks in a directed acyclic graph (DAG).\n    Each inner list contains the tasks that can be completed in parallel at the same time step.\n\n    :param n: The number of nodes (tasks) in the graph.\n    :param edges: A list of directed edges representing dependencies between tasks.\n    :return: A list of lists, where each inner list contains tasks that can be completed in parallel.\n    \"\"\"\n    # Create an adjacency list and an array to count in-degrees\n    adj_list = [[] for _ in range(n)]\n    in_degree = [0] * n\n\n    # Build the graph\n    for u, v in edges:\n        adj_list[u].append(v)\n        in_degree[v] += 1\n\n    # Initialize a queue with all nodes having no incoming edges (in-degree 0)\n    queue = [i for i in range(n) if in_degree[i] == 0]\n\n    # Prepare to hold the result\n    result = []\n\n    # Perform a modified Kahn's algorithm to process nodes in topological order\n    while queue:\n        # Current level of tasks that can be completed in parallel\n        current_level = []\n\n        # Process all nodes at the current level\n        for _ in range(len(queue)):\n            node = queue.pop(0)\n            current_level.append(node)\n\n            # Decrease the in-degree of adjacent nodes\n            for neighbor in adj_list[node]:\n                in_degree[neighbor] -= 1\n                if in_degree[neighbor] == 0:\n                    queue.append(neighbor)\n\n        # Add the current level to the result\n        result.append(current_level)\n\n    return result\n"}
    res = openai.translate_to_python(body.code)
    print(res)
    return res


@router.post("/comparison/generate-turns")
async def generate_turns(body: SolveTaskRequest):
    """
    Generate turns for a conversation
    """
    res = anthropic.generate_turns(body.prompt, language=body.language)
    print(res)
    return res


@router.post("/comparison/compare")
async def compare(body: CompareResponsesRequest):
    """
    Evaluate two models
    """
    res = anthropic.compare_responses(**body.model_dump())
    print(res)
    return res

@router.post("/comparison/reevaluate")
async def reevaluate(body: ReEvaluateResponsesRequest):
    res = anthropic.reevaluate_responses(
        body.prompt,
        body.model_a,
        body.model_b,
        body.output,
        body.comparison_response,
        body.requested_changes,
        body.language,
    )
    print(res)
    return res

@router.post("/comparison/generate-test-code")
async def generate_test_code(body: GenerateTestCodeRequest):
    res = anthropic.generate_test_code(body.prompt, body.answer)
    print(res)
    return res
