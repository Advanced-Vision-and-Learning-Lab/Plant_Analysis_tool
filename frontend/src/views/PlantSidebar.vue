<template>
  <v-card class="sidebar-card" flat>
    <div class="calendar-top-section">
      <div class="selected-date-label" v-if="selectedDate">
        Selected Date: <strong>{{ selectedDate }}</strong>
      </div>
      <v-date-picker
        v-model="selectedDate"
        color="success"
        :min="minDate"
        :max="maxDate"
        @input="emitSelection"
        class="modern-date-picker"
      />
      <v-btn
        color="success"
        large
        block
        class="analyze-btn"
        :disabled="!selectedPlant || !selectedDate"
        @click="$emit('analyze')"
        style="margin: 18px 0 18px 0; font-size: 1.2rem; font-weight: 700; border-radius: 12px;"
      >
        Analyze
      </v-btn>
    </div>
    <v-list dense class="plant-list modern-plant-list">
      <v-list-item
        v-for="plant in filteredPlants"
        :key="plant.id"
        :value="plant.id"
        @click="selectPlant(plant)"
        :class="['modern-plant-item', { 'selected-plant': plant.id === selectedPlant?.id }]"
      >
        <v-list-item-content>
          <v-list-item-title class="plant-title">
            {{ plant.name }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: "PlantSidebar",
  props: {
    plants: Array, // [{id, name, availableDates: [YYYY-MM-DD, ...]}, ...]
    minDate: String,
    maxDate: String,
    value: Object // { plantId, date }
  },
  data() {
    return {
      search: "",
      selectedPlant: null,
      selectedDate: null
    };
  },
  computed: {
    filteredPlants() {
      if (!this.search) return this.plants;
      return this.plants.filter(p =>
        p.name.toLowerCase().includes(this.search.toLowerCase()) ||
        p.id.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },
  watch: {
    value: {
      immediate: true,
      handler(val) {
        if (val) {
          this.selectedPlant = this.plants.find(p => p.id === val.plantId) || null;
          this.selectedDate = val.date || null;
        }
      }
    }
  },
  methods: {
    selectPlant(plant) {
      this.selectedPlant = plant;
      this.emitSelection();
    },
    emitSelection() {
      this.$emit("input", {
        plantId: this.selectedPlant ? this.selectedPlant.id : null,
        date: this.selectedDate
      });
    }
  }
};
</script>

<style scoped>
.sidebar-card {
  width: 320px;
  height: 100%;
  border-radius: 24px 0 0 24px;
  border-right: 1.5px solid #e0e0e0;
  box-shadow: 2px 0 16px rgba(67,160,71,0.06);
  padding: 0;
  font-family: 'Inter', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #f9f9fb 60%, #e3f2fd 100%);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  overflow-y: auto;
}
.calendar-top-section {
  padding: 24px 16px 8px 16px;
  background: #f5f5f5;
  border-radius: 24px 0 0 0;
  box-shadow: 0 2px 12px rgba(67,160,71,0.06);
  border: 2px solid #43a047;
  z-index: 10;
  position: relative;
}
.selected-date-label {
  font-size: 1.08rem;
  color: #388e3c;
  text-align: center;
  margin-bottom: 8px;
  font-weight: 600;
}
.analyze-btn {
  margin-top: 12px;
  margin-bottom: 12px;
}
.plant-list.modern-plant-list {
  overflow-y: auto;
  padding: 0 16px;
  margin-bottom: 12px;
}
.modern-plant-item {
  margin: 10px 0;
  border-radius: 14px;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  cursor: pointer;
  box-shadow: 0 1px 8px rgba(67,160,71,0.04);
  background: #fff;
  padding: 0 12px;
  min-height: 48px;
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  border: 1.5px solid transparent;
}
.modern-plant-item:hover {
  background: #e3f2fd;
  box-shadow: 0 4px 16px rgba(67,160,71,0.10);
  transform: translateY(-2px) scale(1.02);
}
.selected-plant {
  background: #c8e6c9 !important;
  font-weight: bold;
  color: #1b5e20;
  box-shadow: 0 4px 20px rgba(67,160,71,0.14);
  border: 1.5px solid #43a047;
}
.plant-title {
  font-size: 1.18rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: #222;
  padding: 10px 0;
}
</style>
