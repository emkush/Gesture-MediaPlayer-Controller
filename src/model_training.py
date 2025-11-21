#!/usr/bin/env python3
"""
Retrain the palm gesture model with proper data processing.
This will fix the issue where the model predicts everything as palm.
"""

import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def extract_landmarks_from_json(json_file, target_label="palm"):
    """Extract landmarks from JSON annotation file"""
    print(f"Loading data from {json_file}...")
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return [], []
    
    landmarks_list = []
    labels_list = []
    
    for video_id, video_data in data.items():
        if 'landmarks' in video_data and 'labels' in video_data:
            landmarks = video_data['landmarks']
            labels = video_data['labels']
            
            for i, landmark_group in enumerate(landmarks):
                if i < len(labels):
                    label = labels[i]
                    
                    # Convert landmark points to feature vector
                    try:
                        feature_vector = []
                        for point in landmark_group:
                            if len(point) == 2:  # x, y coordinates
                                feature_vector.extend([point[0], point[1], 0.0])  # Add z=0
                            elif len(point) == 3:  # x, y, z coordinates
                                feature_vector.extend(point)
                        
                        # Ensure we have exactly 63 features (21 landmarks * 3 coordinates)
                        if len(feature_vector) == 63:
                            landmarks_list.append(feature_vector)
                            # Binary classification: 1 for palm, 0 for everything else
                            labels_list.append(1 if label == target_label else 0)
                    
                    except Exception as e:
                        print(f"Error processing landmark in {video_id}: {e}")
                        continue
    
    print(f"Extracted {len(landmarks_list)} samples from {json_file}")
    return landmarks_list, labels_list

def prepare_balanced_dataset():
    """Prepare a balanced dataset with palm and non-palm gestures"""
    print("🔄 Preparing balanced dataset...")
    
    all_landmarks = []
    all_labels = []
    
    # Define data files
    data_files = [
        ('/Users/jethrohermawan/310/Project/datasets/ann_subsample/palm.json', 'palm'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_train_val/palm.json', 'palm'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_subsample/fist.json', 'fist'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_subsample/ok.json', 'ok'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_subsample/peace.json', 'peace'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_subsample/stop.json', 'stop'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_train_val/fist.json', 'fist'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_train_val/ok.json', 'ok'),
        ('/Users/jethrohermawan/310/Project/datasets/ann_train_val/peace.json', 'peace'),
    ]
    
    palm_count = 0
    non_palm_count = 0
    
    # Load data from each file
    for file_path, expected_label in data_files:
        if os.path.exists(file_path):
            landmarks, labels = extract_landmarks_from_json(file_path, 'palm')
            all_landmarks.extend(landmarks)
            all_labels.extend(labels)
            
            # Count samples for balancing
            for label in labels:
                if label == 1:
                    palm_count += 1
                else:
                    non_palm_count += 1
    
    print(f"📊 Dataset summary:")
    print(f"   Palm gestures: {palm_count}")
    print(f"   Non-palm gestures: {non_palm_count}")
    print(f"   Total samples: {len(all_landmarks)}")
    
    if len(all_landmarks) == 0:
        print("❌ No data loaded! Check file paths.")
        return None, None
    
    # Balance the dataset
    X = np.array(all_landmarks)
    y = np.array(all_labels)
    
    # If dataset is very imbalanced, balance it
    if palm_count > 0 and non_palm_count > 0:
        min_class_size = min(palm_count, non_palm_count)
        if min_class_size < 50:
            print(f"⚠️ Small dataset size: {min_class_size} samples per class")
        
        # Get balanced samples
        palm_indices = np.where(y == 1)[0]
        non_palm_indices = np.where(y == 0)[0]
        
        # Sample equally from both classes
        max_samples_per_class = min(len(palm_indices), len(non_palm_indices), 1000)
        
        selected_palm = np.random.choice(palm_indices, max_samples_per_class, replace=False)
        selected_non_palm = np.random.choice(non_palm_indices, max_samples_per_class, replace=False)
        
        balanced_indices = np.concatenate([selected_palm, selected_non_palm])
        np.random.shuffle(balanced_indices)
        
        X_balanced = X[balanced_indices]
        y_balanced = y[balanced_indices]
        
        print(f"✅ Balanced dataset: {len(X_balanced)} total samples ({max_samples_per_class} per class)")
        return X_balanced, y_balanced
    
    return X, y

def create_improved_model():
    """Create an improved model architecture"""
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(63,)),
        
        # Normalize input features
        tf.keras.layers.BatchNormalization(),
        
        # Feature extraction layers
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.BatchNormalization(),
        
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        
        # Output layer
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Use better optimizer and metrics
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 'precision', 'recall']
    )
    
    return model

def train_palm_model():
    """Train a proper palm detection model"""
    print("🚀 Training Palm Detection Model")
    print("=" * 40)
    
    # Suppress TensorFlow warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    tf.get_logger().setLevel('ERROR')
    
    # Load and prepare data
    X, y = prepare_balanced_dataset()
    
    if X is None or len(X) == 0:
        print("❌ No training data available. Creating a basic model...")
        model = create_improved_model()
        model.save("palm_gesture_model.h5")
        print("✅ Basic model structure saved (untrained)")
        return model
    
    # Normalize features
    print("🔄 Normalizing features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Training set: {len(X_train)} samples")
    print(f"📊 Test set: {len(X_test)} samples")
    
    # Create and train model
    model = create_improved_model()
    
    # Callbacks for better training
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', 
            patience=10, 
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', 
            factor=0.5, 
            patience=5
        )
    ]
    
    print("🏋️ Training model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=100,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate model
    print("\n📊 Final evaluation:")
    test_loss, test_accuracy, test_precision, test_recall = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Precision: {test_precision:.4f}")
    print(f"Test Recall: {test_recall:.4f}")
    
    # Test with some sample predictions
    print("\n🧪 Testing predictions:")
    sample_predictions = model.predict(X_test[:10], verbose=0)
    for i, (pred, actual) in enumerate(zip(sample_predictions, y_test[:10])):
        pred_label = "PALM" if pred[0] > 0.5 else "NOT PALM"
        actual_label = "PALM" if actual == 1 else "NOT PALM"
        print(f"  Sample {i+1}: Predicted {pred[0]:.3f} ({pred_label}) | Actual: {actual_label}")
    
    # Save model
    model.save("palm_gesture_model.h5")
    print("\n✅ Improved model saved as palm_gesture_model.h5")
    
    # Save scaler for future use
    import joblib
    joblib.dump(scaler, "palm_scaler.pkl")
    print("✅ Scaler saved as palm_scaler.pkl")
    
    return model

def test_model():
    """Test the retrained model"""
    print("\n🧪 Testing retrained model...")
    
    try:
        model = tf.keras.models.load_model("palm_gesture_model.h5")
        
        # Test with various inputs
        test_cases = [
            ("Random gesture", np.random.random(63)),
            ("All zeros", np.zeros(63)),
            ("All ones", np.ones(63)),
        ]
        
        for name, data in test_cases:
            pred = model.predict(data.reshape(1, -1), verbose=0)[0][0]
            print(f"  {name}: {pred:.4f} ({'PALM' if pred > 0.5 else 'NOT PALM'})")
            
    except Exception as e:
        print(f"Error testing model: {e}")

def main():
    train_palm_model()
    test_model()

if __name__ == "__main__":
    main()
