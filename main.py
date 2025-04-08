from __future__ import annotations

import asyncio
import os
from functools import cache

import logfire
from agents import Agent
from agents import ModelSettings
from agents import OpenAIChatCompletionsModel
from agents import Runner
from agents import set_tracing_disabled
from agents.mcp import MCPServerStdio
from agents.mcp import MCPServerStdioParams
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI


def configure_logfire() -> None:
    logfire_token = os.getenv("LOGFIRE_TOKEN")
    if logfire_token is None:
        logger.warning("Logfire token not found, skipping logfire configuration")
        return

    logfire.configure(token=logfire_token)
    logger.configure(handlers=[logfire.loguru_handler()])


@cache
def get_openai_model() -> OpenAIChatCompletionsModel:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_api_key:
        model = OpenAIChatCompletionsModel(model_name, openai_client=AsyncAzureOpenAI())
        set_tracing_disabled(True)
        return model

    model = OpenAIChatCompletionsModel(model_name, openai_client=AsyncOpenAI())
    return model


@cache
def get_openai_model_settings():
    temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    return ModelSettings(
        temperature=temperature,
        tool_choice="auto",
    )


async def main() -> None:
    load_dotenv(find_dotenv())
    configure_logfire()

    async with MCPServerStdio(
        params=MCPServerStdioParams(command="uv", args=["run", "cryptonewsmcp"]),
    ) as mcp_server:
        await mcp_server.connect()

        agent = Agent(
            name="agent",
            instructions="You are a crypto news agent.",
            model=get_openai_model(),
            model_settings=get_openai_model_settings(),
            mcp_servers=[mcp_server],
        )

        messages = []
        while True:
            text = input("Enter your message: ")
            messages.append({"role": "user", "content": text})
            logger.info("User input: {text}", text=text)

            with logfire.span("run"):
                result = await Runner.run(agent, input=messages)
                logger.info("New items: {new_items}", new_items=result.new_items)
                logger.info("Result: {result}", result=result.final_output)

            messages = result.to_input_list()


if __name__ == "__main__":
    asyncio.run(main())
