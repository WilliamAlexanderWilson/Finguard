# Contributing to FinGuard

Thank you for your interest in FinGuard! This is primarily a portfolio project, but contributions are welcome.

## Ways to Contribute

### 🐛 Report Bugs
Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Sample data (anonymized)

### 💡 Suggest Features
Open an issue describing:
- The use case
- Proposed solution
- Any alternative approaches considered

### 🔧 Submit Code
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/finguard.git
cd finguard

# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_categorization.py
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Add comments for complex logic

## Testing

- Add tests for new features
- Ensure existing tests pass
- Use sample data (no real financial data in tests)

## Areas Open for Contribution

- **Industry-Specific Rules**: Add categorization patterns for different industries
- **Integration Examples**: Show integrations with QuickBooks, Xero, etc.
- **Visualization**: Add chart generation for reports
- **Multi-Currency**: Support for foreign exchange
- **Performance**: Optimize for larger datasets

## Questions?

Open an issue or reach out via [your contact method]

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
