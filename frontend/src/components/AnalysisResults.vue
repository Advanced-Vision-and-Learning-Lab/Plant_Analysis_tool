<template>
  <div class="analysis-results">
    <!-- Header -->
    <div class="results-header">
      <h3 class="results-title">{{ title }}</h3>
      <div v-if="showStatus" class="analysis-status" :class="statusClass">
        {{ statusText }}
      </div>
    </div>

    <!-- Content based on analysis state -->
    <div class="results-content">
      <!-- Pre-analysis state -->
      <div v-if="!hasStartedAnalysis" class="pre-analysis">
        <div class="selection-display">
          <h1 class="plant-selection">
            You have selected: <strong>{{ plantName }}</strong>
          </h1>
          
          <div v-if="plantId || analysisDate" class="additional-info">
            <div v-if="plantId" class="info-item">
              <span class="label">Plant ID:</span>
              <span class="value">{{ getDisplayText(plantId) }}</span>
            </div>
            <div v-if="analysisDate" class="info-item">
              <span class="label">Analysis Date:</span>
              <span class="value">{{ getDisplayText(analysisDate) }}</span>
            </div>
          </div>
          
          <div class="instruction-text">
            <p>Configure your analysis parameters and click "Start Analysis" to begin processing.</p>
          </div>
        </div>
      </div>

      <!-- Analysis in progress -->
      <div v-else-if="isAnalyzing" class="analysis-progress">
        <div class="progress-indicator">
          <div class="spinner"></div>
          <h4>Analysis in Progress</h4>
          <p>Processing {{ plantName }} data...</p>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${analysisProgress}%` }"></div>
          </div>
          <span class="progress-text">{{ analysisProgress }}% Complete</span>
        </div>
      </div>

      <!-- Analysis complete - show results with tabs -->
      <div v-else class="analysis-complete">
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
              <ImageGrid 
                :images="mainImages"
                :columns="4"
                :image-size="250"
              />
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
              <SearchableTable
                :headers="vegetationIndicesHeaders"
                :items="vegetationIndicesData"
                search-placeholder="Search vegetation indices..."
                default-sort="index"
              />
            </div>

            <!-- Texture Features Table Tab -->
            <div v-else-if="activeTab === 4" class="tab-panel">
              <SearchableTable
                :headers="textureFeaturesHeaders"
                :items="textureFeaturesData"
                search-placeholder="Search texture features..."
                default-sort="feature"
              />
            </div>

            <!-- Morphological Features Table Tab -->
            <div v-else-if="activeTab === 5" class="tab-panel">
              <SearchableTable
                :headers="morphologicalFeaturesHeaders"
                :items="morphologicalFeaturesData"
                search-placeholder="Search morphological features..."
                default-sort="feature"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImageGrid from './ImageGrid.vue'
import SearchableTable from './SearchableTable.vue'

export default {
  name: 'AnalysisResults',
  components: {
    ImageGrid,
    SearchableTable
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
    
    // Analysis state
    hasStartedAnalysis: {
      type: Boolean,
      default: false
    },
    
    isAnalyzing: {
      type: Boolean,
      default: false
    },
    
    analysisProgress: {
      type: Number,
      default: 0
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
    },
    
    // Custom results data
    customResults: {
      type: Array,
      default: null
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
      ],

      // Main images data
      mainImages: [
        { url: 'https://via.placeholder.com/400x300/4ade80/ffffff?text=Original+Image', label: 'Original Image' },
        { url: 'https://via.placeholder.com/400x300/60a5fa/ffffff?text=Segmentation+Mask', label: 'Segmentation Mask' },
        { url: 'https://via.placeholder.com/400x300/fbbf24/ffffff?text=Overlay+Viz', label: 'Overlay Visualization' },
        { url: 'https://via.placeholder.com/400x300/ef4444/ffffff?text=Segmented+Plant', label: 'Segmented Plant' }
      ],

      // Texture images data
      textureImages: [
        { url: 'https://via.placeholder.com/300x300/4ade80/ffffff?text=Color+Original', label: 'Color Original' },
        { url: 'https://via.placeholder.com/300x300/6b7280/ffffff?text=Color+Grayscale', label: 'Color Grayscale' },
        { url: 'https://via.placeholder.com/300x300/8b5cf6/ffffff?text=Color+LBP', label: 'Color LBP' },
        { url: 'https://via.placeholder.com/300x300/ec4899/ffffff?text=Color+HOG', label: 'Color HOG' },
        { url: 'https://via.placeholder.com/300x300/f59e0b/ffffff?text=Color+Lac1', label: 'Color Lacunarity 1' },
        { url: 'https://via.placeholder.com/300x300/10b981/ffffff?text=Color+Lac2', label: 'Color Lacunarity 2' },
        { url: 'https://via.placeholder.com/300x300/3b82f6/ffffff?text=Color+Lac3', label: 'Color Lacunarity 3' },
        { url: 'https://via.placeholder.com/300x300/ef4444/ffffff?text=Color+EHD', label: 'Color EHD Map' },
        { url: 'https://via.placeholder.com/300x300/22c55e/ffffff?text=Green+Original', label: 'Green Original' },
        { url: 'https://via.placeholder.com/300x300/6b7280/ffffff?text=Green+Grayscale', label: 'Green Grayscale' },
        { url: 'https://via.placeholder.com/300x300/8b5cf6/ffffff?text=Green+LBP', label: 'Green LBP' },
        { url: 'https://via.placeholder.com/300x300/ec4899/ffffff?text=Green+HOG', label: 'Green HOG' },
        { url: 'https://via.placeholder.com/300x300/84cc16/ffffff?text=NIR+Original', label: 'NIR Original' },
        { url: 'https://via.placeholder.com/300x300/6b7280/ffffff?text=NIR+Grayscale', label: 'NIR Grayscale' },
        { url: 'https://via.placeholder.com/300x300/8b5cf6/ffffff?text=NIR+LBP', label: 'NIR LBP' },
        { url: 'https://via.placeholder.com/300x300/ec4899/ffffff?text=NIR+HOG', label: 'NIR HOG' }
      ],

      // Vegetation indices images data
      vegetationIndicesImages: [
        { url: 'https://via.placeholder.com/200x200/22c55e/ffffff?text=NDVI', label: 'NDVI' },
        { url: 'https://via.placeholder.com/200x200/16a34a/ffffff?text=GNDVI', label: 'GNDVI' },
        { url: 'https://via.placeholder.com/200x200/15803d/ffffff?text=EVI2', label: 'EVI2' },
        { url: 'https://via.placeholder.com/200x200/166534/ffffff?text=NDRE', label: 'NDRE' },
        { url: 'https://via.placeholder.com/200x200/14532d/ffffff?text=NDWI', label: 'NDWI' },
        { url: 'https://via.placeholder.com/200x200/134e4a/ffffff?text=NGRDI', label: 'NGRDI' },
        { url: 'https://via.placeholder.com/200x200/0f766e/ffffff?text=ARI', label: 'ARI' },
        { url: 'https://via.placeholder.com/200x200/115e59/ffffff?text=ARI2', label: 'ARI2' },
        { url: 'https://via.placeholder.com/200x200/134e4a/ffffff?text=AVI', label: 'AVI' },
        { url: 'https://via.placeholder.com/200x200/14532d/ffffff?text=CCCI', label: 'CCCI' },
        { url: 'https://via.placeholder.com/200x200/166534/ffffff?text=CIgreen', label: 'CIgreen' },
        { url: 'https://via.placeholder.com/200x200/15803d/ffffff?text=CIRE', label: 'CIRE' },
        { url: 'https://via.placeholder.com/200x200/16a34a/ffffff?text=CVI', label: 'CVI' },
        { url: 'https://via.placeholder.com/200x200/22c55e/ffffff?text=DSWI4', label: 'DSWI4' },
        { url: 'https://via.placeholder.com/200x200/4ade80/ffffff?text=DVI', label: 'DVI' },
        { url: 'https://via.placeholder.com/200x200/65a30d/ffffff?text=ExR', label: 'ExR' },
        { url: 'https://via.placeholder.com/200x200/84cc16/ffffff?text=GEMI', label: 'GEMI' },
        { url: 'https://via.placeholder.com/200x200/a3e635/ffffff?text=GOSAVI', label: 'GOSAVI' },
        { url: 'https://via.placeholder.com/200x200/bef264/ffffff?text=GRNDVI', label: 'GRNDVI' },
        { url: 'https://via.placeholder.com/200x200/d9f99d/ffffff?text=GRVI', label: 'GRVI' },
        { url: 'https://via.placeholder.com/200x200/ecfccb/ffffff?text=GSAVI', label: 'GSAVI' },
        { url: 'https://via.placeholder.com/200x200/f7fee7/ffffff?text=IPVI', label: 'IPVI' },
        { url: 'https://via.placeholder.com/200x200/22c55e/ffffff?text=LCI', label: 'LCI' },
        { url: 'https://via.placeholder.com/200x200/16a34a/ffffff?text=MCARI', label: 'MCARI' },
        { url: 'https://via.placeholder.com/200x200/15803d/ffffff?text=MCARI1', label: 'MCARI1' },
        { url: 'https://via.placeholder.com/200x200/166534/ffffff?text=MCARI2', label: 'MCARI2' },
        { url: 'https://via.placeholder.com/200x200/14532d/ffffff?text=MGRVI', label: 'MGRVI' },
        { url: 'https://via.placeholder.com/200x200/134e4a/ffffff?text=MSAVI', label: 'MSAVI' },
        { url: 'https://via.placeholder.com/200x200/0f766e/ffffff?text=MSR', label: 'MSR' },
        { url: 'https://via.placeholder.com/200x200/115e59/ffffff?text=MTVI1', label: 'MTVI1' },
        { url: 'https://via.placeholder.com/200x200/134e4a/ffffff?text=MTVI2', label: 'MTVI2' },
        { url: 'https://via.placeholder.com/200x200/14532d/ffffff?text=NLI', label: 'NLI' },
        { url: 'https://via.placeholder.com/200x200/166534/ffffff?text=OSAVI', label: 'OSAVI' },
        { url: 'https://via.placeholder.com/200x200/15803d/ffffff?text=PVI', label: 'PVI' },
        { url: 'https://via.placeholder.com/200x200/16a34a/ffffff?text=RDVI', label: 'RDVI' },
        { url: 'https://via.placeholder.com/200x200/22c55e/ffffff?text=RI', label: 'RI' },
        { url: 'https://via.placeholder.com/200x200/4ade80/ffffff?text=RRI1', label: 'RRI1' },
        { url: 'https://via.placeholder.com/200x200/65a30d/ffffff?text=SIPI2', label: 'SIPI2' },
        { url: 'https://via.placeholder.com/200x200/84cc16/ffffff?text=SR', label: 'SR' },
        { url: 'https://via.placeholder.com/200x200/a3e635/ffffff?text=TCARI', label: 'TCARI' },
        { url: 'https://via.placeholder.com/200x200/bef264/ffffff?text=TCARIOSAVI', label: 'TCARIOSAVI' },
        { url: 'https://via.placeholder.com/200x200/d9f99d/ffffff?text=TNDVI', label: 'TNDVI' },
        { url: 'https://via.placeholder.com/200x200/ecfccb/ffffff?text=TSAVI', label: 'TSAVI' },
        { url: 'https://via.placeholder.com/200x200/f7fee7/ffffff?text=WDVI', label: 'WDVI' }
      ],

      // Table headers and data
      vegetationIndicesHeaders: [
        { text: 'Index', value: 'index', sortable: true },
        { text: 'Mean', value: 'mean', sortable: true, decimals: 4 },
        { text: 'Std', value: 'std', sortable: true, decimals: 4 },
        { text: 'Min', value: 'min', sortable: true, decimals: 4 },
        { text: 'Max', value: 'max', sortable: true, decimals: 4 },
        { text: '25%', value: 'q25', sortable: true, decimals: 4 },
        { text: '50%', value: 'median', sortable: true, decimals: 4 },
        { text: '75%', value: 'q75', sortable: true, decimals: 4 }
      ],

      vegetationIndicesData: [
        { index: 'NDVI', mean: 0.7234, std: 0.0892, min: 0.2341, max: 0.8912, q25: 0.6789, median: 0.7345, q75: 0.7891 },
        { index: 'GNDVI', mean: 0.6543, std: 0.0765, min: 0.1987, max: 0.8234, q25: 0.6123, median: 0.6678, q75: 0.7123 },
        { index: 'EVI2', mean: 0.4567, std: 0.0543, min: 0.1234, max: 0.6789, q25: 0.4234, median: 0.4678, q75: 0.5123 },
        { index: 'NDRE', mean: 0.6789, std: 0.0876, min: 0.2345, max: 0.8567, q25: 0.6345, median: 0.6891, q75: 0.7345 },
        { index: 'NDWI', mean: 0.3456, std: 0.0432, min: 0.0987, max: 0.5678, q25: 0.3123, median: 0.3567, q75: 0.3987 },
        { index: 'NGRDI', mean: 0.2345, std: 0.0321, min: 0.0678, max: 0.4567, q25: 0.2123, median: 0.2456, q75: 0.2789 },
        { index: 'ARI', mean: 0.5678, std: 0.0654, min: 0.1456, max: 0.7891, q25: 0.5345, median: 0.5789, q75: 0.6234 },
        { index: 'ARI2', mean: 0.4891, std: 0.0543, min: 0.1234, max: 0.6789, q25: 0.4567, median: 0.5012, q75: 0.5456 },
        { index: 'AVI', mean: 0.6789, std: 0.0765, min: 0.1987, max: 0.8234, q25: 0.6345, median: 0.6891, q75: 0.7345 },
        { index: 'CCCI', mean: 0.4567, std: 0.0543, min: 0.1234, max: 0.6789, q25: 0.4234, median: 0.4678, q75: 0.5123 },
        { index: 'CIgreen', mean: 0.3456, std: 0.0432, min: 0.0987, max: 0.5678, q25: 0.3123, median: 0.3567, q75: 0.3987 },
        { index: 'CIRE', mean: 0.2345, std: 0.0321, min: 0.0678, max: 0.4567, q25: 0.2123, median: 0.2456, q75: 0.2789 },
        { index: 'CVI', mean: 0.5678, std: 0.0654, min: 0.1456, max: 0.7891, q25: 0.5345, median: 0.5789, q75: 0.6234 },
        { index: 'DSWI4', mean: 0.4891, std: 0.0543, min: 0.1234, max: 0.6789, q25: 0.4567, median: 0.5012, q75: 0.5456 },
        { index: 'DVI', mean: 0.6789, std: 0.0765, min: 0.1987, max: 0.8234, q25: 0.6345, median: 0.6891, q75: 0.7345 }
      ],

      textureFeaturesHeaders: [
        { text: 'Feature', value: 'feature', sortable: true },
        { text: 'Band', value: 'band', sortable: true },
        { text: 'Value', value: 'value', sortable: true, decimals: 4 },
        { text: 'Type', value: 'type', sortable: true }
      ],

      textureFeaturesData: [
        { feature: 'Contrast', band: 'Color', value: 0.2345, type: 'GLCM' },
        { feature: 'Homogeneity', band: 'Color', value: 0.6789, type: 'GLCM' },
        { feature: 'Energy', band: 'Color', value: 0.4567, type: 'GLCM' },
        { feature: 'Correlation', band: 'Color', value: 0.7891, type: 'GLCM' },
        { feature: 'Entropy', band: 'Color', value: 0.3456, type: 'GLCM' },
        { feature: 'Variance', band: 'Color', value: 0.5678, type: 'GLCM' },
        { feature: 'Contrast', band: 'Green', value: 0.2123, type: 'GLCM' },
        { feature: 'Homogeneity', band: 'Green', value: 0.7123, type: 'GLCM' },
        { feature: 'Energy', band: 'Green', value: 0.4987, type: 'GLCM' },
        { feature: 'Correlation', band: 'Green', value: 0.8234, type: 'GLCM' },
        { feature: 'Entropy', band: 'Green', value: 0.3123, type: 'GLCM' },
        { feature: 'Variance', band: 'Green', value: 0.5987, type: 'GLCM' },
        { feature: 'Contrast', band: 'NIR', value: 0.1987, type: 'GLCM' },
        { feature: 'Homogeneity', band: 'NIR', value: 0.7456, type: 'GLCM' },
        { feature: 'Energy', band: 'NIR', value: 0.5234, type: 'GLCM' },
        { feature: 'Correlation', band: 'NIR', value: 0.8567, type: 'GLCM' },
        { feature: 'Entropy', band: 'NIR', value: 0.2987, type: 'GLCM' },
        { feature: 'Variance', band: 'NIR', value: 0.6234, type: 'GLCM' },
        { feature: 'LBP_Uniform', band: 'Color', value: 0.4567, type: 'LBP' },
        { feature: 'LBP_NonUniform', band: 'Color', value: 0.5432, type: 'LBP' },
        { feature: 'LBP_Uniform', band: 'Green', value: 0.4987, type: 'LBP' },
        { feature: 'LBP_NonUniform', band: 'Green', value: 0.5012, type: 'LBP' },
        { feature: 'LBP_Uniform', band: 'NIR', value: 0.5234, type: 'LBP' },
        { feature: 'LBP_NonUniform', band: 'NIR', value: 0.4765, type: 'LBP' },
        { feature: 'HOG_Mean', band: 'Color', value: 0.3456, type: 'HOG' },
        { feature: 'HOG_Std', band: 'Color', value: 0.1234, type: 'HOG' },
        { feature: 'HOG_Mean', band: 'Green', value: 0.3678, type: 'HOG' },
        { feature: 'HOG_Std', band: 'Green', value: 0.1345, type: 'HOG' },
        { feature: 'HOG_Mean', band: 'NIR', value: 0.3891, type: 'HOG' },
        { feature: 'HOG_Std', band: 'NIR', value: 0.1456, type: 'HOG' },
        { feature: 'Lacunarity_1', band: 'Color', value: 0.2345, type: 'Lacunarity' },
        { feature: 'Lacunarity_2', band: 'Color', value: 0.3456, type: 'Lacunarity' },
        { feature: 'Lacunarity_3', band: 'Color', value: 0.4567, type: 'Lacunarity' },
        { feature: 'Lacunarity_1', band: 'Green', value: 0.2123, type: 'Lacunarity' },
        { feature: 'Lacunarity_2', band: 'Green', value: 0.3234, type: 'Lacunarity' },
        { feature: 'Lacunarity_3', band: 'Green', value: 0.4345, type: 'Lacunarity' },
        { feature: 'Lacunarity_1', band: 'NIR', value: 0.1987, type: 'Lacunarity' },
        { feature: 'Lacunarity_2', band: 'NIR', value: 0.3123, type: 'Lacunarity' },
        { feature: 'Lacunarity_3', band: 'NIR', value: 0.4234, type: 'Lacunarity' }
      ],

      morphologicalFeaturesHeaders: [
        { text: 'Feature', value: 'feature', sortable: true },
        { text: 'Value', value: 'value', sortable: true, decimals: 2 },
        { text: 'Unit', value: 'unit', sortable: true },
        { text: 'Category', value: 'category', sortable: true }
      ],

      morphologicalFeaturesData: [
        { feature: 'Plant Height', value: 45.23, unit: 'cm', category: 'Size' },
        { feature: 'Plant Width', value: 32.45, unit: 'cm', category: 'Size' },
        { feature: 'Leaf Area', value: 127.89, unit: 'cm²', category: 'Leaf' },
        { feature: 'Leaf Count', value: 12, unit: 'count', category: 'Leaf' },
        { feature: 'Stem Diameter', value: 8.56, unit: 'mm', category: 'Stem' },
        { feature: 'Stem Length', value: 38.91, unit: 'cm', category: 'Stem' },
        { feature: 'Root Length', value: 23.67, unit: 'cm', category: 'Root' },
        { feature: 'Root Area', value: 89.34, unit: 'cm²', category: 'Root' },
        { feature: 'Biomass Estimate', value: 156.78, unit: 'g', category: 'Biomass' },
        { feature: 'Fresh Weight', value: 234.56, unit: 'g', category: 'Biomass' },
        { feature: 'Dry Weight', value: 45.67, unit: 'g', category: 'Biomass' },
        { feature: 'Leaf Area Index', value: 2.34, unit: 'ratio', category: 'Index' },
        { feature: 'Specific Leaf Area', value: 156.78, unit: 'cm²/g', category: 'Index' },
        { feature: 'Leaf Mass Ratio', value: 0.45, unit: 'ratio', category: 'Index' },
        { feature: 'Stem Mass Ratio', value: 0.23, unit: 'ratio', category: 'Index' },
        { feature: 'Root Mass Ratio', value: 0.32, unit: 'ratio', category: 'Index' },
        { feature: 'Compactness', value: 0.67, unit: 'ratio', category: 'Shape' },
        { feature: 'Aspect Ratio', value: 1.39, unit: 'ratio', category: 'Shape' },
        { feature: 'Circularity', value: 0.78, unit: 'ratio', category: 'Shape' },
        { feature: 'Solidity', value: 0.89, unit: 'ratio', category: 'Shape' },
        { feature: 'Convexity', value: 0.92, unit: 'ratio', category: 'Shape' },
        { feature: 'Extent', value: 0.45, unit: 'ratio', category: 'Shape' },
        { feature: 'Perimeter', value: 234.56, unit: 'cm', category: 'Boundary' },
        { feature: 'Convex Perimeter', value: 198.76, unit: 'cm', category: 'Boundary' },
        { feature: 'Feret Diameter', value: 56.78, unit: 'cm', category: 'Boundary' },
        { feature: 'Min Feret Diameter', value: 34.56, unit: 'cm', category: 'Boundary' },
        { feature: 'Max Feret Diameter', value: 67.89, unit: 'cm', category: 'Boundary' },
        { feature: 'Bounding Box Area', value: 1456.78, unit: 'cm²', category: 'Boundary' },
        { feature: 'Convex Hull Area', value: 1234.56, unit: 'cm²', category: 'Boundary' },
        { feature: 'Equivalent Diameter', value: 12.78, unit: 'cm', category: 'Derived' },
        { feature: 'Major Axis Length', value: 45.67, unit: 'cm', category: 'Derived' },
        { feature: 'Minor Axis Length', value: 23.45, unit: 'cm', category: 'Derived' },
        { feature: 'Eccentricity', value: 0.78, unit: 'ratio', category: 'Derived' },
        { feature: 'Orientation', value: 23.45, unit: 'degrees', category: 'Derived' }
      ]
    };
  },
  
  computed: {
    statusText() {
      if (this.isAnalyzing) return 'Processing...';
      if (this.hasStartedAnalysis) return 'Complete';
      return 'Ready';
    },
    
    statusClass() {
      if (this.isAnalyzing) return 'status-processing';
      if (this.hasStartedAnalysis) return 'status-complete';
      return 'status-ready';
    }
  },
  
  methods: {
    getDisplayText(option) {
      if (!option) return '';
      
      if (typeof option === 'string' || typeof option === 'number') {
        return option.toString();
      }
      
      return option.label || option.toString();
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

.status-ready {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.status-processing {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.status-complete {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

/* Pre-analysis state */
.pre-analysis {
  text-align: center;
  padding: 40px 20px;
}

.selection-display h4 {
  color: white;
  font-size: 20px;
  margin-bottom: 16px;
}

.plant-selection {
  color: white;
  font-size: 40px;
  margin-bottom: 24px;
}

.additional-info {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin: 0 auto;
  width: 40%;
  padding: 16px;
  font-size: 20px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-weight: bold;
  color: white;
}

.label {
  font-weight: 500;
}

.instruction-text {
  color: rgba(255, 255, 255, 0.8);
  font-style: italic;
}

/* Analysis progress */
.analysis-progress {
  text-align: center;
  padding: 40px 20px;
}

.progress-indicator h4 {
  color: white;
  margin-bottom: 8px;
}

.progress-indicator p {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4ade80, #22c55e);
  transition: width 0.3s ease;
}

.progress-text {
  color: white;
  font-size: 14px;
}

/* Analysis complete */
.analysis-complete {
  padding-bottom: 20px;
}

.analysis-complete > div {
  margin-bottom: 32px;
}

.analysis-complete h4 {
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
