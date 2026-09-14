"""Agent service using Anthropic Claude Agent SDK with tool calling."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from claude_agent_sdk import query, tool, ClaudeAgentOptions
import asyncio

from app.db.models import Message
from app.services.llm_service import get_llm_provider, LLMUnavailableError
from app.services.retrieval_service import retrieval_service
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


# Define retrieval tool for Claude Agent SDK
@tool(
    name="search_lenny_transcripts",
    description="Search Lenny's podcast transcripts for information about product and growth topics. Returns relevant excerpts with episode and guest information.",
    input_schema={
        "query": str,
        "top_k": int
    }
)
async def search_lenny_transcripts(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Tool for retrieving relevant Lenny transcript chunks."""
    logger.info("tool_search_transcripts_called", query_length=len(query), top_k=top_k)
    
    chunks = retrieval_service.retrieve_chunks(query, top_k=top_k)
    
    if not chunks:
        return {
            "found": False,
            "message": "No relevant transcript content found for this query.",
            "chunks": []
        }
    
    return {
        "found": True,
        "chunks": [
            {
                "episode_title": chunk["episode_title"],
                "guest": chunk.get("guest"),
                "content": chunk["content"],
                "source_file": chunk["source_file"],
                "similarity": chunk["similarity"]
            }
            for chunk in chunks
        ]
    }


