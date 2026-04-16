import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize Groq LLM using LangChain's ChatOpenAI
llm = ChatOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url=settings.GROQ_BASE_URL,
    model=settings.GROQ_MODEL,
    temperature=0.7,
    request_timeout=120.0,  # 2 minute timeout for the request
)

blog_prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="""Write a comprehensive technical blog about {topic}.

Your response must be formatted in Markdown and include:

# [Compelling Title About the Topic]

## Introduction
[Write an engaging 2-3 paragraph introduction that explains what the topic is, why it matters, and what readers will learn]

## [Section 1 Title]
[Detailed technical content with explanations]

## [Section 2 Title] 
[More detailed technical content, include practical examples]

## [Section 3 Title]
[Advanced concepts or best practices]

## Code Examples
```language
// Include at least one practical code example relevant to the topic
[code here]
```

## Summary
[A concise summary of key points and takeaways]

Tags: [tag1, tag2, tag3, tag4]

Ensure the blog is well-structured, technically accurate, and provides real value to developers. Use proper Markdown formatting with headings, lists, and code blocks where appropriate.
"""
)

def generate_blog_content(topic: str) -> str:
    logger.info(f"Calling Groq API with model: {settings.GROQ_MODEL}")
    try:
        prompt = blog_prompt_template.format(topic=topic)
        logger.info(f"Prompt length: {len(prompt)} characters")
        response = llm.invoke(prompt)
        logger.info(f"Groq API response received, content length: {len(response.content)}")
        return response.content
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}", exc_info=True)
        raise

def extract_title_from_markdown(content: str) -> str:
    lines = content.strip().split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:]
        if stripped.startswith("Title: "):
            return stripped[7:]
    
    # Fallback
    return lines[0][:50] if lines else "Untitled"

def extract_tags_from_markdown(content: str) -> list:
    """Extract tags from the end of markdown content."""
    lines = content.strip().split("\n")
    tags = []
    
    # Look for "Tags:" at the end
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.lower().startswith("tags:"):
            tags_part = line[5:].strip()
            # Parse comma-separated tags
            tags = [tag.strip().strip("[]") for tag in tags_part.split(",") if tag.strip()]
            # Remove the tags line from content
            content = "\n".join(lines[:i]).strip()
            break
    
    # If no tags found, generate simple ones from topic
    if not tags:
        # Try to extract from title or content
        words = []
        for line in lines[:5]:  # Check first few lines
            if line.strip().startswith("#"):
                title_words = line.replace("#", "").strip().split()
                words.extend([w for w in title_words if len(w) > 3])
                break
        tags = words[:4] if words else ["Technology"]
    
    return content, tags

def generate_blog(topic: str):
    """Generates a blog and extracts title and tags from the generated content."""
    logger.info(f"Starting blog generation for topic: {topic}")
    content = generate_blog_content(topic)
    
    # Extract title
    title = extract_title_from_markdown(content)
    
    # Extract tags
    content, tags = extract_tags_from_markdown(content)
    
    logger.info(f"Blog generation complete: title={title}, tags={tags}")    
    return {
        "title": title,
        "content": content,
        "tags": tags
    }

def generate_chat_answer(question: str, context: str) -> str:
    chat_prompt = f"""You are Pythia, an AI Knowledge Oracle.
Answer the user's question using ONLY the provided context from the knowledge base.
If the context does not contain the answer, say "The archives do not contain the answer to this question."

Context:
{context}

Question:
{question}
"""
    response = llm.invoke(chat_prompt)
    return response.content
