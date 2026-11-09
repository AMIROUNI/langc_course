
import math

from langc_course.clients.ollama_client import OllamaCloudClient
from dotenv import load_dotenv

load_dotenv()


# =====================================================
# 1. TOKEN BUDGET
# =====================================================

class TokenBudget:

    def __init__(self, max_token_per_request: int = 4000):
        self.max_per_request = max_token_per_request

        self.usage = {
            "total_input": 0,
            "total_output": 0,
            "requests": 0
        }

    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens."""
        return math.ceil(len(text.split()) * 1.3)

    def check_budget(self, text: str) -> tuple[bool, int]:
        """Check whether input text is within the budget."""

        tokens = self.estimate_tokens(text)

        return tokens <= self.max_per_request, tokens

    def record_usage(self, input_tokens: int, output_tokens: int):
        """Record input and output token usage."""

        self.usage["total_input"] += input_tokens
        self.usage["total_output"] += output_tokens
        self.usage["requests"] += 1

    def get_stats(self) -> dict:
        """Return token usage statistics."""

        total_tokens = (
            self.usage["total_input"] +
            self.usage["total_output"]
        )

        requests = self.usage["requests"]

        return {
            "total_requests": requests,
            "total_input_tokens": self.usage["total_input"],
            "total_output_tokens": self.usage["total_output"],
            "total_tokens": total_tokens,
            "average_tokens_per_request": (
                round(total_tokens / requests, 2)
                if requests > 0 else 0
            ),
            "max_tokens_per_request": self.max_per_request
        }


# =====================================================
# 2. BUDGETED LLM
# =====================================================

class BudgetedLLM:

    def __init__(self, llm, max_tokens: int = 4000):
        self.llm = llm
        self.budget = TokenBudget(max_tokens)

    def invoke(self, query: str) -> str:
        """Check the budget, invoke the LLM, and record usage."""

        # Step 1: Check input token budget
        within_budget, input_tokens = self.budget.check_budget(query)

        if not within_budget:
            raise ValueError(
                f"Query exceeds token budget: "
                f"{input_tokens} > {self.budget.max_per_request}"
            )

        # Step 2: Send the query to the LLM
        response = self.llm.invoke(query)

        # Step 3: Extract the response text
        result = (
            response.content
            if hasattr(response, "content")
            else str(response)
        )

        # Step 4: Estimate output tokens
        output_tokens = self.budget.estimate_tokens(result)

        # Step 5: Record usage
        self.budget.record_usage(
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )

        return result

    def get_stats(self) -> dict:
        """Return token usage statistics."""
        return self.budget.get_stats()


# =====================================================
# 3. DEMO
# =====================================================

def demo_token_budgeting():
    """Demonstrate token budgeting."""

    # Initialize your LLM
    llm = OllamaCloudClient(
        model="gemma4:31b",
        embedding_model="embeddinggemma-2:latest",
        temperature=0
    )

    # Wrap the LLM with token budgeting
    budgeted_llm = BudgetedLLM(
        llm=llm,
        max_tokens=100
    )

    queries = [
        "What is AI?",
        "Explain " + "very " * 100 + "complex topic"
    ]

    print("\n========== TOKEN BUDGETING DEMO ==========\n")

    for query in queries:

        try:
            print("Query:", query[:100])

            result = budgeted_llm.invoke(query)

            print("\nLLM Response:")
            print(result)

        except ValueError as error:
            print("\nBudget Error:", error)

        print("\n" + "-" * 60)

    # Display statistics
    print("\nTOKEN USAGE STATISTICS:")
    print(budgeted_llm.get_stats())


if __name__ == "__main__":
    demo_token_budgeting()
