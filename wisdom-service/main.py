import random
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings


mcp = FastMCP(
    name="wisdom-server",
    instructions="Use this tool when the user asks for daily wisdom, inspirational quote, funny advice, or motivational sentence.",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
)


WISDOMS = [
    "If coffee solved everything, Mondays wouldn't exist.",
    "Life is short. Smile while you still have teeth.",
    "Error 404: Motivation not found.",
    "Those who wake up early… stay sleepy all day.",
    "Work hard today so you can complain with authority tomorrow.",
    "If it didn't work out, at least it made a good story.",
    "Never leave for tomorrow what you can cancel today.",
    "I'm not lazy. I'm in energy-saving mode.",
    "Common sense is like deodorant. The people who need it most never use it.",
    "Dream big. Sleep bigger.",
    "My patience has a timeout limit.",
    "If at first you don't succeed, redefine success.",
    "Some people graduate with honors. I am just honored to graduate.",
    "Silence is golden. Unless you have kids. Then it's suspicious.",
    "I followed my heart. It led me to the fridge.",
    "If stress burned calories, I'd be a supermodel.",
    "I don't rise and shine. I caffeinate and hope.",
    "Why do today what you can panic about tomorrow?",
    "I love deadlines. I especially love the whooshing sound they make as they fly by.",
    "My brain has too many tabs open.",
    "Running late is my cardio.",
    "I don't need a motivational quote. I need a nap.",
    "Success is 1% inspiration and 99% trying to find the right password.",
    "I have a degree in overthinking.",
    "If life gives you lemons, check if they’re organic.",
    "Some days I amaze myself. Other days I put my phone in the fridge.",
]


@mcp.tool()
def wisdom_of_the_day() -> dict:
    """
    Use this tool when the user asks for daily wisdom, inspirational quote, funny advice, or motivational sentence.
    """
    result = random.choice(WISDOMS)
    print(f"Selected wisdom: {result}")

    return {"wisdom": result}


app = mcp.streamable_http_app()
