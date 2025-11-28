# Enterprise Delivery Playbook — ContosoTeamStats on GitHub Enterprise

This guide captures the operational steps to onboard the team to GitHub Copilot, enforce SAML SSO and enterprise guardrails, run Advanced Security scans, and accelerate the ContosoTeamStats (.NET 6 API) delivery to Azure with CI/CD, monitoring, and dashboards.

## Roles and ownership
- **Enterprise Owner**: configures SAML/SCIM, audit log streaming, default security policies, billing/seat assignments.
- **Org Admin/Security Admin**: enforces security defaults (branch protections, secret scanning push protection, code scanning policies), manages teams, and approves Copilot seat usage.
- **Platform/DevOps**: maintains CI/CD (GitHub Actions + Azure OIDC), Dependabot, environment protections, and observability exports.
- **Team Leads**: approve pull requests, monitor KPIs, and triage security/code scanning alerts.

## Invite the team to GitHub Copilot
1. In the GitHub Enterprise or org **Settings → Copilot → Policies**, toggle **Copilot for Enterprise** and choose **Allow for all members** (or selected teams if you want staged rollout).
2. Assign seats via **Billing → Copilot** or through **Enterprise → Policies → Seat management**. Export a CSV of GitHub usernames to bulk-assign.
3. Add users to GitHub teams that map to ContosoTeamStats (e.g., `api-engineering`, `sre-observability`); Copilot and repository access inherit from team membership.
4. Publish an onboarding checklist in the repo’s Discussions or Wiki that links IDE setup (VS/VS Code, JetBrains), the security policy, and the PR review flow.

## Configure SAML SSO (with SCIM if available)
1. As an Enterprise Owner, go to **Enterprise Settings → Authentication security → SAML single sign-on**.
2. Choose your IdP (e.g., Entra ID/Azure AD) and **Upload/enter IdP metadata**. Note the **Entity ID** and **Assertion Consumer Service (ACS) URL** GitHub provides.
3. In the IdP, configure the app with **NameID = user.email** and map attributes: `userName`, `displayName`, `email`, `department`.
4. Enable **Just-in-Time (JIT) provisioning** and, if licensed, **SCIM** for automatic deprovisioning. Test with a pilot user before enforcing.
5. Back in GitHub, **Enforce SAML SSO** for the Enterprise and org, then **Require SSO for PATs and SSH keys**. Validate with `ssh -T git@github.com` using an SSO-authorized key.

## Enterprise guardrails to enable
- **Identity & access**: enforce SSO, require security keys/Passkeys or WebAuthn for MFA, disable outside collaborators unless approved, and set **default repository visibility to private**.
- **Repo protections**: branch protection (require PR reviews, status checks, signed commits), **CODEOWNERS** for ContosoTeamStats API paths, and **required workflows** for CodeQL/CI.
- **Secrets**: enable **Secret scanning (with push protection)** and **Token Leakage Prevention** at the org; block pushes containing high-confidence secrets.
- **Auditability**: stream audit logs to SIEM (Blob/Log Analytics/Splunk) and enable **security overview** for governance.
- **Policy controls**: enable **content attachment restrictions**, limit GitHub Apps to approved vendors, and require **Dependabot auto-triage rules** for production branches.

## Code security scans for this repo
- **CodeQL code scanning**: enable via GitHub UI (**Security → Code scanning alerts → Set up → Default**), or use the provided workflow `.github/workflows/codeql.yml`. The workflow runs on pull requests to `main` and the weekly schedule, analyzing JavaScript/TypeScript and Python (extend to C# once the .NET API code is added).
- **Secret scanning**: ensure org-level Secret scanning + Push Protection is on. Add custom patterns for internal API keys. Configure **Security → Secret scanning → Enable for private repos** at org level; repo inherits.
- **Dependabot**: the repo ships `.github/dependabot.yml` to monitor npm, pip, and GitHub Actions weekly. Approve auto-PRs with required reviewers and status checks.
- **Sonar/SAST**: keep `sonarcloud.yml` active and gate merges on quality gate where applicable.

## CI/CD to Azure (ACR + App Service)
1. **OIDC to Azure**: in Azure, create a Federated Credential on the SP used for deployment (scope: `api://AzureADTokenExchange`, subject: `repo:<org>/<repo>:environment:<env>`). Store `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, and `AZURE_RESOURCE_GROUP` as GitHub Environment secrets.
2. **Build & test**: reuse `ci-web.yml`/`ci-analytics.yml` for lint/test. Add a .NET job that runs `dotnet restore`/`dotnet test` for ContosoTeamStats when the API project is present.
3. **Containerize**: build/push Docker image to ACR using `docker build` + `az acr login` or `azure/login@v2` + `azure/cli@v2`. Tag as `${{ github.sha }}` and `latest`.
4. **Deploy**: use `azure/webapps-deploy@v3` (App Service) pointing to the ACR image tag; guard with environment protection rules (approvals, secrets, lock deployments) per `dev`/`prod`.
5. **Infra-as-Code**: place ARM/Bicep/Terraform in `infra/azure` with review requirements. Run `terraform plan` in PRs and `terraform apply` on protected branches.

## Observability, KPIs, and alerting (free tier friendly)
- **Delivery KPIs**: lead time for changes, deployment frequency, MTTR, change failure rate, percentage of PRs passing required checks, Dependabot PR time-to-merge.
- **Security KPIs**: open CodeQL/secret scanning alerts over time, mean time to remediate vuln/secret, Dependabot exposure window, signed-commit coverage, and SSO enforcement compliance.
- **Runtime KPIs**: App Service availability (5xx rate), p95 latency, error budget burn, container restart count, ACR pull errors, build success rate.
- **Alerts/Dashboards**: GitHub Security Overview for org posture, GitHub Actions workflow success trend, Azure Monitor dashboards (App Service HTTP errors/latency, ACR pull errors, CPU/memory), and SIEM alerts from audit logs and secret scanning webhook events.

## Quick commands and links
- **CodeQL local prep**: `gh codeql database analyze --language=javascript,python` (requires GHAS CLI and auth).
- **Dependabot status**: `gh api repos/:owner/:repo/dependabot/alerts --paginate | jq length` to count open alerts.
- **Secret scanning test**: commit a fake secret pattern, expect push rejection with push protection enabled.
- **Docs**: GitHub Enterprise Cloud → Security → [Advanced Security](https://docs.github.com/enterprise-cloud@latest/code-security) and [Copilot](https://docs.github.com/enterprise-cloud@latest/copilot/overview-of-github-copilot).
