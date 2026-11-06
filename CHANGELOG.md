# Changelog

## 2.0.0

### Breaking changes

- Python 3.11 or later is required, Python 3.9 and 3.10 are no longer supported.
- `sp` exits with 1 when a command fails, it used to always exit with 0. Warnings and job responses still exit with 0.
- `-j`, `-c` and `-t` can't be combined anymore.
- `-t` uses real tabs when piped or saved to a file, and aligned columns in a terminal. Empty values are empty instead
  of `None`, and long values aren't cut at 200 characters anymore.
- `padns query a` rejects invalid IoCs, like the other PADNS commands.
- A long running task prints only the `job <id>` hint, instead of the job status.
- Removed `-m/--with-metadata` from `websearch` and `feedsearch`, and the `livescan` entry. Neither did anything.
- API errors stop the command, the error body isn't printed as if it was a result.

### Added

- `whoislive` command: real-time whois information for a domain.
- `job` command: gets the status or the result of a long running task.
- `sp --version`.
- Requests time out after 30 seconds.
- Requests are retried on rate limits and server errors.
- `-f/--fields` on `websearch` and `feedsearch` is sent to the API.

### Changed

- API endpoints migrated to the newer versions.
- Error messages depend on the API status: API key, not found, rate limited or server problems.

### Fixed

- `-l/--limit` works on `websearch`, it was ignored.
- `websearch` and `feedsearch` don't wait at a `> ` prompt when used from the command line.
- `websearch` and `feedsearch` without a query show a clear message.
- A missing API key no longer blocks `help`, and shows a clear message on commands.
- `bulk_enrich` adds each IoC to the autocomplete, not the whole list as one entry.
- `unload padns` no longer crashes.
- IoCs and parameters are encoded in URLs.
- `.env` is only read from `~/.config/SP-CLI/.env`, not from the current folder.

### Internal

- Removed the `pandas` and `numpy` dependencies, and other unused packages.
