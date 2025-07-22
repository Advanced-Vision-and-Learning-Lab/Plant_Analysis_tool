<template>
  <div class="analysis-results">

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

        <!-- Tabs Navigation -->
        <div class="tabs-container">
          <div class="tabs-header sticky-tabs">
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
              <div class="tab-header">
                <h3>Main Images</h3>
                <button v-if="mainImages.length" @click="downloadAllImages()" class="download-all-btn">
                  Download All Images
                </button>
              </div>
              <div v-if="mainImages.length">
                <div class="image-grid">
                  <div v-for="img in mainImages" :key="img.label" class="image-item">
                    <h4 class="image-title">{{ img.label }} Image</h4>
                    <img 
                      :src="img.url" 
                      :alt="img.label" 
                      class="result-image clickable" 
                      @click="openImageModal(img)"
                    />
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
              <div class="tab-header">
                <h3>Texture Images</h3>
                <button v-if="textureImages.length" @click="downloadAllImages()" class="download-all-btn">
                  Download All Images
                </button>
              </div>
              <div v-if="textureImages.length">
                <div class="image-grid">
                  <div v-for="img in textureImages" :key="img.label" class="image-item">
                    <h4 class="image-title">{{ img.label }}</h4>
                    <img 
                      :src="img.url" 
                      :alt="img.label" 
                      class="result-image clickable" 
                      @click="openImageModal(img)"
                    />
                  </div>
                </div>
              </div>
              <div v-else class="no-images-message">
                <h4>No Texture Images Available</h4>
                <p>No texture images were found in the analysis results.</p>
              </div>
            </div>

            <!-- Vegetation Indices Images Tab -->
            <div v-else-if="activeTab === 2" class="tab-panel">
              <div class="tab-header">
                <h3>Vegetation Indices Images</h3>
                <button v-if="availableVegIndexImages.length" @click="downloadAllImages()" class="download-all-btn">
                  Download All Images
                </button>
              </div>
              <div v-if="vegIndexList.length">
                <div class="image-grid">
                  <div v-for="(name) in vegIndexList" :key="name" class="image-item">
                    <h4 class="image-title">{{ name }}</h4>
                    <img 
                      v-if="getVegIndexUrl(name)" 
                      :src="getVegIndexUrl(name)" 
                      :alt="name" 
                      class="result-image clickable" 
                      @click="openImageModal({ label: name, url: getVegIndexUrl(name) })"
                    />
                    <div v-else class="no-image-placeholder">
                      <p>No image available for {{ name }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="no-images-message">
                <h4>No Vegetation Indices Available</h4>
                <p>No vegetation indices were found in the analysis results.</p>
              </div>
            </div>

            <!-- Vegetation Indices Table Tab -->
            <div v-else-if="activeTab === 3" class="tab-panel">
              <div class="tab-header">
                <h3>Vegetation Indices Table</h3>
                <button @click="downloadCSV('vegIndex')" class="download-btn">
                  Download CSV
                </button>
              </div>
              <div class="table-controls">
                <input 
                  v-model="vegIndexSearch" 
                  type="text" 
                  placeholder="Search vegetation indices..." 
                  class="search-input"
                />
                
              </div>
              <div v-if="vegIndexItems.length" class="table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th v-for="header in vegIndexHeaders" :key="header.value" @click="sortTable('vegIndex', header.value)" class="sortable-header">
                        {{ header.text }}
                        <span v-if="sortColumn === header.value" class="sort-indicator">
                          {{ sortDirection === 'asc' ? '↑' : '↓' }}
                        </span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in filteredVegIndexItems" :key="item.index">
                      <td v-for="header in vegIndexHeaders" :key="header.value">
                        {{ formatValue(item[header.value]) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="no-data-message">
                <h4>No Vegetation Indices Data Available</h4>
                <p>No vegetation indices data was found in the analysis results.</p>
              </div>
            </div>

            <!-- Texture Features Table Tab -->
            <div v-else-if="activeTab === 4" class="tab-panel">
              <div class="tab-header">
                <h3>Texture Features Table</h3>
                <button @click="downloadCSV('texture')" class="download-btn">
                  Download CSV
                </button>
              </div>
              <div class="table-controls">
                <input 
                  v-model="textureSearch" 
                  type="text" 
                  placeholder="Search texture features..." 
                  class="search-input"
                />
              </div>
              <div v-if="textureItems.length" class="table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th v-for="header in textureHeaders" :key="header.value" @click="sortTable('texture', header.value)" class="sortable-header">
                        {{ header.text }}
                        <span v-if="sortColumn === header.value" class="sort-indicator">
                          {{ sortDirection === 'asc' ? '↑' : '↓' }}
                        </span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in filteredTextureItems" :key="item.feature">
                      <td v-for="header in textureHeaders" :key="header.value">
                        {{ formatValue(item[header.value]) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="no-data-message">
                <h4>No Texture Features Data Available</h4>
                <p>No texture features data was found in the analysis results.</p>
              </div>
            </div>

            <!-- Morphological Features Table Tab -->
            <div v-else-if="activeTab === 5" class="tab-panel">
              <div class="tab-header">
                <h3>Morphological Features Table</h3>
                <button @click="downloadCSV('morph')" class="download-btn">
                  Download CSV
                </button>
              </div>
              <div class="table-controls">
                <input 
                  v-model="morphSearch" 
                  type="text" 
                  placeholder="Search morphological features..." 
                  class="search-input"
                />
              </div>
              <div v-if="morphItems.length" class="table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th v-for="header in morphHeaders" :key="header.value" @click="sortTable('morph', header.value)" class="sortable-header">
                        {{ header.text }}
                        <span v-if="sortColumn === header.value" class="sort-indicator">
                          {{ sortDirection === 'asc' ? '↑' : '↓' }}
                        </span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in filteredMorphItems" :key="item.feature">
                      <td v-for="header in morphHeaders" :key="header.value">
                        {{ formatValue(item[header.value]) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="no-data-message">
                <h4>No Morphological Features Data Available</h4>
                <p>No morphological features data was found in the analysis results.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showModal" class="image-modal" @click="closeImageModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <button class="modal-download" @click="downloadModalImage" title="Download Image">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7,10 12,15 17,10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
          </button>
          <button class="modal-close" @click="closeImageModal" title="Close">×</button>
        </div>
        <img :src="selectedImage.url" :alt="selectedImage.label" class="modal-image" />
        <h3 class="modal-title">{{ selectedImage.label }}</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnalysisResults',
  props: {
    // Basic props
    species: {
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
      showModal: false,
      selectedImage: null,
      
      // Search and sort state
      vegIndexSearch: '',
      textureSearch: '',
      morphSearch: '',
      sortColumn: '',
      sortDirection: 'asc',
      
      // Vegetation indices list (same as ResultViewer.vue)
      vegIndexList: [
        'ARI','ARI2','AVI','CCCI','CIgreen','CIRE','CVI','DSWI4','DVI',
        'EVI2','ExR','GEMI','GNDVI','GOSAVI','GRNDVI','GRVI','GSAVI',
        'IPVI','LCI','MCARI','MCARI1','MCARI2','MGRVI','MSAVI','MSR',
        'MTVI1','MTVI2','NDRE','NDVI','NDWI','NGRDI','NLI','OSAVI',
        'PVI','RDVI','RI','RRI1','SIPI2','SR','TCARI','TCARIOSAVI',
        'TNDVI','TSAVI','WDVI'
      ],
      
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
  
  watch: {
    // Reset to first tab when new results are loaded
    results: {
      handler(newResults) {
        if (newResults) {
          this.activeTab = 0;
        }
      },
      immediate: true
    }
  },
  
  computed: {
    
    // Extract nested result object if present
    nestedResult() {
      if (!this.results) return null;
      for (const key in this.results) {
        if (key.endsWith('_result') && typeof this.results[key] === 'object') {
          return this.results[key];
        }
      }
      return null;
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
      if (!this.results) {
        console.log('textureImages: no result object');
        return [];
      }
      // Find all keys that match texture_{band}_{suffix} and group by band
      const bands = ['color','green','nir','pca','red','red_edge'];
      const suffixes = [
        '01_orig','02_gray','03_lbp','04_hog','05_lac1','06_lac2','07_lac3','08_ehd_map'
      ];
      let images = [];
      console.log('textureImages computed - result:', this.results);
      for (const band of bands) {
        for (const suffix of suffixes) {
          const key = `texture_${band}_${suffix}`;
          if (this.results[key]) {
            images.push({
              label: `${this.capitalize(band)} ${suffix.replace(/\d+_/, '').replace('_', ' ').replace('.png','')}`,
              band,
              suffix,
              url: this.results[key]
            });
          }
        }
      }
      console.log(`textureImages: found ${images.length} texture images`);
      if (images.length > 0) {
        console.log('textureImages: sample image keys found:', images.slice(0, 3).map(img => img.label));
      } else {
        console.log('textureImages: no texture images found');
      }
      return images;
    },
    
    vegetationIndicesImages() {
      if (!this.results) {
        console.log('vegetationIndicesImages: no result object');
        return [];
      }
      
      console.log('vegetationIndicesImages computed - result:', this.results);
      const images = this.vegIndexList
        .filter(key => this.results[`vegetation_indices_${key}`])
        .map(key => ({
          label: key.toUpperCase(),
          url: this.results[`vegetation_indices_${key}`]
        }));
      
      console.log(`vegetationIndicesImages: found ${images.length} vegetation indices images`);
      if (images.length > 0) {
        console.log('vegetationIndicesImages: sample indices found:', images.slice(0, 5).map(img => img.label));
      } else {
        console.log('vegetationIndicesImages: no vegetation indices images found');
        console.log('vegetationIndicesImages: checking for vegetation_indices keys in result:', 
          Object.keys(this.results).filter(key => key.startsWith('vegetation_indices_')));
      }
      return images;
    },
    
    // Table headers for vegetation indices
    vegIndexHeaders() {
      return [
        { text: 'Index', value: 'index' },
        { text: 'Mean', value: 'mean' },
        { text: 'Std', value: 'std' },
        { text: 'Min', value: 'min' },
        { text: 'Max', value: 'max' },
        { text: '25%', value: 'q25' },
        { text: '50%', value: 'median' },
        { text: '75%', value: 'q75' }
      ];
    },
    
    // Table items for vegetation indices
    vegIndexItems() {
      const nested = this.nestedResult;
      if (!nested || !nested.vegetation_features || !Array.isArray(nested.vegetation_features)) return [];
      return nested.vegetation_features;
    },
    
    // Filtered and sorted vegetation indices
    filteredVegIndexItems() {
      let items = this.vegIndexItems;
      
      // Apply search filter
      if (this.vegIndexSearch) {
        const search = this.vegIndexSearch.toLowerCase();
        items = items.filter(item => 
          item.index && item.index.toLowerCase().includes(search)
        );
      }
      
      // Apply sorting
      if (this.sortColumn && this.sortColumn.startsWith('vegIndex_')) {
        const column = this.sortColumn.replace('vegIndex_', '');
        items = [...items].sort((a, b) => {
          const aVal = a[column];
          const bVal = b[column];
          if (this.sortDirection === 'asc') {
            return aVal > bVal ? 1 : -1;
          } else {
            return aVal < bVal ? 1 : -1;
          }
        });
      }
      
      return items;
    },
    
    // Table headers for texture features
    textureHeaders() {
      return [
        { text: 'Feature', value: 'feature' },
        { text: 'Value', value: 'value' }
      ];
    },
    
    // Table items for texture features
    textureItems() {
      const nested = this.nestedResult;
      if (!nested || !nested.texture_features || !Array.isArray(nested.texture_features)) return [];
      // Flatten all features for all bands
      return nested.texture_features.flatMap(obj =>
        Object.entries(obj).map(([feature, value]) => ({
          feature: obj.plant_id ? `${obj.plant_id} - ${feature}` : feature,
          value
        }))
      );
    },
    
    // Filtered and sorted texture features
    filteredTextureItems() {
      let items = this.textureItems;
      
      // Apply search filter
      if (this.textureSearch) {
        const search = this.textureSearch.toLowerCase();
        items = items.filter(item => 
          item.feature && item.feature.toLowerCase().includes(search)
        );
      }
      
      // Apply sorting
      if (this.sortColumn && this.sortColumn.startsWith('texture_')) {
        const column = this.sortColumn.replace('texture_', '');
        items = [...items].sort((a, b) => {
          const aVal = a[column];
          const bVal = b[column];
          if (this.sortDirection === 'asc') {
            return aVal > bVal ? 1 : -1;
          } else {
            return aVal < bVal ? 1 : -1;
          }
        });
      }
      
      return items;
    },
    
    // Table headers for morphology features
    morphHeaders() {
      return [
        { text: 'Feature', value: 'feature' },
        { text: 'Value', value: 'value' }
      ];
    },
    
    // Table items for morphology features
    morphItems() {
      return Object.entries(this.results?.morphology_features || {}).map(([feature, value]) => ({
        feature,
        value
      }));
    },
    
    // Filtered and sorted morphological features
    filteredMorphItems() {
      let items = this.morphItems;
      
      // Apply search filter
      if (this.morphSearch) {
        const search = this.morphSearch.toLowerCase();
        items = items.filter(item => 
          item.feature && item.feature.toLowerCase().includes(search)
        );
      }
      
      // Apply sorting
      if (this.sortColumn && this.sortColumn.startsWith('morph_')) {
        const column = this.sortColumn.replace('morph_', '');
        items = [...items].sort((a, b) => {
          const aVal = a[column];
          const bVal = b[column];
          if (this.sortDirection === 'asc') {
            return aVal > bVal ? 1 : -1;
          } else {
            return aVal < bVal ? 1 : -1;
          }
        });
      }
      
      return items;
    },
    
    // Available vegetation index images for download
    availableVegIndexImages() {
      return this.vegIndexList
        .filter(name => this.getVegIndexUrl(name))
        .map(name => ({
          label: name,
          url: this.getVegIndexUrl(name)
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
    },
    openImageModal(image) {
      this.selectedImage = image;
      this.showModal = true;
    },
    closeImageModal() {
      this.showModal = false;
      this.selectedImage = null;
    },
    sortTable(tableType, column) {
      if (this.sortColumn === `${tableType}_${column}`) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = `${tableType}_${column}`;
        this.sortDirection = 'asc';
      }
    },
    formatValue(value) {
      if (typeof value === 'number') {
        return value.toFixed(4);
      }
      return value;
    },
    downloadCSV(type) {
      let headers = [];
      let items = [];
      
      if (type === 'vegIndex') {
        headers = this.vegIndexHeaders.map(h => h.text);
        items = this.filteredVegIndexItems;
      } else if (type === 'texture') {
        headers = this.textureHeaders.map(h => h.text);
        items = this.filteredTextureItems;
      } else if (type === 'morph') {
        headers = this.morphHeaders.map(h => h.text);
        items = this.filteredMorphItems;
      }
      
      const csv = [
        headers.join(','),
        ...items.map(row => 
          headers.map(h => {
            const value = row[h.toLowerCase()];
            return JSON.stringify(value);
          }).join(',')
        )
      ].join('\n');
      
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${type}_table.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    },
    
    // Get vegetation index image URL by name (same as ResultViewer.vue)
    getVegIndexUrl(name) {
      const key = `vegetation_indices_${name}`;
      return this.results && this.results[key] ? this.results[key] : null;
    },

    // Download all images for a specific type
    downloadAllImages() {
      // let images = [];
      
      // if (type === 'main') {
      //   images = this.mainImages;
      // } else if (type === 'texture') {
      //   images = this.textureImages;
      // } else if (type === 'vegetation') {
      //   images = this.availableVegIndexImages;
      // }
      
      // if (images.length === 0) {
      //   alert('No images to download for this type.');
      //   return;
      // }

      // const zip = new JSZip();
      // const promises = images.map(async (img, index) => {
      //   try {
      //     const response = await fetch(img.url);
      //     if (!response.ok) {
      //       throw new Error(`Failed to fetch ${img.label}`);
      //     }
      //     const blob = await response.blob();
      //     const name = img.label.replace(/[^a-zA-Z0-9]/g, '_'); // Clean up label for filename
      //     return zip.file(`${name}.png`, blob);
      //   } catch (error) {
      //     console.error(`Error downloading ${img.label}:`, error);
      //     return null;
      //   }
      // });

      // Promise.all(promises).then(() => {
      //   zip.generateAsync({ type: "blob" }).then(function(blob) {
      //     const url = window.URL.createObjectURL(blob);
      //     const a = document.createElement('a');
      //     a.href = url;
      //     a.download = `${type}_images.zip`;
      //     a.click();
      //     window.URL.revokeObjectURL(url);
      //   });
      // }).catch(error => {
      //   console.error('Error creating zip file:', error);
      //   alert('Error creating download file. Please try again.');
      // });
    },

    downloadModalImage() {
      if (this.selectedImage && this.selectedImage.url) {
        const a = document.createElement('a');
        a.href = this.selectedImage.url;
        a.download = `${this.selectedImage.label.replace(/[^a-zA-Z0-9]/g, '_')}.png`; // Default to .png
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
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
  width: 76%;
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
  width: 35px;
}

.analysis-results ::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.26);
  border-radius: 4px;
}

.analysis-results ::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  transition: background 0.3s ease;
}

.analysis-results ::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.705);
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
  /* Place the message in the center of the screen */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.no-results-message h4 {
  color: white;
  font-size: 40px;
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
  justify-content: center;
  overflow-x: auto;
}

.sticky-tabs {
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.15);
}

.tab-button {
  padding: 12px 20px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 18px;
  font-weight: 800;
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

/* Image Tab Header */
.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.tab-header h3 {
  color: white;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* Download All Images Button */
.download-all-btn {
  padding: 8px 16px;
  background: #000000;
  color: #ffffff;
  border: 1px solid #000000;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.download-all-btn:hover {
  background: #333333;
  border-color: #333333;
}

.image-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.image-title {
  color: white;
  margin-top: 0px;
  margin-bottom: 12px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: underline;
  text-decoration-color: rgb(255, 255, 255);
  text-underline-offset: 8px;
  text-decoration-thickness: 4px;
}

.result-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-image.clickable {
  cursor: pointer;
}

.result-image.clickable:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
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

.no-image-placeholder {
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.no-image-placeholder p {
  margin: 0;
  font-style: italic;
}

/* Table Controls */
.table-controls {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 14px;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

/* Download Button - Black background with white text */
.download-btn {
  padding: 8px 16px;
  background: #000000;
  color: #ffffff;
  border: 1px solid #000000;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.download-btn:hover {
  background: #333333;
  border-color: #333333;
}

/* Table Styles - More solid background and bolder text */
.table-container {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
  font-size: 14px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.data-table th { 
  background: rgba(255, 255, 255, 0.2);
  padding: 12px 8px;
  text-align: center;
  font-weight: 700;
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  font-size: 22px;
}

.data-table td {
  padding: 10px 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-weight: 600;
  font-size: 18px;
}

.data-table tr:hover {
  background: rgba(255, 255, 255, 0.1);
}

.sortable-header {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s ease;
  text-align: center;
}

.sortable-header:hover {
  background: rgba(255, 255, 255, 0.25);
}

.sort-indicator {
  margin-left: 4px;
  font-weight: bold;
  color: #4ade80;
}

.no-data-message {
  text-align: center;
  padding: 40px 20px;
  color: white;
}

.no-data-message h4 {
  font-size: 20px;
  margin-bottom: 16px;
  color: #fbbf24;
}

.no-data-message p {
  margin-bottom: 12px;
  line-height: 1.5;
}

/* Image Modal Styles */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 10px;
  z-index: 10;
}

.modal-close {
  background: #000000;
  border: none;
  color: #ffffff;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
  font-weight: bold;
}

.modal-close:hover {
  background: #333333;
}

.modal-download {
  background: #000000;
  border: none;
  color: #ffffff;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.modal-download:hover {
  background: #333333;
}

.modal-image {
  max-width: 100%;
  max-height: 55vh;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.modal-title {
  color: #000000;
  margin-top: 16px;
  font-size: 24px;
  font-weight: 600;
}


</style>
