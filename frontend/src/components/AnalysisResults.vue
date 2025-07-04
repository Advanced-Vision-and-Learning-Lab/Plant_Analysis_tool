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
          <h4>Current Selection</h4>
          <p class="plant-selection">
            You have selected: <strong>{{ plantName }}</strong>
          </p>
          
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

      <!-- Analysis complete - show results -->
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

        <!-- Results Table -->
        <div class="results-table-container">
          <h4>Phenotyping Results</h4>
          <div class="table-wrapper">
            <table class="results-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Value</th>
                  <th>Unit</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(result, index) in analysisResults" :key="index" :class="getRowClass(result)">
                  <td class="parameter-name">{{ result.parameter }}</td>
                  <td class="parameter-value">{{ result.value }}</td>
                  <td class="parameter-unit">{{ result.unit }}</td>
                  <td class="parameter-status">
                    <span class="status-badge" :class="result.status.toLowerCase()">
                      {{ result.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Additional Charts/Visualizations placeholder -->
        <div v-if="showCharts" class="charts-section">
          <h4>Visual Analysis</h4>
          <div class="charts-grid">
            <div class="chart-placeholder">
              <p>Growth Rate Chart</p>
              <div class="chart-mock">📊</div>
            </div>
            <div class="chart-placeholder">
              <p>Health Index</p>
              <div class="chart-mock">📈</div>
            </div>
          </div>
        </div>

        <!-- Export Options -->
        <div class="export-section">
          <h4>Export Results</h4>
          <div class="export-buttons">
            <ConfigurableButton
              text="Download CSV"
              variant="outline"
              size="small"
              @click="exportCSV"
            />
            <ConfigurableButton
              text="Download PDF"
              variant="outline"
              size="small"
              @click="exportPDF"
            />
            <ConfigurableButton
              text="Share Results"
              variant="secondary"
              size="small"
              @click="shareResults"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ConfigurableButton from './ConfigurableButton.vue'

export default {
  name: 'AnalysisResults',
  components: {
    ConfigurableButton
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
      
      // Dummy analysis results - Extended dataset
      defaultResults: [
        { parameter: 'Plant Height', value: '45.2', unit: 'cm', status: 'Normal' },
        { parameter: 'Leaf Area', value: '127.8', unit: 'cm²', status: 'Normal' },
        { parameter: 'Stem Diameter', value: '8.5', unit: 'mm', status: 'Normal' },
        { parameter: 'Chlorophyll Content', value: '42.1', unit: 'SPAD', status: 'High' },
        { parameter: 'Disease Index', value: '0.12', unit: 'ratio', status: 'Low' },
        { parameter: 'Growth Rate', value: '2.8', unit: 'cm/day', status: 'Normal' },
        { parameter: 'Water Stress', value: '0.05', unit: 'ratio', status: 'Low' },
        { parameter: 'Biomass Estimate', value: '156.3', unit: 'g', status: 'Normal' },
        { parameter: 'Root Length', value: '23.7', unit: 'cm', status: 'Normal' },
        { parameter: 'Leaf Count', value: '12', unit: 'count', status: 'Normal' },
        { parameter: 'Flowering Stage', value: '3.2', unit: 'scale', status: 'Normal' },
        { parameter: 'Fruit Count', value: '8', unit: 'count', status: 'High' },
        { parameter: 'Nitrogen Content', value: '2.8', unit: '%', status: 'Normal' },
        { parameter: 'Phosphorus Content', value: '0.45', unit: '%', status: 'Low' },
        { parameter: 'Potassium Content', value: '1.9', unit: '%', status: 'Normal' },
        { parameter: 'Soil pH', value: '6.8', unit: 'pH', status: 'Normal' },
        { parameter: 'Temperature Stress', value: '0.08', unit: 'ratio', status: 'Low' },
        { parameter: 'Light Exposure', value: '85.2', unit: '%', status: 'High' },
        { parameter: 'Humidity Level', value: '62.5', unit: '%', status: 'Normal' },
        { parameter: 'Pest Damage', value: '0.03', unit: 'ratio', status: 'Low' },
        { parameter: 'Leaf Thickness', value: '0.28', unit: 'mm', status: 'Normal' },
        { parameter: 'Stomatal Density', value: '245', unit: 'count/mm²', status: 'Normal' },
        { parameter: 'Photosynthesis Rate', value: '18.7', unit: 'μmol/m²/s', status: 'High' },
        { parameter: 'Transpiration Rate', value: '4.2', unit: 'mmol/m²/s', status: 'Normal' },
        { parameter: 'Carbon Fixation', value: '12.8', unit: 'mg/g/h', status: 'Normal' },
        { parameter: 'Antioxidant Activity', value: '78.3', unit: 'μmol TE/g', status: 'High' },
        { parameter: 'Protein Content', value: '14.2', unit: '%', status: 'Normal' },
        { parameter: 'Carbohydrate Content', value: '68.5', unit: '%', status: 'Normal' },
        { parameter: 'Fiber Content', value: '8.9', unit: '%', status: 'Normal' },
        { parameter: 'Moisture Content', value: '82.1', unit: '%', status: 'Normal' },
        { parameter: 'Ash Content', value: '1.8', unit: '%', status: 'Low' },
        { parameter: 'Lipid Content', value: '2.1', unit: '%', status: 'Low' },
        { parameter: 'Vitamin C', value: '45.6', unit: 'mg/100g', status: 'High' },
        { parameter: 'Carotenoids', value: '12.4', unit: 'mg/100g', status: 'Normal' },
        { parameter: 'Flavonoids', value: '8.7', unit: 'mg/100g', status: 'High' },
        { parameter: 'Phenolic Compounds', value: '156.8', unit: 'mg GAE/100g', status: 'High' },
        { parameter: 'Seed Viability', value: '94.2', unit: '%', status: 'High' },
        { parameter: 'Germination Rate', value: '89.5', unit: '%', status: 'Normal' },
        { parameter: 'Seedling Vigor', value: '7.8', unit: 'index', status: 'Normal' },
        { parameter: 'Stress Tolerance', value: '6.9', unit: 'index', status: 'Normal' }
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
    },
    
    analysisResults() {
      return this.customResults || this.defaultResults;
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
    
    getRowClass(result) {
      return {
        'row-normal': result.status.toLowerCase() === 'normal',
        'row-high': result.status.toLowerCase() === 'high',
        'row-low': result.status.toLowerCase() === 'low',
        'row-warning': result.status.toLowerCase() === 'warning'
      };
    },
    
    exportCSV() {
      console.log('Exporting CSV...');
      this.$emit('export', { type: 'csv', data: this.analysisResults });
    },
    
    exportPDF() {
      console.log('Exporting PDF...');
      this.$emit('export', { type: 'pdf', data: this.analysisResults });
    },
    
    shareResults() {
      console.log('Sharing results...');
      this.$emit('share', this.analysisResults);
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
  font-size: 18px;
  margin-bottom: 24px;
}

.additional-info {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
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

/* Results table */
.table-wrapper {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  margin-bottom: 20px;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}

.results-table th {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.results-table td {
  padding: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.parameter-name {
  font-weight: 500;
}

.parameter-value {
  font-family: 'Courier New', monospace;
  font-weight: bold;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.normal {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.status-badge.high {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

.status-badge.low {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.status-badge.warning {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

/* Charts section */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.chart-placeholder {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  color: white;
}

.chart-mock {
  font-size: 48px;
  margin-top: 16px;
}

/* Export section */
.export-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* Responsive design */
@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .export-buttons {
    flex-direction: column;
  }
  
  .results-table {
    font-size: 14px;
  }
  
  .results-table th,
  .results-table td {
    padding: 8px;
  }
}
</style>
