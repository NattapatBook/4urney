import os
import time
from transformers import pipeline

def intent_routing_using_huggingface(message, candidate_labels, model_name="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", urgent_criteria=0.7):
    """
    Intent routing with huggingface zero shot classification
    """
    start_time = time.time()

    classifier = pipeline("zero-shot-classification", model=model_name)
    output = classifier(
        message,
        candidate_labels=candidate_labels,
        multi_label=False
    )
    end_time = time.time()

    # Sort the scores and corresponding labels in descending order
    sorted_indices = sorted(range(len(output['scores'])), key=lambda k: output['scores'][k], reverse=True)

    # Check if the highest score meets the probability criteria
    if output['labels'][sorted_indices[0]] == "ต้องการติดต่อเจ้าหน้าที่" and output['scores'][sorted_indices[0]] >= urgent_criteria:
        most_probable_label = output['labels'][sorted_indices[0]]
    elif output['labels'][sorted_indices[0]] != "ต้องการติดต่อเจ้าหน้าที่": 
        most_probable_label = output['labels'][sorted_indices[0]]
    else:
        # Use the second highest score if the highest doesn't meet the criteria
        most_probable_label = output['labels'][sorted_indices[1]]

    print(most_probable_label)


    print("Classification time:", end_time - start_time)
    return most_probable_label