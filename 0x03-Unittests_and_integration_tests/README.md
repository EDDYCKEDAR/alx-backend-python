# 0x03. Unittests and Integration Tests

This project focuses on implementing comprehensive unit tests and integration tests for Python backend utilities and client modules. The project demonstrates advanced testing techniques including parameterization, mocking, and integration testing.

## Learning Objectives

By the end of this project, you should be able to:
- Understand the difference between unit and integration tests
- Use common testing patterns such as mocking, parametrizations and fixtures
- Write comprehensive unit tests using the `unittest` framework
- Mock external dependencies effectively
- Create parameterized tests for better test coverage
- Implement integration tests that test component interactions

## Project Structure

```
0x03-Unittests_and_integration_tests/
├── README.md
├── test_utils.py
├── test_client.py
├── utils.py (provided)
├── client.py (provided)
└── fixtures.py (provided)
```

## Requirements

- All files interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7
- All files end with a new line
- First line of all files: `#!/usr/bin/env python3`
- Code uses the pycodestyle style (version 2.5)
- All functions and coroutines are type-annotated
- All modules have documentation
- All classes have documentation
- All functions (inside and outside a class) have documentation

## Dependencies

Install the required packages:

```bash
pip3 install parameterized
```

## Files Description

### test_utils.py

Contains unit tests for the `utils` module with the following test classes:

#### TestAccessNestedMap
- **test_access_nested_map**: Parameterized test that validates the `access_nested_map` function with various nested dictionary inputs
- **test_access_nested_map_exception**: Tests that appropriate KeyError exceptions are raised for invalid paths

#### TestGetJson
- **test_get_json**: Mocks HTTP requests to test the `get_json` function without making actual external calls

#### TestMemoize
- **test_memoize**: Tests the memoization decorator functionality to ensure methods are cached properly

### test_client.py

Contains unit and integration tests for the `client` module with the following test classes:

#### TestGithubOrgClient
- **test_org**: Tests the GitHub organization data retrieval functionality
- **test_public_repos_url**: Tests the public repositories URL property
- **test_public_repos**: Tests the public repositories listing functionality
- **test_has_license**: Parameterized test for license checking functionality

#### TestIntegrationGithubOrgClient
- **setUpClass/tearDownClass**: Manages test fixtures and mocking setup
- **test_public_repos**: Integration test for repository listing
- **test_public_repos_with_license**: Integration test for filtered repository listing

## Testing Techniques Demonstrated

### 1. Parameterized Testing
```python
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2)
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
```

### 2. Mocking External Dependencies
```python
@patch('utils.requests.get')
def test_get_json(self, test_url, test_payload, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = test_payload
    mock_get.return_value = mock_response
```

### 3. Property Mocking
```python
with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
    mock_org.return_value = known_payload
    # Test property behavior
```

### 4. Integration Testing with Fixtures
```python
@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    # Integration test implementation
```

## Running the Tests

Execute the tests using the following commands:

```bash
# Run utils tests
python3 -m unittest test_utils.py

# Run client tests
python3 -m unittest test_client.py

# Run all tests
python3 -m unittest discover

# Run with verbose output
python3 -m unittest -v test_utils.py
python3 -m unittest -v test_client.py
```

## Task Breakdown

### Task 0: Parameterize a unit test
Create parameterized tests for `access_nested_map` function with different nested dictionary structures.

### Task 1: Parameterize a unit test
Test exception handling in `access_nested_map` using `assertRaises` context manager.

### Task 2: Mock HTTP calls
Mock external HTTP requests in `get_json` function testing to avoid actual network calls.

### Task 3: Parameterize and patch
Test the `memoize` decorator functionality using mocking techniques.

### Task 4: Parameterize and patch as decorators
Test GitHub organization client with mocked dependencies using decorators.

### Task 5: Mocking a property
Test property mocking for GitHub client's internal URL property.

### Task 6: More patching
Comprehensive testing of public repositories functionality with multiple mocks.

### Task 7: Parameterize
Test license checking functionality with different license scenarios.

### Task 8: Integration test: fixtures
Implement integration tests using class-level fixtures and comprehensive mocking.

## Key Testing Concepts

### Unit Tests
- Test individual functions or methods in isolation
- Mock external dependencies
- Focus on single responsibility testing
- Fast execution and reliable results

### Integration Tests
- Test interaction between multiple components
- Use real or realistic data fixtures
- Verify end-to-end functionality
- May involve multiple system layers

### Best Practices Demonstrated
- **Isolation**: Each test is independent and doesn't affect others
- **Repeatability**: Tests produce consistent results across runs
- **Clarity**: Test names and structure clearly indicate what's being tested
- **Coverage**: Tests cover both happy paths and error conditions
- **Efficiency**: Minimal external dependencies and fast execution

## Author

This project is part of the ALX Backend Python curriculum, focusing on advanced testing methodologies and best practices in Python development.
