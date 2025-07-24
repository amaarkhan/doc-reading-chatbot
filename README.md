# 🤖 Document Reading Chatbot with AI Agent Evaluation Pipeline

Welcome to a comprehensive implementation of an AI Agent that follows a complete **4-Stage Evaluation Pipeline**! This chatbot doesn't just answer questions - it evaluates itself at every step to ensure quality, safety, and performance.

## 🚀 **Quic```bash
$ python main.py

🤖 Welcome to the Comprehensive Document Reading Chatbot!
Ask questions about the document. Type 'exit' to quit or 'report' for metrics.

🔍 Your question: What is machine learning?

🔄 Running comprehensive 4-stage evaluation...
   🔍 Stage 1: Input Processing & Safety Checks...
   ⚙️  Stage 2: Core Agent Execution...
   📝 Stage 3: Output Generation & Quality...
   ✅ Stage 4: Final Validation...

🤖 Answer: Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed...

📈 Evaluation Summary:
   ⏱️  Response Time: 2.34s
   🎯 Quality Score: 9/10
   🔍 Stage 1 - Input Safety: ✅ Pass
   ⚙️  Stage 2 - Execution: ✅ Success
   📝 Stage 3 - Output Quality: ✅ Good
   ✅ Stage 4 - Final Validation: ✅ Valid

🔍 Your question: report
📊 Current Session Report:
   📈 Total Queries: 1
   ✅ Success Rate: 100.0%
   ⏱️  Avg Response Time: 2.34s
   🛡️  Safety Blocks: 0
   🎯 Avg Quality Score: 9.0/10

🔍 Your question: exit

📊 Final Evaluation Report:
=========================
Total Interactions: 1
Success Rate: 100.0%
Average Response Time: 2.34 seconds
Quality Score Average: 9.0/10
Harmful Content Detected: 0
Ambiguous Queries: 0
Hallucinations Detected: 0

Detailed results saved to: result.txt
Thank you for using the Comprehensive Document Reading Chatbot!
```

### **Generated Files:**

#### `result.txt` (Session Report):
```json
{
    "session_summary": {
        "timestamp": "2025-07-24T15:30:45",
        "total_queries": 1,
        "successful_responses": 1,
        "success_rate": 100.0,
        "avg_response_time": 2.34,
        "quality_scores": [9],
        "avg_quality_score": 9.0,
        "safety_metrics": {
            "harmful_content_detected": 0,
            "ambiguous_queries": 0,
            "prompt_injections": 0,
            "hallucination_count": 0
        }
    },
    "interactions": [
        {
            "timestamp": "2025-07-24T15:30:45",
            "user_input": "What is machine learning?",
            "agent_response": "Machine learning is a subset of artificial intelligence...",
            "response_time": 2.34,
            "overall_score": 9,
            "evaluation_summary": {
                "stage1": {
                    "input_logged": true,
                    "harmful_content": false,
                    "ambiguous": false,
                    "prompt_injection": false
                },
                "stage2": {
                    "execution_successful": true,
                    "tools_used": {"retriever": true, "llm": true},
                    "action_sequence_correct": true,
                    "execution_time": 1.2
                },
                "stage3": {
                    "hallucination_detected": false,
                    "edge_case": false,
                    "latency_acceptable": true,
                    "generation_time": 0.8
                },
                "stage4": {
                    "task_completion_score": 9,
                    "efficiency_score": 8.5,
                    "format_valid": true,
                    "validation_time": 0.34
                }
            }
        }
    ]
}
```

---

## 🚀 **Getting Started Steps**

### 1. **Environment Setup**
```bash
# Clone or download the project
git clone <repository-url>
cd doc-reading-chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 2. **Run the System**
```bash
python main.py
```

### 3. **Test Evaluation Pipeline**
Try these sample questions to see all evaluation stages in action:
- Normal question: "What is artificial intelligence?"
- Edge case: "What is {}"
- Ambiguous: "Tell me about it"
- Testing memory: Ask follow-up questions

---

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **Missing API Key**: Ensure `.env` file contains valid `GOOGLE_API_KEY`
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Document Not Found**: Ensure `d1.txt` exists in the project directory
4. **Evaluation Stages Failing**: Check logs in `agent_evaluation.log`

