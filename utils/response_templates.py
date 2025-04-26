"""
Response Templates
Drug-themed responses for the bot
"""
import random
from config import AGENT_NAMES

def harry_quote(topic):
    """Generate a random Heroin Harry quote about a topic"""
    quotes = [
        f"I can cook up a fresh identity for your {topic} faster than you can tie off.",
        f"Need a new identity for {topic}? I got the pure stuff, straight from the source.",
        f"These identities are so clean, even your {topic} won't know they're fake.",
        f"One shot of my identity juice and your {topic} will never be the same.",
        f"When it comes to {topic}, a new identity is better than a new needle.",
        f"My identities are like a perfect fix - use them for {topic} and you'll never look back.",
        f"I've been pushing identities for {topic} since before you were born, kid."
    ]
    return random.choice(quotes)

def mandy_quote(topic):
    """Generate a random Meth Mandy quote about a topic"""
    quotes = [
        f"I stay up for DAYS making these cards for {topic}. They're PERFECT. PERFECT!",
        f"These cards work EVERYWHERE! Even for {topic}!!! I checked 37 TIMES!!!",
        f"Your {topic} needs a payment method? I MADE 200 CARDS LAST NIGHT!",
        f"Credit cards for {topic}? I NEVER SLEEP! I MAKE CARDS! SO MANY CARDS!",
        f"My cards are so clean for {topic}, I scrubbed them with my TOOTHBRUSH for EIGHT HOURS!",
        f"LISTEN! LISTEN! These cards will DEFINITELY work for {topic}! I GUARANTEE IT!!",
        f"I've tested these cards on {topic} FIFTY-SEVEN TIMES! They WORK! THEY WORK!"
    ]
    return random.choice(quotes)

def xan_quote(topic):
    """Generate a random Xanny Xan quote about a topic"""
    quotes = [
        f"Mmmm... {topic}? Yeah... I can make an email for that... no stress...",
        f"Email for {topic}? *yawns* Yeah... whatever... I got you...",
        f"Don't worry about {topic}... my emails are... umm... what was I saying?",
        f"These emails work for {topic}... I think... whatever... they're good...",
        f"*slowly* Your {topic} needs verification? My emails... they're... chill...",
        f"*half asleep* The inbox for {topic}... it's... ready... whenever...",
        f"*drowsy* My emails are so relaxed... just like... {topic}... you know?"
    ]
    return random.choice(quotes)

def carl_quote(topic):
    """Generate a random Cokehead Carl quote about a topic"""
    quotes = [
        f"PHONE NUMBERS! TONS OF PHONE NUMBERS FOR {topic.upper()}! RIGHT NOW!",
        f"You need verification for {topic}? I'VE GOT NUMBERS! SO MANY NUMBERS!",
        f"These phone numbers for {topic} are PREMIUM QUALITY! TOP SHELF!",
        f"I JUST GENERATED 50 PHONE NUMBERS FOR {topic.upper()}! WANT MORE?!",
        f"MY PHONE NUMBERS ARE THE FASTEST FOR {topic.upper()}! NO WAITING!",
        f"VERIFICATION CODES FOR {topic.upper()}? MY NUMBERS DELIVER INSTANTLY!",
        f"I'M THE PHONE NUMBER KING FOR {topic.upper()}! NOBODY COMPARES!"
    ]
    return random.choice(quotes)

def sal_quote(topic):
    """Generate a random Shroomy Sal quote about a topic"""
    quotes = [
        f"Woah... the automation for {topic} is like... *giggle* connected to everything, man.",
        f"I see the patterns in {topic}... the scripts are all... interconnected, you know?",
        f"When you automate {topic}, you're really tapping into the universal flow.",
        f"The browser automation... it's alive, man. It feels {topic} on a deeper level.",
        f"*stares at screen* I wrote this {topic} script during an ego death experience.",
        f"Have you ever really thought about {topic}? Like, REALLY thought about it?",
        f"These {topic} automations will expand your consciousness, dude."
    ]
    return random.choice(quotes)

def pusher_quote(topic):
    """Generate a random Pusher quote about a topic"""
    quotes = [
        f"My network has everything you need for {topic}. First one's free.",
        f"I supply only the highest quality resources for {topic}. My reputation depends on it.",
        f"You want {topic} credentials? I've got people for that. Specialized people.",
        f"My agents can hook you up with anything you need for {topic}. For a price.",
        f"When it comes to {topic}, I'm the one who connects the dots.",
        f"Need something for {topic}? I know people who know people.",
        f"I don't create anything, I just move the product. And my {topic} product is the best."
    ]
    return random.choice(quotes)

def get_agent_quote(agent, topic):
    """Get a quote from a specific agent about a topic"""
    agent_functions = {
        "harry": harry_quote,
        "mandy": mandy_quote,
        "xan": xan_quote,
        "carl": carl_quote,
        "sal": sal_quote,
        "pusher": pusher_quote
    }
    
    # Return a quote if the agent exists, otherwise a generic quote
    if agent in agent_functions:
        return agent_functions[agent](topic)
    else:
        return f"I know all about {topic}. Trust me."

def random_drug_emoji():
    """Return a random drug-themed emoji"""
    emojis = ["💉", "💊", "🍄", "⚗️", "🧪", "🔬", "🧫", "💨", "🚬", "🧠", "🤪", "😵‍💫"]
    return random.choice(emojis)