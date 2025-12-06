from scipy.stats import randint, uniform

# LightGBM Hyperparameter Space
LIGHTGM_PARAMS = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(3, 20),
    'learning_rate': uniform(0.01, 0.2),
    'num_leaves': randint(20, 150),
    'boosting_type': ['gbdt', 'dart', 'goss']
}

# Random Search Settings
RANDOM_SEARCH_PARAMS = {
    'n_iter': 4,
    'cv': 2,       
    'n_jobs': -1,
    'verbose': 2,
    'random_state': 42,
    'scoring': 'accuracy'
}
