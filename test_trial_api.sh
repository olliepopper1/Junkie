#!/bin/bash

# Trial Junkie API Test Script
echo "Testing Trial Junkie API..."

# Base URL
BASE_URL="http://0.0.0.0:5000"

# Register a test user
echo "Registering test user..."
TIMESTAMP=$(date +%s)
USERNAME="testuser_$TIMESTAMP"
EMAIL="test$TIMESTAMP@example.com"
PASSWORD="Test1234!"

REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"confirm_password\":\"$PASSWORD\"}" \
  -c cookies.txt)

echo "Register response: $REGISTER_RESPONSE"

# Login with the test user
echo "Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  -b cookies.txt -c cookies.txt)

echo "Login response: $LOGIN_RESPONSE"

# Check subscription status
echo "Checking subscription status..."
SUB_STATUS=$(curl -s -X GET "$BASE_URL/api/subscription/status" \
  -b cookies.txt)

echo "Subscription status: $SUB_STATUS"

# Create a payment request
echo "Creating payment request..."
PAYMENT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/create-payment" \
  -H "Content-Type: application/json" \
  -d "{\"service_type\":\"subscription\",\"tier\":\"premium\",\"payment_method\":\"test\"}" \
  -b cookies.txt)

echo "Payment response: $PAYMENT_RESPONSE"

# Extract the payment reference
REFERENCE=$(echo $PAYMENT_RESPONSE | grep -o '"reference":"[^"]*"' | cut -d'"' -f4)
echo "Payment reference: $REFERENCE"

if [ -n "$REFERENCE" ]; then
  # Verify the payment (simulating completed payment)
  echo "Verifying payment..."
  VERIFY_RESPONSE=$(curl -s -X POST "$BASE_URL/api/verify-payment" \
    -H "Content-Type: application/json" \
    -d "{\"reference\":\"$REFERENCE\",\"status\":\"completed\",\"signature\":\"test_signature\"}" \
    -b cookies.txt)

  echo "Verify response: $VERIFY_RESPONSE"
  
  # Check subscription status again
  echo "Checking subscription status after payment..."
  SUB_STATUS=$(curl -s -X GET "$BASE_URL/api/subscription/status" \
    -b cookies.txt)

  echo "Subscription status: $SUB_STATUS"
  
  # Generate Hulu trial
  echo "Generating Hulu trial..."
  TRIAL_RESPONSE=$(curl -s -X POST "$BASE_URL/api/generate-trial" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"hulu\",\"type\":\"hit\",\"automate\":true}" \
    -b cookies.txt)

  echo "Trial generation response: $TRIAL_RESPONSE"
  
  # Get user trials
  echo "Getting user trials..."
  TRIALS=$(curl -s -X GET "$BASE_URL/api/trials" \
    -b cookies.txt)

  echo "User trials: $TRIALS"
else
  echo "Payment reference was not available. Cannot proceed with payment verification and trial generation."
fi

# Clean up
rm -f cookies.txt

echo "API testing completed."