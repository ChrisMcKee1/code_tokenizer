# Code Tokenizer Usage Examples

## 🎯 Core Purpose
Code Tokenizer is your bridge between codebases and Large Language Models (LLMs). It intelligently processes your code to make it LLM-ready, handling everything from language detection to token management.

## 🛠️ CLI Usage Examples

### 1. Template Generation
```bash
# Process codebase to generate templates for LLM interactions
code-tokenizer -d ./my-project -o ./llm-template --format markdown

# Output can be used like:
<TEMPLATE>
<INSTRUCTIONS>
Use the <CODEBASE> code as reference, and convert the high-level <TASK> into detailed steps.
</INSTRUCTIONS>
<TASK>
Implement a new feature
</TASK>
<CODEBASE>
{output from code-tokenizer}
</CODEBASE>
</TEMPLATE>
```

### 2. Large Codebase Analysis
```bash
# Analyze a large project and prepare it for GPT-4
code-tokenizer -d ./my-project -o ./analysis --model gpt-4 --max-tokens 8192
```

### 3. API Documentation Generation
```bash
# Process API code and generate markdown documentation
code-tokenizer -d ./api-src -o ./docs --format markdown --model claude-3-opus
```

### 4. Code Migration Planning
```bash
# Analyze legacy codebase for migration planning
code-tokenizer -d ./legacy-app -o ./migration-analysis --bypass-gitignore
```

### 5. Security Audit Preparation
```bash
# Prepare codebase for security analysis
code-tokenizer -d ./secure-app -o ./security-audit --format json
```

### 6. Technical Debt Assessment
```bash
# Analyze codebase for technical debt
code-tokenizer -d ./project -o ./tech-debt-analysis --model gpt-4
```

### 7. Code Review Assistance
```bash
# Process changes for code review
code-tokenizer -d ./pull-request -o ./review --max-tokens 4000
```

### 8. Architecture Analysis
```bash
# Analyze project architecture
code-tokenizer -d ./microservices -o ./architecture --format json
```

## 🤖 LLM Integration Examples

### 1. Code Review with Context
```python
# Process code for review
tokenizer_output = subprocess.run([
    'code-tokenizer',
    '-d', './pr-changes',
    '-o', './review.md',
    '--model', 'gpt-4'
])

# Send to LLM with context
prompt = f"""
You are a senior code reviewer. Review the following codebase:

{open('./review.md').read()}

Focus on:
1. Code quality
2. Performance implications
3. Security considerations
4. Best practices
"""
```

### 2. Architecture Analysis
```python
# Generate architecture analysis
system_prompt = """You are an expert software architect. Analyze the following codebase 
and provide detailed architectural recommendations."""

user_prompt = f"""
Based on this codebase analysis:

{open('./architecture.json').read()}

Please provide:
1. Current architecture overview
2. Identified patterns
3. Improvement recommendations
4. Scalability considerations
"""
```

### 3. API Documentation Generation
```python
# Process API code
api_docs = f"""
Using this API codebase analysis:

{open('./api-docs.md').read()}

Generate comprehensive API documentation including:
1. Endpoint descriptions
2. Request/response examples
3. Authentication requirements
4. Error handling
5. Rate limiting details
"""
```

### 4. Technical Debt Assessment
```python
tech_debt_prompt = f"""
Analyze this codebase for technical debt:

{open('./tech-debt-analysis.md').read()}

Provide:
1. Debt categorization
2. Impact assessment
3. Prioritized remediation plan
4. Estimated effort
"""
```

### 5. Security Audit
```python
security_prompt = f"""
Perform a security audit on this codebase:

{open('./security-audit.json').read()}

Focus on:
1. Vulnerability identification
2. OWASP Top 10 compliance
3. Security best practices
4. Remediation recommendations
"""
```

### 6. Migration Planning
```python
migration_prompt = f"""
Based on this legacy codebase analysis:

{open('./migration-analysis.md').read()}

Create a detailed migration plan:
1. Current stack assessment
2. Target architecture recommendation
3. Step-by-step migration strategy
4. Risk mitigation plan
"""
```

### 7. Code Generation with Context
```python
generation_prompt = f"""
Using this existing codebase as context:

{open('./analysis.md').read()}

Generate code for a new feature that:
1. Matches existing patterns
2. Follows project conventions
3. Includes proper error handling
4. Adds necessary tests
"""
```

## 🎯 Problem-Solving Examples

1. **Token Management**
   - Problem: Code too large for LLM context windows
   - Solution: `code-tokenizer` automatically handles token counting and splitting

2. **Language Understanding**
   - Problem: Mixed language codebases
   - Solution: Intelligent language detection and processing

3. **Selective Processing**
   - Problem: Need to exclude certain files/directories
   - Solution: `.gitignore` support and custom filtering

4. **Format Compatibility**
   - Problem: Code needs to be formatted for LLM consumption
   - Solution: Multiple output formats (markdown, JSON)

5. **Analytics**
   - Problem: Understanding codebase composition
   - Solution: Detailed statistics and language analysis

## 🔄 Integration Workflows

1. **CI/CD Integration**
```yaml
- name: Analyze Code Changes
  run: |
    code-tokenizer -d . -o analysis.md
    # Send to LLM for review
```

2. **Pre-commit Hook**
```bash
#!/bin/bash
code-tokenizer -d . -o review.md
# Use output for automated code review
```

3. **Documentation Pipeline**
```python
# Automated documentation updates
def update_docs():
    os.system('code-tokenizer -d ./src -o ./docs/api.md')
    # Generate new documentation
```

4. **Development Workflow**
```python
# During development
def analyze_changes():
    os.system('code-tokenizer -d ./changes -o ./analysis.json')
    # Get AI assistance for implementation
``` 