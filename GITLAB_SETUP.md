# GitLab Remote Setup

This folder is repository-ready. A GitLab remote was not created automatically because a GitLab connector is not available in the current ChatGPT environment.

After creating an empty GitLab project named `persistent-agency`, run:

```bash
git init -b main
git add .
git commit -m "Initial Persistent Agency research release"
git remote add origin <YOUR_GITLAB_REPOSITORY_URL>
git push -u origin main
```

Before public release, choose a software license and replace the placeholder licensing note in `README.md`.
