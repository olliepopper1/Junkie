"""
Tests for Trial Junkie agents
"""
import pytest
import asyncio
from unittest.mock import MagicMock, patch

# Import agents for testing
from agents.identity_agent import IdentityAgent
from agents.card_agent import CardAgent
from agents.email_agent import EmailAgent
from agents.phone_agent import PhoneAgent
from agents.automation_agent import AutomationAgent
from agents.pusher import Pusher

# Test identity agent
@pytest.mark.asyncio
async def test_identity_agent_generate():
    """Test identity generation"""
    db_mock = MagicMock()
    agent = IdentityAgent(db_mock)
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "name": {"first": "John", "last": "Doe"},
                    "dob": {"age": 30, "date": "1992-01-01"},
                    "gender": "male",
                    "location": {
                        "city": "New York",
                        "state": "NY",
                        "country": "USA",
                        "street": {"number": 123, "name": "Main St"},
                        "postcode": "10001"
                    },
                    "nat": "US",
                    "login": {"username": "johndoe92"}
                }
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        identity = await agent.generate_identity()
        
        assert identity["name"] == "John Doe"
        assert identity["age"] == 30
        assert identity["gender"] == "male"
        assert "New York" in identity["location"]
        assert identity["nationality"] == "US"
        assert identity["username"] == "johndoe92"

# Test card agent
@pytest.mark.asyncio
async def test_card_agent_generate():
    """Test card generation"""
    db_mock = MagicMock()
    agent = CardAgent(db_mock)
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "card_number": "4111111111111111",
            "expiration_date": "12/25",
            "cvv": "123",
            "card_type": "Visa",
            "name": "JOHN DOE"
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        card = await agent.generate_card()
        
        assert card["number"] == "4111111111111111"
        assert card["expiry"] == "12/25"
        assert card["cvv"] == "123"
        assert card["type"] == "Visa"
        assert card["name"] == "JOHN DOE"

# Test email agent
@pytest.mark.asyncio
async def test_email_agent_generate():
    """Test email generation"""
    db_mock = MagicMock()
    agent = EmailAgent(db_mock)
    
    # Test with identity
    identity = {
        "name": "John Doe",
        "age": 30,
        "username": "johndoe92"
    }
    
    email = await agent.generate_email(identity)
    
    assert "@" in email
    assert "." in email
    assert any(domain in email for domain in agent.domains)

# Test automation agent
@pytest.mark.asyncio
async def test_automation_agent_scripts():
    """Test automation scripts"""
    db_mock = MagicMock()
    agent = AutomationAgent(db_mock)
    
    # Create sample credentials
    credentials = [
        {
            "type": "identity",
            "service": "netflix",
            "value": {
                "name": "John Doe",
                "age": 30,
                "gender": "male"
            }
        },
        {
            "type": "email",
            "service": "netflix",
            "value": "johndoe@example.com"
        },
        {
            "type": "card",
            "service": "netflix",
            "value": {
                "number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123"
            }
        }
    ]
    
    # Test signup script
    result = await agent.run_script("signup", credentials)
    
    assert "status" in result
    assert "details" in result
    assert "steps" in result
    assert len(result["steps"]) > 0

# Test pusher agent
@pytest.mark.asyncio
async def test_pusher_process_hit():
    """Test pusher hit command processing"""
    db_mock = MagicMock()
    
    # Mock the database methods
    db_mock.create_user.return_value = True
    db_mock.save_credential.return_value = True
    db_mock.log_command.return_value = True
    
    # Create pusher with mocked agents
    pusher = Pusher(db_mock)
    
    # Mock the agent methods
    pusher.identity_agent.generate_identity = MagicMock(return_value=asyncio.Future())
    pusher.identity_agent.generate_identity.return_value.set_result({
        "name": "John Doe",
        "age": 30,
        "gender": "male",
        "location": "New York, NY, USA",
        "nationality": "US",
        "username": "johndoe92"
    })
    
    pusher.email_agent.generate_email = MagicMock(return_value=asyncio.Future())
    pusher.email_agent.generate_email.return_value.set_result("johndoe@example.com")
    
    pusher.card_agent.generate_card = MagicMock(return_value=asyncio.Future())
    pusher.card_agent.generate_card.return_value.set_result({
        "number": "4111111111111111",
        "expiry": "12/25",
        "cvv": "123",
        "type": "Visa"
    })
    
    pusher.phone_agent.generate_phone = MagicMock(return_value=asyncio.Future())
    pusher.phone_agent.generate_phone.return_value.set_result("+15551234567")
    
    # Process a hit command
    result = await pusher.process_hit("user123", "testuser", "netflix")
    
    # Check that the result is a discord.Embed
    assert isinstance(result, discord.Embed)
    assert "Trial Ready" in result.title
    assert "netflix" in result.title
