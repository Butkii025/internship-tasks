"""
PREDICT.PY
Author: Priyanshu Vijay
Description: Inference interface for the book-length predictive pipeline.
             Loads serialized model components, dynamically matches categorical
             features with the training baseline log, and runs an interactive 
             user prediction loop via the terminal console.
"""

import os
import joblib
import pandas as pd

def get_live_prediction():
    print("🔮 Initializing Production Inference Engine...")
    
    # 1. Path Verification for Serialized Artifacts
    model_path = 'models/book_length_regressor.pkl'
    features_path = 'models/model_features.pkl'
    
    if not os.path.exists(model_path) or not os.path.exists(features_path):
        raise FileNotFoundError("❌ Serialized model artifacts missing! Please run 'python train_model.py' first.")
    
    # 2. Rehydrate the Saved Model Brain and Structural Matrix Features
    print("💾 Rehydrating serialized artifacts from disk...")
    model = joblib.load(model_path)
    trained_features = joblib.load(features_path)
    
    # Extract valid publishers and book types from one-hot encoded columns
    valid_publishers = sorted([
        col.replace("Publisher_", "") for col in trained_features if col.startswith("Publisher_")
    ])
    valid_types = sorted([
        col.replace("Book_Type_", "") for col in trained_features if col.startswith("Book_Type_")
    ])
    
    print("\n💡 Model layers rehydrated successfully. Ready for real-time inference.")
    
    # 3. Enhanced Options Loop
    while True:
        print("\n" + "="*55)
        print("🤖 STEPHEN KING BOOK-LENGTH PREDICTION DASHBOARD")
        print("="*55)
        print("Options: Type your parameters below, or type 'exit' to quit.")
        print("-"*55)
        
        # Option A: Interactive Year Input
        user_input_year = input("📅 Enter a custom Publication Year (e.g., 2027): ").strip()
        if user_input_year.lower() == 'exit':
            break
            
        try:
            user_year = int(user_input_year)
        except ValueError:
            print("❌ Error: Publication year must be a valid integer.")
            continue

        # Option B: Dynamic Book Type Selection Menu
        print("\n📚 Available Book Types:")
        # Display explicit choices including the baseline reference column dropped during get_dummies
        display_types = ["Novel"] + valid_types if "Novel" not in valid_types else valid_types
        for idx, b_type in enumerate(display_types, 1):
            print(f"  [{idx}] {b_type}")
        print("-"*55)
        
        user_input_type = input("📝 Select a Book Type (Enter number or text): ").strip()
        if user_input_type.lower() == 'exit':
            break
            
        if user_input_type.isdigit():
            t_idx = int(user_input_type) - 1
            user_type = display_types[t_idx] if 0 <= t_idx < len(display_types) else "Novel"
        else:
            user_type = user_input_type

        # Option C: Dynamic Publisher Selection Menu
        print("\n🏢 Known Production Category Publishers:")
        for idx, pub in enumerate(valid_publishers, 1):
            print(f"  [{idx}] {pub}")
        print(f"  [{len(valid_publishers)+1}] Other / New Publisher")
        print("-"*55)
        
        user_input_pub = input("📝 Select a Publisher (Enter number or text): ").strip()
        if user_input_pub.lower() == 'exit':
            break
            
        if user_input_pub.isdigit():
            p_idx = int(user_input_pub) - 1
            if 0 <= p_idx < len(valid_publishers):
                user_publisher = valid_publishers[p_idx]
            else:
                user_publisher = "Other"
        else:
            user_publisher = user_input_pub

        # 4. Reconstruct the Matrix Row to Match Training Alignment
        input_data = {col: 0 for col in trained_features}
        
        # Assign continuous time attribute
        if 'Year' in input_data:
            input_data['Year'] = user_year
            
        # 5. Apply One-Hot Encoding Logic dynamically for Publisher
        encoded_publisher_col = f"Publisher_{user_publisher}"
        if encoded_publisher_col in input_data:
            input_data[encoded_publisher_col] = 1
            print(f"\n🎯 Target constraint matched for category: '{user_publisher}'")
        else:
            if "Publisher_Other" in input_data:
                input_data["Publisher_Other"] = 1
                print(f"\n⚠️ Categorized under rare 'Other' group.")
            else:
                print(f"\n⚠️ Defaulting to baseline publisher variance.")

        # 6. Apply One-Hot Encoding Logic dynamically for Book Type
        encoded_type_col = f"Book_Type_{user_type}"
        if encoded_type_col in input_data:
            input_data[encoded_type_col] = 1
            print(f"🎯 Target constraint matched for book type: '{user_type}'")
        else:
            print(f"⚠️ Defaulting to baseline type context ('Novel').")

        # 7. Build DataFrame with exact matching matrix column ordering sequence
        input_df = pd.DataFrame([input_data])[trained_features]
        
        # 8. Execute Model Inference
        predicted_pages = model.predict(input_df)[0]
        if predicted_pages < 1:
            predicted_pages = 1.0
            
        print("\n==================================================")
        print(f"📚 INFERENCE ML RESULT:")
        print(f"👉 Predicted Expected Page Count: {predicted_pages:.1f} pages")
        print("==================================================\n")
        
        continue_query = input("🔄 Run another prediction? (y/n): ").strip().lower()
        if continue_query not in ['y', 'yes']:
            print("👋 Exiting inference dashboard. Deployment sequence complete!")
            break

if __name__ == "__main__":
    get_live_prediction()