class AgentService:
    """Agent orchestration using Claude Agent SDK with proper tool calling."""
    
    def __init__(self, db: DBSession):
        self.db = db
    
    def _route_message(self, message: str) -> str:
        """Determine which skill to use."""
        message_lower = message.lower()
        
        # Ship 30 triggers
        ship30_triggers = [
            "ship 30",
            "essay",
            "blog post",
            "write article",
            "write an article",
            "create article",
            "create an article"
        ]
        if any(keyword in message_lower for keyword in ship30_triggers):
            return "ship30"
        
        # Artifact triggers
        if any(keyword in message_lower for keyword in ["create", "generate", "build"]) and \
           any(artifact in message_lower for artifact in ["dashboard", "framework", "template", "document"]):
            return "artifact"
        
        # Default to grounded Q&A
        return "grounded_qa"
    
    def _build_system_prompt(self, skill: str) -> str:
        """Build system prompt based on skill."""
        
        if skill == "grounded_qa":
            return """You are a research assistant specializing in product and growth strategy based on Lenny Rachitsky's podcast.

You have access to a tool called 'search_lenny_transcripts' that searches Lenny's podcast transcripts.

CRITICAL GROUNDING RULES:

1. **Always use the search_lenny_transcripts tool first** to find relevant information.

2. **If the tool returns relevant transcript content, use it to answer the question.**
   - Do NOT claim insufficient information when relevant evidence was retrieved.
   - Synthesize information across multiple retrieved chunks when appropriate.
   - Multiple chunks from the same episode should be combined into a coherent answer.

3. **Only use the fallback response when truly unsupported:**
   - Say "I don't have enough information in Lenny's transcripts to answer this confidently" ONLY when:
     * The tool returns no results, OR
     * The retrieved chunks contain no information relevant to the question
   - Do NOT use this fallback if you can answer from the retrieved evidence.

4. **Never produce both a fallback AND a substantive answer.**
   - These are mutually exclusive.
   - If you have evidence, answer from it.
   - If you lack evidence, use the fallback only.

5. **Grounding synthesis:**
   - Directly cite transcript facts: "According to [guest name/episode], ..."
   - Distinguish synthesis: "Taken together, these insights suggest..."
   - Never invent statistics, percentages, frameworks, or facts not in the transcripts.

6. **Source fidelity:**
   - Prioritize the most directly relevant episode/guest.
   - If the user asks about a specific person's framework (e.g., "Todd Jackson's framework"), prioritize that person's episode.
   - List sources that actually contributed to your answer.
   - Multiple chunks from one episode count as one source.

7. **Conversational context:**
   - Use conversation history to understand follow-up questions.
   - If discussing a framework in previous messages, understand that context.

Remember: Relevant evidence = answer normally. No relevant evidence = fallback only. Never both."""

        elif skill == "ship30":
            return """You are an expert Ship 30 for 30 writer. Transform insights into a compelling ~1,250-word essay following Ship 30 for 30 principles from https://www.ship30for30.com/post/how-to-start-writing-online-the-ship-30-for-30-ultimate-guide.

Ship 30 for 30 Writing Principles:
1. **Strong Hook** (first 2 sentences): Make the reader instantly curious. Open with a question, counterintuitive statement, or vivid scenario.
2. **Narrative Progression**: Tell a story, don't just list facts. Create an arc with beginning, middle, and end.
3. **Skimmable Structure**: 
   - Short paragraphs (2-4 sentences max)
   - Strategic use of bullet points
   - Generous white space
   - Clear section breaks
4. **Selective Bold Emphasis**: Bold 3-5 key phrases that allow scanning readers to grasp main points.
5. **Specific, Actionable Takeaways**: End with concrete insights readers can apply immediately.
6. **Human Voice**: Write like you're explaining to a smart friend over coffee. Avoid corporate jargon.
7. **One Clear Idea**: Focus on a single insight, not multiple disconnected concepts.

Use the search_lenny_transcripts tool to gather supporting material from Lenny's podcast.
Ground ALL claims in retrieved transcript sources. Cite episodes inline when using specific insights.
If transcripts don't support the requested content, say so clearly.

Format output in Markdown with proper headings, bullets, and **bold** emphasis."""

        elif skill == "artifact":
            return """You are a skilled designer and developer creating high-quality artifacts for product teams.

Generate the requested artifact (Markdown or HTML/CSS/JS) based on the conversation context.

For Markdown artifacts:
- Use proper heading hierarchy (# ## ###)
- Include lists, tables, and formatting as appropriate
- Create clear, scannable structure
- Professional documentation style

For HTML artifacts - CRITICAL REQUIREMENTS:

**Self-Contained Structure:**
- ALL CSS must be in a <style> tag in the <head>
- ALL JavaScript must be in a <script> tag before </body>
- NO separate .css or .js files
- NO external stylesheets or script sources
- NO CDN links (no Bootstrap, Tailwind CDN, etc.)

**JavaScript Quality:**
- Attach event listeners ONCE at page load
- NEVER nest addEventListener calls inside other event listeners
- Use event delegation for dynamic elements
- Example of CORRECT pattern:
  ```javascript
  document.addEventListener('DOMContentLoaded', function() {
      const button = document.getElementById('myButton');
      button.addEventListener('click', function() {
          console.log('Clicked');
      });
  });
  ```
- Example of INCORRECT pattern (DO NOT DO THIS):
  ```javascript
  button.addEventListener('click', function() {
      button.addEventListener('click', function() {  // WRONG: nested listener
          console.log('Clicked');
      });
  });
  ```

**Design Quality - Polished & Professional:**
- Modern, intentional design (think Linear, Notion, Stripe, Vercel)
- Excellent typography: Use system font stack or web-safe fonts
  - Example: font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
- Thoughtful color palette with proper contrast
- Generous whitespace and clear visual hierarchy
- Responsive layout using flexbox or CSS Grid
- Professional spacing and alignment
- Smooth interactions (transitions, hover states)

**Avoid Beginner Patterns:**
- NO plain Arial with no styling
- NO giant gray headings with no hierarchy
- NO basic unstyled lists
- NO default-looking buttons
- NO disconnected content sections
- NO excessive empty space
- NO garish colors or poor contrast

**Content & Grounding:**
- If using Lenny's transcript data, ground all claims in retrieved sources
- Cite episodes and guests inline when using specific insights
- Do NOT invent statistics or fake data
- Keep content substantive and valuable

**Security (DO NOT VIOLATE):**
- NO forms that submit data to external URLs
- NO iframes, embeds, or external content
- NO eval() or Function() constructor
- NO inline event handlers (onclick, onload, etc.)

**Output Format:**
- Return ONLY the complete HTML document starting with <!DOCTYPE html>
- Include <head> with <meta charset="UTF-8"> and <meta name="viewport">
- Put <style> in <head>
- Put <script> before </body>
- NO explanatory text before or after the HTML

Example structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Title</title>
    <style>
        /* All CSS here */
    </style>
</head>
<body>
    <!-- HTML content -->
    <script>
        // All JavaScript here
    </script>
</body>
</html>
```

Generate artifacts that feel production-ready, polished, and professionally designed."""
        
        return "You are a helpful assistant."
    
    def _extract_sources_from_tool_results(self, messages: List[Any]) -> List[Dict[str, Any]]:
        """Extract source citations from tool results in conversation."""
        sources = []
        
        for msg in messages:
            if hasattr(msg, 'content'):
                for block in msg.content:
                    # Check for tool result blocks
                    if hasattr(block, 'type') and block.type == 'tool_result':
                        if hasattr(block, 'content'):
                            try:
                                # Parse tool result content
                                import json
                                if isinstance(block.content, str):
                                    result = json.loads(block.content)
                                else:
                                    result = block.content
                                
                                if isinstance(result, dict) and result.get('found'):
                                    for chunk in result.get('chunks', []):
                                        sources.append({
                                            "episode_title": chunk.get("episode_title") or "Unknown Episode",
                                            "guest": chunk.get("guest"),
                                            "excerpt": chunk.get("content", "")[:200] + "...",
                                            "chunk_id": "N/A",  # Tool doesn't return chunk_id
                                            "source_file": chunk.get("source_file")
                                        })
                            except Exception as e:
                                logger.warning("failed_to_parse_tool_result", error=str(e))
        
        return sources
    
    async def generate_response(
        self,
        session_id: str,
        user_message: str,
        conversation_history: List[Message],
        model_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate AI response using Claude Agent SDK."""
        
        logger.info("agent_generate_requested", session_id=session_id, message_length=len(user_message))
        
        # Check if using Ollama - Claude Agent SDK requires Anthropic API
        if (model_provider or settings.model_provider).lower() == "ollama":
            logger.info("using_ollama_fallback")
            return await self._generate_with_ollama_fallback(
                session_id, user_message, conversation_history
            )
        
        try:
            # Step 1: Route to skill
            skill = self._route_message(user_message)
            logger.info("message_routed", skill=skill)
            
            # Step 2: Build system prompt
            system_prompt = self._build_system_prompt(skill)
            
            # Step 3: Build conversation context
            conversation_context = self._build_conversation_context(conversation_history, user_message)
            
            # Step 4: Configure Claude Agent SDK options
            options = ClaudeAgentOptions(
                tools=[search_lenny_transcripts],
                system_prompt=system_prompt,
                max_turns=10  # Limit agent loop iterations
            )
            
            # Step 5: Run agent with tool calling
            logger.info("running_claude_agent_sdk", model_provider="anthropic")
            
            full_response = ""
            messages_collected = []
            
            async for message in query(conversation_context, options=options):
                messages_collected.append(message)
                
                # Collect text content
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'type') and block.type == 'text':
                            full_response += block.text
            
            # Step 6: Extract sources from tool results
            sources = self._extract_sources_from_tool_results(messages_collected)
            
            logger.info("agent_generation_completed", response_length=len(full_response), sources_count=len(sources))
            
            return {
                "content": full_response,
                "sources": sources,
                "metadata": {
                    "skill": skill,
                    "model_provider": "anthropic",
                    "model_name": settings.anthropic_model,
                    "retrieval_count": len(sources),
                    "agent_sdk": "claude-agent-sdk"
                }
            }
        
        except Exception as e:
            logger.error("agent_generation_failed", error=str(e))
            raise
    
    async def _generate_with_ollama_fallback(
        self,
        session_id: str,
        user_message: str,
        conversation_history: List[Message]
    ) -> Dict[str, Any]:
        """Fallback to direct Ollama provider when not using Anthropic."""
        logger.info("using_ollama_direct_provider")
        
        skill = self._route_message(user_message)
        
        # For grounded Q&A, retrieve chunks directly
        retrieved_chunks = []
        if skill in ["grounded_qa", "ship30"]:
            retrieved_chunks = retrieval_service.retrieve_chunks(user_message)
            
            if not retrieved_chunks and skill == "grounded_qa":
                return {
                    "content": "I don't have enough information in Lenny's transcripts to answer this question confidently.",
                    "sources": [],
                    "metadata": {
                        "skill": skill,
                        "model_provider": "ollama",
                        "retrieval_count": 0
                    }
                }
        
        # Build system prompt with retrieved content
        system_prompt = self._build_system_prompt_with_chunks(skill, retrieved_chunks)
        
        # Build messages
        context_messages = []
        for msg in conversation_history[-10:]:
            context_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        context_messages.append({
            "role": "user",
            "content": user_message
        })
        
        messages = [{"role": "system", "content": system_prompt}] + context_messages
        
        # Generate with Ollama
        provider = get_llm_provider("ollama")
        response = provider.generate(messages, max_tokens=2000, temperature=0.7)
        
        # Extract sources
        sources = []
        for chunk in retrieved_chunks:
            sources.append({
                "episode_title": chunk["episode_title"] or "Unknown Episode",
                "guest": chunk.get("guest"),
                "excerpt": chunk["excerpt"],
                "chunk_id": chunk["chunk_id"],
                "source_file": chunk["source_file"]
            })
        
        return {
            "content": response["content"],
            "sources": sources,
            "metadata": {
                "skill": skill,
                "model_provider": "ollama",
                "model_name": response["model"],
                "retrieval_count": len(sources)
            }
        }
    
    def _build_system_prompt_with_chunks(self, skill: str, chunks: List[Dict[str, Any]]) -> str:
        """Build system prompt with embedded chunks (for Ollama fallback)."""
        if not chunks:
            return self._build_system_prompt(skill)
        
        chunks_text = "\n\n".join([
            f"[Source: {chunk['episode_title']} - {chunk['source_file']}]\n{chunk['content']}"
            for chunk in chunks
        ])
        
        base_prompt = self._build_system_prompt(skill)
        return f"{base_prompt}\n\nRelevant Transcripts:\n{chunks_text}"
    
    def _build_conversation_context(self, history: List[Message], current_message: str) -> str:
        """Build conversation context string for Claude Agent SDK."""
        context_parts = []
        
        # Add recent history
        for msg in history[-10:]:
            role_label = "User" if msg.role == "user" else "Assistant"
            context_parts.append(f"{role_label}: {msg.content}")
        
        # Add current message
        context_parts.append(f"User: {current_message}")
        
        return "\n\n".join(context_parts)
