# Media File Upload Guide

## ✅ **Image Upload Fix Deployed**

Your Django app now properly serves uploaded media files in both development and production!

## 📸 **How to Upload Images in Django Admin**

### 1. **Access Django Admin**
- Go to: https://quizapp-rx2d.onrender.com/admin/
- Login with your admin credentials

### 2. **Upload Quiz Cover Images**
1. Navigate to **Quizzes** → **Quizzes**
2. Click on any quiz or **Add Quiz**
3. In the **Cover image** field, click **Choose File**
4. Select your image (JPG, PNG, etc.)
5. Click **Save**

### 3. **Supported Image Formats**
- ✅ JPG/JPEG
- ✅ PNG  
- ✅ GIF
- ✅ WebP

### 4. **File Size Recommendations**
- **Optimal size**: 800x400px (2:1 ratio)
- **Max file size**: 5MB (reasonable for web)
- **Format**: JPG for photos, PNG for graphics with transparency

## 🔧 **Technical Implementation**

### **What Was Fixed:**
1. **Custom Media Serving View**: Created `media_views.py` to serve uploaded files in production
2. **URL Configuration**: Added production-specific media URL handling
3. **Security**: Implemented path traversal protection and file validation
4. **Caching**: Added appropriate cache headers for better performance
5. **Fallback System**: Default cover image when no upload is provided

### **File Locations:**
- **Uploads go to**: `/media/quiz_covers/`
- **URLs format**: `https://quizapp-rx2d.onrender.com/media/quiz_covers/filename.jpg`
- **Fallback image**: `/static/homepage/images/default-quiz-cover.svg`

### **Model Usage:**
```python
# In templates, use the safe method:
{{ quiz.get_cover_image_url }}

# This automatically handles:
# - Real uploaded images: /media/quiz_covers/image.jpg
# - Missing images: /static/homepage/images/default-quiz-cover.svg
```

## 🧪 **Testing the Fix**

### **Test Upload:**
1. Go to admin panel
2. Edit any quiz
3. Upload a cover image
4. Save the quiz
5. Visit the quiz list page
6. Your uploaded image should now display properly!

### **Expected Behavior:**
- ✅ Images uploaded via admin display correctly
- ✅ Missing images show default SVG placeholder  
- ✅ Images are cached for better performance
- ✅ No 404 errors for media files

## ⚠️ **Important Notes**

### **Production Considerations:**
- **File Persistence**: Files uploaded on Render may be lost during deployments
- **Recommendation**: For production, consider using cloud storage (AWS S3, Cloudinary, etc.)
- **Current Solution**: Works great for testing and small-scale usage

### **Alternative Solutions** (if needed later):
1. **Cloudinary Integration** (recommended for production)
2. **AWS S3 Storage**
3. **Google Cloud Storage**
4. **Azure Blob Storage**

## 🎯 **Quick Test Steps**

1. **Upload Test**: Go to admin → Quizzes → Upload image → Save
2. **View Test**: Visit quiz list page → Verify image displays
3. **URL Test**: Check browser network tab → Media files return 200 status
4. **Fallback Test**: Remove image → Verify default SVG shows

Your media upload system is now fully functional! 🎉