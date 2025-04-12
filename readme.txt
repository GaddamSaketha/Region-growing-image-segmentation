Project Overview:

This project is a web-based image processing application that performs image segmentation using a region-growing algorithm. The segmentation is controlled through user-defined parameters like seed point coordinates, intensity thresholds, and neighborhood connectivity.

Features:

1. Segmentation Algorithm: Implements a region-growing algorithm that expands from a user-specified seed point to similar-intensity regions.
2. Connectivity: Allows choosing between 4- and 8-connectivity to control the region-growing behavior.
3. Intermediate Results: Generates intermediate images at configurable progress stages during segmentation.

Setup Instructions:

1. Python Setup: Ensure you have Python 3.x installed on your system.

2. Required Libraries: Install Flask and Pillow for the application. 
	pip install Flask Pillow

3. Folder Structure:
	Create a folder named files in the same directory as main.py.
	Ensure the following files are available in the project directory:
	main.py (the primary application code)
	templates/index.html (upload and parameter input form)
	templates/result.html (display results)
	static/styles.css (CSS for the web pages)

4. Starting the Server: Run the application by executing the main.py file.
	python main.py

5. Access the Web App: Open a web browser and visit http://localhost:5000.

How to Use the Application:

1. Uploading the Image:
	Click the "Browse" button to select a .pgm image file.
	Provide the X and Y coordinates of the seed point to start segmentation.

2. Setting Parameters:
	Enter the intensity threshold value to limit region growth.
	Choose between 4- or 8-connectivity to control region expansion.

3. Processing the Image:
	Click the "Process Image" button to start segmentation.
	The application will analyze the uploaded image and show two intermediate and one final segmentation results.

Generated Results:
1. Intermediate Results:
	Images captured during the early stages of segmentation.
	Useful for tracking the algorithm's progress.

2. Final Segmentation:
	The complete segmented image with the regions identified.