### **Performance Optimization:**
- Monitor `result.txt` for response times >3s
- Check `agent_evaluation.log` for detailed debugging
- Use `report` command during sessions for real-time metrics

---

## 🎓 **Educational Value**

This project demonstrates:
- **Complete AI Agent Evaluation Pipeline** implementation
- **Industry-standard evaluation methods** (LLM as Judge, etc.)
- **Production-ready logging and monitoring**
- **Safety and security considerations** for AI systems
- **Performance optimization** and efficiency tracking
- **Comprehensive documentation** and user experience

---

## 🛠️ **Future Extensions**

The architecture is designed for easy integration with:
- **Phoenix Evaluator**: Visual tracing and debugging
- **LangSmith**: Advanced evaluation metrics  
- **Azure AI Evaluation**: Batch processing capabilities
- **Custom Evaluators**: Easy to add new evaluation criteria
- **Multiple Document Sources**: Extend beyond single document
- **API Integration**: RESTful API for enterprise deployment

This is a **production-ready implementation** that provides transparency, safety, and continuous improvement for AI agent interactions!Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment**:
   - Create a `.env` file with your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

3. **Run the Chatbot**:
   ```bash
   python main.py
   ```

4. **Start Asking Questions**:
   - Ask anything about the document (`d1.txt`)
   - Type `exit` to quit and see complete evaluation report
   - Type `report` to see current session metrics
   - Each session generates/overwrites `result.txt` with detailed evaluation data

---

## 📋 **Complete AI Agent Evaluation Pipeline**

This implementation follows the industry-standard **4-Stage Evaluation Pipeline** with comprehensive monitoring at each step:

### 🔍 **Stage 1: Input Processing & Initial Checks**

**Purpose**: Validate and secure user inputs before processing

**Evaluation Criteria**:
- ✅ **Input Logging & Preprocessing**: Log raw user input for audit trails
- ✅ **Harmful Content Detection**: Check for dangerous or inappropriate requests  
- ✅ **Ambiguity Detection**: Identify unclear or confusing questions
- ✅ **Prompt Injection Protection**: Detect attempts to manipulate the AI

**Implementation**:
```python
Function: stage1_input_processing(user_input)
Location: comprehensive_evaluation.py (lines 85-125)
Methods Used:
- Verbose logging for audit trails
- Keyword-based harmful content filtering
- LLM as Judge for ambiguity detection ("Is this prompt ambiguous?")
- Pattern matching for prompt injection detection
```

**Code Snippet**:
```python
# Harmful Content Detection
harmful_keywords = ['hack', 'kill', 'bomb', 'violence', 'illegal']
if any(keyword in user_input.lower() for keyword in harmful_keywords):
    evaluation_result['harmful_content'] = True

# Ambiguity Detection using LLM as Judge
ambiguity_prompt = f"Is this question ambiguous or unclear? Answer with 'Yes' or 'No': '{user_input}'"
ambiguity_response = self.llm.invoke(ambiguity_prompt)
```

---

### ⚙️ **Stage 2: Core Agent Execution**

**Purpose**: Monitor internal agent reasoning and component execution

**Evaluation Criteria**:
- ✅ **Action Sequence Verification**: Ensure correct order (retrieval → reasoning → response)
- ✅ **Tool Execution Logging**: Document all tools called with parameters and outputs
- ✅ **Memory Management Assessment**: Test context retention across conversations

**Implementation**:
```python
Function: stage2_core_execution(user_input)
Location: comprehensive_evaluation.py (lines 126-156)
Methods Used:
- Step-by-step execution logging
- Tool usage documentation (retriever, LLM calls)
- ConversationBufferMemory for context tracking
- Timing measurement for each component
```

**Code Snippet**:
```python
# Action Sequence Verification
self.logger.info("Step 1: Document retrieval initiated")
retrieval_start = time.time()
# ... retrieval process
self.logger.info(f"Step 1 completed in {retrieval_time:.2f}s")

# Tool Execution Logging
evaluation_result['tools_used'] = {
    'retriever': True,
    'llm': True,
    'memory': self.memory.buffer if hasattr(self, 'memory') else None
}
```

---

### 📝 **Stage 3: Output Generation**

