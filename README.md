# Webpage Downloader

Download a web page to a local HTML file.

## Requirements

- Python 3 (standard library only — no third-party packages)
- Internet access

## Usage

```bash
python3 main.py https://example.com
python3 main.py https://example.com --output page.html
python3 main.py https://example.com --timeout 10
```

## Options

| Option | Description |
| --- | --- |
| `--output`, `-o` | Output file (default: derived from the URL, e.g. `index.html`) |
| `--timeout` | Request timeout in seconds (default: `30`) |
| `--user-agent` | User-Agent header to send |

## Example

```bash
$ python3 main.py https://example.com --output example.html
Downloaded https://example.com (HTTP 200, text/html, 1256 bytes) -> example.html
```

Network errors (bad host, HTTP error, timeout) are reported on stderr
and exit with code 1 instead of crashing.

## License

MIT — see `LICENSE`.
