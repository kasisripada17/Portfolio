Desert Vistas Photography Portfolio

📸 Project Overview

This repository hosts the Desert Vistas Photography Portfolio, a static website showcasing the "Red Earth Collection," which features stunning photography of the American Southwest and various global locations. The site is designed to be fully responsive, visually engaging, and provides a clear presentation of high-quality images using a responsive grid layout.

The project utilizes a custom data structure (JavaScript array) to manage image metadata, ensuring easy updates and integration with dynamic features like the image modal viewer.

✨ Features

Responsive Gallery Grid: Uses CSS columns to create a dynamic, masonry-style gallery that adapts beautifully to mobile, tablet, and desktop screens.

Image Modal Viewer: Clicking on any image opens a full-screen modal showing the image in high detail along with its title, location, and description.

Watermarking: Images are protected with a visible watermark on both the gallery tiles and the modal viewer.

Asset Protection: JavaScript is used to prevent right-click context menus and dragging on images, adding a layer of basic protection.

Minimalist Design: Built using Tailwind CSS for a clean, modern, and high-contrast user interface.

Contact Form: A simple contact section is included for user inquiries (currently simulated for demonstration).

🛠 Technologies Used

HTML5: Structure of the web page.

CSS3 (via Tailwind CSS): Utility-first styling for rapid, responsive design.

JavaScript (ES6+): For gallery rendering, modal logic, and interaction handling.

Lucide Icons: Simple, modern icons for UI elements.

🚀 Setup and Installation

This is a static HTML/CSS/JavaScript project, meaning no complex backend setup is required.

Clone the repository:

git clone [YOUR_REPO_URL]
cd desert-vistas-portfolio


Add Image Assets:
The project expects image files to be located in a directory named images/ relative to the index.html file. Ensure your image files match the names listed in the photos JavaScript array in index.html.

Run Locally (Recommended):
For the best experience and to prevent cross-origin issues, you should run the project using a local web server. Python is the easiest way:

# If you have Python 3
python3 -m http.server 8000

# Or, if you have Python 2
python -m SimpleHTTPServer 8000


Access:
Open your web browser and navigate to http://localhost:8000.

🖼 Customizing the Gallery

To add or remove photos, modify the photos JavaScript array located inside the <script> tag at the bottom of index.html:

const photos = [
    { id: 1, title: "Grand Arch", location: "Arches National Park, UT", description: "...", filepath: "arches_arch.jpeg", ratio: "3/2", dimensions: "4500x3000 px" },
    // Add new objects here
];


Make sure that:

The id is unique.

The filepath exactly matches the file name in your images/ folder.

The ratio is set correctly (e.g., "4/3", "3/2", "16/9") to help with the visual layout.

🤝 Contributing

Contributions are welcome! If you have suggestions for improving the code, performance, or accessibility, please feel free to submit a pull request or open an issue.
