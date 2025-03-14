# Contributing to AlgoTradePro5

## Development Rules

### Rule 1: Feature Branches
- Create feature branches for all changes
- Use descriptive names: `feat/feature-name`, `fix/issue-name`
- Keep commits small and focused
- Push changes frequently to avoid losing context

### Rule 2: Clean Workspace
- Remove redundant files after committing
- Organize files in appropriate directories
- Maintain clean integration
- Remove unintegrated/rogue files

### Rule 3: Testing
- Include tests with all new code
- Maintain test coverage above 80%
- Test all risk management rules
- Validate AI model integrations

## Code Standards

### Python Style Guide
- Follow PEP 8
- Use type hints
- Document all functions
- Max line length: 100 characters

### Documentation Requirements
- Update README.md for major changes
- Maintain architecture-analysis.md
- Update integration-guide.md
- Record changes in journal.md

### Commit Messages
```
type(scope): Short description

- Detailed bullet points
- For complex changes
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

## Development Workflow

### 1. Starting Development
```powershell
# Create feature branch
git checkout -b feat/your-feature

# Install dependencies
pip install -r requirements.txt
```

### 2. Before Committing
- Run all tests
- Update documentation
- Check code formatting
- Verify GPU compatibility

### 3. Code Review Requirements
- No direct pushes to main
- All changes via Pull Requests
- Required reviews: 1
- All tests must pass

## Testing Guidelines

### Unit Tests
- Test each component independently
- Mock external dependencies
- Test error conditions
- Verify risk management rules

### Integration Tests
- Test component interactions
- Validate data flow
- Check system recovery
- Test performance metrics

### Performance Testing
- Benchmark critical operations
- Test under load
- Validate resource usage
- Check memory leaks

## Environment Setup

### Development Environment
- Windows 11
- Python 3.8+
- CUDA Toolkit
- Docker Desktop
- VSCode with extensions:
  - Python
  - Docker
  - Git
  - CUDA Tools

### Local Testing
```powershell
# Run unit tests
python -m pytest tests/unit

# Run integration tests
python -m pytest tests/integration

# Test GPU setup
python validate_cuda.py
```

## Debug Logging

### Log Levels
- ERROR: System failures
- WARNING: Potential issues
- INFO: General operations
- DEBUG: Detailed tracing

### Log Format
```python
logger.info(
    "Operation: %s, Status: %s, Details: %s",
    operation_name,
    status,
    details
)
```

## Performance Guidelines

### Resource Management
- Release GPU memory explicitly
- Use connection pooling
- Implement proper cleanup
- Monitor memory usage

### Optimization
- Profile critical paths
- Optimize database queries
- Minimize API calls
- Use efficient algorithms

## Security Guidelines

### Data Protection
- No credentials in code
- Use environment variables
- Encrypt sensitive data
- Sanitize all inputs

### Access Control
- Limit API permissions
- Use principle of least privilege
- Monitor access logs
- Regular security audits

## Error Recovery

### System Failures
1. Log error details
2. Save system state
3. Attempt recovery
4. Notify if needed

### Data Recovery
1. Maintain backups
2. Version critical data
3. Document recovery steps
4. Test recovery plans

## Support

### Getting Help
- Check existing issues
- Review documentation
- Run diagnostics
- Contact maintainers

### Reporting Issues
- Use issue templates
- Include system details
- Attach relevant logs
- Describe reproduction steps