# Alternative Platform Integration

While Agent3D focuses on GitHub CLI workflows, teams using GitLab or Bitbucket can adapt the same principles with their respective command line tools.

## GitLab
1. Install the [GitLab CLI](https://gitlab.com/gitlab-org/cli) and authenticate with your account.
2. Use `glab` commands to check merge request status, view diffs, and leave comments.
3. Mirror the DDD pass workflow by triggering pipelines after each pass and ensuring documentation stays in sync with merge requests.

## Bitbucket
1. Use [Bitbucket's REST API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/) or `bb` command line tools if available.
2. Check pull request status, add comments, and enforce documentation updates before merges.
3. Incorporate Bitbucket Pipelines to run tests and documentation validation for each pass.

## General Tips
- Maintain the same commit conventions and DDD pass sequence regardless of platform.
- Ensure CI pipelines validate that documentation and code remain aligned.
- Update your platform-specific configuration in `.agent3d-config.yml` if custom hooks or scripts are required.
