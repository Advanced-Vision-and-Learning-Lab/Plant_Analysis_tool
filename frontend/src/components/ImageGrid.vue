<template>
  <div class="image-grid-container">
    <!-- Image Grid -->
    <div class="image-grid" :style="{ gridTemplateColumns: `repeat(${columns}, 1fr)` }">
      <div 
        v-for="(image, index) in images" 
        :key="index" 
        class="image-item"
        @click="openLightbox(index)"
      >
        <div class="image-wrapper">
          <img 
            :src="image.url" 
            :alt="image.label || `Image ${index + 1}`"
            class="grid-image"
            :style="{ maxWidth: imageSize + 'px', maxHeight: imageSize + 'px' }"
          />
          <div class="image-overlay">
            <div class="image-label">{{ image.label || `Image ${index + 1}` }}</div>
            <div class="image-actions">
              <button 
                class="action-btn download-btn"
                @click.stop="downloadImage(image.url, image.label)"
                title="Download Image"
              >
                📥
              </button>
              <button 
                class="action-btn zoom-btn"
                @click.stop="openLightbox(index)"
                title="Enlarge Image"
              >
                🔍
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <div v-if="showLightbox" class="lightbox-overlay" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <div class="lightbox-header">
          <h3>{{ currentImage?.label || `Image ${currentIndex + 1}` }}</h3>
          <div class="lightbox-actions">
            <button 
              class="lightbox-btn"
              @click="downloadImage(currentImage?.url, currentImage?.label)"
              title="Download"
            >
              📥
            </button>
            <button 
              class="lightbox-btn close-btn"
              @click="closeLightbox"
              title="Close"
            >
              ✕
            </button>
          </div>
        </div>
        <div class="lightbox-image-container">
          <button 
            v-if="images.length > 1" 
            class="nav-btn prev-btn"
            @click="previousImage"
            :disabled="currentIndex === 0"
          >
            ‹
          </button>
          <img 
            :src="currentImage?.url" 
            :alt="currentImage?.label || `Image ${currentIndex + 1}`"
            class="lightbox-image"
          />
          <button 
            v-if="images.length > 1" 
            class="nav-btn next-btn"
            @click="nextImage"
            :disabled="currentIndex === images.length - 1"
          >
            ›
          </button>
        </div>
        <div v-if="images.length > 1" class="lightbox-footer">
          <span class="image-counter">{{ currentIndex + 1 }} / {{ images.length }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageGrid',
  props: {
    images: {
      type: Array,
      required: true,
      default: () => []
    },
    columns: {
      type: Number,
      default: 4
    },
    imageSize: {
      type: Number,
      default: 200
    },
    showLabels: {
      type: Boolean,
      default: true
    }
  },
  
  data() {
    return {
      showLightbox: false,
      currentIndex: 0
    };
  },
  
  computed: {
    currentImage() {
      return this.images[this.currentIndex];
    }
  },
  
  methods: {
    openLightbox(index) {
      this.currentIndex = index;
      this.showLightbox = true;
      document.body.style.overflow = 'hidden';
    },
    
    closeLightbox() {
      this.showLightbox = false;
      document.body.style.overflow = 'auto';
    },
    
    previousImage() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    
    nextImage() {
      if (this.currentIndex < this.images.length - 1) {
        this.currentIndex++;
      }
    },
    
    downloadImage(url, label) {
      if (!url) return;
      
      const a = document.createElement('a');
      a.href = url;
      a.download = label ? `${label}.png` : url.split('/').pop();
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    
    // Keyboard navigation
    handleKeydown(event) {
      if (!this.showLightbox) return;
      
      switch (event.key) {
        case 'Escape':
          this.closeLightbox();
          break;
        case 'ArrowLeft':
          this.previousImage();
          break;
        case 'ArrowRight':
          this.nextImage();
          break;
      }
    }
  },
  
  mounted() {
    document.addEventListener('keydown', this.handleKeydown);
  },
  
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleKeydown);
    document.body.style.overflow = 'auto';
  }
};
</script>

<style scoped>
.image-grid-container {
  width: 100%;
}

.image-grid {
  display: grid;
  gap: 16px;
  padding: 16px;
}

.image-item {
  position: relative;
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.image-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.grid-image {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
  transition: filter 0.2s ease;
}

.image-item:hover .grid-image {
  filter: brightness(0.8);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12px;
  opacity: 0;
  transition: opacity 0.2s ease;
  border-radius: 8px;
}

.image-item:hover .image-overlay {
  opacity: 1;
}

.image-label {
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-align: center;
  margin-bottom: 8px;
}

.image-actions {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 4px;
  padding: 6px 8px;
  cursor: pointer;
  color: white;
  font-size: 14px;
  transition: background 0.2s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Lightbox Styles */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.lightbox-content {
  background: white;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.lightbox-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.lightbox-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.lightbox-actions {
  display: flex;
  gap: 8px;
}

.lightbox-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 16px;
  transition: background 0.2s ease;
}

.lightbox-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.close-btn {
  font-size: 18px;
  font-weight: bold;
}

.lightbox-image-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  min-height: 400px;
}

.lightbox-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 50%;
  font-size: 24px;
  transition: background 0.2s ease;
}

.nav-btn:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.7);
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.prev-btn {
  left: 20px;
}

.next-btn {
  right: 20px;
}

.lightbox-footer {
  padding: 12px 20px;
  text-align: center;
  border-top: 1px solid #eee;
  background: #f8f9fa;
}

.image-counter {
  color: #666;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .image-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 12px;
    padding: 12px;
  }
  
  .lightbox-content {
    max-width: 95vw;
    max-height: 95vh;
  }
  
  .lightbox-image-container {
    padding: 10px;
    min-height: 300px;
  }
  
  .nav-btn {
    padding: 8px 12px;
    font-size: 20px;
  }
  
  .prev-btn {
    left: 10px;
  }
  
  .next-btn {
    right: 10px;
  }
}

@media (max-width: 480px) {
  .image-grid {
    grid-template-columns: 1fr !important;
  }
}
</style> 