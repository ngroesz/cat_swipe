from flask import request
from user_agents import parse


def ua_is_browser():
    user_agent_string = request.headers.get('User-Agent')
    if user_agent_string and isinstance(user_agent_string, str):
        user_agent = parse(request.headers.get('User-Agent'))
        return user_agent.is_mobile or user_agent.is_tablet or user_agent.is_pc
    return False


def format_json(json):
    formatted_json = json.replace("\n", '').replace("\r", '')

    return formatted_json
