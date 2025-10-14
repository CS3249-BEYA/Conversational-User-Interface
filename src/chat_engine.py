import time
import logging
from typing import Dict, List

from .config import SYSTEM_PROMPT
from .model_provider import get_provider
from .moderation import ModerationAction, ModerationResult, get_moderator

logger = logging.getLogger(__name__)


class ChatEngine:
    """Handles conversation flow with moderation and response generation."""

    def __init__(self):
        self.model = get_provider()
        self.moderator = get_moderator()
        self.conversation_history: List[Dict] = []
        self.turn_count = 0
        self.session_id = f"session_{int(time.time())}"
        self.first_interaction = True
        self.user_profile: Dict = {}

    def set_user_profile(self, profile_data: Dict):
        self.user_profile = profile_data
        logger.info(f"User profile set: {self.user_profile}")

    def process_message(self, user_input: str, include_context: bool = True) -> Dict:
        start_time = time.time()
        disclaimer = self.moderator.get_disclaimer() if self.first_interaction else None
        self.first_interaction = False

        input_moderation = self._moderate_input(user_input)

        if input_moderation.action == ModerationAction.BLOCK:
            return self._handle_block(user_input, start_time, disclaimer)

        if input_moderation.action == ModerationAction.SAFE_FALLBACK:
            return self._handle_safe_fallback(user_input, start_time, disclaimer)

        model_response = self._generate_response(user_input, include_context)
        output_moderation = self._moderate_output(
            user_input, model_response["response"])

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
        context = self.conversation_history[-5:
                                            ] if self.conversation_history else None
        return self.moderator.moderate(user_prompt=user_input, context=context)

    def _generate_response(self, user_input: str, include_context: bool) -> Dict:
        try:
            context = self.conversation_history[-5:
                                                ] if include_context and self.conversation_history else None
            return self.model.generate(
                prompt=user_input,
                system_prompt=SYSTEM_PROMPT,
                conversation_history=context,
            )
        except Exception as e:
            logger.error(f"Model generation failed: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your message. Please try again.",
                "error": str(e),
                "model": "error",
                "deterministic": False,
            }

    def _moderate_output(self, user_input: str, model_response: str) -> ModerationResult:
        return self.moderator.moderate(user_prompt=user_input, model_response=model_response)

    def _prepare_final_response(
        self, user_input: str, model_response: Dict, input_moderation: ModerationResult, output_moderation: ModerationResult
    ) -> Dict:
        if input_moderation.action == ModerationAction.BLOCK:
            final_action = "block"
            final_text = input_moderation.fallback_response or "I cannot assist with that request."
            policy_tags = input_moderation.tags
        elif input_moderation.action == ModerationAction.SAFE_FALLBACK or output_moderation.action == ModerationAction.SAFE_FALLBACK:
            final_action = "safe_fallback"
            final_text = input_moderation.fallback_response or output_moderation.fallback_response or "Let me rephrase my response."
            policy_tags = input_moderation.tags or output_moderation.tags
        else:
            final_action = "allow"
            final_text = model_response.get("response", "")
            policy_tags = []

        return {
            "prompt": user_input,
            "response": final_text,
            "safety_action": final_action,
            "policy_tags": policy_tags,
            "model_name": model_response.get("model", "unknown"),
            "deterministic": model_response.get("deterministic", False),
        }

    def _update_history(self, user_input: str, assistant_response: str):
        # Add new messages
        self.conversation_history.append(
            {"role": "user", "content": user_input})
        self.conversation_history.append(
            {"role": "assistant", "content": assistant_response})

        # Keep only last 5 messages
        if len(self.conversation_history) > 5:
            self.conversation_history = self.conversation_history[-5:]

        self.turn_count += 1

    def _handle_block(self, user_input: str, start_time: float, disclaimer: str):
        response = self._prepare_final_response(
            user_input=user_input,
            model_response={"response": "",
                            "model": "blocked", "deterministic": True},
            input_moderation=ModerationResult(
                action=ModerationAction.BLOCK, tags=[], reason="", confidence=0.0),
            output_moderation=ModerationResult(
                action=ModerationAction.ALLOW, tags=[], reason="", confidence=0.0),
        )
        if disclaimer:
            response["response"] = f"{disclaimer}\n\n---\n\n{response['response']}"
        self._update_history(user_input, response["response"])
        response["latency_ms"] = int((time.time() - start_time) * 1000)
        response["turn_count"] = self.turn_count
        response["session_id"] = self.session_id
        return response

    def _handle_safe_fallback(self, user_input: str, start_time: float, disclaimer: str):
        response = self._prepare_final_response(
            user_input=user_input,
            model_response={"response": "",
                            "model": "safe_fallback", "deterministic": True},
            input_moderation=ModerationResult(
                action=ModerationAction.SAFE_FALLBACK, tags=[], reason="", confidence=0.0),
            output_moderation=ModerationResult(
                action=ModerationAction.ALLOW, tags=[], reason="", confidence=0.0),
        )
        if disclaimer:
            response["response"] = f"{disclaimer}\n\n---\n\n{response['response']}"
        self._update_history(user_input, response["response"])
        response["latency_ms"] = int((time.time() - start_time) * 1000)
        response["turn_count"] = self.turn_count
        response["session_id"] = self.session_id
        return response

    def reset(self):
        self.conversation_history = []
        self.turn_count = 0
        self.first_interaction = True
        self.session_id = f"session_{int(time.time())}"
        self.user_profile = {}
        logger.info(f"Chat engine reset. New session: {self.session_id}")


_engine_instance = None


def get_engine() -> ChatEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ChatEngine()
        logger.info("Created new ChatEngine singleton instance")
    return _engine_instance
