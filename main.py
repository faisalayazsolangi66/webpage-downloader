#!/usr/bin/env python3
"""Download a web page to a local HTML file.

Usage:
    python3 main.py https://example.com
    python3 main.py https://example.com --output page.html
    python3 main.py https://example.com --timeout 10
"""
import argparse
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; webpage-downloader/1.0)"


def default_filename(url):
    parsed = urllib.parse.urlparse(url)
    name = os.path.basename(parsed.path.rstrip("/")) or "index.html"
    if not name.endswith((".html", ".htm")):
        name += ".html"
    return name or "index.html"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Download a web page to a local HTML file.")
    parser.add_argument("url", help="URL of the page to download")
    parser.add_argument("--output", "-o",
                        help="output file (default: derived from the URL)")
    parser.add_argument("--timeout", type=float, default=30,
                        help="request timeout in seconds (default: 30)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT,
                        help="User-Agent header to send")
    args = parser.parse_args(argv)

    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    parsed = urllib.parse.urlparse(args.url)
    if parsed.scheme not in ("http", "https"):
        parser.error("URL must start with http:// or https://")

    output = args.output or default_filename(args.url)
    request = urllib.request.Request(
        args.url, headers={"User-Agent": args.user_agent})
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            data = response.read()
            content_type = response.headers.get_content_type()
            status = response.status
    except urllib.error.HTTPError as exc:
        print(f"error: HTTP {exc.code} {exc.reason} for {args.url}",
              file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"error: cannot reach {args.url}: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print(f"error: timed out after {args.timeout}s fetching {args.url}",
              file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: network error fetching {args.url}: {exc}", file=sys.stderr)
        return 1

    try:
        with open(output, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        print(f"error: cannot write {output}: {exc}", file=sys.stderr)
        return 1

    print(f"Downloaded {args.url} (HTTP {status}, {content_type}, "
          f"{len(data)} bytes) -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
