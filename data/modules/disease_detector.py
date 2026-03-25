import os
import json
import numpy as np
from PIL import Image
import tf_keras as keras
from tf_keras.applications import MobileNetV2
from tf_keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tf_keras.models import Model
from tf_keras.preprocessing.image import ImageDataGenerator

DATA_DIR   = "data/datasets/color"
MODEL_DIR  = "data/models"
IMG_SIZE   = 224
BATCH_SIZE = 32

def train_and_save_disease_model():
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        subset='training',
        class_mode='categorical'
    )

    val_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        subset='validation',
        class_mode='categorical'
    )

    # Save class labels
    class_labels = {v: k for k, v in train_gen.class_indices.items()}
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(f"{MODEL_DIR}/class_labels.json", "w") as f:
        json.dump(class_labels, f)

    # MobileNetV2 - freeze base
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False

    x      = base_model.output
    x      = GlobalAveragePooling2D()(x)
    x      = Dense(128, activation='relu')(x)
    x      = Dropout(0.3)(x)
    output = Dense(len(class_labels), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("🚀 Training started...")
    model.fit(train_gen, epochs=5, validation_data=val_gen, verbose=1)

    model.save(f"{MODEL_DIR}/disease_model.keras")
    print("✅ Disease model saved!")

def predict_disease(image):
    model = keras.models.load_model(f"{MODEL_DIR}/disease_model.keras")
    with open(f"{MODEL_DIR}/class_labels.json") as f:
        class_labels = json.load(f)

    img       = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)[0]
    top3_idx    = predictions.argsort()[-3:][::-1]

    results = []
    for idx in top3_idx:
        label      = class_labels[str(idx)]
        parts      = label.split("__")
        plant      = parts[0] if len(parts) > 0 else label
        disease    = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
        confidence = round(float(predictions[idx]) * 100, 2)
        results.append({
            "plant":      plant,
            "disease":    disease,
            "confidence": confidence,
            "raw_label":  label
        })

    return results

if __name__ == "__main__":
    train_and_save_disease_model()