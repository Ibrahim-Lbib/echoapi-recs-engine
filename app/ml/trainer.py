import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.event import Event
from app.models.item import Item
from app.models.recommendation_cache import RecommendationCache
from app.models.user import User
from app.ml.similarity import SimilarityEngine

class Trainer:
    @staticmethod
    async def train_v1(db: AsyncSession):
        """
        Trains the model and returns a mapping of internal user IDs to recommended external item IDs.
        """
        # 1. Fetch data
        stmt_events = select(Event)
        res_events = await db.execute(stmt_events)
        events = res_events.scalars().all()

        if not events:
            return {}

        stmt_items = select(Item)
        res_items = await db.execute(stmt_items)
        items = {i.id: i.external_item_id for i in res_items.scalars().all()}

        # 2. Prepare interaction data
        data = []
        for e in events:
            weight = {"purchase": 3, "click": 2, "view": 1}.get(e.event_type, 1)
            data.append({"user_id": e.user_id, "item_id": e.item_id, "weight": weight})

        df = pd.DataFrame(data)
        pivot = df.pivot_table(index="user_id", columns="item_id", values="weight", fill_value=0)

        # 3. Calculate similarities
        sim_df = SimilarityEngine.calculate_similarities(pivot)

        # 4. Generate recommendations
        recommendations_map = {}
        for user_internal_id in pivot.index:
            top_recs_internal = SimilarityEngine.get_top_recommendations_item_based(user_internal_id, pivot, sim_df)
            external_recs = [items[iid] for iid in top_recs_internal if iid in items]
            recommendations_map[int(user_internal_id)] = external_recs

        return recommendations_map
