# 🔧 Code Tokenizer Examples

> Transform your code into intelligent, AI-ready components

## 🤖 AI Framework Integration

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">⚡ Semantic Kernel</h3></summary>


> Perfect for enterprise .NET applications with deep code understanding

<details open>

#### 🎯 When to Use

- Building enterprise .NET applications that need deep code understanding capabilities
- Implementing AI-powered code review and analysis systems
- Creating intelligent documentation generators that understand code context
- Developing automated architectural analysis tools
- Building smart refactoring assistants that understand full codebase context

#### 💡 Value

- AI receives precisely filtered, tokenized code context through Semantic Kernel's plugin system
- Enables deep code understanding while respecting token limits and context windows
- Combines enterprise-grade AI orchestration with intelligent code processing
- Transforms raw code into AI-optimized context for better analysis
- Maintains security and compliance while enabling powerful AI features

#### 🚀 Real Use

- AI performs architectural reviews with full system context awareness
- AI generates accurate documentation with implementation details
- AI suggests improvements based on deep code understanding

#### 📚 Documentation

- [Overview](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [Native Plugins](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-native-plugins?pivots=programming-language-csharp)
- [Microsoft.Extensions.AI](https://learn.microsoft.com/en-us/dotnet/ai/ai-extensions)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```csharp
using Microsoft.SemanticKernel;
using System.ComponentModel;
using System.Diagnostics;

// Code Tokenizer Plugin
public class CodeTokenizerPlugin
{
    private readonly ILoggerFactory _loggerFactory;

    public CodeTokenizerPlugin(ILoggerFactory loggerFactory)
    {
        _loggerFactory = loggerFactory;
    }

    [KernelFunction("extract_context")]
    [Description("Extracts context from code for LLM processing")]
    public async Task<string> ExtractContextAsync(
        [Description("Directory containing code to process")] string directory,
        [Description("Output file path for the context")] string output,
        [Description("LLM model to use for tokenization")] string model = "gpt-4o")
    {
        var logger = _loggerFactory.CreateLogger<CodeTokenizerPlugin>();
        
        try
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = "code-tokenizer",
                Arguments = $"-d {directory} -o {output} --model {model}",
                RedirectStandardOutput = true,
                UseShellExecute = false
            };

            using var process = Process.Start(startInfo);
            await process.WaitForExitAsync();
            
            // Read the generated context file
            if (File.Exists(output))
            {
                return await File.ReadAllTextAsync(output);
            }
            
            throw new Exception("Context file was not generated");
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Error extracting context from code");
            throw;
        }
    }
}

// Code Review Plugin
public class CodeReviewPlugin
{
    private readonly ILoggerFactory _loggerFactory;
    private readonly IChatClient _chatClient;

    public CodeReviewPlugin(ILoggerFactory loggerFactory, string endpoint, string deploymentName, string apiKey)
    {
        _loggerFactory = loggerFactory;
        _chatClient = new Azure.AI.Inference.ChatCompletionsClient(
            new($"https://{endpoint}.openai.azure.com/openai/deployments/{deploymentName}"),
            new AzureKeyCredential(apiKey))
        .AsChatClient("claude-3-sonnet");
    }

    [KernelFunction("review_code")]
    [Description("Reviews code content and provides feedback")]
    public async Task<string> ReviewCodeAsync(
        [Description("Code content to review in markdown format")] string codeContent,
        [Description("Type of review to perform (e.g., security, performance, style)")] string reviewType = "comprehensive")
    {
        var logger = _loggerFactory.CreateLogger<CodeReviewPlugin>();
        
        try
        {
            var prompt = $"Conduct a {reviewType} code review for the following code:\n\n{codeContent}";
            return await _chatClient.GetResponseAsync(prompt);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Error performing code review");
            throw;
        }
    }
}

