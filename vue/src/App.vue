<script setup>
import { ref } from "vue";
import AppLayout from "./components/layouts/AppLayout.vue";

import LandingPage from "./pages/LandingPage.vue";

import HomePage from "./pages/HomePage.vue";

const currentPage = ref("landing");

function navigateTo(page) {
  currentPage.value = page;
}
</script>

<template>
  <div id="app">
    <LandingPage v-if="currentPage === 'landing'" @navigate="navigateTo" />

    <AppLayout v-else @navigate="navigateTo">
      <HomePage v-if="currentPage === 'home'" @navigate="navigateTo" />
    </AppLayout>
  </div>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap");
body {
  font-family: "Poppins", "Noto Sans Thai", sans-serif;
}
.background_app {
  overflow: hidden;
  /*background-color: #3a2d4b;*/
  background-color: #333333;
  background-attachment: fixed;
  width: 100vw;
  overflow: hidden;
}
::-webkit-scrollbar {
  width: 8px;
}

/* Track */
::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1) !important;
}

/* Handle */
::-webkit-scrollbar-thumb {
  opacity: 0.1;
  background: rgba(0, 0, 0, 0.5);
}
.gradient-text {
  background: linear-gradient(
    45deg,
    rgba(254, 56, 147, 1) 0%,
    rgba(55, 61, 133, 1) 59%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.bg-wave {
  display: inline-block;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );

  background-size: 400% 400%;
  animation: bgAnimation 12s ease infinite;
  color: #ffffff;
  font-size: 1.5rem;
  text-align: center;
  padding: 10px;
  border-radius: 8px;
  position: absolute;
}

@keyframes bgAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
