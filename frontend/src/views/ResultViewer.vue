<template>
  <div>
    <!-- Main layout row: sidebar and main content -->
    <v-row class="result-viewer-row" no-gutters>
      <!-- Sidebar: plant/date selection and dark mode toggle -->
      <v-col cols="12" md="3" lg="2" class="sidebar-col">
        <PlantSidebar
          :plants="plants"
          :minDate="minDate"
          :maxDate="maxDate"
          v-model="sidebarSelection"
          @analyze="onAnalyze"
        />
        <!-- Dark mode switch -->
        <v-switch
          v-model="$vuetify.theme.dark"
          label="Dark mode"
          class="mt-4"
          inset
        />
      </v-col>
      <!-- Main content area: results, images, tables -->
      <v-col cols="12" md="9" lg="10" class="main-content-col">
        <!-- Loading bar -->
        <v-progress-linear
          v-if="loading"
          indeterminate
          color="primary"
          absolute
          top
        ></v-progress-linear>
        <!-- Snackbar for notifications -->
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
          {{ snackbarText }}
        </v-snackbar>
        <!-- Instruction if no plant/date selected -->
        <div v-if="!sidebarSelection.plantId || !sidebarSelection.date">
          <div class="center-instruction">
            Please select the date and plant number and click Analyze to start.
          </div>
        </div>
        <div v-else>
          <!-- Hidden analyze button (could be used for manual trigger) -->
          <v-btn color="primary" @click="onAnalyze" :disabled="loading" style="margin: 24px 0; display: none;">
            Analyze
          </v-btn>
          <!-- Image size slider -->
          <v-row class="mb-4" align="center">
            <v-col cols="12" md="6" lg="4">
              <v-slider
                v-model="imageSize"
                :min="100"
                :max="700"
                :step="10"
                label="Image Size"
                thumb-label
                ticks
              />
            </v-col>
          </v-row>
          <div v-if="result">
            <!-- Tabs for different result types -->
            <v-tabs v-model="currentTab" background-color="white" grow style="position:sticky;top:0;z-index:1;">
              <v-tab v-for="tab in tabs" :key="tab">{{ tab }}</v-tab>
            </v-tabs>
            <v-tabs-items v-model="currentTab">
              <!-- Images Tab -->
              <v-tab-item>
                <v-row>
                  <v-col v-for="img in imageList" :key="img.label" cols="12" md="6" lg="3">
                    <div class="image-item">
                      <h4>{{ img.label }}
                        <!-- Download image button with tooltip -->
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn icon small v-bind="attrs" v-on="on" @click="downloadImage(img.url)">
                              <v-icon>mdi-download</v-icon>
                            </v-btn>
                          </template>
                          <span>Download image</span>
                        </v-tooltip>
                      </h4>
                      <!-- Clickable image opens gallery -->
                      <img v-if="getImageUrl(img.key)" :src="getImageUrl(img.key)" @click="openGallery(imageList.map(i=>i.url), imageList.findIndex(i=>i.key===img.key))" class="clickable-img desktop-img" :style="{ maxWidth: imageSize + 'px', maxHeight: imageSize + 'px' }" />
                    </div>
                  </v-col>
                </v-row>
                <!-- Lightbox for image viewing -->
                <vue-easy-lightbox
                  :visible="showViewer"
                  :imgs="galleryImgs"
                  :index="galleryIndex"
                  @hide="showViewer = false"
                />
              </v-tab-item>
              <!-- Morphology Images Tab -->
              <v-tab-item>
                <v-row>
                  <v-col v-for="img in morphImageList" :key="img.key" cols="12" md="6" lg="3">
                    <div class="image-item">
                      <h4>{{ img.label }}
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn icon small v-bind="attrs" v-on="on" @click="downloadImage(img.url)">
                              <v-icon>mdi-download</v-icon>
                            </v-btn>
                          </template>
                          <span>Download image</span>
                        </v-tooltip>
                      </h4>
                      <img v-if="img.url" :src="img.url" @click="openGallery(morphImageList.map(i=>i.url), morphImageList.findIndex(i=>i.key===img.key))" class="clickable-img desktop-img" :style="{ maxWidth: imageSize + 'px', maxHeight: imageSize + 'px' }" />
                    </div>
                  </v-col>
                </v-row>
                <vue-easy-lightbox
                  :visible="showViewer"
                  :imgs="galleryImgs"
                  :index="galleryIndex"
                  @hide="showViewer = false"
                />
              </v-tab-item>
              <!-- Texture Images Tab -->
              <v-tab-item>
                <v-row>
                  <v-col v-for="img in textureImageList" :key="img.label" cols="12" md="6" lg="3">
                    <div class="image-item">
                      <h4>{{ img.label }}
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn icon small v-bind="attrs" v-on="on" @click="downloadImage(img.url)">
                              <v-icon>mdi-download</v-icon>
                            </v-btn>
                          </template>
                          <span>Download image</span>
                        </v-tooltip>
                      </h4>
                      <img v-if="img.url" :src="img.url" @click="openGallery(textureImageList.map(i=>i.url), textureImageList.findIndex(i=>i.url===img.url))" class="clickable-img desktop-img" :style="{ maxWidth: imageSize + 'px', maxHeight: imageSize + 'px' }" />
                    </div>
                  </v-col>
                </v-row>
                <vue-easy-lightbox
                  :visible="showViewer"
                  :imgs="galleryImgs"
                  :index="galleryIndex"
                  @hide="showViewer = false"
                />
              </v-tab-item>
              <!-- Vegetation Indices Images Tab -->
              <v-tab-item>
                <v-row>
                  <v-col v-for="(name, idx) in vegIndexList" :key="name" cols="12" md="4" lg="3">
                    <div class="image-item">
                      <h4>{{ name }}
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn icon small v-bind="attrs" v-on="on" @click="downloadImage(getVegIndexUrl(name))">
                              <v-icon>mdi-download</v-icon>
                            </v-btn>
                          </template>
                          <span>Download image</span>
                        </v-tooltip>
                      </h4>
                      <img v-if="getVegIndexUrl(name)" :src="getVegIndexUrl(name)" @click="openGallery(vegIndexList.map(n=>getVegIndexUrl(n)), idx)" class="clickable-img desktop-img" :style="{ maxWidth: imageSize + 'px', maxHeight: imageSize + 'px' }" />
                    </div>
                  </v-col>
                </v-row>
                <vue-easy-lightbox
                  :visible="showViewer"
                  :imgs="galleryImgs"
                  :index="galleryIndex"
                  @hide="showViewer = false"
                />
              </v-tab-item>
              <!-- Vegetation Indices Table Tab -->
              <v-tab-item>
                <!-- Search and download for veg indices table -->
                <v-text-field
                  v-model="vegIndexSearch"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                  class="mb-2"
                />
                <v-btn color="primary" small class="mb-2" @click="downloadCSV('vegIndex')">
                  Download CSV
                </v-btn>
                <v-data-table
                  :headers="vegIndexHeadersWithTooltips"
                  :items="vegIndexItems"
                  :search="vegIndexSearch"
                  class="elevation-1"
                  dense
                  :items-per-page="10"
                  :footer-props="{ itemsPerPageOptions: [5, 10, 25, 50] }"
                  :sort-by="['index']"
                />
              </v-tab-item>
              <!-- Texture Features Table Tab -->
              <v-tab-item>
                <v-text-field
                  v-model="textureSearch"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                  class="mb-2"
                />
                <v-btn color="primary" small class="mb-2" @click="downloadCSV('texture')">
                  Download CSV
                </v-btn>
                <v-data-table
                  :headers="textureHeadersWithTooltips"
                  :items="textureItems"
                  :search="textureSearch"
                  class="elevation-1"
                  dense
                  :items-per-page="10"
                  :footer-props="{ itemsPerPageOptions: [5, 10, 25, 50] }"
                  :sort-by="['feature']"
                />
              </v-tab-item>
              <!-- Morphological Features Table Tab -->
              <v-tab-item>
                <v-text-field
                  v-model="morphSearch"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                  class="mb-2"
                />
                <v-btn color="primary" small class="mb-2" @click="downloadCSV('morph')">
                  Download CSV
                </v-btn>
                <v-data-table
                  :headers="morphHeadersWithTooltips"
                  :items="morphItems"
                  :search="morphSearch"
                  class="elevation-1"
                  dense
                  :items-per-page="10"
                  :footer-props="{ itemsPerPageOptions: [5, 10, 25, 50] }"
                  :sort-by="['feature']"
                />
              </v-tab-item>
            </v-tabs-items>
          </div>
        </div>
        <!-- Floating action button for analyze all (future feature) -->
        <v-btn fab color="primary" fixed bottom right @click="analyzeAll" class="fab-btn">
          <v-icon>mdi-rocket</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <!-- Footer with about and navigation -->
    <footer class="result-footer">
      <div class="footer-content">
        <div class="footer-about">
          <strong>Plant Analysis Platform</strong><br>
          Empowering researchers and agronomists with advanced AI-driven plant phenotyping.<br>
          Analyze plant images for biotic and abiotic stress, visualize results, and extract actionable insights with ease.
        </div>
        <div class="footer-actions">
          <v-btn text color="primary" @click="$router.push('/')">Return to Main Menu</v-btn>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