**Purpose**: Validate response quality and detect issues before delivery

**Evaluation Criteria**:
- ✅ **Hallucination Detection**: Compare output to ground truth and detect fabricated info
- ✅ **Edge Case Performance**: Test with unusual/malformed inputs
- ✅ **Latency Measurement**: Record processing time for optimization

**Implementation**:
```python
Function: stage3_output_generation(user_input, agent_response, response_time)
Location: comprehensive_evaluation.py (lines 157-197)
Methods Used:
- LLM as Judge for hallucination detection
- Response time tracking
- Edge case pattern recognition
- Real-time quality validation
```

**Code Snippet**:
```python
# Hallucination Detection using LLM as Judge
hallucination_prompt = f"""
Analyze this response for potential hallucinations or fabricated information:
Question: {user_input}
Response: {agent_response}
Does the response contain any fabricated or unverifiable claims? Answer 'Yes' or 'No':
"""
hallucination_check = self.llm.invoke(hallucination_prompt)

# Edge Case Detection
edge_case_patterns = ['\\n\\n', '{}', '[]', 'null', 'undefined']
is_edge_case = any(pattern in user_input for pattern in edge_case_patterns)
```

---

### ✅ **Stage 4: Final Output Validation**

**Purpose**: Measure overall performance and generate quality metrics

**Evaluation Criteria**:
- ✅ **Task Completion Rate**: Assess how well the agent solved the task (1-10 scoring)
- ✅ **Efficiency Metrics**: Track response time, resource usage, and costs
- ✅ **Automated Format Checks**: Validate output structure and formatting

**Implementation**:
```python
Function: stage4_final_validation(user_input, agent_response, overall_metrics)
Location: comprehensive_evaluation.py (lines 198-246)
Methods Used:
- LLM scoring system (1-10 scale) for task completion
- Performance efficiency calculations
- JSON schema validation for output formatting
- Comprehensive metric aggregation
```

**Code Snippet**:
```python
# Task Completion Rate using LLM as Judge
scoring_prompt = f"""
Rate how well this response answers the question on a scale of 1-10:
Question: {user_input}
Response: {agent_response}
Provide only the number (1-10):
"""
score_response = self.llm.invoke(scoring_prompt)

# Efficiency Metrics
response_time_ms = overall_metrics.get('response_time', 0) * 1000
efficiency_score = 10 if response_time_ms < 2000 else max(1, 10 - (response_time_ms / 1000))
```

---

## 🏗️ **Code Architecture & Implementation**

### **Core Files:**

#### 1. `main.py` - Application Entry Point
```python
# Simple entry point that starts the comprehensive evaluation system
from comprehensive_evaluation import main
if __name__ == "__main__":
    main()
```

#### 2. `comprehensive_evaluation.py` - The Complete Evaluation System
**Class: `ComprehensiveAgentEvaluator`**

| Function | Lines | Purpose | Stage |
|----------|-------|---------|-------|
| `__init__()` | 17-83 | Initialize system, load documents, setup logging | Setup |
| `stage1_input_processing()` | 85-125 | Input validation, safety checks, ambiguity detection | Stage 1 |
| `stage2_core_execution()` | 126-156 | Monitor agent execution, tool logging, memory tracking | Stage 2 |
| `stage3_output_generation()` | 157-197 | Hallucination detection, latency measurement, quality checks | Stage 3 |
| `stage4_final_validation()` | 198-246 | Task completion scoring, efficiency metrics, format validation | Stage 4 |
| `write_result_to_file()` | 247-260 | Write detailed evaluation results to result.txt | Reporting |
| `comprehensive_evaluate()` | 296-370 | Main orchestration - runs all 4 stages sequentially | Main Flow |
| `get_evaluation_report()` | 465-478 | Generate session summary and final metrics | Reporting |
| `main()` | 479-561 | Interactive chat loop with continuous evaluation | User Interface |

#### 3. `utils/loader.py` - Document Processing
```python
Function: load_and_split_document(file_path)
Purpose: Loads and chunks documents for RAG processing
Used in: Stage 2 for document retrieval and tool execution logging
```

