#!/bin/bash
set -e

echo "Creating DLQ..."

awslocal sqs create-queue \
  --queue-name process-weather-dlq-local

DLQ_URL=$(awslocal sqs get-queue-url \
  --queue-name process-weather-dlq-local \
  --query 'QueueUrl' --output text)

DLQ_ARN=$(awslocal sqs get-queue-attributes \
  --queue-url $DLQ_URL \
  --attribute-name QueueArn \
  --query 'Attributes.QueueArn' --output text)

echo "Creating main queue with redrive policy..."

awslocal sqs create-queue \
  --queue-name process-weather-sqs-local \
  --attributes "{\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"$DLQ_ARN\\\",\\\"maxReceiveCount\\\":\\\"5\\\"}\"}"

echo "Queues created!"