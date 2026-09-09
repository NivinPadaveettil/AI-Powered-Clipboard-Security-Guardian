from predict import predict
from core.risk_scoring import calculate_risk

print("=" * 60)
print("AI Clipboard Detector")
print("=" * 60)

while True:

    text = input("\nClipboard Text (or 'quit'): ")

    if text.lower() == "quit":
        break

    label, confidence = predict(text)

    risk = calculate_risk(label, confidence)

    print("\n========== Detection ==========")
    print("Category      :", risk.category)
    print(f"Confidence    : {risk.confidence:.4f}")
    print("Risk Level    :", risk.risk_level)
    print("Risk Score    :", risk.risk_score)
    print("Explanation   :", risk.explanation)
    print("Action        :", risk.action)
    print("Auto Clear    :", risk.timeout, "seconds")