import joblib
import os
from app.utils.logger import logger

class ModelLoader:
    @staticmethod
    def load_model(model_path: str):
        """
        Utility to load a trained model (e.g., pickle or joblib).
        For now, this is a placeholder for future model deployment.
        """
        if os.path.exists(model_path):
            try:
                model = joblib.load(model_path)
                logger.info(f"Model loaded from {model_path}")
                return model
            except Exception as e:
                logger.error(f"Failed to load model from {model_path}: {e}")
                return None
        logger.warning(f"Model file not found at {model_path}")
        return None

    @staticmethod
    def save_model(model, model_path: str):
        """
        Utility to save a trained model.
        """
        try:
            joblib.dump(model, model_path)
            logger.info(f"Model saved to {model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model to {model_path}: {e}")
            return False
