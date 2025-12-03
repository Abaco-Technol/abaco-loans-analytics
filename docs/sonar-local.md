# SonarCloud / SonarQube local execution

Run code quality scans locally when a SonarQube server is available. The hosted CI workflow uses SonarCloud; local scans require an accessible server endpoint and matching tokens.

## Prerequisites
- Java 17+ available in the shell
- `sonar-scanner` installed or invoked via `npx sonar-scanner`
- A reachable SonarQube/SonarCloud server (for local containers, default is http://localhost:9000)
- `SONAR_TOKEN` exported in the environment

## Execution
From the repository root:
```bash
sonar-scanner -Dproject.settings=sonar-project.properties
```
If `sonar-scanner` is not on PATH, run:
```bash
npx --yes sonar-scanner -Dproject.settings=sonar-project.properties
```

## Troubleshooting
- Connection errors to `localhost:9000` indicate the SonarQube server is not running or reachable; start the server container and retry.
- Ensure network proxies allow access to the configured server.
- Verify `SONAR_TOKEN` matches the target project key and organization.
