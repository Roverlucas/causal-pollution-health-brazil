# Contributing

Thank you for your interest in contributing to this project. This repository supports a research paper submitted to The Lancet Planetary Health.

## How to Contribute

### Reporting Issues

If you find bugs in the pipeline, data processing errors, or inconsistencies in the results, please open a GitHub Issue with:

1. A clear description of the problem
2. Steps to reproduce (if applicable)
3. Expected vs actual behavior
4. Your environment (Python version, OS)

### Suggesting Improvements

We welcome suggestions for:

- Additional sensitivity analyses
- Alternative causal identification strategies
- Improved visualizations
- Extended coverage to other cities or time periods
- Code optimizations

Please open an Issue to discuss before submitting a Pull Request.

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Ensure the pipeline still runs: `make all`
5. Commit with clear messages
6. Push and open a Pull Request

### Code Style

- Python code follows PEP 8
- Use type hints where practical
- Keep functions focused and well-documented
- Configuration belongs in `src/utils/config.py`, not hardcoded

## Reproducibility

To reproduce the full analysis:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make all
```

You will need access to the Clima360 Brasil Supabase API. Set the following environment variables:

```bash
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
```

## Contact

- Lucas Rover — lucasrover@alunos.utfpr.edu.br
- Yara de Souza Tadano — yaratadano@utfpr.edu.br
