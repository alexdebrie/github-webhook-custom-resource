## Github Webhook Custom Resource

This directory includes code for deploying a [CloudFormation custom resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) that provisions a [GitHub webhook](https://developer.github.com/webhooks/).

It is a companion to a blog post on [using CloudFormation custom resources](https://alexdebrie.com/posts/cloudformation-custom-resources/).

## Usage

### Deploying the custom resource

Check the [README](./gh-custom-resource/README.md) in the `gh-custom-resource` directory for instructions on deploying the custom resource.

### Using the custom resource

After you've deployed the custom resource, you can use the `template.yaml` in this directory to deploy a sample application.

Example usage:

```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name github-webhook-test \
  --parameter-overrides REPO=alexdebrie/alexdebrie.com ENDPOINT=http://requestbin.fullcontact.com/z0azobz0
```

Be sure to override the `REPO` and `ENDPOINT` values with your own values.