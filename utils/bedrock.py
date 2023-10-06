# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""Helper utilities for working with Amazon Bedrock from Python notebooks"""
# Python Built-Ins:
from typing import Optional
import configparser
import os
from langchain.llms.bedrock import Bedrock

config = configparser.ConfigParser()
config.read(os.path.expanduser("~\.aws\credentials"))
# External Dependencies:
import boto3
from botocore.config import Config

def get_bedrock_client(
    assumed_role: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    region: Optional[str] = None,
    inference_modifier: dict = None
):
    print("Initializing bedrock client")
    """Create a boto3 client for Amazon Bedrock, with optional configuration overrides

    Parameters
    ----------
    assumed_role :
        Optional ARN of an AWS IAM role to assume for calling the Bedrock service. If not
        specified, the current active credentials will be used.
    endpoint_url :
        Optional override for the Bedrock service API Endpoint. If setting this, it should usually
        include the protocol i.e. "https://..."
    region :
        Optional name of the AWS Region in which the service should be called (e.g. "us-east-1").
        If not specified, AWS_REGION or AWS_DEFAULT_REGION environment variable will be used.
    """

    if region is None:
        target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
    else:
        target_region = region

    print(f"Create new client\n  Using region: {target_region}")
    session_kwargs = {"region_name": target_region}
    client_kwargs = {**session_kwargs}

    profile_name = os.environ.get("AWS_PROFILE")
    if profile_name:
        print(f"  Using profile: {profile_name}")
        session_kwargs["profile_name"] = profile_name

    retry_config = Config(
        region_name=target_region,
        retries={
            "max_attempts": 10,
            "mode": "standard",
        },
    )

    try:
        session = boto3.Session(**session_kwargs)
    except Exception as e:
        raise ValueError(f"Failed to create a valid boto3 Session: {str(e)}")

    aws_access_key_id = config.get("default", "aws_access_key_id")
    aws_secret_access_key = config.get("default", "aws_secret_access_key")

    client_kwargs["aws_access_key_id"] = aws_access_key_id
    client_kwargs["aws_secret_access_key"] = aws_secret_access_key

    bedrock_client = session.client(
        service_name="bedrock",
        config=retry_config,
        **client_kwargs
    )

    print("boto3 Bedrock client successfully created!")
    print(bedrock_client._endpoint)
    # Instantiate the Bedrock class
    llm_bedrock_client = Bedrock(model_id = "anthropic.claude-v2",
                                 client = bedrock_client,
                    model_kwargs = inference_modifier
                    )
    return llm_bedrock_client
        
         