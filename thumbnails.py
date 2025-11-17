<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Folder-Based Photo Gallery</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Load Lucide Icons for aesthetic elements -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        /* Custom styles for aesthetic */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f7f5; /* Very light off-white */
            color: #333;
        }
        /* Uses grid instead of columns for a predictable layout when only image name is shown */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }
        
        .photo-card {
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .photo-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Style for the modal background */
        .modal-overlay {
            background-color: rgba(0, 0, 0, 0.95); 
            backdrop-filter: blur(10px);
            z-index: 50;
        }

        /* Watermark Styling - Now dynamically positioned by JS based on image boundaries */
        .watermark-overlay {
            position: absolute; /* Relative to its transformed parent, #zoomableContainer */
            transform: rotate(-10deg); 
            opacity: 0; /* Default hidden, visible when image is loaded */
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            z-index: 10;
            user-select: none; 
            white-space: nowrap;
            /* Added transition for smooth movement/fade-in */
            transition: transform 0.3s ease-out, opacity 0.3s;
        }
        .watermark-visible {
            opacity: 0.15 !important;
        }
        
        /* Make images non-draggable and non-selectable */
        .protected-image {
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            pointer-events: auto; 
            -webkit-user-drag: none;
            user-drag: none;
        }

        /* Styles for the Zoom/Pan Feature */
        #zoomableContainer {
            width: 100%;
            height: 100%;
            overflow: hidden; 
            cursor: zoom-in; 
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative; /* Needed for watermark absolute positioning */
        }

        #modalImage {
            /* MODIFIED: Changed origin to center for proper zoom */
            transform-origin: center center; 
            transition: transform 0.3s ease-out; 
            max-height: 100%;
            max-width: 100%;
            object-fit: contain;
            user-select: none;
        }

        /* Cursor change when zoomed in */
        .panning {
            cursor: grab !important;
        }
        .panning:active {
            cursor: grabbing !important;
        }
        
        /* ADJUSTED: Custom class to shift the image focus UP to show more of the top content (40% from top) */
        .object-center-down {
            object-position: 50% 40%; 
        }

        /* Simple CSS for the loading spinner */
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid #f87171; /* red-400 */
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <!-- Header & Navigation -->
    <header class="bg-white/90 sticky top-0 border-b border-gray-200 shadow-sm z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
            <!-- UPDATED: Branding with Logo and Channel Name -->
            <a href="#" onclick="showPage('category-grid-page')" class="flex items-center space-x-2">
                <img src="logo.jpg" alt="Epic Travel Cuts Logo" class="h-8 w-8 rounded-full" onerror="this.onerror=null;this.src='https://placehold.co/32x32/1a1a1a/ffffff?text=E';" />
                <h1 class="text-2xl font-extrabold tracking-tight text-red-700">EPIC TRAVEL CUTS</h1>
            </a>
            <nav>
                <a href="#" onclick="showPage('category-grid-page')" class="text-gray-600 hover:text-red-700 font-medium transition duration-150 ease-in-out px-3 py-2 rounded-lg">Folders</a>
                <a href="#contact" class="text-gray-600 hover:text-red-700 font-medium transition duration-150 ease-in-out px-3 py-2 rounded-lg">Contact</a>
            </nav>
        </div>
    </header>

    <!-- Hero Section - Now loads dynamically from data.json -->
    <section class="relative h-64 bg-gray-900 flex items-end justify-center overflow-hidden mb-12 pb-8">
        <!-- MODIFIED: Using custom class 'object-center-down' to shift the focus further down (visually) -->
        <img id="heroImage" 
             src="https://placehold.co/1200x400/374151/ffffff?text=Loading+Collections..." 
             alt="Image Collections Banner" 
             class="absolute inset-0 w-full h-full object-cover object-center-down opacity-70"
             onerror="this.onerror=null; this.src='https://placehold.co/1200x400/581c1c/ffffff?text=Image+Collections';"
             loading="lazy">
        <div class="relative z-10 text-center p-4 bg-black/30 rounded-xl">
            <h2 class="text-5xl md:text-6xl font-bold text-white mb-2">Image Collections</h2>
        </div>
    </section>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- ============================================== -->
        <!-- 1. CATEGORY SELECTION VIEW (Folder List) -->
        <!-- ============================================== -->
        <div id="category-grid-page">
            <h2 class="text-3xl font-semibold text-center mb-10 text-gray-800 border-b-2 border-red-700 inline-block pb-1 mx-auto">Select a Folder</h2>
            
            <div id="categoryGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Folder thumbnails injected here by JavaScript -->
                <div id="loadingSpinner" class="col-span-full flex justify-center items-center py-10">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>

        <!-- ============================================== -->
        <!-- 2. PHOTO GALLERY VIEW (Images in Folder) -->
        <!-- ============================================== -->
        <div id="photo-gallery-page" class="hidden">
            <button onclick="showPage('category-grid-page')" 
                    class="mb-6 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition">
                <i data-lucide="arrow-left" class="w-4 h-4 inline-block mr-2 align-middle"></i>
                Back to Folders
            </button>

            <h2 id="galleryTitle" class="text-3xl font-semibold mb-6 text-gray-800 border-b-2 border-red-700 inline-block pb-1"></h2>

            <div id="gallery" class="gallery-grid">
                <!-- Photo cards for the selected folder will be injected here -->
            </div>
        </div>
    </main>
    
    <!-- Contact Section -->
    <section id="contact" class="bg-gray-800 text-white py-16 mt-12">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-4xl font-bold mb-6 text-red-500">Contact Information</h2>
            <!-- UPDATED: Static contact information -->
            <div class="space-y-4 text-lg">
                <div class="flex items-center justify-center space-x-3">
                    <i data-lucide="user" class="w-6 h-6 text-red-400"></i>
                    <span class="font-semibold">Name:</span> 
                    <span>Kasi Viswanadh</span>
                </div>
                <div class="flex items-center justify-center space-x-3">
                    <i data-lucide="mail" class="w-6 h-6 text-red-400"></i>
                    <span class="font-semibold">Email:</span> 
                    <a href="mailto:kasisripada17@gmail.com" class="text-red-300 hover:text-red-100 transition">kasisripada17@gmail.com</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 py-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-400">
            <p>&copy; 2025 EPIC TRAVEL CUTS. All Rights Reserved.</p>
        </div>
    </footer>

    <!-- Image Modal (Simplified - No Sidebar) -->
    <div id="imageModal" class="fixed inset-0 hidden modal-overlay items-center justify-center p-2 md:p-4" onclick="closeModal(event)">
        <div id="modalContentContainer" class="bg-gray-900 rounded-xl shadow-2xl max-w-full max-h-[95vh] w-[95vw] h-[95vh] overflow-hidden" onclick="event.stopPropagation()">
            
            <div id="modalImageArea" class="w-full h-full flex items-center justify-center relative">
                
                <div id="zoomableContainer" 
                     onmousedown="startPan(event)" 
                     onmousemove="panImage(event)" 
                     onmouseup="stopPan()" 
                     onmouseleave="stopPan()"
                     ontouchstart="startPan(event)"
                     ontouchmove="panImage(event)"
                     ontouchend="stopPan()">
                    
                    <img id="modalImage" 
                         src="" 
                         alt="Selected Photo" 
                         class="protected-image"
                         oncontextmenu="return false;"
                         ondragstart="return false;">

                    <!-- UPDATED: Watermark moved inside the zoomable container to move with the image -->
                    <div id="watermark" class="watermark-overlay">EPIC TRAVEL CUTS</div>
                </div>
                
                <!-- Close Button -->
                <button onclick="closeModal()" class="absolute top-2 right-2 p-2 rounded-full bg-black/50 text-white hover:bg-red-700 transition z-20">
                    <i data-lucide="x" class="w-6 h-6"></i>
                </button>

                <!-- Navigation Buttons (Prev/Next) -->
                <button id="prevPhotoBtn" onclick="navigatePhoto(-1)" 
                        class="absolute left-4 top-1/2 transform -translate-y-1/2 p-3 rounded-full bg-black/50 text-white hover:bg-black transition z-20 disabled:opacity-30">
                    <i data-lucide="chevron-left" class="w-8 h-8"></i>
                </button>
                <button id="nextPhotoBtn" onclick="navigatePhoto(1)" 
                        class="absolute right-4 top-1/2 transform -translate-y-1/2 p-3 rounded-full bg-black/50 text-white hover:bg-black transition z-20 disabled:opacity-30">
                    <i data-lucide="chevron-right" class="w-8 h-8"></i>
                </button>

                <!-- Zoom Controls -->
                <div class="absolute bottom-4 right-4 flex space-x-2 z-20">
                    <button id="zoomInBtn" onclick="zoom(true)" class="p-2 rounded-full bg-black/70 text-white hover:bg-black transition disabled:opacity-50" title="Zoom In">
                        <i data-lucide="zoom-in" class="w-6 h-6"></i>
                    </button>
                    <button id="zoomOutBtn" onclick="zoom(false)" class="p-2 rounded-full bg-black/70 text-white hover:bg-black transition disabled:opacity-50" title="Zoom Out">
                        <i data-lucide="zoom-out" class="w-6 h-6"></i>
                    </button>
                </div>
            </div>
            
        </div>
    </div>


    <script>
        // --- PHOTO DATA (Dynamic Loading) ---
        let photos = [];
        
        // --- Global State for Navigation and Zoom/Pan ---
        let currentPhotoList = []; 
        let currentPhotoIndex = -1; 
        let scale = 1;
        let translateX = 0;
        let translateY = 0;
        let isDragging = false;
        let startX = 0;
        let startY = 0;
        const maxScale = 4;
        const minScale = 1;

        // Elements
        let modalImage;
        let zoomableContainer;
        let watermark; 

        // --- Core Utility: Get the final image source URL ---
        const getImageUrl = (rawPath) => `images/${rawPath}`;
        
        // --- Page Navigation Logic ---

        /**
         * Scans the 'photos' array and dynamically builds a list of unique categories
         */
        function getCategories() {
            const categoriesMap = {};
            
            photos.forEach(photo => {
                const folderName = photo.location; 
                
                if (!categoriesMap[folderName]) {
                    categoriesMap[folderName] = { 
                        folderName: folderName, 
                        name: folderName,       
                        // Use thumbnail for the category cover
                        coverImage: photo.thumbnailPath || photo.fullPath 
                    };
                }
            });
            
            const validCategories = Object.values(categoriesMap).filter(cat => cat.folderName.length > 0);
            
            let finalCategories = validCategories.sort((a, b) => a.name.localeCompare(b.name));
            
            return finalCategories;
        }

        function renderCategoryGrid() {
            const categories = getCategories();
            const categoryGridElement = document.getElementById('categoryGrid');
            const loadingSpinner = document.getElementById('loadingSpinner');
            
            loadingSpinner.classList.add('hidden');
            let html = '';

            if (categories.length === 0) {
                categoryGridElement.innerHTML = `<p class="col-span-full text-center text-xl text-gray-500">No folders found. Check your data structure.</p>`;
                return;
            }

            categories.forEach(category => {
                const safeName = category.folderName.replace(/'/g, "\\'"); 
                const imageSource = getImageUrl(category.coverImage); 

                html += `
                    <div class="cursor-pointer group relative overflow-hidden rounded-xl shadow-xl" 
                         onclick="openCategory('${safeName}')">
                        
                        <!-- Background Image (uses thumbnail path) -->
                        <img src="${imageSource}" 
                             alt="${category.name} Collection" 
                             class="w-full h-80 object-cover transition duration-500 group-hover:scale-105"
                             onerror="this.onerror=null; this.src='https://placehold.co/600x320/3c3b37/ffffff?text=${category.name.replace(/\s/g, '+')}';"
                             loading="lazy">
                        
                        <!-- Overlay & Text (Folder Name) -->
                        <div class="absolute inset-0 bg-black/50 group-hover:bg-black/40 transition duration-300 flex items-center justify-center">
                            <h3 class="text-3xl font-bold text-white tracking-wide p-4 border-b-2 border-red-500">${category.name}</h3>
                        </div>
                    </div>
                `;
            });
            
            categoryGridElement.innerHTML = html;
        }
        
        function showPage(pageId) {
            document.getElementById('category-grid-page').classList.add('hidden');
            document.getElementById('photo-gallery-page').classList.add('hidden');

            document.getElementById(pageId).classList.remove('hidden');
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
            lucide.createIcons(); 
        }

        function openCategory(folderName) {
            
            const filteredPhotos = photos.filter(photo => {
                return photo.location === folderName;
            });

            currentPhotoList = filteredPhotos.sort((a, b) => a.title.localeCompare(b.title));
            
            document.getElementById('galleryTitle').textContent = `${folderName} (${filteredPhotos.length} images)`;

            renderGallery(currentPhotoList);
            showPage('photo-gallery-page');
        }


        // Function to render the gallery items (Uses Thumbnail path for speed)
        function renderGallery(photoList) {
            const galleryElement = document.getElementById('gallery');
            let html = '';

            photoList.forEach((photo, index) => { 
                // CRUCIAL: Use thumbnailPath here
                const imageUrl = getImageUrl(photo.thumbnailPath || photo.fullPath); 
                
                html += `
                    <div class="photo-card" onclick="openModal(${index})">
                        <div class="bg-white rounded-xl shadow-lg overflow-hidden cursor-pointer relative">
                            
                            <!-- Image (uses thumbnail) -->
                            <img src="${imageUrl}" 
                                 alt="${photo.title}" 
                                 class="w-full object-cover rounded-t-xl protected-image"
                                 onerror="this.onerror=null; this.src='https://placehold.co/600x400/3c3b37/ffffff?text=Image+Missing';"
                                 loading="lazy"
                                 style="aspect-ratio: 4/3;"
                                 oncontextmenu="return false;"
                                 ondragstart="return false;"> 
                            
                            <!-- Caption (Image File Name Only) -->
                            <div class="p-3 text-center">
                                <p class="text-sm font-medium text-gray-700 truncate">${photo.title}</p>
                            </div>
                        </div>
                    </div>
                `;
            });

            galleryElement.innerHTML = html;
            lucide.createIcons(); 
        }

        // --- CORE MODAL LOGIC (Simplified) ---

        function updateModalContent(photo) {
            // 1. Reset Zoom/Pan state
            scale = minScale;
            translateX = 0;
            translateY = 0;
            modalImage.style.transform = ''; 
            watermark.style.opacity = '0'; // Hide watermark initially
            watermark.classList.remove('watermark-visible');


            // 2. Populate Modal Details (CRUCIAL: Use the fullPath here)
            modalImage.src = getImageUrl(photo.fullPath); 
            
            // 3. Set up onload to position and display watermark
            modalImage.onload = () => {
                // Ensures initial transform and watermark positioning happen after image dimensions are known
                updateTransform(); 
                watermark.classList.add('watermark-visible'); // Show watermark
            };

            // 4. Update Navigation/Zoom controls
            updateTransform(); 
            updateNavigationButtons();
        }

        function openModal(index) {
            if (currentPhotoList.length === 0) return; 

            modalImage = document.getElementById('modalImage');
            zoomableContainer = document.getElementById('zoomableContainer');
            watermark = document.getElementById('watermark'); 
            
            currentPhotoIndex = index;
            const photo = currentPhotoList[currentPhotoIndex];
            
            updateModalContent(photo);

            const modal = document.getElementById('imageModal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            document.body.style.overflow = 'hidden'; 
            lucide.createIcons(); 
        }

        function closeModal(event) {
            if (!event || event.target === document.getElementById('imageModal')) {
                const modal = document.getElementById('imageModal');
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                document.body.style.overflow = ''; 
                currentPhotoIndex = -1; // Reset index
                watermark.classList.remove('watermark-visible'); // Hide watermark
            }
        }

        // --- NAVIGATION LOGIC ---

        function updateNavigationButtons() {
            const prevBtn = document.getElementById('prevPhotoBtn');
            const nextBtn = document.getElementById('nextPhotoBtn');

            const isFirst = currentPhotoIndex <= 0;
            const isLast = currentPhotoIndex >= currentPhotoList.length - 1;

            prevBtn.disabled = isFirst;
            nextBtn.disabled = isLast;

            prevBtn.classList.toggle('opacity-30', isFirst);
            nextBtn.classList.toggle('opacity-30', isLast);
        }

        function navigatePhoto(direction) {
            let newIndex = currentPhotoIndex + direction;
            
            if (newIndex >= 0 && newIndex < currentPhotoList.length) {
                currentPhotoIndex = newIndex;
                const newPhoto = currentPhotoList[currentPhotoIndex];
                updateModalContent(newPhoto);
            }
        }
        
        // --- ZOOM/PAN CONTROL FUNCTIONS ---
        function updateTransform() {
            modalImage.style.transform = `scale(${scale}) translate(${translateX}px, ${translateY}px)`;
            
            // --- Watermark Logic ---
            if (modalImage.offsetHeight > 0 && watermark) {
                // Get the size of the unscaled image (imited by the modal container)
                const imgWidth = modalImage.offsetWidth;
                const imgHeight = modalImage.offsetHeight;
                const wmWidth = watermark.offsetWidth;
                const wmHeight = watermark.offsetHeight;

                // 1. Calculate Initial Position (Offset from the center to the bottom-right corner of the image)
                const margin = 30; // Inner padding from the image edge
                const initialOffsetX = (imgWidth / 2) - (wmWidth / 2) - margin;
                const initialOffsetY = (imgHeight / 2) - (wmHeight / 2) - margin;
                
                // 2. Apply Combined Transform to lock watermark to the image surface
                watermark.style.transform = 
                    `translate(${initialOffsetX}px, ${initialOffsetY}px) ` + 
                    `scale(${scale}) ` +                                      
                    `translate(${translateX}px, ${translateY}px) ` +          
                    `rotate(-10deg)`;                                        
            }
            // --- End Watermark Logic ---


            document.getElementById('zoomInBtn').disabled = scale >= maxScale;
            document.getElementById('zoomOutBtn').disabled = scale <= minScale;
            if (scale > minScale) {
                zoomableContainer.classList.add('panning');
                zoomableContainer.style.cursor = 'grab';
            } else {
                zoomableContainer.classList.remove('panning');
                zoomableContainer.style.cursor = 'zoom-in';
            }
        }
        function centerImage() {
            translateX = 0;
            translateY = 0;
        }
        function zoom(zoomIn) {
            const newScale = zoomIn ? Math.min(maxScale, scale + 0.5) : Math.max(minScale, scale - 0.5);
            if (newScale !== scale) {
                scale = newScale;
                if (scale === minScale) {
                    centerImage();
                }
                updateTransform();
            }
        }
        function startPan(e) {
            if (scale > minScale && (e.button === 0 || e.touches)) {
                e.preventDefault();
                isDragging = true;
                const clientX = e.clientX || e.touches[0].clientX;
                const clientY = e.clientY || e.touches[0].clientY;
                startX = clientX - translateX * scale; 
                startY = clientY - translateY * scale; 
                zoomableContainer.style.cursor = 'grabbing';
            }
        }
        function panImage(e) {
            if (!isDragging || scale <= minScale) return;
            e.preventDefault();

            const clientX = e.clientX || e.touches[0].clientX;
            const clientY = e.clientY || e.touches[0].clientY;
            
            let newX = (clientX - startX) / scale;
            let newY = (clientY - startY) / scale;
            
            const container = zoomableContainer.getBoundingClientRect();
            const imgWidthNatural = modalImage.offsetWidth; 
            const imgHeightNatural = modalImage.offsetHeight;
            
            // X-axis limits
            if (imgWidthNatural * scale > container.width) {
                const maxPanX = (imgWidthNatural * scale - container.width) / (2 * scale); 
                newX = Math.min(Math.max(newX, -maxPanX), maxPanX);
            } else {
                newX = 0;
            }

            // Y-axis limits
            if (imgHeightNatural * scale > container.height) {
                const maxPanY = (imgHeightNatural * scale - container.height) / (2 * scale);
                newY = Math.min(Math.max(newY, -maxPanY), maxPanY);
            } else {
                newY = 0;
            }

            translateX = newX;
            translateY = newY;
            updateTransform();
        }
        function stopPan() {
            isDragging = false;
            if (scale > minScale) {
                zoomableContainer.style.cursor = 'grab';
            }
        }
        function handleScrollZoom(e) {
            if (document.getElementById('imageModal').classList.contains('flex')) {
                e.preventDefault();
                const zoomIn = e.deltaY < 0; 
                zoom(zoomIn);
            }
        }
        
        /**
         * Loads image data from the data.json file.
         */
        async function loadPhotoData() {
            const loadingSpinner = document.getElementById('loadingSpinner');
            loadingSpinner.classList.remove('hidden');

            const fallbackFileNames = [
                { full: "Arches/IMG_7140.jpeg", thumbnail: "Arches/IMG_7140_thumb.jpeg" },
                { full: "Canyonlands/IMG_7071.jpeg", thumbnail: "Canyonlands/IMG_7071_thumb.jpeg" },
                { full: "Arches/IMG_7092.jpeg", thumbnail: "Arches/IMG_7092_thumb.jpeg" }
            ];
            let rawData = fallbackFileNames;

            try {
                const response = await fetch('data.json');
                if (!response.ok) {
                    console.warn(`Could not fetch data.json. Using fallback demo data.`);
                } else {
                    const fetchedData = await response.json();
                    // Assume fetchedData is an array of objects like { "full": "...", "thumbnail": "..." }
                    rawData = fetchedData.map(item => typeof item === 'string' ? { full: item, thumbnail: item } : item);
                }

            } catch (error) {
                console.error("Failed to load data.json. Using fallback demo data.", error);
            }
            
            // Process the raw data into the 'photos' structure
            photos = rawData.map((data, index) => {
                const fullPath = data.full;
                const thumbnailPath = data.thumbnail || data.full; // Fallback to full if thumbnail is missing
                
                const parts = fullPath.split('/');
                const folderName = parts[0]; 
                const fileNameOnly = parts.length > 1 ? parts[1] : fullPath; 
                
                if (parts.length > 1) {
                    return {
                        id: index + 1,
                        title: fileNameOnly, 
                        location: folderName, 
                        fullPath: fullPath, // High resolution for modal
                        thumbnailPath: thumbnailPath, // Low resolution for gallery
                    };
                }
                return null;
            }).filter(photo => photo !== null); 
            
            renderCategoryGrid();
            setHeroBanner();
        }

        /**
         * Sets the hero banner image dynamically.
         */
        function setHeroBanner() {
            const heroImageElement = document.getElementById('heroImage');
            if (!heroImageElement || photos.length === 0) return;
            
            // Try to find a photo whose title or path suggests a good banner image
            const bannerPhoto = photos.find(p => p.title.toLowerCase().includes('road') || p.location === 'Canyonlands');
            
            if (bannerPhoto) {
                // Use the fullPath for a quality banner image
                heroImageElement.src = getImageUrl(bannerPhoto.fullPath);
                heroImageElement.alt = "Hero Banner: " + bannerPhoto.location;
            } else {
                // Fallback: Use the cover image of the first category
                const categories = getCategories();
                if (categories.length > 0) {
                    heroImageElement.src = getImageUrl(categories[0].coverImage); 
                    heroImageElement.alt = `Hero Banner: ${categories[0].name} Collection`;
                }
            }
        }


        // Initialize the category grid on page load
        window.onload = () => {
            loadPhotoData(); 
            document.addEventListener('wheel', handleScrollZoom, { passive: false });
        };

        // Add a keyboard listener for closing the modal with the Escape key
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('imageModal').classList.contains('flex')) {
                if (e.key === 'Escape') {
                    closeModal();
                } else if (e.key === 'ArrowRight') {
                    navigatePhoto(1);
                } else if (e.key === 'ArrowLeft') {
                    navigatePhoto(-1);
                }
            }
        });

    </script>
</body>
</html>