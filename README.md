# sandbox-demo

A tiny throwaway web service used to exercise the sandbox platform end to end:
build → run → edit → publish → review → push to GitHub → merge.

## What it is

A single-file Python service (standard library only — no dependencies) that serves:

| route       | response                                              |
|-------------|-------------------------------------------------------|
| `/`         | an HTML page showing the greeting, version, host      |
| `/health`   | `{"status":"ok"}`                                      |
| `/api/info` | JSON: service, version, greeting, host, time          |

## Run it

```bash
docker compose up -d --build
```

The platform's `deploy.sh` publishes container port `8000` to an ephemeral host
port and prints the reachable `URL:`.

## Make a change to test the review loop

Edit `GREETING` (or `VERSION`) in [`app.py`](app.py), then publish and send the
session to review — that is the whole point of this repo.
