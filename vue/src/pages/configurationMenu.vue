<template>
  <div :style="{ width: '100%', margin: '0', padding: '0' }">
    <v-row
      justify="center"
      align="center"
      class="bg-wave"
      no-gutters
      :style="{
        height: `auto`,
        minHeight: `100dvh`,
        width: `100%`,
        display: `flex`,
      }"
    >
      <v-col cols="12" sm="12" md="10" lg="10" xl="8" xxl="8">
        <div :style="{ marginTop: `90px`, width: `100%` }">
          <v-row class="ma-2" :style="{ paddingInline: `10px` }">
            <v-col cols="12" class="pa-1" :style="{ height: `100%` }">
              <v-card
                class="rounded-xl"
                :style="{ height: `calc(100dvh - 110px)` }"
              >
                <v-card-title>
                  <p class="gradient-text" :style="{ fontWeight: 'bold' }">
                    "Configuration Settings"
                  </p>
                  <span :style="{ fontSize: '0.8rem', color: 'grey' }">
                    Customize and manage settings to suit your preferences.
                  </span>
                </v-card-title>
                <v-card-text
                  class="pa-4 mb-5"
                  :style="{
                    overflowY: `auto`,
                    overflowX: `hidden`,
                    maxHeight: `calc(100% - 100px)`,
                    width: `100%`,
                  }"
                >
                  <div
                    :style="{ display: `flex`, flexDirection: `column` }"
                    v-for="(key, idx) in Object.keys(menu)"
                    :key="`main_menu_${key}_${idx}`"
                  >
                    <v-container>
                      <p
                        class="mb-2"
                        :style="{
                          display: `flex`,
                          alignSelf: `start`,
                          fontWeight: `bold`,
                          fontSize: `1.1rem`,
                        }"
                      >
                        {{ menuNamed(key) }}
                      </p>
                      <v-row>
                        <v-col
                          class="mb-5"
                          :style="{
                            height: `15rem`,
                            width: `15rem`,
                            filter: item.disabled ? `grayscale(1)` : ``,
                          }"
                          :cols="
                            windowWidth > 1500 ? 3 : windowWidth > 960 ? 6 : 12
                          "
                          v-for="item in menu[key]"
                        >
                          <v-card
                            :elevation="item.disabled ? `0` : `3`"
                            :disabled="item.disabled"
                            @click="clickChangeMenu(item.link)"
                            class="rounded-lg hover-tilt-glow-wave"
                            :style="{
                              height: `100%`,
                              backgroundColor: item.disabled ? `lightgrey` : ``,
                              filter: item.disabled ? `grayscale(1)` : ``,
                            }"
                          >
                            <v-card-text
                              :style="{
                                display: `flex`,
                                flexDirection: `column`,
                                height: `100%`,
                              }"
                            >
                              <div>
                                <v-icon
                                  class="gradient-text"
                                  :style="{ fontSize: `2.5rem` }"
                                  >{{ item.icon }}</v-icon
                                >
                              </div>
                              <div class="long_text_wrap my-3">
                                <span
                                  :style="{ fontSize: `1.2rem` }"
                                  :class="`gradient-text`"
                                  >{{ item.name }}</span
                                >
                              </div>
                              <div>
                                <span>{{
                                  truncateText(item.description, 100)
                                }}</span>
                              </div>
                            </v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-container>
                  </div>
                </v-card-text>
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
  name: "configurationMenu",
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      menu: {
        Configuration: [
          {
            icon: `mdi-account-cog`,
            name: `User Management`,
            description: `Manage user roles, permissions, and account settings.`,
            disabled: true,
          },
          {
            icon: `mdi-source-branch`,
            name: `Channel Management`,
            description: `Configure and monitor communication channels.`,
            disabled: true,
          },
          {
            icon: `mdi-brain`,
            name: `AI Management`,
            description: `Oversee AI configurations, settings, and performance.`,
            disabled: false,
            link: {
              internal: true,
              src: `AI_Management`,
            },
          },
          {
            icon: `mdi-database-settings`,
            name: `Data Management`,
            description: `Organize, analyze, and manage your data effectively.`,
            disabled: true,
          },
        ],
        Test: [
          {
            icon: `mdi-upload`,
            name: `Upload_Test`,
            description: `Only for developer`,
            link: {
              internal: true,
              src: `Upload_Test`,
            },
          },
        ],
      },
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
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    truncateText(text, maxLength) {
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + "...";
      }
      return text;
    },
    menuNamed(string) {
      let name = string.replaceAll(`_`, ` `);
      return name;
    },
    clickChangeMenu(item) {
      if (item.internal) {
        this.$emit("navigate", item.src);
      } else {
        window.open(item.src, "_blank");
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

.hover-tilt-glow-wave {
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease,
    border 0.3s ease;
  background: white;
  border: 2px solid;
  border-image-slice: 1;
  border-image-source: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );
  border-radius: 50px;
}

.hover-tilt-glow-wave:hover {
  transform: scale(1.1) rotateX(5deg) rotateY(10deg);
  z-index: 999;
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );
  background-size: 300% 300%;
  animation: gradient-move 1.5s linear infinite;
  box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.3),
    0px 10px 20px rgba(255, 255, 255, 0.4);
  border: 2px solid black !important;
}

@keyframes gradient-move {
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
