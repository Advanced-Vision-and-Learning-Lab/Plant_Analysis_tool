<template>
  <div id="plant-details">
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
        { width: 2216, height: 15, x: -10, y: 175, opacity: 0.8 },
        { width: 15, height: 750, x: 350, y: 200, opacity: 0.8 }]"
      />

      <main class="content">
        <!-- Main content layout with left sidebar -->
        <div class="content-layout">
          <!-- Parameters Section - Left Side -->
          <div class="parameters-section">
            <h3 class="parameters-title">Analysis Parameters</h3>

            <!-- Plant ID Selection -->
            <div class="parameter-group">
              <ConfigurableDropdown
                v-model="selectedPlantId"                
                :options="plantIdOptions"
                :display-text="plantIdDisplayText"
                label="Plant ID"
                placeholder="Select Plant ID"
                size="small"
                :searchable="true"
                @change="handlePlantIdChange"
                class="dropdown"
              />
            </div>

            <!-- Date Selection -->
            <div class="parameter-group">
              <ConfigurableDropdown
                v-model="selectedDate"
                :options="dateOptions"
                :display-text="dateDisplayText"
                label="Analysis Date"
                placeholder="Select Date"
                size="small"
                :disabled="!selectedPlantId"
                :searchable="true"
                @change="handleDateChange"
                class="dropdown"
              />
            </div>

            <!-- Back Button -->
            <!-- <ConfigurableButton
                text="← Back to Selection"
                variant="secondary"
                size="medium"
                @click="goBack"
                class="back-button"
              /> -->

            <!-- Analysis Button -->
            <div class="parameter-group">
              <ConfigurableButton
                text="Start Analysis"
                variant="primary"
                size="medium"
                :disabled="!canStartAnalysis"
                @click="handleAnalyzeClick"
                class="analyze-button"
              />
            </div>

            <!-- Reset Button -->
            <div class="parameter-group">
              <ConfigurableButton
                text="Reset Parameters"
                variant="outline"
                size="medium"
                @click="resetParameters"
                class="reset-button"
              />
            </div>


            <!-- Status Display -->
            <div class="status-area">
              <div v-if="!selectedPlantId" class="status-message">
                <h3>Step 1: Select Plant ID</h3>
                <p>Choose a Plant ID from the parameters panel to begin analysis.</p>
              </div>

              <div v-else-if="!selectedDate" class="status-message">
                <h3>Step 2: Select Analysis Date</h3>
                <p>Plant ID <strong>{{ getDisplayText(selectedPlantId) }}</strong> selected. Now choose an analysis date.</p>
              </div>

              <div v-else class="status-message">
                <!-- Loading Progress Indicator -->
                <div v-if="isAnalyzing" class="loading-section">
                  <h3>Analysis in Progress...</h3>
                  <div class="progress-container">
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: analysisProgress + '%' }"></div>
                    </div>
                    <div class="progress-text">{{ Math.round(analysisProgress) }}%</div>
                  </div>
                  <p>Please wait while we process your data...</p>
                </div>
                
                <!-- Analysis Results Status -->
                <div v-else>
                  <h3 v-if="results">Analysis Successful</h3>
                  <h3 v-else-if="analysisFailed">Analysis Failed, Please try again</h3>
                  <h3 v-else>Ready for Analysis</h3>
                  <div class="config-summary">
                    <div class="config-item">
                      <strong>Plant Species:</strong> {{ species }}
                    </div>
                    <div class="config-item">
                      <strong>Plant ID:</strong> {{ getDisplayText(selectedPlantId) }}
                    </div>
                    <div class="config-item">
                      <strong>Date:</strong> {{ getDisplayText(selectedDate) }}
                    </div>
                  </div>
                </div>
              </div>
              <!-- Go Back Button -->
            <div class="parameter-group">
              <ConfigurableButton
                text="Back"
                variant="outline"
                size="medium"
                @click="goBack"
                class="back-button"
              />
            </div>
            </div>
          </div>

          <!-- Main Content Area - Right Side -->
          <div class="main-content-area">
            <div class="content-header">
              <!-- <h1 class="title">{{ species }}</h1>
              <h2 class="subtitle">Plant Analysis Dashboard</h2> -->
              
            </div>

            <!-- Analysis Results Component -->
            <AnalysisResults
              :plant-name="species"
              :plant-id="selectedPlantId"
              :analysis-date="selectedDate"
              :has-started-analysis="hasStartedAnalysis"
              :is-analyzing="isAnalyzing"
              :analysis-progress="analysisProgress"
              :results="results"
              :show-charts="true"
              title="Phenotyping Analysis Results"
              @export="handleExport"
              @share="handleShare"
              class = "analysis-results"
            />
          </div>
        </div> 
      </main>
      
    </div>
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue'
import backgroundImage from '@/assets/greenhouse-img2.jpg'
import ConfigurableButton from '../components/ConfigurableButton.vue'
import ConfigurableDropdown from '@/components/ConfigurableDropdown.vue';
import AnalysisResults from '../components/AnalysisResults.vue'
import { getPlantResults, analyzePlant } from '@/api.js'

