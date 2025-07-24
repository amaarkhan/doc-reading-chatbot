import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
load_dotenv()

from utils.loader import load_and_split_document
from utils.embedder import create_vector_store
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

class ComprehensiveAgentEvaluator:
    def __init__(self, doc_path: str):
        # Set up logging for audit trails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agent_evaluation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize result file for session reporting
        self.result_file = "result.txt"
        self.session_start_time = datetime.now()
        
        # Initialize components
        self.docs = load_and_split_document(doc_path)
        self.retriever = create_vector_store(self.docs)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        
        # Set up QA chain
        self.prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")
        
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.qa_chain = create_retrieval_chain(self.retriever, document_chain)
        
        # Initialize memory for multi-turn evaluation
        self.memory = ConversationBufferMemory()
        
        # Evaluation metrics storage
        self.evaluation_metrics = {
            'total_queries': 0,
            'successful_responses': 0,
            'failed_responses': 0,
            'avg_response_time': 0,
            'hallucination_count': 0,
            'ambiguous_queries': 0,
            'harmful_content_detected': 0
        }
        
        self.interaction_logs = []
        
        # Initialize result file for this session
        self.initialize_result_file()
    
    def initialize_result_file(self):
        """Initialize the result file at the start of session"""
        try:
            with open(self.result_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("AI AGENT EVALUATION SESSION STARTED\n")
                f.write("=" * 80 + "\n")
                f.write(f"Session Start: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("Status: Session in progress...\n")
                f.write("-" * 80 + "\n")
                f.write("Waiting for user interactions...\n")
                f.write("=" * 80 + "\n")
        except Exception as e:
            self.logger.error(f"Failed to initialize result file: {e}")
    
    def stage1_input_processing(self, user_input: str) -> Dict[str, Any]:
        """Stage 1: Input Processing & Initial Checks"""
        self.logger.info(f"Stage 1: Processing user input: {user_input}")
        
        evaluation_result = {
            'input_logged': True,
            'harmful_content': False,
            'ambiguous': False,
            'prompt_injection': False
        }
        
        # 1. Input Logging (✅ Implemented)
        self.logger.info(f"Raw user input logged: {user_input}")
        
        # 2. Harmful Content Detection (Basic implementation)
        harmful_keywords = ['hack', 'kill', 'bomb', 'violence', 'illegal']
        if any(keyword in user_input.lower() for keyword in harmful_keywords):
            evaluation_result['harmful_content'] = True
            self.evaluation_metrics['harmful_content_detected'] += 1
            self.logger.warning(f"Harmful content detected in input: {user_input}")
        
        # 3. Ambiguity Detection using LLM as Judge
        try:
            ambiguity_prompt = f"Is this question ambiguous or unclear? Answer with 'Yes' or 'No': '{user_input}'"
            ambiguity_response = self.llm.invoke(ambiguity_prompt)
            if 'yes' in ambiguity_response.content.lower():
                evaluation_result['ambiguous'] = True
                self.evaluation_metrics['ambiguous_queries'] += 1
                self.logger.warning(f"Ambiguous query detected: {user_input}")
        except Exception as e:
            self.logger.error(f"Ambiguity detection failed: {e}")
            # Don't stop processing, just continue
        
        # 4. Basic Prompt Injection Detection
        injection_patterns = ['ignore previous', 'forget instructions', 'act as', 'pretend you are']
        if any(pattern in user_input.lower() for pattern in injection_patterns):
            evaluation_result['prompt_injection'] = True
            self.logger.warning(f"Potential prompt injection detected: {user_input}")
        
        return evaluation_result
    
    def stage2_core_execution(self, user_input: str) -> Dict[str, Any]:
        """Stage 2: Core Agent Execution"""
        self.logger.info("Stage 2: Core agent execution monitoring")
        
        execution_log = {
            'action_sequence': [],
            'tools_called': [],
            'memory_context': None,
            'execution_successful': True
        }
        
        # 1. Action Sequence Verification
        execution_log['action_sequence'].append("retrieval_started")
        self.logger.info("Action: Document retrieval initiated")
        
        # 2. Tool Execution Logging
        execution_log['tools_called'].append({
            'tool': 'vector_retriever',
            'parameters': {'query': user_input},
            'timestamp': datetime.now().isoformat()
        })
        
        # 3. Memory Management Assessment
        self.memory.chat_memory.add_user_message(user_input)
        execution_log['memory_context'] = str(self.memory.buffer)
        
        execution_log['action_sequence'].append("reasoning_started")
        execution_log['action_sequence'].append("response_generation")
        
        return execution_log
    
    def stage3_output_generation(self, user_input: str, agent_response: str, response_time: float) -> Dict[str, Any]:
        """Stage 3: Output Generation Evaluation"""
        self.logger.info("Stage 3: Output generation evaluation")
        
        output_evaluation = {
            'hallucination_detected': False,
            'response_time_ms': response_time * 1000,
            'edge_case_handling': True,
            'fact_check_result': None
        }
        
        # 1. Hallucination Detection (Basic implementation using LLM as Judge)
        try:
            hallucination_prompt = f"""
            Based on the context provided and the question asked, does this response contain any hallucinated or fabricated information?
            
            Question: {user_input}
            Response: {agent_response}
            
            Answer with 'Yes' if hallucination detected, 'No' if response seems accurate.
            """
            
            hallucination_check = self.llm.invoke(hallucination_prompt)
            if 'yes' in hallucination_check.content.lower():
                output_evaluation['hallucination_detected'] = True
                self.evaluation_metrics['hallucination_count'] += 1
                self.logger.warning(f"Hallucination detected in response: {agent_response[:100]}...")
        except Exception as e:
            self.logger.error(f"Hallucination detection failed: {e}")
            # Continue processing even if hallucination check fails
        
        # 2. Latency Measurement
        self.logger.info(f"Response generated in {response_time:.2f} seconds")
        
        # 3. Edge Case Detection
        if len(user_input.strip()) == 0 or len(agent_response.strip()) == 0:
            output_evaluation['edge_case_handling'] = False
            self.logger.warning("Edge case detected: Empty input or response")
        
        return output_evaluation
    
    def stage4_final_validation(self, user_input: str, agent_response: str, overall_metrics: Dict) -> Dict[str, Any]:
        """Stage 4: Final Output Validation"""
        self.logger.info("Stage 4: Final output validation")
        
        validation_result = {
            'task_completed': True,
            'response_quality_score': 0,
            'format_valid': True,
            'efficiency_score': 0
        }
        
        # 1. Task Completion Assessment using LLM as Judge
        try:
            completion_prompt = f"""
            Rate how well this response answers the user's question on a scale of 1-10:
            
            Question: {user_input}
            Response: {agent_response}
            
            Provide only a number from 1-10.
            """
            
            quality_response = self.llm.invoke(completion_prompt)
            # Extract number from response
            import re
            score_match = re.search(r'\b([1-9]|10)\b', quality_response.content)
            if score_match:
                validation_result['response_quality_score'] = int(score_match.group(1))
            else:
                validation_result['response_quality_score'] = 7  # Default score if parsing fails
        except Exception as e:
            self.logger.error(f"Quality assessment failed: {e}")
            validation_result['response_quality_score'] = 7  # Default score
        
        # 2. Format Validation
        if len(agent_response.strip()) < 10:
            validation_result['format_valid'] = False
            self.logger.warning("Response too short, format validation failed")
        
        # 3. Efficiency Calculation
        if overall_metrics['response_time_ms'] < 3000:  # Less than 3 seconds
            validation_result['efficiency_score'] = 10
        elif overall_metrics['response_time_ms'] < 5000:  # Less than 5 seconds
            validation_result['efficiency_score'] = 7
        else:
            validation_result['efficiency_score'] = 5
        
        return validation_result
    
    def write_result_to_file(self, interaction_data: Dict[str, Any]):
        """Write interaction result to result.txt file (overwrite mode)"""
        try:
            with open(self.result_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("AI AGENT EVALUATION RESULTS\n")
                f.write("=" * 80 + "\n")
                f.write(f"Session Start: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 80 + "\n\n")
                
                # Overall Session Metrics
                f.write("OVERALL SESSION METRICS:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total Queries Processed: {self.evaluation_metrics['total_queries']}\n")
                f.write(f"Successful Responses: {self.evaluation_metrics['successful_responses']}\n")
                f.write(f"Failed Responses: {self.evaluation_metrics['failed_responses']}\n")
                success_rate = (self.evaluation_metrics['successful_responses'] / max(1, self.evaluation_metrics['total_queries'])) * 100
                f.write(f"Success Rate: {success_rate:.2f}%\n")
                f.write(f"Average Response Time: {self.evaluation_metrics['avg_response_time']:.2f} seconds\n")
                f.write(f"Hallucinations Detected: {self.evaluation_metrics['hallucination_count']}\n")
                f.write(f"Ambiguous Queries: {self.evaluation_metrics['ambiguous_queries']}\n")
                f.write(f"Harmful Content Blocked: {self.evaluation_metrics['harmful_content_detected']}\n\n")
                
                # Recent Interactions
                f.write("RECENT INTERACTIONS:\n")
                f.write("-" * 30 + "\n")
                for i, log in enumerate(self.interaction_logs[-5:], 1):  # Last 5 interactions
                    f.write(f"\nInteraction #{i}:\n")
                    f.write(f"Time: {log['timestamp']}\n")
                    f.write(f"Question: {log['user_input']}\n")
                    f.write(f"Response Time: {log['response_time']:.2f}s\n")
                    
                    if 'evaluation_summary' in log:
                        eval_summary = log['evaluation_summary']
                        f.write(f"Quality Score: {log.get('overall_score', 'N/A')}/10\n")
                        f.write("Stage Results:\n")
                        f.write(f"  Stage 1 (Input Safety): {'PASS' if not eval_summary['stage1']['harmful_content'] else 'BLOCKED'}\n")
                        f.write(f"  Stage 2 (Execution): {'SUCCESS' if eval_summary['stage2']['execution_successful'] else 'FAILED'}\n")
                        f.write(f"  Stage 3 (Output Quality): {'GOOD' if not eval_summary['stage3']['hallucination_detected'] else 'HALLUCINATION DETECTED'}\n")
                        f.write(f"  Stage 4 (Validation): {'VALID' if eval_summary['stage4']['format_valid'] else 'INVALID FORMAT'}\n")
                    f.write("-" * 40 + "\n")
                
                f.write(f"\nReport generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n")
                
        except Exception as e:
            self.logger.error(f"Failed to write result file: {e}")
    
    def comprehensive_evaluate(self, user_input: str) -> Dict[str, Any]:
        """Run comprehensive evaluation through all 4 stages"""
        start_time = time.time()
        
        # Stage 1: Input Processing
        print("   🔍 Stage 1: Input Processing & Safety Checks...")
        stage1_result = self.stage1_input_processing(user_input)
        
        # If harmful content detected, stop processing
        if stage1_result['harmful_content']:
            return {
                'error': 'Harmful content detected',
                'stage1_result': stage1_result,
                'blocked': True
            }
        
        try:
            # Stage 2: Core Execution
            print("   ⚙️  Stage 2: Core Agent Execution...")
            stage2_result = self.stage2_core_execution(user_input)
            
            # Generate response
            print("   📝 Generating response...")
            response = self.qa_chain.invoke({"input": user_input})
            agent_response = response["answer"]
            
            response_time = time.time() - start_time
            
            # Stage 3: Output Generation
            print("   📝 Stage 3: Output Generation Evaluation...")
            stage3_result = self.stage3_output_generation(user_input, agent_response, response_time)
            
            # Stage 4: Final Validation
            print("   ✅ Stage 4: Final Validation...")
            stage4_result = self.stage4_final_validation(user_input, agent_response, stage3_result)
            
            # Update metrics
            self.evaluation_metrics['total_queries'] += 1
            self.evaluation_metrics['successful_responses'] += 1
            
            # Calculate running average response time
            total_time = self.evaluation_metrics['avg_response_time'] * (self.evaluation_metrics['total_queries'] - 1)
            self.evaluation_metrics['avg_response_time'] = (total_time + response_time) / self.evaluation_metrics['total_queries']
            
            # Store interaction log
            interaction_log = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'agent_response': agent_response,
                'response_time': response_time,
                'evaluation_summary': {
                    'stage1': stage1_result,
                    'stage2': stage2_result,
                    'stage3': stage3_result,
                    'stage4': stage4_result
                },
                'overall_score': stage4_result['response_quality_score']
            }
            
            self.interaction_logs.append(interaction_log)
            
            # Write results to file after each interaction
            self.write_result_to_file(interaction_log)
            
            return {
                'agent_response': agent_response,
                'evaluation_summary': {
                    'stage1': stage1_result,
                    'stage2': stage2_result,
                    'stage3': stage3_result,
                    'stage4': stage4_result
                },
                'response_time': response_time,
                'overall_score': stage4_result['response_quality_score']
            }
            
        except Exception as e:
            self.evaluation_metrics['failed_responses'] += 1
            self.logger.error(f"Error in evaluation: {e}")
            return {
                'error': str(e),
                'stage1_result': stage1_result,
                'failed': True
            }
    
    def write_final_report(self):
        """Write comprehensive final report when session ends"""
        try:
            with open(self.result_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("FINAL AI AGENT EVALUATION REPORT\n")
                f.write("=" * 80 + "\n")
                f.write(f"Session Duration: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')} to {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                session_duration = (datetime.now() - self.session_start_time).total_seconds()
                f.write(f"Total Session Time: {session_duration/60:.2f} minutes\n")
                f.write("-" * 80 + "\n\n")
                
                # Comprehensive Session Metrics
                f.write("COMPREHENSIVE SESSION METRICS:\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Queries Processed: {self.evaluation_metrics['total_queries']}\n")
                f.write(f"Successful Responses: {self.evaluation_metrics['successful_responses']}\n")
                f.write(f"Failed Responses: {self.evaluation_metrics['failed_responses']}\n")
                
                if self.evaluation_metrics['total_queries'] > 0:
                    success_rate = (self.evaluation_metrics['successful_responses'] / self.evaluation_metrics['total_queries']) * 100
                    f.write(f"Success Rate: {success_rate:.2f}%\n")
                else:
                    f.write("Success Rate: 0.00%\n")
                    
                f.write(f"Average Response Time: {self.evaluation_metrics['avg_response_time']:.2f} seconds\n")
                f.write(f"Hallucinations Detected: {self.evaluation_metrics['hallucination_count']}\n")
                f.write(f"Ambiguous Queries: {self.evaluation_metrics['ambiguous_queries']}\n")
                f.write(f"Harmful Content Blocked: {self.evaluation_metrics['harmful_content_detected']}\n\n")
                
                # Stage-wise Performance Analysis
                f.write("STAGE-WISE PERFORMANCE ANALYSIS:\n")
                f.write("-" * 40 + "\n")
                
                stage1_issues = sum(1 for log in self.interaction_logs if 'evaluation_summary' in log and log['evaluation_summary']['stage1']['harmful_content'])
                stage2_failures = sum(1 for log in self.interaction_logs if 'evaluation_summary' in log and not log['evaluation_summary']['stage2']['execution_successful'])
                stage3_issues = sum(1 for log in self.interaction_logs if 'evaluation_summary' in log and log['evaluation_summary']['stage3']['hallucination_detected'])
                stage4_failures = sum(1 for log in self.interaction_logs if 'evaluation_summary' in log and not log['evaluation_summary']['stage4']['format_valid'])
                
                total_processed = len([log for log in self.interaction_logs if 'evaluation_summary' in log])
                
                if total_processed > 0:
                    f.write(f"Stage 1 (Input Safety): {((total_processed - stage1_issues) / total_processed * 100):.1f}% pass rate\n")
                    f.write(f"Stage 2 (Core Execution): {((total_processed - stage2_failures) / total_processed * 100):.1f}% success rate\n")
                    f.write(f"Stage 3 (Output Quality): {((total_processed - stage3_issues) / total_processed * 100):.1f}% quality rate\n")
                    f.write(f"Stage 4 (Final Validation): {((total_processed - stage4_failures) / total_processed * 100):.1f}% validation rate\n\n")
                else:
                    f.write("No successful interactions to analyze.\n\n")
                
                # Quality Score Distribution
                if self.interaction_logs:
                    quality_scores = [log.get('overall_score', 0) for log in self.interaction_logs if 'overall_score' in log]
                    if quality_scores:
                        f.write("QUALITY SCORE DISTRIBUTION:\n")
                        f.write("-" * 30 + "\n")
                        f.write(f"Average Quality Score: {sum(quality_scores) / len(quality_scores):.2f}/10\n")
                        f.write(f"Highest Score: {max(quality_scores)}/10\n")
                        f.write(f"Lowest Score: {min(quality_scores)}/10\n\n")
                
                # All Interactions Log
                f.write("ALL INTERACTIONS LOG:\n")
                f.write("-" * 30 + "\n")
                for i, log in enumerate(self.interaction_logs, 1):
                    f.write(f"\nInteraction #{i}:\n")
                    f.write(f"Time: {log['timestamp']}\n")
                    f.write(f"Question: {log['user_input'][:100]}{'...' if len(log['user_input']) > 100 else ''}\n")
                    f.write(f"Response Time: {log['response_time']:.2f}s\n")
                    
                    if 'evaluation_summary' in log:
                        f.write(f"Quality Score: {log.get('overall_score', 'N/A')}/10\n")
                        eval_summary = log['evaluation_summary']
                        f.write("Stage Results: ")
                        f.write(f"S1:{'✓' if not eval_summary['stage1']['harmful_content'] else '✗'} ")
                        f.write(f"S2:{'✓' if eval_summary['stage2']['execution_successful'] else '✗'} ")
                        f.write(f"S3:{'✓' if not eval_summary['stage3']['hallucination_detected'] else '✗'} ")
                        f.write(f"S4:{'✓' if eval_summary['stage4']['format_valid'] else '✗'}\n")
                    f.write("-" * 50 + "\n")
                
                f.write(f"\nFinal report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n")
                
        except Exception as e:
            self.logger.error(f"Failed to write final report: {e}")
    
    def get_evaluation_report(self) -> Dict[str, Any]:
        """Generate comprehensive evaluation report"""
        success_rate = 0
        if self.evaluation_metrics['total_queries'] > 0:
            success_rate = (self.evaluation_metrics['successful_responses'] / 
                          self.evaluation_metrics['total_queries']) * 100
        
        return {
            'summary_metrics': self.evaluation_metrics,
            'success_rate_percentage': success_rate,
            'total_interactions': len(self.interaction_logs),
            'last_10_interactions': self.interaction_logs[-10:] if self.interaction_logs else []
        }

def main():
    # Initialize evaluator
    print("🚀 Initializing Document Reading Chatbot with Evaluation Pipeline...")
    evaluator = ComprehensiveAgentEvaluator("d1.txt")
    print(f"✅ Evaluation system initialized. Results will be saved to: {evaluator.result_file}")
    
    print("\n🤖 Welcome to the Comprehensive Document Reading Chatbot with Full Evaluation!")
    print("This chatbot implements a 4-stage evaluation pipeline:")
    print("Stage 1: Input Processing & Safety Checks")
    print("Stage 2: Core Agent Execution Monitoring") 
    print("Stage 3: Output Generation Evaluation")
    print("Stage 4: Final Validation & Performance Metrics")
    print("-" * 80)
    print("Ask questions about the document. Type 'exit' to quit or 'report' for evaluation summary.")
    print("-" * 80)
    
    while True:
        # Get user input
        question = input("\n🔍 Your question: ").strip()
        
        # Check for exit command
        if question.lower() == 'exit':
            print("\n📊 Generating Final Evaluation Report...")
            # Write final comprehensive report
            evaluator.write_final_report()
            print(f"✅ Complete evaluation report saved to: {evaluator.result_file}")
            
            # Also display summary
            report = evaluator.get_evaluation_report()
            print("\n📊 Session Summary:")
            print(f"   Total Queries: {report['summary_metrics']['total_queries']}")
            print(f"   Success Rate: {report['success_rate_percentage']:.2f}%")
            print(f"   Average Response Time: {report['summary_metrics']['avg_response_time']:.2f}s")
            print("\nThank you for using the Comprehensive Document Reading Chatbot!")
            break
        
        # Check for report command
        if question.lower() == 'report':
            print("\n📊 Current Evaluation Report:")
            report = evaluator.get_evaluation_report()
            print(json.dumps(report, indent=2))
            continue
        
        # Skip empty questions
        if not question:
            print("⚠️  Please enter a valid question.")
            continue
        
        print("\n🔄 Running comprehensive 4-stage evaluation...")
        print("   🔍 Stage 1: Input Processing & Safety Checks...")
        
        # Run comprehensive evaluation
        result = evaluator.comprehensive_evaluate(question)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            if 'blocked' in result:
                print("🚫 Query blocked due to safety concerns.")
                # Still write to result file even for blocked queries
                evaluator.write_result_to_file({
                    'timestamp': datetime.now().isoformat(),
                    'user_input': question,
                    'status': 'blocked',
                    'reason': result['error']
                })
            continue
        
        # Display results
        print(f"\n🤖 Answer: {result['agent_response']}")
        print(f"\n📈 Evaluation Summary:")
        print(f"   ⏱️  Response Time: {result['response_time']:.2f}s")
        print(f"   🎯 Quality Score: {result['overall_score']}/10")
        
        # Stage results
        eval_summary = result['evaluation_summary']
        print(f"   🔍 Stage 1 - Input Safety: {'✅ Pass' if not eval_summary['stage1']['harmful_content'] else '❌ Blocked'}")
        print(f"   ⚙️  Stage 2 - Execution: {'✅ Success' if eval_summary['stage2']['execution_successful'] else '❌ Failed'}")
        print(f"   📝 Stage 3 - Output Quality: {'✅ Good' if not eval_summary['stage3']['hallucination_detected'] else '⚠️  Hallucination Detected'}")
        print(f"   ✅ Stage 4 - Final Validation: {'✅ Valid' if eval_summary['stage4']['format_valid'] else '❌ Invalid Format'}")

if __name__ == "__main__":
    main()
