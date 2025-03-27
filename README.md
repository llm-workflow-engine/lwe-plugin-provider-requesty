# LLM Workflow Engine (LWE) Requesty Provider plugin

Requesty Provider plugin for [LLM Workflow Engine](https://github.com/llm-workflow-engine/llm-workflow-engine)

Access to [Requesty](https://www.requesty.ai/solution/llm-routing/models) models.

## Installation

### From packages

Install the latest version of this software directly from github with pip:

```bash
pip install git+https://github.com/llm-workflow-engine/lwe-plugin-provider-requesty
```

### From source (recommended for development)

Install the latest version of this software directly from git:

```bash
git clone https://github.com/llm-workflow-engine/lwe-plugin-provider-requesty.git
```

Install the development package:

```bash
cd lwe-plugin-provider-requesty
pip install -e .
```

## Configuration

Get an [API key](https://app.requesty.ai/router) from Requesty.

Export the key to the `REQUESTY_API_KEY` environment variable.

Add the following to `config.yaml` in your profile:

```yaml
plugins:
  enabled:
    - provider_requesty
    # Any other plugins you want enabled...
  # THIS IS OPTIONAL -- By default the plugin loads all model data via an API
  # call on startup. This does make startup time longer, and the CLI completion
  # for selecting models is very long!
  # You can instead provide a 'models' object here with the relevant data, and
  # It will be used instead of an API call.
  provider_requesty:
    models:
      # 'id' parameter of the model as it appears in the API.
      # This is also listed on the model summary page on the Requesty
      # website.
      "openai/gpt-4o":
        # The only parameter, and it's required.
        max_tokens: 128000
```

## Usage

From a running LWE shell:

```
/provider requesty
/model model_name openai/gpt-4o-mini
```
