# SonarQube local scanning

Use these steps to run the SonarQube/SonarCloud scanner locally with the project settings in `sonar-project.properties`.

## Prerequisites
- Java 11+ available on your PATH.
- SonarScanner CLI installed. Example installs:
  - macOS (Homebrew): `brew install sonar-scanner`
  - Linux (zip): download the [latest release](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/) and add the `bin` directory to your PATH.
- Network access to SonarCloud with credentials configured in the environment (`SONAR_TOKEN`).

## Run the scanner
From the repository root, execute:

```bash
sonar-scanner -Dproject.settings=sonar-project.properties
```

If the command is not found, confirm the CLI is on your PATH or reinstall. Keep `sonar.sources` aligned to active code paths (`apps`, `streamlit_app`) and avoid disabling rules—fix findings instead to preserve auditability.