// Example usage in an ASP.NET Core application
public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        // Add logging
        builder.Services.AddLogging();

        // Add Azure AI Inference services
        builder.Services.AddAzureInferenceClient(options =>
        {
            options.Endpoint = builder.Configuration["AzureOpenAI:Endpoint"]!;
            options.DeploymentName = builder.Configuration["AzureOpenAI:DeploymentName"]!;
            options.ApiKey = builder.Configuration["AzureOpenAI:ApiKey"]!;
        });

        // Configure Semantic Kernel
        builder.Services.AddScoped<IKernel>(sp =>
        {
            var loggerFactory = sp.GetRequiredService<ILoggerFactory>();
            var configuration = sp.GetRequiredService<IConfiguration>();
            var inferenceClient = sp.GetRequiredService<IChatClient>();
            
            // Create kernel builder
            var kernelBuilder = Kernel.CreateBuilder()
                .AddAzureInferenceChatCompletion(inferenceClient);
            
            // Add plugins
            kernelBuilder.Plugins.AddFromType<CodeTokenizerPlugin>("CodeTokenizer");
            kernelBuilder.Plugins.AddFromObject(new CodeReviewPlugin(
                loggerFactory,
                configuration["AzureOpenAI:Endpoint"]!,
                configuration["AzureOpenAI:DeploymentName"]!,
                configuration["AzureOpenAI:ApiKey"]!
            ), "CodeReview");

            // Build the kernel
            return kernelBuilder.Build();
        });

        // Add controllers
        builder.Services.AddControllers();
        
        var app = builder.Build();
        app.MapControllers();
        app.Run();
    }
}

public record ReviewRequest(string Directory, string? ReviewType);

// Example of using chat completion
public class ChatExample
{
    public static async Task RunChatExample(IKernel kernel)
    {
        var chatHistory = new ChatHistory();
        chatHistory.AddUserMessage("Conduct a code review");

        var chatCompletion = kernel.GetRequiredService<IChatCompletionService>();

        var executionSettings = new OpenAIPromptExecutionSettings 
        {
            FunctionCallBehavior = FunctionCallBehavior.AutoInvokeKernelFunctions
        };

        var response = await chatCompletion.GetChatMessageContentAsync(
            chatHistory,
            executionSettings: executionSettings,
            kernel: kernel);
            
        Console.WriteLine(response);
    }
}
</details>
</details>


<div align="center">

---

</div>

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">🔗 LangChain</h3></summary>


> Perfect for building AI-powered code analysis pipelines

<details open>

#### 🎯 When to Use

- Building AI-powered code analysis pipelines that need to process large codebases
- Creating multi-step analysis workflows with context preservation
- Implementing automated documentation generation systems
- Developing intelligent code review pipelines
- Building custom AI tools that need deep code understanding

#### 💡 Value

- AI gets structured, filtered code context through LangChain's tool system
- Enables accurate analysis across multiple files and directories
- Maintains context throughout multi-step analysis processes
- Provides flexible integration with various AI models
- Supports custom tool creation for specialized analysis

#### 🚀 Real Use

- AI performs multi-step code analysis with full context awareness
- AI generates comprehensive documentation with actual code examples
- AI provides accurate refactoring suggestions based on full codebase understanding

#### 📚 Documentation

- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [Custom Tools](https://python.langchain.com/docs/modules/agents/tools/custom_tools)
- [Tool Wrappers](https://python.langchain.com/docs/modules/agents/tools/how_to/tool_input_validation)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```python
from langchain.tools import BaseTool
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import subprocess
from typing import Optional

# CLI Tool wrapper for LangChain
class CodeTokenizerTool(BaseTool):
    name = "code_tokenizer"
    description = "Extracts context from code for LLM processing"

    def _run(self, directory: str, output: str = "./context/output.md", model: str = "gpt-4o") -> str:
        """Run code-tokenizer CLI tool."""
        result = subprocess.run(
            ["code-tokenizer", "-d", directory, "-o", output, "--model", model],
            capture_output=True,
            text=True
        )
        return result.stdout

    def _arun(self, directory: str, output: str = "./context/output.md", model: str = "gpt-4o") -> str:
        """Run code-tokenizer CLI tool asynchronously."""
        raise NotImplementedError("Async not implemented")

# Example LangChain integration
def create_code_review_chain():
    # Initialize the tool
    tokenizer_tool = CodeTokenizerTool()
    
    # Create LangChain components
    llm = OpenAI(temperature=0)
    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            input_variables=["code_context"],
            template="Review this code:\n\n{code_context}"
        )
    )
    
    # Create a tool that uses both code-tokenizer and LLM
    def review_code(directory: str) -> str:
        # Extract context using code-tokenizer
        tokenizer_tool.run({"directory": directory})
        
        # Load the context
        with open('./context/output.md', 'r') as f:
            code_context = f.read()
        
        # Run the review chain
        return chain.run(code_context=code_context)
    
    return Tool(
        name="Code Review",
        func=review_code,
        description="Review code using context from Code Tokenizer"
    )

# Example usage in a FastAPI application
from fastapi import FastAPI

app = FastAPI()
review_tool = create_code_review_chain()

