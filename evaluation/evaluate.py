# evaluation/evaluate.py
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

def evaluate_predictions(documents):
    true_labels = [doc.true_label for doc in documents]
    pred_labels = [doc.predicted_label for doc in documents]

    labels = sorted(list(set(true_labels + pred_labels)))  # כל התוויות האפשריות

    # Confusion Matrix
    cm = confusion_matrix(true_labels, pred_labels, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)


    # Classification Report
    print("Classification Report:\n")
    print(classification_report(true_labels, pred_labels, labels=labels))
