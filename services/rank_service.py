from models.user import RankEnum

RANK_THRESHOLD = [
    (0, RankEnum.incompetent),
    (10, RankEnum.beginner),
    (20, RankEnum.specialist),
    (30, RankEnum.expert),
    (40, RankEnum.master)
]

def get_rank_for_score(score: int) -> RankEnum:
    for threshold, rank in reversed(RANK_THRESHOLD):
        if score >= threshold:
            return rank
    return RankEnum.incompetent