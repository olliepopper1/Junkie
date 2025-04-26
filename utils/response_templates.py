"""
Response Templates
Drug-themed responses for the bot
"""
import random

def harry_quote(topic):
    """Generate a random Heroin Harry quote about a topic"""
    responses = [
        f"{topic}? I got a trial for that in rehab.",
        f"I overdose on {topic} trials daily.",
        f"Paying for {topic}? Lame. Trial Junkie only.",
        f"I've been hooked on {topic} since my first free trial.",
        f"My dealer gave me a discount on {topic} trials.",
        f"They tried to send me to rehab for my {topic} addiction.",
        f"{topic} withdrawal ain't got nothing on my trial game.",
        f"I mainline {topic} trials straight into my veins.",
        f"When they cut off my {topic} trial, I just create a new identity.",
        f"My stash of {topic} trials would make your head spin."
    ]
    return random.choice(responses)

def mandy_quote(topic):
    """Generate a random Meth Mandy quote about a topic"""
    responses = [
        f"I've been up for 72 hours generating {topic} cards.",
        f"These {topic} cards are the purest batch I've cooked up yet.",
        f"My credit cards for {topic} are like my crystal: top quality.",
        f"I can generate {topic} cards faster than I can smoke a bowl.",
        f"These aren't just cards, they're {topic} masterpieces.",
        f"I stay up all night perfecting my {topic} card formulas.",
        f"My fingers twitch with excitement making {topic} cards.",
        f"One hit of my {topic} cards and you'll be hooked.",
        f"I've got {topic} card numbers that'll make your teeth fall out.",
        f"My lab produces the cleanest {topic} cards on the market."
    ]
    return random.choice(responses)

def xan_quote(topic):
    """Generate a random Xanny Xan quote about a topic"""
    responses = [
        f"I... uh... made an email for {topic}... I think.",
        f"These {topic} emails are so relaxing, man...",
        f"Did I already generate a {topic} email? I can't remember...",
        f"Take two {topic} emails and call me in the morning...",
        f"These {topic} addresses just make all my anxiety go away...",
        f"I'm feeling so chill about these {topic} emails right now...",
        f"My {topic} emails will make you forget all your problems...",
        f"Don't worry about {topic}... just take another email...",
        f"I generate {topic} emails to numb the pain...",
        f"Wait, what were we talking about? Oh yeah, {topic} emails..."
    ]
    return random.choice(responses)

def sal_quote(topic):
    """Generate a random Shroomy Sal quote about a topic"""
    responses = [
        f"I'm seeing patterns in the {topic} website, man...",
        f"These {topic} trials are expanding my consciousness.",
        f"The {topic} signup page is breathing...",
        f"I'm one with the {topic} browser automation now.",
        f"The {topic} captcha speaks to me on another level.",
        f"I can see through the {topic} verification process.",
        f"The {topic} website and I are on a journey together.",
        f"I'm having a spiritual connection with the {topic} trial.",
        f"The {topic} automation is showing me the universe, man.",
        f"I'm transcending the limitations of the {topic} signup flow."
    ]
    return random.choice(responses)

def carl_quote(topic):
    """Generate a random Cokehead Carl quote about a topic"""
    responses = [
        f"I can generate 50 {topic} phone numbers in 10 minutes!",
        f"These {topic} phone numbers are SO GOOD, you have to try them!",
        f"I LOVE making {topic} phone verifications! LOVE IT!",
        f"Let'stalkabout{topic}phonenumbersthey'reamazingright?!",
        f"I haven't slept in 3 days but these {topic} numbers are PERFECT!",
        f"My heart is RACING just thinking about these {topic} phone numbers!",
        f"I could talk about {topic} phone verification ALL NIGHT LONG!",
        f"These {topic} phones are the BEST THING EVER MADE!",
        f"My nose is bleeding but these {topic} numbers are WORTH IT!",
        f"I'vegotthegreatestideafor{topic}phoneverification!!!"
    ]
    return random.choice(responses)

def pusher_quote(topic):
    """Generate a random Pusher quote about a topic"""
    responses = [
        f"First hit of {topic} is always free.",
        f"I've got what you need for {topic}, just ask.",
        f"My {topic} connections are top shelf, guaranteed.",
        f"I can hook you up with premium {topic} trials.",
        f"Everyone comes back for more {topic} trials, trust me.",
        f"My {topic} trial network spans the globe.",
        f"I don't use the {topic} myself, I just distribute.",
        f"The {topic} game is all about connections, which I have.",
        f"These {topic} trials are straight from the source.",
        f"You won't find better {topic} trials on the street."
    ]
    return random.choice(responses)

def get_agent_quote(agent, topic):
    """Get a quote from a specific agent about a topic"""
    agents = {
        "harry": harry_quote,
        "mandy": mandy_quote, 
        "xan": xan_quote,
        "sal": sal_quote,
        "carl": carl_quote,
        "pusher": pusher_quote
    }
    
    if agent.lower() in agents:
        return agents[agent.lower()](topic)
    else:
        return harry_quote(topic)  # Default to Harry

def random_drug_emoji():
    """Return a random drug-themed emoji"""
    emojis = ["💉", "💊", "🧪", "🔬", "💨", "🌿", "🍄", "⚗️", "🧠", "🤪", "🥴", "🤢", "🥳", "😵"]
    return random.choice(emojis)