@app.post("/review")
async def review_code(directory: str):
    return {"review": review_tool.run(directory)}
```

</details>
</details>

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">🌟 Azure OpenAI SDK</h3></summary>


> Perfect for enterprise-grade code analysis solutions

<details open>

#### 🎯 When to Use

- Building enterprise-grade code analysis solutions
- Implementing secure AI integration in Azure environments
- Creating compliant code review systems
- Developing scalable documentation generators
- Building Azure-integrated AI assistants

#### 💡 Value

- AI receives enterprise-compliant code context
- Enables secure and accurate code analysis in Azure environments
- Provides scalable AI integration with Azure services
- Maintains enterprise security standards
- Supports compliance requirements

#### 🚀 Real Use

- AI performs secure code reviews with full system context
- AI generates compliant documentation with implementation details
- AI suggests improvements while respecting enterprise patterns

#### 📚 Documentation

- [Azure OpenAI Client Library](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.openai-readme)
- [Azure OpenAI Assistants](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/assistant)
- [Azure AI SDK](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```csharp
using Azure.AI.OpenAI;
using Microsoft.Extensions.Azure;

public class CodeReviewAssistant
{
    private readonly OpenAIClient _client;
    private readonly CodeTokenizerTool _tokenizer;

    public CodeReviewAssistant(OpenAIClient client)
    {
        _client = client;
        _tokenizer = new CodeTokenizerTool();
    }

    public async Task<string> CreateAssistant(string directory)
    {
        // Extract context using code-tokenizer
        await _tokenizer.ExtractContext(
            directory,
            "./context/assistant-context.md",
            "gpt-4o"
        );

        // Load the context
        var codeContext = await File.ReadAllTextAsync("./context/assistant-context.md");

        // Create the assistant
        var assistant = await _client.GetAssistantAsync(new AssistantCreateOptions
        {
            Name = "Code Review Assistant",
            Instructions = $"Use this codebase context for reviews: {codeContext}",
            Model = "gpt-4",
            Tools = { new AssistantTool { Type = "code_interpreter" } }
        });

        return assistant.Value.Id;
    }

    public async Task<string> GetCodeReview(string assistantId, string codeContext)
    {
        var thread = await _client.CreateThreadAsync();
        
        await _client.CreateMessageAsync(thread.Id, new ChatRequestMessage
        {
            Role = "user",
            Content = $"Review this code context:\n\n{codeContext}"
        });

        var run = await _client.CreateRunAsync(thread.Id, new RunCreateOptions
        {
            AssistantId = assistantId
        });

        // Wait for completion and get the review
        while (run.Status != "completed")
        {
            await Task.Delay(1000);
            run = await _client.GetRunAsync(thread.Id, run.Id);
        }

        var messages = await _client.GetMessagesAsync(thread.Id);
        return messages.Last().Content;
    }
}

// Example usage in an ASP.NET Core application
[ApiController]
[Route("[controller]")]
public class CodeReviewController : ControllerBase
{
    private readonly CodeReviewAssistant _assistant;

    public CodeReviewController(CodeReviewAssistant assistant)
    {
        _assistant = assistant;
    }

    [HttpPost("review")]
    public async Task<IActionResult> ReviewCode([FromBody] ReviewRequest request)
    {
        var assistantId = await _assistant.CreateAssistant(request.Directory);
        var review = await _assistant.GetCodeReview(assistantId, request.Context);
        return Ok(review);
    }
}
```

</details>
</details>

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">🤖 OpenAI Assistants</h3></summary>


> Perfect for building persistent, context-aware code analysis assistants

<details open>

#### 🎯 When to Use

- Creating specialized code review assistants
- Building persistent code analysis systems
- Implementing context-aware documentation generators
- Developing intelligent code improvement systems
- Building long-running code analysis workflows

#### 💡 Value

- AI maintains persistent understanding of code context
- Enables more accurate and consistent analysis over time
- Provides thread-based conversation management
- Supports complex multi-step analysis
- Maintains context across multiple interactions

#### 🚀 Real Use

- AI performs contextual code reviews with historical understanding
- AI generates documentation that maintains consistency
- AI suggests improvements based on full project context

#### 📚 Documentation

- [Assistants API](https://platform.openai.com/docs/api-reference/assistants)
- [Assistants Overview](https://platform.openai.com/docs/assistants/overview)
- [Code Interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```python
from openai import OpenAI
import subprocess
from pathlib import Path

