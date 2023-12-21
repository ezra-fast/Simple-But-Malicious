# This code requires a Cascade Classifier XML file for police car detection in order to work properly - this is hard to generate

import cv2

def detect_police_cars(image_path, cascade_path):
    # Load the cascade classifier for car detection
    cascade_classifier = cv2.CascadeClassifier(cascade_path)

    # Load and process the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect police cars in the image using the cascade classifier
    cars = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if police cars are detected
    if len(cars) > 0:
        print("Police cars detected!")
        for (x, y, w, h) in cars:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Police Car Detection', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No police cars detected.")

# Provide the paths to the image and cascade classifier XML file
image_path = 'path/to/your/image.jpg'
cascade_path = 'path/to/your/cascade_classifier.xml'

# Call the detect_police_cars function
detect_police_cars(image_path, cascade_path)
