# Python Calculator Module

A simple and robust calculator module implementing basic arithmetic operations following Domain-Driven Design principles.

**Core Principle:** "Write the docs, then write the code—keep it lean, test it for real."

## Features

- Basic arithmetic operations:
  - Addition
  - Subtraction
  - Multiplication
  - Division
- Input validation
- Error handling for division by zero
- Floating-point number support

## Usage

```python
from calculator import Calculator

# Create a calculator instance
calc = Calculator()

# Perform calculations
result_add = calc.add(5, 3)      # Returns 8
result_sub = calc.subtract(5, 3)  # Returns 2
result_mul = calc.multiply(5, 3)  # Returns 15
result_div = calc.divide(6, 2)    # Returns 3.0
```

## Installation

```bash
# Local installation
pip install .
```

## Testing

The module includes comprehensive unit tests to ensure reliability:

```bash
python -m pytest tests/
```

## Domain Model

The calculator module follows these DDD concepts:

- **Entity**: Calculator (maintains calculation state)
- **Value Objects**: Numbers and Operations
- **Services**: Arithmetic operations
- **Aggregates**: Calculation history (future feature)

## Development Guidelines

1. Follow DDD principles for any new features
2. Maintain test coverage for all operations
3. Document any new functionality
4. Follow PEP 8 style guidelines
5. Add appropriate type hints

## Error Handling

The module includes robust error handling:

- Division by zero protection
- Type checking for inputs
- Invalid operation handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details
