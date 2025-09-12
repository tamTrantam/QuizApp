# IELTS E-Learning Platform - HTML & CSS Documentation

## 📋 Table of Contents

1. [Overview](#overview)

2. [File Structure](#file-structure)

3. [Changes Made](#changes-made)
4. [CSS Module System](#css-module-system)
5. [Hero Section Guide](#hero-section-guide)
6. [HTML Template Structure](#html-template-structure)
7. [How to Edit and Customize](#how-to-edit-and-customize)
8. [Common Tasks](#common-tasks)

---

## 📊 Overview

This documentation explains the modular CSS system and HTML structure created for the IELTS E-Learning platform. The system is designed to be:

- **Modular**: CSS is split into separate files for easy maintenance
- **Reusable**: Components can be used across different pages
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Customizable**: Easy to change colors, fonts, and layouts

---

## 📁 File Structure

The main files and directories are organized as follows:

static/homepage/css/
├── main.css                    # Main CSS file that imports all modules
└── modules/
    ├── variables.css           # Colors, fonts, spacing definitions
    ├── base.css               # Basic HTML element styling
    ├── header.css             # Header and navigation styling
    ├── buttons.css            # All button styles
    ├── cards.css              # Card layouts and hero sections
    ├── quiz.css               # Quiz-specific styling
    ├── footer.css             # Footer styling
    └── responsive.css         # Mobile and tablet adjustments

static/homepage/images/
└── hero-bg.jpg               # Custom hero background image

Homepage/templates/homepage/
└── home.html                 # Main homepage template
```

---

## 🔄 Changes Made

### **1. CSS Modularization (Major Change)**

**Before:**
- Single large `MainPage.css` file (hard to maintain)
- All styles mixed together

**After:**
- 8 separate CSS modules
- Each module handles specific components
- Easy to find and edit specific styles

**Why this is better:**
- **Maintainability**: Find styles quickly
- **Organization**: Related styles grouped together  
- **Collaboration**: Multiple people can work on different modules
- **Performance**: Can load only needed styles

### **2. Hero Section Enhancement**

**Before:**
```css
.hero {
    background: url('placeholder-image') no-repeat center center;
    background-size: cover;
    color: white;
    padding: 120px 20px;
    text-align: center;
}
```

**After:**
```css
.hero {
    /* Enhanced with multiple options */
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    background-size: cover;
    background-position: center center;
    /* Plus 4 different hero image themes */
}
```

**New Features Added:**
- Multiple hero themes (`.hero-ielts`, `.hero-study`, `.hero-books`, `.hero-local`)
- Gradient overlays for better text readability
- Enhanced typography with text shadows
- Responsive design with proper content structure
- Custom image support using Django static files

### **3. Template Structure Improvements**

**Before:**
```html
<div class="hero">
    <h2>Title</h2>
    <p>Description</p>
</div>
```

**After:**
```html
<div class="hero hero-local" style="background-image: ...">
    <div class="hero-content">
        <h2>Title</h2>
        <p>Enhanced description</p>
        <a href="#" class="btn btn-primary">Call to Action</a>
    </div>
</div>
```

---

## 🎨 CSS Module System

### **How It Works:**

1. **main.css** imports all modules:
```css
@import url('modules/variables.css');
@import url('modules/base.css');
@import url('modules/header.css');
/* ... other imports */
```

2. **variables.css** defines global values:
```css
:root {
    --primary: #4a90e2;        /* Main blue color */
    --secondary: #ff6f61;      /* Orange accent */
    --spacing-sm: 10px;        /* Small spacing */
    --spacing-md: 20px;        /* Medium spacing */
}
```

3. **Other modules** use these variables:
```css
.card {
    background: var(--card-bg);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
}
```

### **Benefits:**
- **Consistency**: Same colors/spacing throughout site
- **Easy Updates**: Change one variable, updates everywhere
- **Maintainability**: Find specific styles quickly

---

## 🎯 Hero Section Guide

### **Available Hero Types:**

#### **1. Basic Hero (Gradient Background)**
```html
<div class="hero">
    <div class="hero-content">
        <h2>Your Title</h2>
        <p>Your description</p>
    </div>
</div>
```

#### **2. IELTS Theme Hero**
```html
<div class="hero hero-ielts">
    <div class="hero-content">
        <h2>Your Title</h2>
        <p>Your description</p>
    </div>
</div>
```

#### **3. Study Theme Hero**
```html
<div class="hero hero-study">
    <!-- Content here -->
</div>
```

#### **4. Books Theme Hero**
```html
<div class="hero hero-books">
    <!-- Content here -->
</div>
```

#### **5. Custom Image Hero (Current Implementation)**
```html
<div class="hero hero-local" style="background-image: linear-gradient(rgba(74, 144, 226, 0.7), rgba(255, 111, 97, 0.7)), url('{% static 'homepage/images/hero-bg.jpg' %}');">
    <div class="hero-content">
        <h2>Your Title</h2>
        <p>Your description</p>
        <a href="#" class="btn btn-primary">Button Text</a>
    </div>
</div>
```

### **How Hero Images Work:**

1. **CSS Class**: Defines the basic hero structure
2. **Theme Class**: Adds specific background image and gradient
3. **Inline Style**: For custom images using Django static files
4. **Hero Content**: Wrapper for proper text positioning

---

## 🏗️ HTML Template Structure

### **Current home.html Structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags, title, fonts -->
    <link rel="stylesheet" type="text/css" href="{% static 'homepage/css/main.css' %}">
</head>
<body>

<!-- HEADER SECTION -->
<header>
    <h1>IELTS E-learning Platform</h1>
    <p>Fun, Interactive & Youth-Centered IELTS Learning</p>
</header>

<!-- NAVIGATION MENU -->
<nav>
    <a href="#courses">Courses</a>
    <a href="#quiz">Quick Quiz</a>
    <a href="#practice">Practice Tests</a>
    <a href="#mock">Mock Exams</a>
</nav>

<!-- HERO SECTION -->
<div class="hero hero-local" style="background-image: ...">
    <div class="hero-content">
        <h2>Master IELTS with Interactive Learning</h2>
        <p>Join thousands of students achieving their dream scores...</p>
        <a href="{% url 'quizzes:quiz_list' %}" class="btn btn-primary">Start Learning Today</a>
    </div>
</div>

<!-- COURSES SECTION -->
<div class="section" id="courses">
    <h2>Learning Modules</h2>
    <div class="cards">
        <div class="card">
            <h3>📚 Reading</h3>
            <p>Master reading comprehension...</p>
        </div>
        <!-- More cards -->
    </div>
</div>

<!-- QUIZ SECTION -->
<div class="section" id="quiz">
    <div class="quiz">
        <h2>Ready to Test Your Skills?</h2>
        <p>Take our interactive quizzes...</p>
        <a href="{% url 'quizzes:quiz_list' %}">
            <button>Start Quiz Now</button>
        </a>
    </div>
</div>

<!-- PRACTICE SECTION -->
<div class="section" id="practice">
    <!-- Similar to courses section -->
</div>

<!-- MOCK EXAM SECTION -->
<div class="section" id="mock">
    <!-- Special quiz layout -->
</div>

<!-- FOOTER -->
<footer>
    <p>&copy; 2025 EffioDominion IELTS E-learning Platform...</p>
</footer>

</body>
</html>
```

### **Key Components Explained:**

#### **1. Cards Layout**
```html
<div class="cards">
    <div class="card">
        <h3>Title with Emoji</h3>
        <p>Description text</p>
    </div>
</div>
```
- **cards**: Container that creates responsive grid
- **card**: Individual card with hover effects

#### **2. Quiz Layout**
```html
<div class="quiz">
    <h2>Quiz Title</h2>
    <p>Quiz description</p>
    <button>Action Button</button>
</div>
```
- Special styling with gradient background
- Centered text and prominent button

#### **3. Section Layout**
```html
<div class="section" id="unique-id">
    <!-- Section content -->
</div>
```
- Standard spacing and layout
- ID for navigation links

---

## ✏️ How to Edit and Customize

### **1. Changing Colors**

**Location:** `static/homepage/css/modules/variables.css`

```css
:root {
    --primary: #4a90e2;        /* Change this for main color */
    --secondary: #ff6f61;      /* Change this for accent color */
    --accent: #f5a623;         /* Change this for highlights */
}
```

**Example - Make it green themed:**
```css
:root {
    --primary: #27ae60;        /* Green */
    --secondary: #2ecc71;      /* Light green */
    --accent: #f39c12;         /* Orange accent */
}
```

### **2. Changing Fonts**

**Location:** `static/homepage/css/modules/variables.css`

```css
:root {
    --font-family: 'Poppins', Arial, sans-serif;
    --font-size-base: 16px;
    --font-size-lg: 1.2rem;
    --font-size-xl: 1.5rem;
}
```

**To use different font:**
1. Add font link in HTML head:
```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;600;700&display=swap" rel="stylesheet">
```
2. Update variable:
```css
--font-family: 'Roboto', Arial, sans-serif;
```

### **3. Changing Spacing**

**Location:** `static/homepage/css/modules/variables.css`

```css
:root {
    --spacing-xs: 5px;         /* Extra small */
    --spacing-sm: 10px;        /* Small */
    --spacing-md: 20px;        /* Medium */
    --spacing-lg: 30px;        /* Large */
    --spacing-xl: 40px;        /* Extra large */
    --spacing-xxl: 60px;       /* Extra extra large */
}
```

### **4. Adding New Hero Image**

**Steps:**
1. Add image to `static/homepage/images/`
2. Update template:
```html
<div class="hero hero-local" style="background-image: linear-gradient(rgba(74, 144, 226, 0.7), rgba(255, 111, 97, 0.7)), url('{% static 'homepage/images/your-new-image.jpg' %}');">
```

**Or create new hero theme in CSS:**
```css
.hero.hero-custom {
    background-image: 
        linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
        url('path-to-your-image.jpg');
}
```

### **5. Modifying Card Layouts**

**Location:** `static/homepage/css/modules/cards.css`

**Current card:**
```css
.card {
    background: var(--card-bg);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    transition: var(--transition);
}
```

**Add custom card type:**
```css
.card.card-special {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    color: white;
    border: 2px solid gold;
}
```

**Use in HTML:**
```html
<div class="card card-special">
    <h3>Special Card</h3>
    <p>This card has custom styling</p>
</div>
```

### **6. Adding New Buttons**

**Location:** `static/homepage/css/modules/buttons.css`

**Current buttons:**
- `.btn` - Basic button
- `.btn-primary` - Main action button
- `.btn-secondary` - Secondary action button

**Add new button type:**
```css
.btn-success {
    background: #27ae60;
    color: white;
    border: 2px solid #27ae60;
}

.btn-success:hover {
    background: #2ecc71;
    transform: translateY(-2px);
}
```

---

## 🛠️ Common Tasks

### **1. Change Homepage Hero Image**

1. Add your image to `static/homepage/images/`
2. Update `home.html`:
```html
<div class="hero hero-local" style="background-image: linear-gradient(rgba(74, 144, 226, 0.7), rgba(255, 111, 97, 0.7)), url('{% static 'homepage/images/YOUR-IMAGE.jpg' %}');">
```

### **2. Add New Section to Homepage**

1. Add to `home.html` before footer:
```html
<div class="section" id="new-section">
    <h2 style="text-align: center; margin-bottom: 30px;">New Section Title</h2>
    <div class="cards">
        <div class="card">
            <h3>Feature 1</h3>
            <p>Description</p>
        </div>
        <!-- Add more cards -->
    </div>
</div>
```

2. Add navigation link:
```html
<nav>
    <a href="#courses">Courses</a>
    <a href="#quiz">Quick Quiz</a>
    <a href="#practice">Practice Tests</a>
    <a href="#mock">Mock Exams</a>
    <a href="#new-section">New Section</a> <!-- Add this -->
</nav>
```

### **3. Customize Colors for Dark Theme**

**Update variables.css:**
```css
:root {
    /* Dark theme colors */
    --primary: #3498db;
    --secondary: #e74c3c;
    --bg-main: #2c3e50;
    --bg-secondary: #34495e;
    --text-main: #ecf0f1;
    --text-secondary: #bdc3c7;
    --card-bg: #34495e;
}
```

### **4. Make Cards Bigger/Smaller**

**Update cards.css:**
```css
.card {
    padding: var(--spacing-xl);     /* Bigger cards */
    /* OR */
    padding: var(--spacing-sm);     /* Smaller cards */
}
```

### **5. Change Mobile Breakpoints**

**Update responsive.css:**
```css
/* Current mobile breakpoint */
@media (max-width: 768px) {
    /* Mobile styles */
}

/* Change to different breakpoint */
@media (max-width: 992px) {
    /* Tablet styles */
}
```

---

## 🔧 Technical Notes

### **CSS Variables (Custom Properties)**
- Use `var(--variable-name)` to access variables
- Defined in `:root` selector for global access
- Can be overridden in specific components

### **CSS Grid vs Flexbox**
- **Cards layout**: Uses CSS Grid for responsive columns
- **Hero content**: Uses Flexbox for centering
- **Navigation**: Uses Flexbox for horizontal layout

### **Django Template Integration**
- `{% static %}` tag for CSS and image files
- `{% url %}` tag for internal links
- Must load static files: `{% load static %}`

### **Responsive Design Approach**
- Mobile-first design in responsive.css
- Uses CSS Grid with `auto-fit` and `minmax()`
- Flexible spacing using CSS variables

---

## 🎯 Best Practices

1. **Always use CSS variables** for consistent styling
2. **Test on mobile devices** after making changes
3. **Keep related styles in the same module**
4. **Use semantic class names** (`.hero-content` not `.big-text`)
5. **Comment your custom changes** for future reference
6. **Backup files before major changes**

---

## 📱 Mobile Responsiveness

The system automatically adapts to different screen sizes:

- **Desktop (>768px)**: Full grid layout, large hero
- **Tablet (768px-480px)**: 2-column grid, medium hero  
- **Mobile (<480px)**: Single column, compact hero

**Key responsive features:**
- Cards stack vertically on mobile
- Text sizes scale down appropriately
- Spacing reduces for smaller screens
- Navigation becomes more compact

---

This documentation should help you understand and modify the HTML/CSS system I've created. Each module is designed to be independent, making it easy to customize specific parts without affecting others.