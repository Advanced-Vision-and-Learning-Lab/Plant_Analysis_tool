<template>
  <div class="welcome-container">
    <div class="welcome-card">
      <h1>Welcome to Plant Phenotyping Analysis</h1>
      <p>
        Analyze your plant images for biotic and abiotic stress with advanced AI-powered tools.
      </p>
      <img src="@/assets/imaging.png" alt="Plant Imaging Process" class="imaging" />
      <div class="button-group">
        <button v-if="!showPlants" @click="selectType('biotic')" class="welcome-btn biotic">Biotic</button>
        <button v-if="!showPlants" @click="selectType('abiotic')" class="welcome-btn abiotic">Abiotic</button>
        <template v-if="showPlants && selectedType === 'biotic'">
          <button class="welcome-btn biotic" @click="goToAnalyze('Sorghum')">Sorghum</button>
          <button class="welcome-btn back-btn" @click="resetSelection">Back</button>
        </template>
        <template v-if="showPlants && selectedType === 'abiotic'">
          <button class="welcome-btn abiotic" disabled>Corn</button>
          <button class="welcome-btn abiotic" disabled>Rice</button>
          <button class="welcome-btn back-btn" @click="resetSelection">Back</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Welcome",
  data() {
    return {
      showPlants: false,
      selectedType: null
    };
  },
  methods: {
    selectType(type) {
      this.selectedType = type;
      this.showPlants = true;
    },
    resetSelection() {
      this.showPlants = false;
      this.selectedType = null;
    },
    goToAnalyze(plant) {
      this.$router.push({ path: '/analyze', query: { type: this.selectedType, plant } });
    }
  }
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0ffe6 0%, #b3e6ff 100%);
}
.welcome-card {
  background: white;
  border-radius: 32px;
  box-shadow: 0 12px 48px rgba(0,0,0,0.12);
  padding: 64px 56px;
  text-align: center;
  max-width: 600px;
  width: 100%;
}
.logo {
  width: 80px;
  margin-bottom: 16px;
}
h1 {
  margin-bottom: 18px;
  color: #2e7d32;
  font-size: 2.5rem;
  font-weight: 700;
}
p {
  color: #555;
  margin-bottom: 40px;
  font-size: 1.25rem;
}
.button-group {
  display: flex;
  gap: 32px;
  justify-content: center;
  margin-top: 32px;
  flex-wrap: wrap;
}
.welcome-btn {
  padding: 20px 48px;
  border: none;
  border-radius: 12px;
  font-size: 1.25rem;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 12px rgba(67,160,71,0.08);
  font-weight: 600;
}
.biotic {
  background: #43a047;
  color: white;
}
.abiotic {
  background: #0288d1;
  color: white;
}
.welcome-btn:disabled {
  background: #bdbdbd;
  color: #eee;
  cursor: not-allowed;
  opacity: 0.7;
}
.back-btn {
  background: #eee;
  color: #333;
  margin-left: 12px;
}
.welcome-btn:hover:not(:disabled) {
  opacity: 0.95;
  box-shadow: 0 4px 24px rgba(67,160,71,0.18);
}
.imaging {
  width: 100%;
  max-width: 420px;
  margin: 32px auto 40px auto;
  display: block;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(67,160,71,0.10);
}
@media (max-width: 900px) {
  .welcome-card {
    padding: 32px 12px;
    max-width: 98vw;
  }
  .imaging {
    max-width: 260px;
  }
  .button-group {
    gap: 12px;
  }
}
</style>
