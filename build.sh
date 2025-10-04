uv run setup.py build_ext --inplace
uv run pytest -s -m "not benchmark"
uv run run_profile.py