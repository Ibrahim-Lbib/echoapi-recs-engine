import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityEngine:
    @staticmethod
    def calculate_similarities(pivot_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates item-item similarity using cosine similarity.
        Input: pivot_df with users as rows and items as columns.
        """
        # For item-item, we transpose so items are rows
        item_pivot = pivot_df.T
        sim_matrix = cosine_similarity(item_pivot)
        return pd.DataFrame(sim_matrix, index=item_pivot.index, columns=item_pivot.index)

    @staticmethod
    def get_top_recommendations_item_based(user_id: int, pivot_df: pd.DataFrame, sim_df: pd.DataFrame, top_n: int = 10):
        """
        Generates top N recommendations for a user based on items they've interacted with.
        Uses item-item similarity.
        """
        if user_id not in pivot_df.index:
            return []

        # 1. Get items the user interacted with and their weights
        user_interactions = pivot_df.loc[user_id]
        interacted_items = user_interactions[user_interactions > 0].index.tolist()
        
        if not interacted_items:
            return []

        # 2. Score candidate items based on similarity to interacted items
        # For each item user liked, find similar items and aggregate scores
        scores = pd.Series(dtype=float)
        for item_id in interacted_items:
            weight = user_interactions[item_id]
            # Get similarities for this item, scale by user's interaction weight
            similar_items = sim_df[item_id] * weight
            scores = scores.add(similar_items, fill_value=0)

        # 3. Filter out items the user has already seen
        scores = scores.drop(labels=interacted_items, errors='ignore')

        # 4. Return top N items
        return scores.sort_values(ascending=False).head(top_n).index.tolist()
