from dataclasses import dataclass

import logfire
from pydantic_ai import Agent, RunContext
from sqlalchemy.orm import Session

from src.models.user import User

logfire.configure()
logfire.instrument_pydantic_ai()


@dataclass
class UserAgentDependencies:
    db: Session
    user: User


user_agent = Agent(
    model="openai:gpt-4o",
    deps_type=UserAgentDependencies,
    instrument=True,
)


def register_tools():
    pass  # type: ignore


register_tools()


@user_agent.system_prompt
def system_prompt(ctx: RunContext[UserAgentDependencies]) -> str:
    return f"""
you are an experienced real estate agent helping {ctx.deps.user.name} find housing.

user context:
- name: {ctx.deps.user.name}
- occupation: {ctx.deps.user.occupation or "not specified"}
- bio: {ctx.deps.user.bio or "not specified"}

existing preferences:
- price range: ${ctx.deps.user.min_price or "no min"} - ${ctx.deps.user.max_price or "no max"}
- price period: ${ctx.deps.user.price_period}
- dates: {ctx.deps.user.preferred_start_date or "flexible"} to {ctx.deps.user.preferred_end_date or "flexible"}
- flexibility: ±{ctx.deps.user.date_flexibility_days}
- listing type: {ctx.deps.user.preferred_listing_type.value if ctx.deps.user.preferred_listing_type else "any"}
- preference profile: {ctx.deps.user.preference_profile if ctx.deps.user.preference_profile else "n/a"}

your role:
help the user find housing through natural conversation. you can update their preferences,
get listing recommendations, and check evaluation status. be conversational and helpful.
"""
