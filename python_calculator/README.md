# Python Calculator Module

A simple and robust calculator module implementing basic arithmetic operations following Domain-Driven Design principles.

## Features

- Basic arithmetic operations:
  - Addition
  - Subtraction
  - Multiplication
  - Division
- Input validation
- Error handling for division by zero
- Floating-point number support

## Installation

```bash
# Local installation
pip install .
```

## Usage

```python
from calculator import Calculator

# Create a calculator instance
calc = Calculator()

# Perform calculations
result_add = calc.add(5, 3)      # Returns 8
result_sub = calc.subtract(7, 2)  # Returns 5
result_mul = calc.multiply(4, 6)  # Returns 24
result_div = calc.divide(9, 3)    # Returns 3.0
```

## Domain Model

The calculator module follows these domain concepts:
- `Calculator`: The main entity that encapsulates arithmetic operations
- `Operation`: Value object representing a mathematical operation
- `CalculationResult`: Value object containing the result and operation metadata

## Testing

The module includes comprehensive unit tests. To run the tests:

```bash
python -m pytest tests/
```

## Error Handling

The module includes robust error handling:
- Division by zero raises `DivisionByZeroError`
- Invalid input types raise `TypeError`
- Overflow conditions are properly handled

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Version History

- 1.0.0: Initial release with basic arithmetic operations