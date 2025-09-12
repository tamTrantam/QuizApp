# EffioDominion CSS Architecture Guide

## 📁 File Structure
```
static/homepage/css/
├── main.css                 # Main entry point - imports all modules
├── MainPage.css             # 🚫 OLD FILE - deprecated
└── modules/
    ├── variables.css        # 🎨 Colors, spacing, theme configuration
    ├── base.css            # 🏗️  Reset, layout, utilities
    ├── header.css          # 🎯 Header & navigation
    ├── buttons.css         # 🔘 All button styles
    ├── cards.css           # 🃏 Card components
    ├── quiz.css            # 📝 Quiz-taking interface
    ├── footer.css          # 🦶 Footer component
    └── responsive.css      # 📱 Mobile-first responsive design
```

## 🎯 Module Purposes

### `variables.css` - Theme Configuration
- CSS custom properties (variables)
- Color palette definitions
- Spacing scale
- Border radius values
- Shadow definitions
- Transition timings

### `base.css` - Foundation
- Global resets and normalizations
- Typography base styles
- Layout utilities (grid, flex)
- Container classes
- Spacing utilities

### `header.css` - Navigation
- Site header styling
- Navigation menu
- Brand/logo area
- Mobile navigation

### `buttons.css` - Interactive Elements
- Button base styles
- Button variants (primary, secondary, outline)
- Button sizes (small, medium, large)
- Button states (hover, disabled, active)
- Special buttons (gradient, social auth)

### `cards.css` - Content Containers
- Basic card layout
- Quiz cards
- Interactive quiz cards
- Hero sections
- Empty states
- Card responsive behavior

### `quiz.css` - Quiz Interface
- Quiz container layout
- Progress bars
- Question cards
- Answer choices
- Media elements (images, audio)
- Reading passages
- Navigation controls

### `footer.css` - Site Footer
- Footer layout and styling
- Footer responsive behavior

### `responsive.css` - Mobile Design
- Mobile-first breakpoints
- Tablet adaptations
- Desktop enhancements
- Print styles
- High DPI support

## 🚀 Usage in Templates

### Primary Method (Recommended)
```html
<link rel="stylesheet" type="text/css" href="{% static 'homepage/css/main.css' %}">
```

### Individual Module (Advanced)
```html
<!-- Only if you need specific modules -->
<link rel="stylesheet" type="text/css" href="{% static 'homepage/css/modules/variables.css' %}">
<link rel="stylesheet" type="text/css" href="{% static 'homepage/css/modules/buttons.css' %}">
```

## 🛠️ Customization Guide

### Adding New Colors
Edit `modules/variables.css`:
```css
:root {
    --new-color: #your-color;
    --new-color-hover: #darker-shade;
}
```

### Creating New Button Styles
Edit `modules/buttons.css`:
```css
.btn-custom {
    background: var(--new-color);
    color: var(--text-white);
}

.btn-custom:hover {
    background: var(--new-color-hover);
}
```

### Adding New Card Variants
Edit `modules/cards.css`:
```css
.card-special {
    border: 2px solid var(--accent);
    background: var(--new-color);
}
```

## 📱 Responsive Breakpoints

- **Mobile**: Default (< 768px)
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px - 1199px
- **Large Desktop**: 1200px+

## 🎨 CSS Variables Quick Reference

### Colors
- `--primary`: #ff6f61 (Main brand color)
- `--secondary`: #4a90e2 (Secondary brand)
- `--accent`: #f5a623 (Accent color)
- `--success`: #28a745 (Success states)
- `--text`: #333 (Primary text)
- `--text-light`: #666 (Secondary text)

### Spacing
- `--spacing-xs`: 5px
- `--spacing-sm`: 10px
- `--spacing-md`: 15px
- `--spacing-lg`: 20px
- `--spacing-xl`: 30px
- `--spacing-xxl`: 40px

### Transitions
- `--transition-fast`: 0.2s ease
- `--transition-normal`: 0.3s ease
- `--transition-slow`: 0.5s ease

## 🔧 Maintenance Tips

1. **Edit individual modules** instead of main.css
2. **Keep variables.css updated** when adding colors/spacing
3. **Test responsive behavior** across all breakpoints
4. **Use CSS custom properties** for consistent theming
5. **Follow BEM methodology** for new class names

## 🚫 Deprecated Files

- `MainPage.css` - Keep for backup, but use `main.css` going forward

## ✅ Benefits of This Structure

- ✅ **Maintainable**: Easy to find and edit specific styles
- ✅ **Scalable**: Add new modules as features grow
- ✅ **Consistent**: Variables ensure unified design
- ✅ **Efficient**: Only load needed styles
- ✅ **Collaborative**: Multiple developers can work on different modules
- ✅ **Modern**: Uses CSS custom properties and modern techniques