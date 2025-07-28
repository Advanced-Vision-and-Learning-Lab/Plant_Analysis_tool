<template>
  <div id="upload-data">
    <!-- Background layers -->
    <div class="background-container">
      <!-- Background image layer -->
      <div
        class="background-image"
        :style="backgroundImageStyle"
        v-if="backgroundImage"
      ></div>

      <!-- Gradient overlay -->
      <div
        class="gradient-overlay"
        :style="gradientStyle"
      ></div>
    </div>

    <!-- Content -->
    <div class="app-content">
      <AppHeader :whiteBars="[
        { width: 2216, height: 16, x: -10, y: 175, opacity: 0.8 }]"
      />

      <main class="content">
        <div class="title-container">
          <h1 class="title">Upload Data</h1>
          <div class="back-button" @click="goBack" >
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 12H5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 19L5 12L12 5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="tooltip">Back </div>
          </div>
        </div>
        
        <div class="description">
          Upload your plant images for analysis with our advanced AI-powered tools.
        </div>
        
        <div class="upload-container">
          <div class="upload-area">
            <div class="upload-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M17 8L12 3L7 8" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 3V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="upload-title">Drag and drop your files here</h3>
            <p class="upload-subtitle">or click to browse</p>
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileUpload" 
              multiple 
              accept="image/*"
              class="file-input"
            />
            <button class="browse-button" @click="$refs.fileInput.click()">
              Browse Files
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue'
import backgroundImage from '@/assets/greenhouse-img2.jpg'

export default {
  name: 'UploadData',
  components: {
    AppHeader
  },
  data() {
    return {
      // Background configuration
      backgroundImage: backgroundImage,
      backgroundImageOpacity: 0.8,
      
      // Gradient configuration
      gradientTopColor: '#08B6E0',
      gradientBottomColor: '#05AF6B',
      gradientOpacity: 0.7,
    };
  },
  computed: {
    backgroundImageStyle() {
      if (!this.backgroundImage) return {};
      
      return {
        backgroundImage: `url(${this.backgroundImage})`,
        opacity: this.backgroundImageOpacity
      };
    },
    
    gradientStyle() {
      const topColor = this.hexToRgba(this.gradientTopColor, this.gradientOpacity);
      const bottomColor = this.hexToRgba(this.gradientBottomColor, this.gradientOpacity);
      
      return {
        background: `linear-gradient(to bottom, ${topColor}, ${bottomColor})`
      };
    }
  },
  methods: {
    goBack() {
      this.$router.push({ name: 'HomePage' });
    },
    
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length > 0) {
        console.log('Files selected:', files);
        // TODO: Implement file upload logic
        // You can add your file upload API call here
      }
    },
    
    // Helper method to convert hex color to rgba with opacity
    hexToRgba(hex, opacity) {
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      return `rgba(${r}, ${g}, ${b}, ${opacity})`;
    }
  }
}
</script>

<style>
/* Global styles to remove scrollbars */
html, body {
  overflow: hidden;
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

/* Hide scrollbars for webkit browsers */
::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbars for Firefox */
html {
  scrollbar-width: none;
}
</style>

<style scoped>
#upload-data {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: relative;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

/* Background container that covers the entire screen */
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

/* Background image layer */
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

/* Gradient overlay */
.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Content container */
.app-content {
  position: relative;
  z-index: 1;
  min-height: 97vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  text-align: center;
}

.content {
  width: 100%;
  max-width: 1200px;
}

.title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-top: 200px;
  margin-bottom: 20px;
}

.title {
  color: white;
  font-size: 73px;
  margin-top: -10px;
  margin-bottom: 0px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  font-weight: 900;
}

.back-button {
  position: absolute;
  top: 400px;
  left: 400px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.back-button svg {
  display: block;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.tooltip {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  pointer-events: none;
  backdrop-filter: blur(10px);
}

.back-button:hover .tooltip {
  opacity: 1;
  visibility: visible;
  bottom: -35px;
}

.description {
  color: white;
  font-size: 20px;
  max-width: 450px;
  margin: 0 auto 40px auto;
  text-shadow: 1px 1px 2px rgb(0, 0, 0);
  line-height: 1.6;
  opacity: 0.9;
}

.upload-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 40px;
}

.upload-area {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  min-width: 400px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.15);
}

.upload-icon {
  margin-bottom: 20px;
}

.upload-icon svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.upload-title {
  color: white;
  font-size: 24px;
  margin-bottom: 10px;
  font-weight: 600;
}

.upload-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  margin-bottom: 30px;
}

.file-input {
  display: none;
}

.browse-button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.browse-button:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

/* Responsive design */
@media (max-width: 768px) {
  .title {
    font-size: 48px;
  }
  
  .description {
    font-size: 16px;
    max-width: 350px;
  }
  
  .upload-area {
    min-width: 300px;
    padding: 40px 20px;
  }
  
  .upload-title {
    font-size: 20px;
  }
}
</style>
