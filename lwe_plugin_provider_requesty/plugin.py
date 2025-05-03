import os
from typing import Optional
import requests

from langchain_openai import ChatOpenAI
from pydantic import Field

from lwe.core.provider import Provider, PresetValue

REQUESTY_API_BASE = "https://router.requesty.ai/v1"
REQUESTY_DEFAULT_MODEL = "openai/gpt-4o-mini"


class ChatRequesty(ChatOpenAI):

    model_name: str = Field(default=REQUESTY_DEFAULT_MODEL, alias="model")
    """Model name to use."""
    openai_api_base: Optional[str] = Field(default=REQUESTY_API_BASE, alias="base_url")
    """Base URL path for API requests, leave blank if not using a proxy or service
        emulator."""

    @property
    def _llm_type(self):
        """Return type of llm."""
        return "requesty"

    def __init__(self, **kwargs):
        if 'openai_api_key' in kwargs:
            openai_api_key = kwargs.pop('openai_api_key')
        else:
            openai_api_key = os.getenv('REQUESTY_API_KEY')
        if not openai_api_key:
            raise ValueError("REQUESTY_API_KEY is not set")
        # Ugly hack: If OpenAI organization is set, temporarily remove it from the environment.
        openai_org_id = os.environ.pop('OPENAI_ORG_ID', None)
        openai_organization = os.environ.pop('OPENAI_ORGANIZATION', None)
        super().__init__(openai_api_key=openai_api_key, **kwargs)
        if openai_org_id:
            os.environ['OPENAI_ORG_ID'] = openai_org_id
        if openai_organization:
            os.environ['OPENAI_ORGANIZATION'] = openai_organization


class ProviderRequesty(Provider):
    """
    Access to Requesty chat models via the OpenAI API
    """

    def fetch_models(self):
        models_url = f"{REQUESTY_API_BASE}/models"
        try:
            response = requests.get(models_url)
            response.raise_for_status()
            models_data = response.json()
            models_list = models_data.get('data')
            if not models_list:
                raise ValueError('Could not retrieve models')
            models = {model['id']: {'max_tokens': model['context_window']} for model in models_list}
            return models
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not retrieve models: {e}")

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': False,
        }

    @property
    def default_model(self):
        return REQUESTY_DEFAULT_MODEL

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return ChatRequesty

    def customization_config(self):
        return {
            "verbose": PresetValue(bool),
            "model_name": PresetValue(str, options=self.available_models),
            "temperature": PresetValue(float, min_value=0.0, max_value=2.0),
            "openai_api_base": PresetValue(str, include_none=True),
            "openai_api_key": PresetValue(str, include_none=True, private=True),
            "request_timeout": PresetValue(int),
            "max_retries": PresetValue(int, 1, 10),
            "max_tokens": PresetValue(int, include_none=True),
            "model_kwargs": {
                "top_p": PresetValue(float, min_value=0.0, max_value=1.0, include_none=True),
                "top_k": PresetValue(int, min_value=0, max_value=20, include_none=True),
                "min_p": PresetValue(float, min_value=0.0, max_value=1.0, include_none=True),
                "top_a": PresetValue(float, min_value=0.0, max_value=1.0, include_none=True),
                "frequency_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
                "presence_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
                "repitition_penalty": PresetValue(float, min_value=0, max_value=2.0),
                "logit_bias": dict,
                "logprobs": PresetValue(bool, include_none=True),
                "top_logprobs": PresetValue(int, min_value=0, max_value=20),
                "response_format": dict,
                "seed": PresetValue(int),
                "stop": PresetValue(str, include_none=True),
                "functions": None,
                "function_call": None,
            },
        }