// Import child components and API helpers
import PlantSidebar from './PlantSidebar.vue';
import VueEasyLightbox from 'vue-easy-lightbox';
import { getPlantResults, analyzePlant } from '@/api.js';

export default {
  name: 'ResultViewer',
  components: { PlantSidebar, VueEasyLightbox },
  data() {
    // Main state for sidebar, plant list, results, UI, etc.
    const availableDates = [
      '2024-12-04',
      '2024-12-10',
      '2024-12-16',
      '2025-01-13',
      '2025-01-24',
      '2025-01-31',
      '2025-02-05',
      '2025-02-14',
      '2025-03-03',
      '2025-03-12',
      '2025-03-24',
      '2025-04-01',
      '2025-04-15',
      '2025-04-16',
      '2025-04-17',
      '2025-04-21'
    ];

    return {
      sidebarSelection: { plantId: null, date: null }, // Selected plant/date
      plants: Array.from({ length: 48 }, (_, i) => ({
        id: `plant${i + 1}`,
        name: `Plant ${i + 1}`,
        availableDates
      })),
      minDate: '2024-12-04',
      maxDate: '2025-04-21',
      result: null, // Analysis result data
      loading: false, // Loading state
      currentTab: 0, // Active tab index
      tabs: [
        'Images',
        'Morphology Images',
        'Texture Images',
        'Vegetation Indices Images',
        'Vegetation Indices Table',
        'Texture Features Table',
        'Morphological Features Table'
      ],
      showViewer: false, // Lightbox visibility
      viewerImg: '', // Current image in viewer
      vegIndexList: [
        // List of vegetation indices
        'ARI','ARI2','AVI','CCCI','CIgreen','CIRE','CVI','DSWI4','DVI',
        'EVI2','ExR','GEMI','GNDVI','GOSAVI','GRNDVI','GRVI','GSAVI',
        'IPVI','LCI','MCARI','MCARI1','MCARI2','MGRVI','MSAVI','MSR',
        'MTVI1','MTVI2','NDRE','NDVI','NDWI','NGRDI','NLI','OSAVI',
        'PVI','RDVI','RI','RRI1','SIPI2','SR','TCARI','TCARIOSAVI',
        'TNDVI','TSAVI','WDVI'
      ],
      textureBands: ['color','green','nir','red_edge','red','pca'],
      textureSuffixes: [
        '01_orig.png','02_gray.png','03_lbp.png','04_hog.png',
        '05_lac1.png','06_lac2.png','07_lac3.png','08_ehd_map.png'
      ],
      error: null,
      vegIndexSearch: '',
      textureSearch: '',
      morphSearch: '',
      aboutDialog: false,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      galleryImgs: [],
      galleryIndex: 0,
      hasAnalyzed: false,
      imageSize: 350, // Default image size in px
    };
  },
  watch: {
    // Reset result when sidebar selection changes
    sidebarSelection: {
      handler() {
        this.hasAnalyzed = false;
        this.result = null;
      },
      immediate: true
    }
  },
  computed: {
    // Extract nested result object if present
    nestedResult() {
      if (!this.result) return null;
      for (const key in this.result) {
        if (key.endsWith('_result') && typeof this.result[key] === 'object') {
          return this.result[key];
        }
      }
      return null;
    },
    // Format vegetation indices for table display
    formattedVegIndices() {
      const nested = this.nestedResult;
      if (!nested || !nested.vegetation_features || !Array.isArray(nested.vegetation_features) || nested.vegetation_features.length === 0) {
        return {};
      }
      const v = nested.vegetation_features[0] || {};
      const out = {};
      Object.keys(v).forEach(k => {
        if (k.endsWith('_mean')) {
          const idx = k.replace('_mean','');
          out[idx] = {
            mean: v[`${idx}_mean`],
            std: v[`${idx}_std`],
            min: v[`${idx}_min`],
            max: v[`${idx}_max`],
            q25: v[`${idx}_q25`],
            median: v[`${idx}_median`],
            q75: v[`${idx}_q75`]
          };
        }
      });
      return out;
    },
    // Morphological features for table
    morphology() {
      return this.result?.morphology_features || {};
    },
    // Texture statistics for table
    textureStats() {
      const nested = this.nestedResult;
      if (!nested || !nested.texture_features || !Array.isArray(nested.texture_features) || nested.texture_features.length === 0) {
        return {};
      }
      return nested.texture_features[0] || {};
    },
    // Plant folder name
    folderName() {
      return this.result?.plant_id;
    },
    // List of main images to display
    imageList() {
      if (!this.result) return [];
      const keys = ['original', 'mask', 'overlay', 'segmented'];
      return keys.filter(k => this.result[k]).map(k => ({ label: this.capitalize(k), key: k, url: this.result[k] }));
    },
    // Morphology images to display
    morphImageList() {
      if (!this.result) return [];
      const prefix = 'morphology_images_';
      return Object.keys(this.result)
        .filter(k => k.startsWith(prefix))
        .map(k => ({
          label: this.capitalize(k.replace(prefix, '').replace(/_/g, ' ')),
          key: k,
          url: this.result[k]
        }));
    },
    // List of texture images to display
    textureImageList() {
      if (!this.result) return [];
      // Find all keys that match texture_{band}_{suffix} and group by band
      const bands = ['color','green','nir','pca','red','red_edge'];
      const suffixes = [
        '01_orig','02_gray','03_lbp','04_hog','05_lac1','06_lac2','07_lac3','08_ehd_map'
      ];
      let images = [];
      for (const band of bands) {
        for (const suffix of suffixes) {
          const key = `texture_${band}_${suffix}`;
          if (this.result[key]) {
            images.push({
              label: `${this.capitalize(band)} ${suffix.replace(/\d+_/, '').replace('_', ' ').replace('.png','')}`,
              band,
              suffix,
              url: this.result[key]
            });
          }
        }
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
    // Table headers for morphology features
    morphHeaders() {
      return [
        { text: 'Feature', value: 'feature' },
        { text: 'Value', value: 'value' }
      ];
    },
    // Table items for morphology features
    morphItems() {
      return Object.entries(this.morphology).map(([feature, value]) => ({
        feature,
        value
      }));
    },
    // Add tooltips to veg index headers
    vegIndexHeadersWithTooltips() {
      return this.vegIndexHeaders.map(h => ({
        ...h,
        cellClass: 'header-cell',
        align: 'center',
        sortable: true,
        text: h.text + (h.value === 'mean' ? ' ℹ️' : '')
      }));
    },
    // Add tooltips to texture headers
    textureHeadersWithTooltips() {
      return this.textureHeaders.map(h => ({
        ...h,
        cellClass: 'header-cell',
        align: 'center',
        sortable: true,
        text: h.text + (h.value === 'value' ? ' ℹ️' : '')
      }));
    },
    // Add tooltips to morph headers
    morphHeadersWithTooltips() {
      return this.morphHeaders.map(h => ({
        ...h,
        cellClass: 'header-cell',
        align: 'center',
        sortable: true,
        text: h.text + (h.value === 'value' ? ' ℹ️' : '')
      }));
    },
    // Morphology table for advanced use
    morphologyTable() {
      if (!this.result) return [];
      if (Array.isArray(this.result.morphology_features)) return this.result.morphology_features;
      if (typeof this.result.morphology_features === 'object') return [this.result.morphology_features];
      return [];
    },
    // Texture table for advanced use
    textureTable() {
      const nested = this.nestedResult;
      if (!nested) return [];
      if (Array.isArray(nested.texture_features)) return nested.texture_features;
      if (typeof nested.texture_features === 'object') return [nested.texture_features];
      return [];
    },
    // Veg indices table for advanced use
    vegIndicesTable() {
      const nested = this.nestedResult;
      if (!nested) return [];
      if (Array.isArray(nested.vegetation_features)) return nested.vegetation_features;
      if (typeof nested.vegetation_features === 'object') return [nested.vegetation_features];
      return [];
    },
  },
  methods: {
    // Get image URL by key
    getImageUrl(key) {
      return this.result && this.result[key] ? this.result[key] : '';
    },
    // Get texture image URL by band and suffix
    getTextureUrl(band, suffix) {
      const key = `texture_${band}_${suffix}`;
      return this.result && this.result[key] ? this.result[key] : '';
    },
    // Get vegetation index image URL by name
    getVegIndexUrl(name) {
      const key = `vegetation_indices_${name}`;
      return this.result && this.result[key] ? this.result[key] : '';
    },
    // Capitalize a string
    capitalize(s) {
      return s.charAt(0).toUpperCase() + s.slice(1);
    },
    // Fetch results for selected plant/date
    async fetchResults(plantId, date) {
      this.loading = true;
      try {
        this.result = await getPlantResults(plantId, date);
      } catch (e) {
        if (e.response?.status === 404) {
          try {
            await analyzePlant(plantId, date);
            this.result = await getPlantResults(plantId, date);
          } catch (analysisError) {
            console.error('Analysis failed:', analysisError);
            alert('Failed to analyze plant. Please try again later.');
          }
        } else {
          console.error('Failed to load results:', e);
          alert('Error loading results. Please try again later.');
        }
      } finally {
        this.loading = false;
      }
    },
    // Trigger analysis and poll for results
    async triggerAnalysis(plantId, date) {
      this.loading = true;
      try {
        await analyzePlant(plantId, date);
        await this.pollForResult(plantId, date);
      } catch (e) {
        this.showSnackbar('Failed to analyze plant. Please try again later.', 'error');
      } finally {
        this.loading = false;
      }
    },
    // Check if all results are ready
    allResultsReady(result) {
      // Check for main images
      const mainImages = ['original', 'mask', 'overlay', 'segmented'];
      const allMainImages = mainImages.every(k => result && result[k]);
      // Feature tables presence
      // Morphology
      const morph = result && result.morphology_features;
      const hasMorph = morph && Object.keys(morph).length > 0;
      // Texture and vegetation features (from nested _result)
      let nested = null;
      for (const key in result) {
        if (key.endsWith('_result') && typeof result[key] === 'object') {
          nested = result[key];
          break;
        }
      }
      const hasTexture = nested && nested.texture_features && Array.isArray(nested.texture_features) && nested.texture_features.length > 0;
      const hasVegFeatures = nested && nested.vegetation_features && Array.isArray(nested.vegetation_features) && nested.vegetation_features.length > 0;
      return allMainImages && hasMorph && hasTexture && hasVegFeatures;
    },
    // Poll for results every 3 seconds until all are ready
    async pollForResult(plantId, date) {
      // Poll every 3 seconds, always update UI with whatever is available
      const poll = setInterval(async () => {
        try {
          const result = await getPlantResults(plantId, date);
          if (result) {
            this.result = result; // Always update with whatever is available
            if (this.allResultsReady(result)) {
              clearInterval(poll);
            }
          }
        } catch (e) {
          // Still processing, keep polling
        }
      }, 3000);
    },
    // Open image in lightbox
    openImage(imgUrl) {
      this.viewerImg = imgUrl
      this.showViewer = true
    },
    // Download table as CSV
    downloadCSV(type) {
      let headers = [];
      let items = [];
      if (type === 'vegIndex') {
        headers = this.vegIndexHeaders.map(h => h.text);
        items = this.vegIndexItems;
      } else if (type === 'texture') {
        headers = this.textureHeaders.map(h => h.text);
        items = this.textureItems;
      } else if (type === 'morph') {
        headers = this.morphHeaders.map(h => h.text);
        items = this.morphItems;
      }
      const csv = [
        headers.join(','),
        ...items.map(row => headers.map(h => JSON.stringify(row[h.toLowerCase()])).join(','))
      ].join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${type}_table.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    },
    // Download image by URL
    downloadImage(url) {
      const a = document.createElement('a');
      a.href = url;
      a.download = url.split('/').pop();
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    // Show snackbar notification
    showSnackbar(text, color = 'success') {
      this.snackbarText = text;
      this.snackbarColor = color;
      this.snackbar = true;
    },
    // Open gallery lightbox with images
    openGallery(imgs, idx) {
      this.galleryImgs = imgs;
      this.galleryIndex = idx;
      this.showViewer = true;
    },
    // Placeholder for analyze all feature
    analyzeAll() {
      this.showSnackbar('Analyze All feature coming soon!', 'info');
    },
    // Trigger analysis for selected plant/date
    onAnalyze() {
      if (this.sidebarSelection.plantId && this.sidebarSelection.date) {
        this.triggerAnalysis(this.sidebarSelection.plantId, this.sidebarSelection.date);
        this.hasAnalyzed = true;
      }
    }
  }
};
</script>

<style scoped>
/* Layout and style for result viewer */
.result-viewer-row {
  min-height: 100vh;
  width: 100vw;
  margin: 0;
}
.sidebar-col {
  background: #fafafa;
  border-right: 1px solid #e0e0e0;
  min-height: 100vh;
  max-width: 320px;
  padding: 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
.main-content-col {
  position: relative;
  max-width: calc(100vw - 320px);
  min-height: 100vh;
  background: #fff;
  padding: 0;
  box-sizing: border-box;
}
.result-viewer {
  padding: 1rem;
  font-family: sans-serif;
}
.tabs {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}
.tabs button {
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  background: #f0f0f0;
  border: none;
}
.tabs button.active {
  background: #1976d2;
  color: white;
}
.loading {
  font-style: italic;
}
.image-grid, .thumb-grid, .band-section .thumb-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}
.image-item {
  text-align: center;
}
.image-item img, .thumb-grid img.thumb {
  max-width: 200px;
  border: 1px solid #ccc;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}
.data-table th, .data-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}
.status {
  font-size: 1.1rem;
  color: green;
  margin-top: 1rem;
}
.clickable-img {
  max-width: 200px;
}
.desktop-img {
  cursor: zoom-in;
}
.result-footer {
  border-top: 1px solid #eee;
  padding: 16px;
  margin-top: 24px;
}
.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.footer-about {
  font-size: 0.9rem;
  color: #555;
}
</style>
