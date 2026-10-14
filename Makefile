.PHONY: sync lint typecheck test check figure clean
sync:
	uv sync --locked --dev
lint:
	uv run ruff check .
	uv run ruff format --check .
typecheck:
	uv run pyright
test:
	uv run pytest
check: lint typecheck test
figure:
	uv run python -m rt_analysis.figure
clean:
	rm -f figure1.png
