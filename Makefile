.PHONY: dev

# run dev (venv + docker-compose + fastapi)
dev:
	 . .venv/bin/activate && docker compose up -d && fastapi dev app/main.py