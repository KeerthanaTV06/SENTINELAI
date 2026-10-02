def promote_model(challenger_metrics, champion_metrics):
    if challenger_metrics['f1'] > champion_metrics['f1'] + 0.005:
        return True
    return False
