import os
import shutil
import random


base_dir = "/Users/ishanlahiru/Downloads/archive/PetImages"  
output_dir = "/Users/ishanlahiru/mlp-mixer-project/dataset"

categories = ["Cat", "Dog"]
split_ratio = 0.8  # 80% train, 20% test

for category in categories:
    img_dir = os.path.join(base_dir, category)
    images = os.listdir(img_dir)
    random.shuffle(images)

    split_index = int(len(images) * split_ratio)
    train_images = images[:split_index]
    test_images = images[split_index:]

    # Train folder
    train_path = os.path.join(output_dir, "train", category.lower() + "s")
    os.makedirs(train_path, exist_ok=True)
    for img in train_images:
        src = os.path.join(img_dir, img)
        dst = os.path.join(train_path, img)
        if os.path.isfile(src):
            shutil.copy(src, dst)

    # Test folder
    test_path = os.path.join(output_dir, "test", category.lower() + "s")
    os.makedirs(test_path, exist_ok=True)
    for img in test_images:
        src = os.path.join(img_dir, img)
        dst = os.path.join(test_path, img)
        if os.path.isfile(src):
            shutil.copy(src, dst)

print(" Dataset split into 80% train and 20% test successfully!")
            
