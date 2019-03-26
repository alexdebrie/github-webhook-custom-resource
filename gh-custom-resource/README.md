## Github Webhook Custom Resource

This directory includes code for deploying a [CloudFormation custom resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) that provisions a [GitHub webhook](https://developer.github.com/webhooks/).

It is a companion to a blog post on [using CloudFormation custom resources](https://alexdebrie.com/posts/cloudformation-custom-resources/).

## Usage

### Deploying the custom resource

First, you will need to deploy the custom resource into your AWS account.

To do that, follow these steps:

1. Clone this repository and change into this directory.

2. Install the required packages and the [Serverless Framework](https://github.com/serverless/serverless):

	```bash
	npm install
	npm install -g serverless
	```

3. [Provision a Github access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) and add it to the `serverless.yml`

4. Deploy the service:

	```bash
	serverless deploy
	```

After you have done this, your custom resource will be deployed, and it will export the ARN of the function with the name `GithubWebhookFunction`.

### Using the custom resource

To use the custom resource, you'll need to use the exported ARN as the `ServiceToken` in a custom resource in a CloudFormation template:

```yml
GithubWebhook:
  Type: 'Custom::GithubWebhook'
  Version: '1.0'
  Properties:
    ServiceToken: !ImportValue GithubWebhookFunction
    Repo: <Github repo to subscribe to>
    Events: <comma separated list of events>
    Endpoint: <endpoint to send the webhooks>
```

In addition to the `ServiceToken` property, you will need to provide `Repo`, `Events`, and `Endpoint` properties.

For an example template, see the [`template.yaml` in the root of this repository](../template.yaml).