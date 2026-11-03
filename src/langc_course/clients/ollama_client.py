
import os
import requests
import ollama

from typing import Optional, Any,ClassVar

from pydantic import Field, PrivateAttr
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult


class OllamaCloudClient(BaseChatModel):

    model: str
    embedding_model: str
    temperature: float = 0

    api_key: Optional[str] = Field(default=None, exclude=True)

    _headers: dict = PrivateAttr()
    _embedding_client: Any = PrivateAttr()

    BASE_URL : ClassVar[str] =  "https://ollama.com/v1"

    def __init__(
        self,
        model: str,
        embedding_model: str,
        api_key: Optional[str] = None,
        temperature: float = 0,
        **kwargs
    ):

        super().__init__(
            model=model,
            embedding_model=embedding_model,
            temperature=temperature,
            api_key=api_key or os.getenv("OLLAMA_API_KEY"),
            **kwargs
        )

        if not self.api_key:
            raise ValueError("OLLAMA_API_KEY is missing")

        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        self._embedding_client = ollama.Client(
            host="http://localhost:11434"
        )

    # --------------------------------
    # LANGCHAIN CHAT MODEL
    # --------------------------------
# @property makes the method behave like a read-only attribute.
    @property
    def _llm_type(self) -> str:
        return "ollama-cloud"

    @property
    def _identifying_params(self) -> dict:
        return {
            "model": self.model,
            "temperature": self.temperature
        }

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager=None,
        **kwargs
    ) -> ChatResult:

        formatted_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = "user"

            elif isinstance(message, SystemMessage):
                role = "system"

            elif isinstance(message, AIMessage):
                role = "assistant"

            else:
                raise ValueError(
                    f"Unsupported message type: {type(message)}"
                )

            formatted_messages.append({
                "role": role,
                "content": message.content
            })

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "stream": False
        }

        if stop:
            payload["stop"] = stop

        response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=self._headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]

        generation = ChatGeneration(
            message=AIMessage(content=content)
        )

        return ChatResult(generations=[generation])

    # --------------------------------
    # LOCAL EMBEDDINGS
    # --------------------------------

    def embed(self, texts: list[str]) -> list[list[float]]:

        if not texts:
            return []

        response = self._embedding_client.embed(
            model=self.embedding_model,
            input=texts
        )

        return response.embeddings
