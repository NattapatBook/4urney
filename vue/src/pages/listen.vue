<template>
  <div :style="{ width: '100%', margin: '0', padding: '0' }">
    <v-row
      justify="center"
      align="center"
      class="bg-wave"
      no-gutters
      :style="{
        height: `auto`,
        minHeight: `100vh`,
        width: `100%`,
        justifyItems: `center`,
      }"
    >
      <v-col cols="12">
        <div :style="{ marginTop: `84px`, width: `100%` }">
          <v-row class="ma-2">
            <!-- list panel -->
            <v-col
              v-if="!hideListuserPanel"
              :cols="windowWidth > 1280 ? 3 : windowWidth > 960 ? 4 : 12"
              class="pa-1"
              :style="{ height: `100%` }"
            >
              <v-card
                :style="{
                  height: `calc(100vh - 14vh)`,
                  marginBottom: windowWidth > 960 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <v-card-title>
                  <v-btn
                    @click="hideListuserPanel = true"
                    :icon="`mdi-chevron-left`"
                  />
                </v-card-title>
                <v-card-text>
                  <v-btn @click="scrollTo(`chatPanel`)">go chat</v-btn>
                  <v-btn @click="scrollTo(`dashboard`)">dashboard</v-btn>
                </v-card-text>
              </v-card>
            </v-col>
            <!-- hide list panel -->
            <v-col
              v-else
              class="pa-1"
              :style="{
                height: `100%`,
                maxWidth: `fit-content`,
                flex: `0 0 auto`,
              }"
            >
              <v-card
                :style="{
                  height: `calc(100vh - 14vh)`,
                  marginBottom: windowWidth > 960 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <v-btn
                  @click="hideListuserPanel = false"
                  :icon="`mdi-chevron-right`"
                />
              </v-card>
            </v-col>
            <!-- chat panel -->
            <v-col
              id="chatPanel"
              class="pa-1"
              :style="{
                height: `100%`,
              }"
            >
              <v-card
                :style="{
                  height: `calc(100vh - 14vh)`,
                  marginBottom: windowWidth > 960 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
                >chat col
              </v-card>
            </v-col>
            <v-col
              id="dashboard"
              :cols="windowWidth > 1280 ? 4 : windowWidth > 960 ? 4 : 12"
              class="pa-1"
              :style="{
                height: `100%`,
                display: testDash ? `none` : ``,
              }"
            >
              <v-card
                :style="{
                  height: `calc(100vh - 14vh)`,
                  marginBottom: windowWidth > 960 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                Dash
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "listen",
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      hideListuserPanel: false,
      testDash: false,
    };
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    // Resizes the window and updates window dimensions
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    // Toggles the visibility of the first column
    toggleFirstCol() {
      this.isFirstColMinimized = !this.isFirstColMinimized;
    },
    scrollTo(id) {
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    },
  },
};
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}
.bg-wave {
  box-sizing: border-box;
}

/* Add custom styles to handle vertical toolbar */
.v-col {
  transition: all 0.3s ease;
}

.v-card {
  padding: 10px;
}
</style>
