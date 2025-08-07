<template>
  <div class="plant-timeline">
    <div class="timeline-content">
      <!-- Chart Container -->
      <div class="chart-container">
        <canvas ref="timelineChart" width="800" height="400"></canvas>
      </div>
      
      <!-- Configuration Panel -->
      <div class="config-panel">
        <h3>Display Configuration</h3>
        
        <!-- Feature Selection -->
        <div class="config-group">
          <label>Feature Type:</label>
          <select v-model="selectedFeatureType" @change="onFeatureTypeChange">
            <option value="">Select Feature Type</option>
            <option value="vegetation">Vegetation Index</option>
            <option value="texture">Texture Feature</option>
          </select>
        </div>
        
                 <div class="config-group">
           <label>Specific Feature:</label>
           <select v-model="selectedFeature" :disabled="!selectedFeatureType">
             <option value="">Select Feature</option>
             <option v-for="feature in availableFeatures" :key="feature" :value="feature">
               {{ feature }}
             </option>
           </select>
         </div>
         
         <!-- Texture Band and Type Selection (for texture features) -->
         <div v-if="selectedFeatureType === 'texture'" class="config-group">
           <label>Texture Band:</label>
           <select v-model="selectedTextureBand" @change="updateTextureFeatures">
             <option value="">Select Band</option>
             <option value="color">Color</option>
             <option value="green">Green</option>
             <option value="nir">NIR</option>
             <option value="pca">PCA</option>
             <option value="red_edge">Red Edge</option>
             <option value="red">Red</option>
           </select>
         </div>
         
         <div v-if="selectedFeatureType === 'texture' && selectedTextureBand" class="config-group">
           <label>Texture Type:</label>
           <select v-model="selectedTextureType">
             <option value="">Select Type</option>
             <option v-for="type in availableTextureTypes" :key="type" :value="type">
               {{ type }}
             </option>
           </select>
         </div>
        
        <!-- Display Options -->
        <div class="config-group">
          <label>Display Options:</label>
          <div class="checkbox-group">
            <label>
              <input type="checkbox" v-model="showImages" />
              Show Images
            </label>
            <label>
              <input type="checkbox" v-model="showErrorBars" />
              Show Error Bars
            </label>
          </div>
        </div>
        
        <div class="config-group">
          <label>Number of Images:</label>
          <input 
            type="number" 
            v-model="numImages" 
            min="1" 
            max="10" 
            :disabled="!showImages"
          />
        </div>
        
        <!-- Date Range -->
        <div class="config-group">
          <label>Date Range:</label>
          <div class="date-range">
            <input type="date" v-model="startDate" />
            <span>to</span>
            <input type="date" v-model="endDate" />
          </div>
        </div>
        
        <!-- Update Button -->
        <button @click="updateChart" :disabled="!canUpdate" class="update-btn">
          Update Chart
        </button>
      </div>
    </div>
    
    <!-- Images Display -->
    <div v-if="showImages && selectedImages.length > 0" class="images-section">
      <h3>Timeline Images</h3>
      <div class="images-grid">
        <div v-for="image in selectedImages" :key="image.date" class="image-item">
          <h4>{{ image.date }}</h4>
          <img :src="image.url" :alt="`Image for ${image.date}`" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'PlantTimeline',
  props: {
    timelineData: {
      type: Object,
      required: true
    },
    config: {
      type: Object,
      default: () => ({
        featureType: '',
        specificFeature: '',
        displayImages: false,
        numImages: 5
      })
    }
  },
  
  data() {
    return {
      chart: null,
      selectedFeatureType: this.config.featureType || '',
      selectedFeature: this.config.specificFeature || '',
      selectedTextureBand: '',
      selectedTextureType: '',
      showImages: this.config.displayImages || false,
      showErrorBars: true,
      numImages: this.config.numImages || 5,
      startDate: '',
      endDate: '',
      availableFeatures: [],
      availableTextureTypes: []
    };
  },
  
  computed: {
    canUpdate() {
      if (this.selectedFeatureType === 'vegetation') {
        return this.selectedFeatureType && this.selectedFeature;
      } else if (this.selectedFeatureType === 'texture') {
        return this.selectedFeatureType && this.selectedTextureBand && this.selectedTextureType;
      }
      return false;
    },
    
    selectedImages() {
      if (!this.showImages || !this.timelineData) return [];
      
      const allDates = [...new Set([
        ...this.timelineData.vegetation_timeline.map(v => v.date),
        ...this.timelineData.texture_timeline.map(t => t.date)
      ])].sort();
      
      if (allDates.length <= this.numImages) {
        return allDates.map(date => ({
          date,
          url: this.getImageUrl(date)
        }));
      }
      
      // Select evenly spaced images
      const step = Math.floor(allDates.length / this.numImages);
      const selectedDates = [];
      for (let i = 0; i < this.numImages; i++) {
        const index = i * step;
        if (index < allDates.length) {
          selectedDates.push(allDates[index]);
        }
      }
      
      return selectedDates.map(date => ({
        date,
        url: this.getImageUrl(date)
      }));
    }
  },
  
  watch: {
    timelineData: {
      handler() {
        this.initializeDates();
        this.updateAvailableFeatures();
        if (this.chart) {
          this.updateChart();
        }
      },
      immediate: true
    }
  },
  
  mounted() {
    this.initializeChart();
    this.initializeDates();
    this.updateAvailableFeatures();
  },
  
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  },
  
  methods: {
    initializeChart() {
      const ctx = this.$refs.timelineChart.getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: []
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Plant Timeline Analysis'
            },
            legend: {
              display: true
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Date'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Value'
              }
            }
          }
        }
      });
    },
    
    initializeDates() {
      if (!this.timelineData) return;
      
      const allDates = [...new Set([
        ...this.timelineData.vegetation_timeline.map(v => v.date),
        ...this.timelineData.texture_timeline.map(t => t.date)
      ])].sort();
      
      if (allDates.length > 0) {
        this.startDate = allDates[0];
        this.endDate = allDates[allDates.length - 1];
      }
    },
    
    updateAvailableFeatures() {
      if (!this.timelineData) return;
      
      if (this.selectedFeatureType === 'vegetation') {
        this.availableFeatures = [...new Set(
          this.timelineData.vegetation_timeline.map(v => v.index_type)
        )];
      } else if (this.selectedFeatureType === 'texture') {
        this.availableFeatures = [...new Set(
          this.timelineData.texture_timeline.map(t => t.band_name)
        )];
      } else {
        this.availableFeatures = [];
      }
    },
    
    updateTextureFeatures() {
      if (!this.timelineData || !this.selectedTextureBand) {
        this.availableTextureTypes = [];
        return;
      }
      
      this.availableTextureTypes = [...new Set(
        this.timelineData.texture_timeline
          .filter(t => t.band_name === this.selectedTextureBand)
          .map(t => t.texture_type)
      )];
      
      this.selectedTextureType = '';
    },
    
    onFeatureTypeChange() {
      this.selectedFeature = '';
      this.selectedTextureBand = '';
      this.selectedTextureType = '';
      this.updateAvailableFeatures();
    },
    
    updateChart() {
      if (!this.chart || !this.timelineData) return;
      
      const data = this.getChartData();
      
      this.chart.data.labels = data.labels;
      this.chart.data.datasets = data.datasets;
      this.chart.update();
    },
    
    getChartData() {
      if (!this.timelineData) return { labels: [], datasets: [] };
      
      let timelineData = [];
      
      if (this.selectedFeatureType === 'vegetation') {
        if (!this.selectedFeature) return { labels: [], datasets: [] };
        timelineData = this.timelineData.vegetation_timeline
          .filter(v => v.index_type === this.selectedFeature)
          .filter(v => this.isDateInRange(v.date));
      } else if (this.selectedFeatureType === 'texture') {
        if (!this.selectedTextureBand || !this.selectedTextureType) return { labels: [], datasets: [] };
        timelineData = this.timelineData.texture_timeline
          .filter(t => t.band_name === this.selectedTextureBand && t.texture_type === this.selectedTextureType)
          .filter(t => this.isDateInRange(t.date));
      }
      
      const labels = timelineData.map(d => d.date);
      
      const datasets = [
        {
          label: 'Mean',
          data: timelineData.map(d => d.mean),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1
        },
        {
          label: 'Median',
          data: timelineData.map(d => d.median),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.1
        }
      ];
      
      if (this.showErrorBars) {
        datasets.push({
          label: 'Q25-Q75 Range',
          data: timelineData.map(d => ({
            y: d.mean,
            yMin: d.q25,
            yMax: d.q75
          })),
          borderColor: 'rgba(75, 192, 192, 0.5)',
          backgroundColor: 'rgba(75, 192, 192, 0.1)',
          type: 'bar'
        });
      }
      
      return { labels, datasets };
    },
    
    isDateInRange(date) {
      if (!this.startDate && !this.endDate) return true;
      if (this.startDate && date < this.startDate) return false;
      if (this.endDate && date > this.endDate) return false;
      return true;
    },
    
    getImageUrl(date) {
      // This would need to be implemented based on your image storage structure
      // For now, return a placeholder
      return `https://via.placeholder.com/200x150?text=${date}`;
    }
  }
};
</script>

<style scoped>
.plant-timeline {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: #f5f5f5;
}

.timeline-content {
  display: flex;
  flex: 1;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-container {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  height: 400px;
}

.config-panel {
  width: 300px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.config-panel h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.config-group {
  margin-bottom: 16px;
}

.config-group label {
  display: block;
  margin-bottom: 6px;
  color: #555;
  font-weight: 500;
  font-size: 14px;
}

.config-group select,
.config-group input[type="number"],
.config-group input[type="date"] {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background: white;
}

.config-group select:focus,
.config-group input:focus {
  outline: none;
  border-color: #4ade80;
  box-shadow: 0 0 0 2px rgba(74, 222, 128, 0.2);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #4ade80;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-range input {
  flex: 1;
}

.date-range span {
  color: #666;
  font-size: 12px;
}

.update-btn {
  width: 100%;
  padding: 12px;
  background: #4ade80;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.update-btn:hover:not(:disabled) {
  background: #22c55e;
}

.update-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.images-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.images-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.image-item {
  text-align: center;
}

.image-item h4 {
  margin: 0 0 8px 0;
  color: #555;
  font-size: 14px;
  font-weight: 500;
}

.image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}
</style>
