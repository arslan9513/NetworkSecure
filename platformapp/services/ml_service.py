from dataclasses import dataclass
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score


@dataclass
class TrainResult:
    accuracy: float
    precision: float
    recall: float


def train_algorithm(algorithm: str) -> TrainResult:
    rng = np.random.default_rng(42)
    X = rng.normal(size=(600, 6))
    y = (X[:, 0] + 0.5 * X[:, 1] - X[:, 2] > 0).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if algorithm == 'rf':
        model = RandomForestClassifier(n_estimators=120, random_state=42)
    elif algorithm == 'nn':
        model = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=200, random_state=42)
    else:
        model = LogisticRegression(max_iter=200)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return TrainResult(
        accuracy=accuracy_score(y_test, y_pred),
        precision=precision_score(y_test, y_pred, zero_division=0),
        recall=recall_score(y_test, y_pred, zero_division=0),
    )
