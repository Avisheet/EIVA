from transformers import pipeline

emotion_pipeline = pipeline(
    task="text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)

def get_top_emotions(text: str, top_k: int = 3):
    """
    Returns the top-k emotions and their scores for a given text.
    """
    results = emotion_pipeline(text)[0]
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return sorted_results[:top_k]

if __name__ == "__main__":
    while True:
        user_input = input("Enter text (or type 'quit' to exit): ")
        if user_input.lower() == "quit":
            break

        top_emotions = get_top_emotions(user_input, top_k=3)

        print("\nTop 3 Emotions:")
        for emo in top_emotions:
            print(f"- {emo['label']}: {emo['score']*100:.2f}%")
        print()