export default {
  name: 'PlantDetails',
  components: {
    AppHeader,
    ConfigurableDropdown,
    ConfigurableButton,
    AnalysisResults
  },
  data() {
    return {
      species: this.$route.params.speciesName,
      // Background configuration
      backgroundImage: backgroundImage,
      backgroundImageOpacity: 0.9,

      // Gradient configuration
      gradientTopColor: '#08B6E0',
      gradientBottomColor: '#05AF6B',
      gradientOpacity: 0.65,

      // Form data
      selectedPlantId: null,
      selectedDate: null,

      // Analysis state
      hasStartedAnalysis: false,
      isAnalyzing: false,
      analysisProgress: 0,
      results: null,
      analysisFailed: false,

      // Options data
      plantIdOptions: Array.from({ length: 48 }, (_, i) => ({
        label: `Plant ${i + 1}`,
        value: `plant${i + 1}`
      })),
      
      dateOptions: [
        { label: '2024-12-04', value: '2024-12-04' },
        { label: '2024-12-10', value: '2024-12-10' },
        { label: '2024-12-16', value: '2024-12-16' },
        { label: '2025-01-13', value: '2025-01-13' },
        { label: '2025-01-24', value: '2025-01-24' },
        { label: '2025-01-31', value: '2025-01-31' },
        { label: '2025-02-05', value: '2025-02-05' },
        { label: '2025-02-14', value: '2025-02-14' },
        { label: '2025-03-03', value: '2025-03-03' },
        { label: '2025-03-12', value: '2025-03-12' },
        { label: '2025-03-24', value: '2025-03-24' },
        { label: '2025-04-01', value: '2025-04-01' },
        { label: '2025-04-15', value: '2025-04-15' },
        { label: '2025-04-16', value: '2025-04-16' },
        { label: '2025-04-17', value: '2025-04-17' },
        { label: '2025-04-21', value: '2025-04-21' }
      ]
     
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
    },

    canStartAnalysis() {
      return this.selectedPlantId && this.selectedDate;
    },

    plantIdDisplayText() {
      if (!this.selectedPlantId) return "Select a Plant ID";
      
      // Find the option that matches the selected value
      const selectedOption = this.plantIdOptions.find(option => 
        option.value === this.selectedPlantId
      );
      
      return selectedOption ? selectedOption.label : this.selectedPlantId.label;
    },
    
    dateDisplayText() {
      if (!this.selectedDate) return "Select a Date";
      
      // Find the option that matches the selected value
      const selectedOption = this.dateOptions.find(option => 
        option.value === this.selectedDate
      );
      
      return selectedOption ? selectedOption.label : this.selectedDate.label;
    }
  },
  methods: {
    goBack() {
      // Navigate back to home page using router
      this.$router.push({ name: 'HomePage' });
    },

    handlePlantIdChange(plantId) {
      console.log('Plant ID changed to:', plantId);
      // Update the selected plant ID
      this.selectedPlantId = plantId;
      // Clear date selection when plant ID changes
      this.selectedDate = null;
      this.results = null;
    },

    handleDateChange(date) {
      this.selectedDate = date; 
      this.results = null;
      console.log('Date changed to:', date);

    },

    handleAnalyzeClick() {
      if (this.canStartAnalysis) {
        console.log('Starting analysis for:', {
          species: this.species,
          plantId: this.selectedPlantId,
          date: this.selectedDate
        });

        // Start the analysis process
        this.hasStartedAnalysis = true;
        this.isAnalyzing = true;
        this.analysisProgress = 0;
        this.results = null;
        this.analysisFailed = false;
        this.fetchResults(this.species, this.selectedPlantId.value, this.selectedDate.value);
      }
    },

    async fetchResults(species, plantId, date) {
      this.isAnalyzing = true;
      this.analysisProgress = 0;
      this.analysisFailed = false;
      console.log('fetchResults: started for', species, plantId, date);
      try {
        const result = await getPlantResults(species, plantId, date);
        if (result && result.error) {
          console.error('fetchResults: Analysis failed:', result.error);
          this.isAnalyzing = false;
          this.analysisProgress = 0;
          this.analysisFailed = true;
          alert(result.error);
          return;
        }
        this.results = result;
        this.analysisProgress = 100;
        this.isAnalyzing = false;
        this.analysisFailed = false;
        console.log('fetchResults: Analysis succeeded, results fetched from backend.');
      } catch (e) {
        if (e.response && e.response.status === 404) {
          try {
            console.log('fetchResults: No results found, triggering analysis...');
            await analyzePlant(species, plantId, date);
            this.results = await getPlantResults(species, plantId, date);
            this.analysisProgress = 100;
            this.isAnalyzing = false;
            this.analysisFailed = false;
            console.log('fetchResults: Analysis triggered and results fetched.');
          } catch (analysisError) {
            console.error('fetchResults: Analysis failed after triggering:', analysisError);
            this.isAnalyzing = false;
            this.analysisProgress = 0;
            this.analysisFailed = true;
            alert('Failed to analyze plant. Please try again later.');
          }
        } else {
          console.error('fetchResults: Failed to load results:', e);
          this.isAnalyzing = false;
          this.analysisProgress = 0;
          this.analysisFailed = true;
          alert('Error loading results. Please try again later.');
        }
      }
    },

    pollForResult(species, plantId, date) {
      this.analysisProgress = 10;
      let progress = 10;
      const poll = setInterval(async () => {
        try {
          const result = await getPlantResults(species, plantId, date);
          if (result) {
            this.results = result;
            progress += Math.random() * 20 + 10;
            this.analysisProgress = Math.min(progress, 95);
            if (this.allResultsReady(result)) {
              this.analysisProgress = 100;
              this.isAnalyzing = false;
              clearInterval(poll);
              console.log('Analysis succeeded: Results are now ready.');
            }
          }
        } catch (e) {
          // Still processing, keep polling
        }
      }, 3000);
    },

    allResultsReady(result) {
      // Check for main images
      const mainImages = ['original', 'mask', 'overlay', 'segmented'];
      const allMainImages = mainImages.every(k => result && result[k]);
      // Check for at least one vegetation index image
      const vegIndexKeys = [
        'ndvi', 'gndvi', 'evi2', 'ndre', 'ndwi', 'ngrdi', 'ari', 'ari2', 'avi', 'ccci', 
        'cigreen', 'cire', 'cvi', 'dswi4', 'dvi', 'exr', 'gemi', 'gosavi', 'grndvi', 
        'grvi', 'gsavi', 'ipvi', 'lci', 'mcari', 'mcari1', 'mcari2', 'mgrvi', 'msavi', 
        'msr', 'mtvi1', 'mtvi2', 'nli', 'osavi', 'pvi', 'rdvi', 'ri', 'rri1', 'sipi2', 
        'sr', 'tcari', 'tcariosavi', 'tndvi', 'tsavi', 'wdvi'
      ];
      const allVegIndices = vegIndexKeys.some(name => result && result[`vegetation_indices_${name}`]);
      // Check for morphology features
      const morph = result && result.morphology_features;
      const hasMorph = morph && Object.keys(morph).length > 0;
      return allMainImages && allVegIndices && hasMorph;
    },

    resetParameters() {
      this.selectedPlantId = null;
      this.selectedDate = null;
      this.species = null;
      this.hasStartedAnalysis = false;
      this.isAnalyzing = false;
      this.analysisProgress = 0;
      this.results = null;
      this.analysisFailed = false;
      console.log('Parameters reset');
    },

    handleExport(exportData) {
      console.log('Export requested:', exportData);
      // Implement export logic here
      if (exportData.type === 'csv') {
        alert('CSV export would be implemented here');
      } else if (exportData.type === 'pdf') {
        alert('PDF export would be implemented here');
      }
    },

    handleShare(data) {
      console.log('Share requested:', data);
      // Implement sharing logic here
      alert('Sharing functionality would be implemented here');
    },

    getDisplayText(option) {
      if (!option) return '';

      if (typeof option === 'string' || typeof option === 'number') {
        return option.toString();
      }

      return option.label || option.toString();
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

#plant-details {
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
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  text-align: center;
}

.content {
  width: 100%;
  max-width: 1400px;
  padding-top: 120px;
}

/* Main layout with left sidebar */
.content-layout {
  display: flex;
  gap: 30px;
  min-height: calc(100vh - 200px);
  align-items: flex-start;
}

/* Parameters Section - Left Sidebar */
.parameters-section {
  width: 300px;
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(30px);
  position: fixed;
  top: 180px;
  left: 0px;

}

.parameters-title {
  color: white;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  text-align: center;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 12px;
  opacity: 0.8;
}


.parameter-group {
  margin-bottom: 20px;
}

.dropdown {
  width: 70%;
}

.analyze-button,
.reset-button {
  width: 70%;
  margin-top: 8px;
  font-weight: bold;
}

/* Main Content Area - Right Side */
.main-content-area {
  flex: 1;
  min-height: 500px;
}

.content-header {
  text-align: center;
  margin-bottom: 40px;
}

.content-header .title {
  font-size: 48px;
  margin-bottom: 10px;
}

.content-header .subtitle {
  font-size: 32px;
  margin-bottom: 20px;
}


/* Status Area */
.status-area {
  height: 225px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 32px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.status-message {
  margin-top: -30px;
  color: white;
}

.status-message h3 {
  font-size: 28px;
  margin-bottom: 16px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.status-message p {
  font-size: 18px;
  line-height: 1.6;
  opacity: 0.9;
  margin-bottom: 20px;
}

.config-summary {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  text-align: left;
}

.config-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 16px;
}

.config-item:last-child {
  border-bottom: none;
}

.title {
  color: white;
  font-size: 64px;
  margin-top: 200px;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  font-weight: 700;
}

.subtitle {
  color: white;
  font-size: 60px;
  margin-bottom: 10px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  font-weight: 500;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  margin-top: 10px;
  width: 40%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  font-size: 18px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}


.plant-info {
  margin-top: 40px;
}

.plant-description {
  color: white;
  font-size: 24px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  margin: 20px 0;
}

.details-content {
  color: white;
  font-size: 18px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  max-width: 600px;
  margin: 0 auto;
  text-align: left;
}

.details-content ul {
  margin: 20px 0;
  padding-left: 20px;
}

.details-content li {
  margin: 8px 0;
  line-height: 1.5;
}

/* Loading Progress Indicator Styles */
.loading-section {
  margin-top: -30px;
  color: white;
}

.loading-section h3 {
  font-size: 28px;
  margin-bottom: 16px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.progress-container {
  position: relative;
  width: 100%;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-bar {
  position: relative;
  height: 100%;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #4ade80, #22c55e);
  border-radius: 10px;
  transition: width 0.3s ease-in-out;
  min-width: 0%;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  z-index: 1;
}

</style>