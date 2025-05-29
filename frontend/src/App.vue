<template>
  <v-app>
    <div class="header-bar">
      <img src="@/assets/logo.png" alt="Logo" class="header-logo" />
    </div>
    <v-main>
      <router-view />
    </v-main>
    <div>
      <v-btn @click="show = true">Open Calendar</v-btn>
      <v-dialog v-model="show" attach="body">
        <v-card>
          <v-date-picker v-model="date" />
        </v-card>
      </v-dialog>
    </div>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data: () => ({
    show: false,
    date: null
  })
};
</script>

<style>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
}
.logo-header {
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  min-height: 80px;
}
.header-bar {
  width: 100vw;
  min-width: 100vw;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  background: #7c2328;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 0;
  box-sizing: border-box;
  height: 140px;
}
.header-logo {
  max-width: 100%;
  max-height: 110px;
  width: auto;
  height: auto;
  object-fit: contain;
  transform: scale(1.2);
}
</style>
