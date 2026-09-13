# Security policy

## Supported scope

Security fixes track the latest revision of the default branch `bakboem-dev`. Historical commits and locally generated media evidence do not carry a separate security-maintenance promise.

## Private vulnerability reports

Use the GitHub repository's private vulnerability reporting entry. Do not open a public issue for an unfixed vulnerability. Reports should include as much of the following as possible:

- Affected commits and components
- Reproduction steps and a minimal input
- Actual impact and attack preconditions
- Any verified mitigation
- Whether leaked tokens, model credentials, or personal data are involved

Do not publish exploit details before maintainers complete an initial confirmation. Ordinary defects and feature requests should still use public issues.

## Local service boundary

The operator console and observatory are machine-local tools and may bind loopback only. Do not expose ports `4320` or `4319` directly to a LAN or the internet. Do not commit evidence packages that contain tokens, personal paths, or unsanitized logs to a public repository.

Model weights and the Hugging Face cache are not part of this repository. Users must protect their own cache directories, access tokens, and upstream model credentials.
