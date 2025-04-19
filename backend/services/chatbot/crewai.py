from crewai import Agent, Task, Crew
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import ElasticsearchStore
import requests

def process_query(text: str, model: str) -> str:
    """
    Process chatbot query using CrewAI agents.
    """
    try:
        # Initialize LangChain for RAG
        embeddings = SentenceTransformerEmbeddings(model_name="distilbert-base-nli-mean-tokens")
        vector_store = ElasticsearchStore(
            index_name="knowledge",
            embedding=embeddings,
            es_url="http://localhost:9200"
        )

        # Define agents
        manager_agent = Agent(
            role="Manager",
            goal="Coordinate query processing and model selection",
            backstory="Experienced in managing AI workflows"
        )
        knowledge_agent = Agent(
            role="Knowledge",
            goal="Retrieve relevant information from knowledge base",
            backstory="Expert in information retrieval"
        )
        execution_agent = Agent(
            role="Execution",
            goal="Execute commands via APIs",
            backstory="Skilled in API integration"
        )
        learning_agent = Agent(
            role="Learning",
            goal="Update knowledge base with new information",
            backstory="Continuous learner"
        )

        # Define tasks
        knowledge_task = Task(
            description=f"Retrieve information for query: {text}",
            agent=knowledge_agent,
            tools=[vector_store.as_retriever()]
        )
        execution_task = Task(
            description=f"Execute command for query: {text}",
            agent=execution_agent
        )
        learning_task = Task(
            description="Update knowledge base with query results",
            agent=learning_agent
        )

        # Create crew
        crew = Crew(
            agents=[manager_agent, knowledge_agent, execution_agent, learning_agent],
            tasks=[knowledge_task, execution_task, learning_task],
            verbose=True
        )

        # Select model
        if model == "MiniCPM":
            response = requests.post("http://localhost:8001/inference", json={"text": text})
            result = response.json().get("response", "No response")
        elif model == "Grok":
            response = requests.post("https://api.x.ai/grok", json={"query": text})
            result = response.json().get("response", "No response")
        elif model == "DeepSeek":
            response = requests.post("https://api.deepseek.com", json={"query": text})
            result = response.json().get("response", "No response")
        elif model == "OpenAI":
            response = requests.post("https://api.openai.com/v1/completions", json={"prompt": text})
            result = response.json().get("choices", [{}])[0].get("text", "No response")
        else:
            result = "Invalid model"

        # Run crew
        crew_output = crew.kickoff()
        return f"{result}\nCrew output: {crew_output}"
    except Exception as e:
        return f"Error: {str(e)}"