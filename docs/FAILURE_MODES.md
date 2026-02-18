# Failure Modes and Handling

## Malformed payload (422)
- Trigger: required fields missing or invalid constraints.
- Response: standardized error envelope with `VALIDATION_ERROR`.
- Client action: fix payload schema before retry.

## Upstream model/API timeout
- Trigger: external provider timeout during summarization.
- Current behavior: fallback path can be enabled by running without API key.
- Recommended next step: add explicit timeout + retry policy and circuit breaker.

## Unsupported document content
- Trigger: empty or non-meaningful document text.
- Response: validation error if minimum constraints fail.
- Client action: provide cleaned, non-empty text input.

## Retry guidance
- Safe retries: idempotent read/summary requests.
- Non-safe retries: future write actions should carry idempotency keys.