class CodeReviewAssistant:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key)

    async def extract_context(self, directory: str, include_patterns: list[str] = None) -> str:
        """Extract context from code using the code-tokenizer CLI."""
        # Build the command
        cmd = ["code-tokenizer", "-d", directory, "-o", "context.md", "--model", "gpt-4o"]
        if include_patterns:
            cmd.extend(["--include", ",".join(include_patterns)])
        
        # Run code-tokenizer CLI
        subprocess.run(cmd, check=True)
        
        # Read the generated context
        with open("context.md", "r") as f:
            return f.read()

    async def create_assistant(self, directory: str) -> str:
        """Create an OpenAI Assistant with code context."""
        # Extract context using code-tokenizer CLI
        code_context = await self.extract_context(
            directory=directory,
            include_patterns=["*.py", "*.js", "*.ts"]  # Customize patterns as needed
        )
        
        # Create the assistant
        assistant = await self.client.beta.assistants.create(
            name="Code Review Assistant",
            instructions=f"Use this codebase context for reviews: {code_context}",
            model="gpt-4-turbo-preview",
            tools=[{"type": "code_interpreter"}]
        )
        
        return assistant

# Example usage
async def main():
    assistant = CodeReviewAssistant()
    
    # Create assistant with context from multiple directories
    gpt_assistant = await assistant.create_assistant("./gpt/knowledge")
    
    # Extract context for specific file types
    function_context = await assistant.extract_context(
        directory="./examples/functions",
        include_patterns=["*.ts", "*.js"]
    )
    
    print(f"Assistant created with ID: {gpt_assistant.id}")
    print(f"Function context extracted: {len(function_context)} characters")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

### [AutoGen](https://microsoft.github.io/autogen/)

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">🔄 AutoGen</h3></summary>


> Perfect for building autonomous, multi-agent code analysis systems

<details open>

#### 🎯 When to Use
- Building autonomous code analysis agents that need to understand codebases
- Creating self-directed code review systems
- Implementing automated documentation generators
- Developing intelligent code improvement agents
- Building multi-agent code analysis systems

#### 💡 Value
- AI agents receive complete code context for autonomous operation
- Enables self-directed analysis and improvement suggestions
- Supports multi-agent collaboration on code analysis
- Provides flexible agent configuration for different tasks
- Maintains context across agent interactions

#### 🚀 Real Use
- AI agents perform self-directed code reviews with full context
- AI generates comprehensive documentation autonomously
- AI suggests improvements based on deep code understanding

