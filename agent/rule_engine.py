import re


def extract_auth_methods(text):

    methods = []

    text = text.lower()

    if "oauth" in text:
        methods.append("OAuth2")

    if "api key" in text:
        methods.append("API Key")

    if "bearer" in text:
        methods.append("Bearer Token")

    if "basic auth" in text:
        methods.append("Basic Auth")

    if "jwt" in text:
        methods.append("JWT")

    return list(set(methods))


def extract_api_surface(text):

    text = text.lower()

    api = []

    if "rest api" in text or "web api" in text or "rest" in text:
        api.append("REST")

    if "graphql" in text:
        api.append("GraphQL")

    if "webhook" in text:
        api.append("Webhooks")

    if "sdk" in text:
        api.append("SDK")

    return list(set(api))


def extract_self_serve(text):

    text = text.lower()

    if "contact sales" in text:
        return "Contact Sales"

    if "partner" in text:
        return "Partner Gated"

    if "free trial" in text:
        return "Self Serve (Trial)"

    if (
        "sign up" in text
        or "create an app" in text
        or "developer portal" in text
        or "developer docs" in text
    ):
        return "Self Serve"

    return "Unknown"


def extract_buildability(text):

    text = text.lower()

    if (
        "api"
        in text
        or "oauth"
        in text
        or "sdk"
        in text
        or "webhook"
        in text
    ):
        return "Yes"

    return "No"


def extract_mcp(text):

    text = text.lower()

    if "mcp" in text:
        return "Yes"

    return "No"