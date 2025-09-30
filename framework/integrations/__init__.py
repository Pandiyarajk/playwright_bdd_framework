"""Integration modules."""

from framework.integrations.jira_integration import JiraIntegration
from framework.integrations.zephyr_integration import ZephyrIntegration
from framework.integrations.teams_webhook import TeamsWebhook, create_teams_webhook

__all__ = ["JiraIntegration", "ZephyrIntegration", "TeamsWebhook", "create_teams_webhook"]