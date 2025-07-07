<template>
  <div class="analysis-results">
    <!-- Header -->
    <div class="results-header">
      <h3 class="results-title">{{ title }}</h3>
      <div v-if="showStatus" class="analysis-status" :class="statusClass">
        {{ statusText }}
      </div>
    </div>

    <!-- Content based on results state -->
    <div class="results-content">
      <!-- No results state -->
      <div v-if="!results" class="no-results">
        <div class="no-results-message">
          <h4>No Results Available</h4>
          <p>Please run an analysis to see results here.</p>
        </div>
      </div>

      <!-- Results available - show with tabs -->
      <div v-else class="results-available">
        <!-- Results Summary -->
        <div class="results-summary">
          <h4>Analysis Summary</h4>
          <div class="summary-grid">
            <div class="summary-item">
              <span class="summary-label">Plant Type:</span>
              <span class="summary-value">{{ plantName }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Plant ID:</span>
              <span class="summary-value">{{ getDisplayText(plantId) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Analysis Date:</span>
              <span class="summary-value">{{ getDisplayText(analysisDate) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Processing Time:</span>
              <span class="summary-value">{{ processingTime }}s</span>
            </div>
          </div>
        </div>

        <!-- Tabs Navigation -->
        <div class="tabs-container">
          <div class="tabs-header">
            <button
              v-for="(tab, index) in tabs"
              :key="index"
              class="tab-button"
              :class="{ active: activeTab === index }"
              @click="activeTab = index"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- Tab Content -->
          <div class="tab-content">
            <!-- Images Tab -->
            <div v-if="activeTab === 0" class="tab-panel">
              <div v-if="mainImages.length">
                <div class="image-grid">
                  <div v-for="img in mainImages" :key="img.label" class="image-item">
                    <h4>{{ img.label }}</h4>
                    <img :src="img.url" :alt="img.label" class="result-image" />
                  </div>
                </div>
              </div>
              <div v-else class="no-images-message">
                <h4>No Images Available</h4>
                <p>No images were found in the analysis results.</p>
                <p><strong>Debug Info:</strong> Plant ID: {{ getDisplayText(plantId) }}, Date: {{ getDisplayText(analysisDate) }}</p>
              </div>
            </div>

            <!-- Texture Images Tab -->
            <div v-else-if="activeTab === 1" class="tab-panel">
              <ImageGrid 
                :images="textureImages"
                :columns="3"
                :image-size="280"
              />
            </div>

            <!-- Vegetation Indices Images Tab -->
            <div v-else-if="activeTab === 2" class="tab-panel">
              <ImageGrid 
                :images="vegetationIndicesImages"
                :columns="4"
                :image-size="200"
              />
            </div>

            <!-- Vegetation Indices Table Tab -->
            <div v-else-if="activeTab === 3" class="tab-panel">
              <!-- <SearchableTable
                :headers="vegetationIndicesHeaders"
                :items="vegetationIndicesData"
                search-placeholder="Search vegetation indices..."
                default-sort="index"
              /> -->
            </div>

            <!-- Texture Features Table Tab -->
            <div v-else-if="activeTab === 4" class="tab-panel">
              <!-- <SearchableTable
                :headers="textureFeaturesHeaders"
                :items="textureFeaturesData"
                search-placeholder="Search texture features..."
                default-sort="feature"
              /> -->
            </div>

            <!-- Morphological Features Table Tab -->
            <div v-else-if="activeTab === 5" class="tab-panel">
              <!-- <SearchableTable
                :headers="morphologicalFeaturesHeaders"
                :items="morphologicalFeaturesData"
                search-placeholder="Search morphological features..."
                default-sort="feature"
              /> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImageGrid from './ImageGrid.vue'
// import SearchableTable from './SearchableTable.vue'

export default {
  name: 'AnalysisResults',
  components: {
    ImageGrid
    // SearchableTable
  },
  props: {
    // Basic props
    plantName: {
      type: String,
      required: true
    },
    
    plantId: {
      type: [String, Object],
      default: null
    },
    
    analysisDate: {
      type: [String, Object],
      default: null
    },
    
    // Results data
    results: {
      type: Object,
      default: null
    },
    
    // Configuration
    title: {
      type: String,
      default: 'Analysis Results'
    },
    
    showStatus: {
      type: Boolean,
      default: true
    },
    
    showCharts: {
      type: Boolean,
      default: true
    }
  },
  
  data() {
    return {
      processingTime: 2.3,
      activeTab: 0,
      
      // Tab definitions
      tabs: [
        { label: 'Images', key: 'images' },
        { label: 'Texture Images', key: 'texture-images' },
        { label: 'Vegetation Indices Images', key: 'veg-indices-images' },
        { label: 'Vegetation Indices Table', key: 'veg-indices-table' },
        { label: 'Texture Features Table', key: 'texture-features-table' },
        { label: 'Morphological Features Table', key: 'morphological-features-table' }
      ]
    };
  },
  
  computed: {
    statusText() {
      if (this.results) return 'Complete';
      return 'No Results';
    },
    
    statusClass() {
      if (this.results) return 'status-complete';
      return 'status-no-results';
    },
    
    mainImages() {
      if (!this.results) {
        console.log('mainImages: no results object');
        return [];
      }
      const keys = ['original', 'mask', 'overlay', 'segmented'];
      const images = keys.filter(k => this.results[k]).map(k => ({ label: this.capitalize(k), key: k, url: this.results[k] }));
      console.log('mainImages computed - results:', this.results);
      if (images.length > 0) {
        console.log(`mainImages: found ${images.length} images`);
      } else {
        console.log('mainImages: no images found');
      }
      return images;
    },
    
    textureImages() {
      if (!this.results) return [];
      
      const textureKeys = [
        'color_original', 'color_grayscale', 'color_lbp', 'color_hog', 'color_lac1', 'color_lac2', 'color_lac3', 'color_ehd',
        'green_original', 'green_grayscale', 'green_lbp', 'green_hog',
        'nir_original', 'nir_grayscale', 'nir_lbp', 'nir_hog'
      ];
      
      return textureKeys
        .filter(key => this.results[key])
        .map(key => ({
          label: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          url: this.results[key]
        }));
    },
    
    vegetationIndicesImages() {
      if (!this.results) return [];
      
      const vegIndexKeys = [
        'ndvi', 'gndvi', 'evi2', 'ndre', 'ndwi', 'ngrdi', 'ari', 'ari2', 'avi', 'ccci', 
        'cigreen', 'cire', 'cvi', 'dswi4', 'dvi', 'exr', 'gemi', 'gosavi', 'grndvi', 
        'grvi', 'gsavi', 'ipvi', 'lci', 'mcari', 'mcari1', 'mcari2', 'mgrvi', 'msavi', 
        'msr', 'mtvi1', 'mtvi2', 'nli', 'osavi', 'pvi', 'rdvi', 'ri', 'rri1', 'sipi2', 
        'sr', 'tcari', 'tcariosavi', 'tndvi', 'tsavi', 'wdvi'
      ];
      
      return vegIndexKeys
        .filter(key => this.results[`vegetation_indices_${key}`])
        .map(key => ({
          label: key.toUpperCase(),
          url: this.results[`vegetation_indices_${key}`]
        }));
    }
  },
  
  methods: {
    getDisplayText(option) {
      if (!option) return '';
      if (typeof option === 'string' || typeof option === 'number') {
        return option.toString();
      }
      return option.label || option.toString();
    },
    capitalize(s) {
      return s.charAt(0).toUpperCase() + s.slice(1);
    }
  },
  
  emits: ['export', 'share']
}
</script>

<style scoped>
.analysis-results {
  padding: 24px;
  position: fixed;
  top: 200px;
  left: 380px;
  width: 77%;
  height: 73%;
  backdrop-filter: blur(30px);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Custom scrollbar styles for the results area */
.analysis-results ::-webkit-scrollbar {
  width: 8px;
}

.analysis-results ::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.analysis-results ::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  transition: background 0.3s ease;
}

.analysis-results ::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.analysis-results ::-webkit-scrollbar-corner {
  background: transparent;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.results-title {
  color: white;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.results-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 8px;
  margin-right: -8px;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) rgba(255, 255, 255, 0.1);
}

.analysis-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.status-complete {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-no-results {
  background: rgba(107, 114, 128, 0.2);
  color: #9ca3af;
  border: 1px solid rgba(107, 114, 128, 0.3);
}

/* No results state */
.no-results {
  text-align: center;
  padding: 40px 20px;
}

.no-results-message h4 {
  color: white;
  font-size: 20px;
  margin-bottom: 16px;
}

.no-results-message p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
}

/* Results available */
.results-available {
  padding-bottom: 20px;
}

.results-available > div {
  margin-bottom: 32px;
}

.results-available h4 {
  color: white;
  font-size: 18px;
  margin-bottom: 16px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.results-summary {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-label {
  font-weight: 500;
}

/* Tabs Styles */
.tabs-container {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

.tabs-header {
  display: flex;
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow-x: auto;
}

.tab-button {
  padding: 12px 20px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  transition: all 0.2s ease;
  border-bottom: 2px solid transparent;
}

.tab-button:hover {
  color: white;
  background: rgba(255, 255, 255, 0.05);
}

.tab-button.active {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border-bottom-color: #4ade80;
}

.tab-content {
  padding: 20px;
}

.tab-panel {
  min-height: 400px;
}

/* Image grid styles */
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.image-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.image-item h4 {
  color: white;
  margin-bottom: 12px;
  font-size: 16px;
}

.result-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.no-images-message {
  text-align: center;
  padding: 40px 20px;
  color: white;
}

.no-images-message h4 {
  font-size: 20px;
  margin-bottom: 16px;
  color: #fbbf24;
}

.no-images-message p {
  margin-bottom: 12px;
  line-height: 1.5;
}

.no-images-message strong {
  color: #4ade80;
}

/* Responsive design */
@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .tabs-header {
    flex-wrap: wrap;
  }
  
  .tab-button {
    flex: 1;
    min-width: 120px;
    text-align: center;
  }
  
  .tab-content {
    padding: 16px;
  }
}
</style>
