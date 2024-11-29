<script setup lang="ts">
import { ref, onMounted } from "vue";
import AppLayout from "./components/layouts/AppLayout.vue";

import LandingPage from "./pages/LandingPage.vue";

import HomePage from "./pages/HomePage.vue";

import { createPersistentWebSocket } from "@/utils/websocket";
import Listen from "./pages/listen.vue";

const currentPage = ref("landing");

function navigateTo(page) {
  currentPage.value = page;
}

const messages = ref([]);
const ws = createPersistentWebSocket("chat_center/chat/", (event) => {
  messages.value.push(event);
});
onMounted(async () => {
  //nothing just meme
  console.log(
    "%c%s",
    "font-size: 13em; color: #ff6347; background: #222; padding: 100px; text-align: center;",
    "👀 I see you creeping... 😏 What you doing here? 🤔"
  );

  console.log(ws);
});
const message = ref("");
function sendmessage() {
  ws.send(message.value);
  message.value = "";
}
</script>

<template>
  <div id="app" :style="{ overflowX: 'hidden' }">
    <!-- Background -->
    <div
      :class="currentPage === `landing` ? `` : `bg-wave`"
      :style="{ minHeight: currentPage === `landing` ? `` : `100%` }"
    ></div>

    <!-- LandingPage -->
    <transition name="fade" mode="out-in">
      <div :key="`landing_app_${currentPage}`">
        <LandingPage v-if="currentPage === 'landing'" @navigate="navigateTo" />
      </div>
    </transition>

    <!-- App Layout -->
    <transition name="fade" mode="out-in">
      <AppLayout v-if="currentPage !== 'landing'" @navigate="navigateTo">
        <transition name="minimal-fade" mode="out-in">
          <HomePage v-if="currentPage === 'home'" @navigate="navigateTo" />
          <Listen v-else-if="currentPage === 'listen'" @navigate="navigateTo" />
        </transition>
      </AppLayout>
    </transition>
  </div>
</template>

<style scoped>
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* Minimal Fade Transition */
.minimal-fade-enter-active,
.minimal-fade-leave-active {
  transition: opacity 0.4s ease; /* Smoother and quicker fade */
}

.minimal-fade-enter,
.minimal-fade-leave-to {
  opacity: 0;
}

.minimal-fade-enter-to,
.minimal-fade-leave {
  opacity: 1;
}
</style>

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

/* Animation */

.bg-wave {
  display: inline-block;
  width: 100%;
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

.shake {
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20%,
  60% {
    transform: translateX(-10px);
  }
  40%,
  80% {
    transform: translateX(10px);
  }
}

.hover-bounce:hover {
  transform: scale(1.1) translateY(-10px);
  z-index: 999;
  animation: bounce 0.4s ease-out;
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.2), 0px 5px 10px rgba(0, 0, 0, 0.1);
}

@keyframes bounce {
  0% {
    transform: scale(1.05) translateY(-5px);
  }
  50% {
    transform: scale(1.1) translateY(-15px);
  }
  100% {
    transform: scale(1.1) translateY(-10px);
  }
}

.hover-tilt-glow {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-tilt-glow:hover {
  transform: scale(1.1) rotateX(10deg) rotateY(10deg);
  z-index: 999;
  box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.3),
    0px 10px 20px rgba(255, 255, 255, 0.4);
  animation: glow-pulse 1s ease infinite;
}

@keyframes glow-pulse {
  0% {
    box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.3),
      0px 10px 20px rgba(255, 255, 255, 0.2);
  }
  50% {
    box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.2),
      0px 10px 25px rgba(255, 255, 255, 0.6);
  }
  100% {
    box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.3),
      0px 10px 20px rgba(255, 255, 255, 0.2);
  }
}

.hover-tilt-glow {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  perspective: 1000px;
}
</style>