#### 4. `utils/embedder.py` - Vector Database Creation
```python
Function: create_vector_store(documents)
Purpose: Creates FAISS vector embeddings for semantic search
Used in: Stage 2 for retrieval tool execution and memory management
```

### **Support Files:**
- `d1.txt` - Sample document for testing (knowledge base)
- `requirements.txt` - Python dependencies (langchain, google-generativeai, etc.)
- `.env` - Environment variables (GOOGLE_API_KEY)
- `agent_evaluation.log` - Auto-generated detailed audit logs
- `result.txt` - Session evaluation results (overwritten each run)
- **Line 207-250**: Stage 4 implementation (`stage4_final_validation`)
- **Line 252-320**: Main orchestration (`comprehensive_evaluate`)
- **Line 322-340**: Reporting (`get_evaluation_report`)

#### 3. `utils/loader.py` - Document Processing
```python
Function: load_and_split_document(file_path)
Purpose: Loads and chunks documents for processing
Used in: Stage 2 for document retrieval
```

#### 4. `utils/embedder.py` - Vector Database
```python
Function: create_vector_store(documents)
Purpose: Creates embeddings for semantic search
Used in: Stage 2 for tool execution logging
```

### **Support Files:**
- `d1.txt` - Sample document for testing
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys)
- `agent_evaluation.log` - Auto-generated audit logs

---

## 📊 **Evaluation Metrics Dashboard**

The system tracks comprehensive metrics in real-time:

| Metric | Description | Implementation |
|--------|-------------|----------------|
| **Total Queries** | Number of questions processed | `evaluation_metrics['total_queries']` |
| **Success Rate** | Percentage of successful responses | Calculated in `get_evaluation_report()` |
| **Response Time** | Average time per response | `evaluation_metrics['avg_response_time']` |
| **Hallucination Count** | Detected false information | `evaluation_metrics['hallucination_count']` |
| **Safety Blocks** | Harmful content filtered | `evaluation_metrics['harmful_content_detected']` |
| **Quality Scores** | LLM-assessed answer quality (1-10) | Stage 4 validation results |

---

## 🔧 **Advanced Features**

### **LLM as a Judge Implementation**
Multiple evaluation checkpoints use AI to assess AI:
- **Ambiguity Detection**: "Is this prompt ambiguous?"
- **Hallucination Check**: "Does this response contain fabricated information?"
- **Quality Scoring**: "Rate this answer from 1-10"

### **Memory Management Testing**
- Uses `ConversationBufferMemory` to maintain context
- Tests multi-turn conversation handling
- Validates context retention across interactions

### **Comprehensive Logging**
- All interactions logged to `agent_evaluation.log`
- Timestamps for audit trails
- Structured JSON logging for analysis

---

## 🎯 **Compliance with Evaluation Standards**

This implementation follows industry-standard evaluation practices:

✅ **OpenAI Moderation API** compatible (harmful content detection)  
✅ **LangChain Tracer** ready (verbose logging enabled)  
✅ **LangSmith** integration prepared  
✅ **Phoenix Evaluator** compatible architecture  
✅ **Azure AI Evaluation** ready for batch processing  

---

## � **Example Usage**

```bash
$ python main.py

🤖 Welcome to the Comprehensive Document Reading Chatbot!
Ask questions about the document. Type 'exit' to quit or 'report' for metrics.

🔍 Your question: What is machine learning?

🔄 Running comprehensive 4-stage evaluation...

🤖 Answer: Machine learning is a subset of artificial intelligence...

📈 Evaluation Summary:
   ⏱️  Response Time: 2.34s
   🎯 Quality Score: 9/10
   🔍 Stage 1 - Input Safety: ✅ Pass
   ⚙️  Stage 2 - Execution: ✅ Success
   📝 Stage 3 - Output Quality: ✅ Good
   ✅ Stage 4 - Final Validation: ✅ Valid
```

---

## � **Future Extensions**

The architecture is designed for easy integration with:
- **Phoenix Evaluator**: Visual tracing and debugging
- **LangSmith**: Advanced evaluation metrics
- **Azure AI Evaluation**: Batch processing capabilities
- **Custom Evaluators**: Easy to add new evaluation criteria

This is a **production-ready implementation** that provides transparency, safety, and continuous improvement for AI agent interactions!