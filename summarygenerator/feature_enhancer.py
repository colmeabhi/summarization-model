import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def enhance_features(feature_matrix, n_hidden=8, noise=0.1, seed=42):
    """
    Replacement for the old theano RBM.
    We squash the features with PCA and then rebuild them, which smooths
    them out kind of like the RBM did. A bit of noise is added like the
    RBM's random sampling, but with a fixed seed so the same text always
    gives the same summary.
    """
    scaler = StandardScaler()
    scaled = scaler.fit_transform(feature_matrix)

    # PCA cant have more components than rows or columns
    n_components = min(n_hidden, feature_matrix.shape[0], feature_matrix.shape[1])
    pca = PCA(n_components=n_components)

    reduced = pca.fit_transform(scaled)
    rebuilt = pca.inverse_transform(reduced)

    rng = np.random.default_rng(seed)
    rebuilt = rebuilt + rng.normal(0, noise, rebuilt.shape)

    result = scaler.inverse_transform(rebuilt)

    # RBM outputs are always positive
    return np.abs(result)
