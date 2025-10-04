# guides.bundle.json Truncation Postmortem (2025-11-27)

## Summary
While adding shortage coverage to `data/guides.bundle.json`, we overwrote the entire bundle with only the shortage catalog payload. This truncated the file from ~37k lines to 703 lines, stripping metadata, XP tables, routes, source registry entries, and extras. The validator did not flag the issue, so the broken bundle shipped until we restored it from `Guide.bundle.backup.JSON` in a follow-up commit.

## Impact
- `data/guides.bundle.json` shrank from 37,272 lines in commit `839cfa9` to only 703 lines in commit `870a419`, removing nearly all content required by the shortages UI and downstream tooling.
- The truncated file was invalid JSON: it started with raw `"verified_at_utc"` fields instead of the expected `"guideCatalog"` object wrapper and lacked every top-level section (`metadata`, `routes`, etc.).
- Any deployment built from that commit would have crashed JSON consumers and left the shortages interface without data.

## Timeline
- **2025-11-26 (commit `839cfa9`)** – Bundle was healthy at 37k+ lines with all schema sections intact.
- **2025-11-27 (commit `870a419`)** – Attempted to sync shortage cards and accidentally overwrote the bundle with only the `guideCatalog.data.guides` payload, shrinking the file to 703 lines.
- **2025-11-27 (commit `58c3a85`)** – Restored the bundle from the backup file and introduced additional validation in `scripts/check_guides_bundle.py` to guard against silent truncation.

## Root Cause Analysis
1. We generated the refreshed shortage entries by scripting against the bundle, but the write step mistakenly dumped `bundle["guideCatalog"]["data"]["guides"]` instead of the full `bundle`. Because the helper wrote directly to `data/guides.bundle.json`, everything outside the guide catalog array was lost.
2. The existing `scripts/check_guides_bundle.py` at the time only asserted that the file contained valid JSON. Because the truncated file still parsed (despite being semantically wrong), CI and manual validation passed, allowing the bad commit to land.
3. We relied on line-count parity and manual inspection to confirm integrity, but we did not re-open the file after the script ran, so the truncation went unnoticed until downstream tests failed.

## Contributing Factors
- The bundle’s size (~37k lines) makes manual diff review unwieldy, so the massive deletion wasn’t obvious in the scrollback.
- Lack of a smoke-test that enumerates required top-level keys (`metadata`, `routes`, `sourceRegistry`, etc.) meant the validator produced a false positive.
- Working directly on the live bundle instead of a throwaway copy eliminated an escape hatch once the script misbehaved.

## Detection & Response
- The regression surfaced only after running broader coverage tooling and noticing missing routes, prompting a manual inspection of the bundle.
- Recovery required copying `data/Guide.bundle.backup.JSON` over `data/guides.bundle.json` and recommitting the restored bundle alongside strengthened validation logic.

## Preventive Actions
1. **Always edit a temporary bundle** – Copy `data/guides.bundle.json` to a scratch path, run transformation scripts against the copy, and diff against the original before replacing it.
2. **Enhance automated validation** – Extend `scripts/check_guides_bundle.py` to require the nine critical top-level sections and verify that `guideCatalog.guide_count` matches the number of entries (already completed in `58c3a85`). Consider adding schema snapshots or JSON schema validation for deeper coverage.
3. **Add canary assertions to helper scripts** – Whenever we script bundle mutations, assert that the output still contains expected keys (e.g., `"metadata"`, `"routes"`) before writing to disk.
4. **Track line-count deltas** – Record the pre- and post-edit line counts (or checksum) of the bundle during editing sessions. Abort and investigate if the delta exceeds the expected size of the change.
5. **Document the safe workflow** – Capture the above safeguards in `agent.md` so future updates follow the temp-file + validation routine by default.

## Follow-Up Tasks
- Automate a `scripts/check_guides_bundle.py --strict` mode that also validates a handful of route entries to ensure nested data survives edits.
- Create a small helper script (`scripts/update_guide_catalog.py`) that handles bundle mutations atomically and leaves the original untouched if validation fails.
- Add CI coverage to block commits where `data/guides.bundle.json` shrinks below an expected minimum size or fails the strict validator.
