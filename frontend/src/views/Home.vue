<template>
  <div>
    <h1>Select Plant Group</h1>
    <button @click="selectGroup('Biotic-East')">Biotic-East</button>
    <button @click="selectGroup('Abiotic-west')">Abiotic-west</button>
  </div>
</template>

<script>
export default {
  methods: {
    selectGroup(group) {
      localStorage.setItem('plantGroup', group);
      if (group === 'Biotic-East') {
        localStorage.setItem('plantType', 'Sorghum');
      }
      this.$router.push('/select-plant');
    }
  }
};
</script>
