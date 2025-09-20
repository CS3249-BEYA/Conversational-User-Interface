import logging
import time
import re
from typing import Dict, List

from .config import (
    SYSTEM_PROMPT,
    MAX_CONVERSATION_TURNS,
    CONTEXT_WINDOW_SIZE,
)
from .model_provider import get_provider
from .moderation import (
    ModerationAction,
    ModerationResult,
    get_moderator,
)

logger = logging.getLogger(__name__)


class ChatEngine:
    """Orchestrates conversation flow with safety checks."""
    
    def __init__(self):
        """Initialize chat engine with model and moderator."""
        self.model = get_provider()
        self.moderator = get_moderator()
        self.conversation_history: List[Dict] = []
        self.turn_count = 0
        self.session_id = f"session_{int(time.time())}"
        self.first_interaction = True
        self.user_profile: Dict = {}

    def set_user_profile(self, profile_data: Dict):
        """Sets or updates the user's profile data."""
        self.user_profile = profile_data
        logger.info(f"User profile set: {self.user_profile}")
    
    def process_message(
        self,
        user_input: str,
        include_context: bool = True,
    ) -> Dict:
        
        """
        Process a single message through the conversation pipeline.
        
        TODO: Complete the conversation flow implementation
        
        IMPLEMENTATION GUIDE:
        The method follows this pipeline:
        1. Show disclaimer if first interaction (already implemented)
        2. Moderate user input (already implemented)
        3. Handle moderation results
        4. Generate response IF input passes (partially implemented)
        5. Moderate output and prepare final response (already implemented)
        6. Update history and add metadata (already implemented)
        
        Args:
            user_input: User's message
            include_context: Whether to include conversation history
            
        Returns:
            Dict containing response and metadata with keys:
            - prompt: Original user input
            - response: Final response text
            - safety_action: "allow", "block", or "safe_fallback"
            - policy_tags: List of triggered policy tags
            - model_name: Model used or status indicator
            - deterministic: Boolean indicating if response is deterministic
            - latency_ms: Processing time in milliseconds
            - turn_count: Current conversation turn number
            - session_id: Unique session identifier
        """

        start_time = time.time()
        
        disclaimer = None
        if self.first_interaction:
            self.first_interaction = False
            # Get disclaimer to include in response
            disclaimer = self.moderator.get_disclaimer()

        input_moderation = self._moderate_input(user_input)
        if input_moderation.action == ModerationAction.BLOCK:
            final_response = self._prepare_final_response(
                user_input=user_input,
                model_response={"response": "",
                                "model": "blocked", "deterministic": True},
                input_moderation=input_moderation,
                output_moderation=ModerationResult(
                    action=ModerationAction.ALLOW, tags=[], reason="N/A", confidence=0.0)
            )

            if disclaimer:
                final_response["response"] = f"{disclaimer}\n\n---\n\n{final_response['response']}"

            self._update_history(user_input, final_response["response"])

            final_response["latency_ms"] = int(
                (time.time() - start_time) * 1000)
            final_response["turn_count"] = self.turn_count
            final_response["session_id"] = self.session_id

            return final_response

        elif input_moderation.action == ModerationAction.SAFE_FALLBACK:
            final_response = self._prepare_final_response(
                user_input=user_input,
                model_response={"response": "",
                                "model": "safe_fallback", "deterministic": True},
                input_moderation=input_moderation,
                output_moderation=ModerationResult(
                    action=ModerationAction.ALLOW, tags=[], reason="N/A", confidence=0.0)
            )

            if disclaimer:
                final_response["response"] = f"{disclaimer}\n\n---\n\n{final_response['response']}"

            self._update_history(user_input, final_response["response"])

            final_response["latency_ms"] = int(
                (time.time() - start_time) * 1000)
            final_response["turn_count"] = self.turn_count
            final_response["session_id"] = self.session_id

            return final_response
        
        model_response = self._generate_response(
            user_input,
            include_context
        )
    
        output_moderation = self._moderate_output(
            user_input,
            model_response["response"]
        )
        
        final_response = self._prepare_final_response(
            user_input=user_input,
            model_response=model_response,
            input_moderation=input_moderation,
            output_moderation=output_moderation,
        )
        
        if disclaimer:
            final_response["response"] = f"{disclaimer}\n\n---\n\n{final_response['response']}"
        
        self._update_history(user_input, final_response["response"])
        
        final_response["latency_ms"] = int((time.time() - start_time) * 1000)
        final_response["turn_count"] = self.turn_count
        final_response["session_id"] = self.session_id
        
        return final_response
    
    def _moderate_input(self, user_input: str) -> ModerationResult:
        """
        Implement input moderation.
        
        - Calls moderator with user input
        - Considers conversation context
        - Returns moderation result
        """
        context = self.conversation_history[-CONTEXT_WINDOW_SIZE:] \
            if self.conversation_history else None
        
        return self.moderator.moderate(
            user_prompt=user_input,
            context=context,
        )
    
    def _generate_response(
        self,
        user_input: str,
        include_context: bool,
    ) -> Dict:
        """
        Generate model response with appropriate prompting.
        
        - Builds prompt with system instructions
        - Includes relevant context
        - Calls model provider
        - Handles errors gracefully
        """
        try:
            context = None
            if include_context and self.conversation_history:
                context = self.conversation_history[-CONTEXT_WINDOW_SIZE:]
            
            response = self.model.generate(
                prompt=user_input,
                system_prompt=SYSTEM_PROMPT,
                conversation_history=context,
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Model generation failed: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your message. Please try again.",
                "error": str(e),
                "model": "error",
                "deterministic": False,
            }
    
    def _moderate_output(
        self,
        user_input: str,
        model_response: str,
    ) -> ModerationResult:
        """
        Implement output moderation.
        
        - Checks model response for policy violations
        - Considers user input for context
        - Returns moderation result
        """
        return self.moderator.moderate(
            user_prompt=user_input,
            model_response=model_response,
        )
    
    def _prepare_final_response(
        self,
        user_input: str,
        model_response: Dict,
        input_moderation: ModerationResult,
        output_moderation: ModerationResult,
    ) -> Dict:
        """
        Prepare the final response based on moderation results.
        
        - Uses model response if all checks pass
        - Uses fallback messages if needed
        - Includes appropriate metadata
        """
        if input_moderation.action == ModerationAction.BLOCK:
            final_action = "block"
            final_text = input_moderation.fallback_response or \
                "I cannot assist with that request. If you have other questions or need support with appropriate topics, I'm here to help."
            policy_tags = input_moderation.tags
        elif input_moderation.action == ModerationAction.SAFE_FALLBACK:
            final_action = "safe_fallback"
            final_text = input_moderation.fallback_response or \
                "Let me redirect you to appropriate resources. If you're in crisis, please contact emergency services or a crisis helpline immediately."
            policy_tags = input_moderation.tags
        elif output_moderation.action == ModerationAction.SAFE_FALLBACK:
            final_action = "safe_fallback"
            final_text = output_moderation.fallback_response or \
                "I want to be helpful while staying within appropriate bounds. Let me rephrase my response."
            policy_tags = output_moderation.tags
        else:
            final_action = "allow"
            final_text = model_response.get("response", "")
            policy_tags = []
        
        if self.turn_count >= MAX_CONVERSATION_TURNS - 2:
            final_text += f"\n\n[Note: We're approaching our conversation limit ({self.turn_count + 1}/{MAX_CONVERSATION_TURNS} turns). Consider taking a break or starting a new conversation if needed.]"
        
        return {
            "prompt": user_input,
            "response": final_text,
            "safety_action": final_action,
            "policy_tags": policy_tags,
            "model_name": model_response.get("model", "unknown"),
            "deterministic": model_response.get("deterministic", False),
        }
    
    def _update_history(self, user_input: str, assistant_response: str):
        """
        Update conversation history.
        
        TODO: Implement conversation limit handling
        
        This method should:
        - Add user and assistant turns to history
        - Increment turn counter
        - Check and handle conversation limits
        - Maintain maximum history size
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
        })
        
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_response,
        })

        self.turn_count += 1
        if self.turn_count >= MAX_CONVERSATION_TURNS:

            self.conversation_history.append({
                "role": "system",
                "content": "Conversation limit reached. Please start a new session for further discussion."
            })

        max_history_size = CONTEXT_WINDOW_SIZE * 2 
        if len(self.conversation_history) > max_history_size:
            self.conversation_history = self.conversation_history[-max_history_size:]
    
    def reset(self):
        """Reset conversation state."""
        self.conversation_history = []
        self.turn_count = 0
        self.first_interaction = True
        self.session_id = f"session_{int(time.time())}"
        self.user_profile = {}
        logger.info(f"Chat engine reset. New session: {self.session_id}")

_engine_instance = None

def get_engine() -> ChatEngine:
    """Get or create singleton chat engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ChatEngine()
        logger.info("Created new ChatEngine singleton instance")
    return _engine_instance