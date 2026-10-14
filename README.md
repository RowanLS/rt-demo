# Reaction-time demo

This is the staged Python project for **Better Code, Less Pain**.

## Explore the stages

```bash
git switch --detach 00-start
git switch --detach 01-uv
# ... up to 09-final
```

Compare stages with `git diff 04-complexity 05-tests`.
Some stages deliberately fail their newly introduced quality checks.

## Run the final stage

```bash
git switch --detach 09-final
uv sync --locked
make check
make figure
```

## Raw data

The CSV is illustrative and kept unchanged across every tag. Invalid examples
are synthetic data created in tests, not edits to raw observations.

## Licence

Original material is MIT-licensed; see LICENSE.
