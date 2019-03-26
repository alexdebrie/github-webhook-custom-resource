import logging
import os

from crhelper import CfnResource
import requests

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL')

WEBHOOK_URL = "https://api.github.com/repos/{repo}/hooks"
WEBHOOK_URL_ID = "https://api.github.com/repos/{repo}/hooks/{webhook_id}"

HEADERS = {
    "Authorization": "token {token}".format(token=os.environ.get('GITHUB_TOKEN'))
}


@helper.create
def create(event, context):
    logger.info("Got Create")
    properties = event.get('ResourceProperties', {})

    repo = properties.get('Repo')
    if not repo:
        raise Exception('Must provide a "Repo" value in properties.')

    url = WEBHOOK_URL.format(repo=repo)
    payload = _make_payload(properties)

    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()

    data = resp.json()
    webhook_id = data['id']

    physical_id = _encode_physical_id(webhook_id, repo)

    helper.Data.update({"webhookId": webhook_id})
    return physical_id


@helper.update
def update(event, context):
    logger.info("Got Update")
    properties = event.get('ResourceProperties', {})

    repo = properties.get('Repo')
    if not repo:
        raise Exception('Must provide a "Repo" value in properties.')

    physical_id = event['PhysicalResourceId']
    webhook_id, old_repo = _decode_physical_id(physical_id)
    payload = _make_payload(properties)

    # If the repo has changed, we need to delete the old webhook and create a new one, 
    # plus update the PhysicalResourceId
    if repo != old_repo:
        delete_url = WEBHOOK_URL_ID.format(repo=repo, webhook_id=webhook_id)
        resp = requests.delete(delete_url, headers=HEADERS)
        resp.raise_for_status()

        create_url = WEBHOOK_URL.format(repo=repo)
        resp = requests.post(url, json=payload, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        webhook_id = data['id']

        physical_id = _encode_physical_id(webhook_id, repo)
    else:
        update_url = WEBHOOK_URL_ID.format(repo=repo, webhook_id=webhook_id)
        resp = requests.patch(update_url, json=payload, headers=HEADERS)
        resp.raise_for_status()

    return physical_id


@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    physical_id = event['PhysicalResourceId']
    webhook_id, old_repo = _decode_physical_id(physical_id)

    delete_url = WEBHOOK_URL_ID.format(repo=repo, webhook_id=webhook_id)
    resp = requests.delete(delete_url, headers=HEADERS)
    resp.raise_for_status()


def _make_payload(properties):
    events = properties.get('Events')
    if not events:
        raise Exception('Must provide an "Events" value in properties.')
    if isinstance(events, str):
        events = [events]

    endpoint = properties.get('Endpoint')
    if not endpoint:
        raise Exception('Must provide an "Endpoint" value in properties.')

    content_type = properties.get('ContentType', 'json')

    return {
        "active": True,
        "events": events,
        "config": {
            "url": endpoint,
            "content_type": content_type
        }
    }


def _encode_physical_id(webhook_id, repo):
    return "GitHubWebhookZZ{webhook_id}ZZ{repo}".format(webhook_id=webhook_id, repo=repo)


def _decode_physical_id(physical_id):
    elements = physical_id.split('ZZ', 2)
    return {
      "id": elements[1],
      "repo": elements[2]
    }


def handler(event, context):
    helper(event, context)