#### 📚 Documentation
- [AutoGen Overview](https://microsoft.github.io/autogen/docs/Getting-Started)
- [Agent Configuration](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat)
- [Multi-Agent Systems](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat#multiagent-conversation)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```python
import subprocess
from autogen import AssistantAgent, UserProxyAgent

def setup_code_review_agents():
    # Generate context using code-tokenizer CLI
    subprocess.run([
        "code-tokenizer",
        "-d ./autogen/agents",
        "-o", "./context/agent-defs.md",
        "--model", "claude-3"
    ], check=True)
    
    # Generate context for scenarios
    subprocess.run([
        "code-tokenizer",
        "-d ./scenarios",
        "-o", "./context/scenarios.md",
        "--include", "*.py"
    ], check=True)
    
    # Load code context from Code Tokenizer output
    with open('./context/agent-defs.md', 'r') as f:
        code_context = f.read()
    
    assistant = AssistantAgent(
        name="code_reviewer",
        system_message=f"Review code using this context: {code_context}",
        llm_config={"temperature": 0}
    )
    
    user_proxy = UserProxyAgent(
        name="user_proxy",
        code_execution_config={"work_dir": "coding"}
    )
    
    return assistant, user_proxy
```

</details>
</details>

</details>

# 📚 Documentation & Analysis

> Streamline your documentation and codebase analysis


<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">📖 Documentation Generation</h3></summary>


> Perfect for maintaining comprehensive and up-to-date documentation

<details open>

#### 🎯 When to Use

- Generating comprehensive API documentation
- Creating codebase overviews and architecture diagrams
- Maintaining up-to-date technical documentation
- Analyzing code patterns and dependencies
- Building searchable knowledge bases

#### 💡 Value

- AI understands code context and relationships
- Enables automatic documentation updates
- Supports technical writing and explanations
- Maintains documentation accuracy
- Provides insights into code structure

#### 🚀 Real Use

- AI generates detailed API documentation
- AI creates architecture diagrams from code
- AI maintains technical documentation
- AI analyzes code patterns and dependencies
- AI builds searchable knowledge bases

#### 📚 Documentation

- [Documentation Best Practices](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
- [API Documentation](https://swagger.io/docs/)
- [Architecture Documentation](https://c4model.com/)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```powershell
# Generate comprehensive documentation
code-tokenizer -d . -o ./docs/overview.md --model gpt-4o

# Create API documentation
code-tokenizer -d ./src/api -o ./docs/api.md --model gpt-4o

# Generate architecture diagrams
code-tokenizer -d ./src -o ./docs/architecture.md --model gpt-4o --diagram

# Analyze code patterns
code-tokenizer -d ./src -o ./docs/patterns.md --model gpt-4o --analyze

# Build knowledge base
code-tokenizer -d . -o ./docs/kb.md --model gpt-4o --kb
```

</details>
</details>

</details>

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">🔍 Microservices Analysis</h3></summary>


> Perfect for analyzing and validating distributed system architectures

<details open>

#### 🎯 When to Use
- Analyzing service boundaries across distributed systems
- Validating contract compatibility between services
- Monitoring breaking changes in service interfaces
- Evaluating domain model consistency
- Assessing microservice coupling and cohesion

#### 💡 Value
- AI receives clean, filtered view of service contracts
- Enables accurate analysis of service interactions
- Validates service boundary consistency
- Identifies potential coupling issues
- Maintains service compatibility tracking

#### 🚀 Real Use
- AI detects breaking changes across service boundaries
- AI generates service compatibility matrices
- AI validates domain model consistency

#### 📚 Documentation
- [Microservices Architecture Guide](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)
- [Domain-Driven Design](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd)
- [API Design Guidelines](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```powershell
# Generate service interface analysis
code-tokenizer -d ./services -o ./analysis/interfaces.md --include "*.{proto,ts,cs}" --exclude "**/obj/**" --model gpt-4o

# Extract domain model analysis
code-tokenizer -d ./src/domain -o ./analysis/domain.md --include "*.{ts,cs,py}" --exclude "*.test.*"

# Analyze service boundaries
code-tokenizer -d ./src/services -o ./analysis/boundaries.md --include "*.{ts,cs,py}" --exclude "*.test.*,**/obj/**"

# Generate compatibility report
@"
# Microservices Analysis Report

## Service Interfaces
$(Get-Content ./analysis/interfaces.md)

## Domain Models
$(Get-Content ./analysis/domain.md)

## Service Boundaries
$(Get-Content ./analysis/boundaries.md)
"@ | Set-Content ./analysis/microservices-report.md
```

</details>
</details>

</details>

<details open style="list-style-type: none;">
<summary style="list-style-type: none; display: flex; align-items: center;"><h3 style="display: inline-block; margin: 0;">⚛️ Frontend Application Analysis</h3></summary>


> Perfect for evaluating component patterns and UI/UX implementation

<details open>

#### 🎯 When to Use
- Analyzing component library patterns and consistency
- Evaluating state management implementations
- Reviewing routing and navigation flows
- Assessing component composition patterns
- Validating UI/UX implementation standards

#### 💡 Value
- AI receives clean component code without test noise
- Enables pattern recognition across components
- Validates state management consistency
- Identifies potential performance issues
- Maintains UI/UX standard compliance

#### 🚀 Real Use
- AI generates component API documentation with examples
- AI identifies inconsistent component patterns
- AI suggests performance optimizations

#### 📚 Documentation
- [React Architecture](https://react.dev/learn/thinking-in-react)
- [Next.js Documentation](https://nextjs.org/docs)
- [State Management](https://redux.js.org/style-guide/style-guide)

<details>
<summary><h4 style="display: inline-block; margin: 0;">📟 Code Example</h4></summary>

```powershell
# Analyze component library
code-tokenizer -d ./src/components -o ./analysis/components.md --include "*.{tsx,jsx}" --exclude "*.test.*,*.stories.*" --model gpt-4o

# Analyze state management
code-tokenizer -d ./src/store -o ./analysis/state.md --include "*.{ts,js}"

# Review routing implementation
code-tokenizer -d ./src/pages -o ./analysis/routing.md --include "*.{tsx,jsx}"

# Generate frontend analysis report
@"
# Frontend Analysis Report

## Component Patterns
$(Get-Content ./analysis/components.md)

## State Management
$(Get-Content ./analysis/state.md)

## Routing Structure
$(Get-Content ./analysis/routing.md)
"@ | Set-Content ./analysis/frontend-report.md
```

</details>
</details>
</details>