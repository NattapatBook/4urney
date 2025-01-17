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
              <!--list-->
              <v-card
                v-if="componentsMode === `list`"
                class="rounded-xl"
                :style="{ height: `calc(100dvh - 110px)` }"
              >
                <v-card-title>
                  <p class="gradient-text" :style="{ fontWeight: 'bold' }">
                    "Digital Twin Portfolio"
                  </p>
                  <span :style="{ fontSize: '0.8rem', color: 'grey' }">
                    "Explore digital twins or create and optimize your own to
                    reflect and enhance real-world assets."
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
                  <!--menu-->
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
                            //height: `15rem`,
                            //width: `15rem`,
                            filter: item.disabled ? `grayscale(1)` : ``,
                          }"
                          :cols="
                            windowWidth > 1500 ? 4 : windowWidth > 960 ? 6 : 12
                          "
                          v-for="item in menu[key]"
                        >
                          <v-card
                            :elevation="item.disabled ? `0` : `3`"
                            :disabled="item.disabled"
                            class="rounded-lg hover-tilt-glow-wave"
                            :style="{
                              height: `100%`,
                              backgroundColor: item.disabled ? `lightgrey` : ``,
                              filter: item.disabled ? `grayscale(1)` : ``,
                              cursor: `pointer`,
                            }"
                            @click="clickBot(item)"
                          >
                            <v-card-text
                              :style="{
                                display: `flex`,
                                flexDirection: `column`,
                                justifyContent: `center`,
                                height: `100%`,
                              }"
                            >
                              <div>
                                <v-avatar
                                  :style="{ height: `80px`, width: `80px` }"
                                >
                                  <v-img
                                    v-if="item.img"
                                    :src="item.img"
                                    aspect-ratio="1"
                                  ></v-img>
                                  <v-img
                                    v-else
                                    :src="`https://ui-avatars.com/api/?name=${truncateText(
                                      item.name,
                                      15
                                    )}`"
                                    aspect-ratio="1"
                                  ></v-img>
                                </v-avatar>
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
                                  truncateText(item.description, 76)
                                }}</span>
                              </div>
                              <div
                                :style="{
                                  width: `100%`,
                                  display: `flex`,
                                  justifyContent: `center`,
                                }"
                              >
                                <div
                                  class="mr-1 mt-1 py-1 px-2 rounded-xl"
                                  v-for="(chip, idx) in item.tag"
                                  :key="`digitalTwin_${item.id}_${chip}_${idx}`"
                                  :style="{
                                    display: idx >= 2 ? `none` : ``,
                                    maxWidth: `40%`,
                                    backgroundColor: `#fac9e7`,
                                    whiteSpace: `nowrap`,
                                    overflow: `hidden`,
                                    textOverflow: `ellipsis`,
                                  }"
                                >
                                  <span
                                    :style="{
                                      whiteSpace: `nowrap`,
                                      overflow: `hidden`,
                                      textOverflow: `ellipsis`,
                                    }"
                                    >{{ chip }}</span
                                  >
                                </div>
                                <div
                                  v-if="item.tag.length > 2"
                                  class="mr-1 mt-1 py-1 px-2 rounded-xl"
                                  :style="{
                                    display: idx >= 2 ? `none` : ``,
                                    maxWidth: `40%`,
                                    backgroundColor: `#fac9e7`,
                                    whiteSpace: `nowrap`,
                                    overflow: `hidden`,
                                    textOverflow: `ellipsis`,
                                  }"
                                >
                                  <span
                                    :style="{
                                      whiteSpace: `nowrap`,
                                      overflow: `hidden`,
                                      textOverflow: `ellipsis`,
                                      fontWeight: `bold`,
                                    }"
                                    >+{{ item.tag.length - 2 }}</span
                                  >
                                </div>
                              </div>
                            </v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-container>
                  </div>
                  <!--add new-->
                  <div :style="{ display: `flex`, flexDirection: `column` }">
                    <v-container>
                      <v-row>
                        <v-col class="mb-5" cols="12">
                          <v-card
                            @click="clickBot(null)"
                            class="rounded-lg hover-tilt-glow-wave"
                            :style="{
                              height: `100%`,

                              cursor: `pointer`,
                            }"
                          >
                            <v-card-text
                              :style="{
                                display: `flex`,
                                flexDirection: `column`,
                                justifyContent: `center`,
                                height: `100%`,
                              }"
                            >
                              <div
                                :style="{
                                  display: `flex`,
                                  alignItems: `center`,
                                  justifyContent: `center`,
                                }"
                              >
                                <v-icon
                                  class="gradient-text"
                                  :style="{ fontSize: `1.5rem` }"
                                  >mdi-plus-circle-outline</v-icon
                                >
                                &nbsp;
                                <span class="gradient-text"
                                  >Create New Digital Twin</span
                                >
                              </div>
                            </v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-container>
                  </div>
                </v-card-text>
              </v-card>
              <!--create&edit-->
              <DigitalTwinConfig
                v-else-if="componentsMode === `createBot`"
                @backToMain="componentsMode = `list`"
                :item="botItem"
              />
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DigitalTwinConfig from "@/components/digitalTwin/digitalTwinConfig.vue";

export default {
  name: "configurationMenu",
  components: { DigitalTwinConfig },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      menu: {
        Org_Digital_Twin: [
          {
            id: "111",
            name: "Agriculture Expert",
            description:
              "Focused on optimizing agriculture with expertise in fertilizers, drone technology, and crop disease management.",
            tag: ["Fertilizer", "DroneCrop", "Disease"],
            img: "https://jakkanoom.github.io/4urneyRoadmap/assets/twilight-C5vCOEMj.png",
            disabled: false,
          },
          {
            id: "222",
            name: "Data Analyst",
            description:
              "Specializes in data visualization and summarization for actionable insights.",
            tag: ["VisualizationData", "Summarization"],
            img: "https://jakkanoom.github.io/4urneyRoadmap/assets/starlight-B5KTr0eO.png",
            disabled: false,
          },
          {
            id: "333",
            name: "Sales Person",
            description:
              "A knowledgeable resource for products, sales strategies, and expertise.",
            tag: ["Product", "KnowledgeSales", "Expertise"],
            img: "https://jakkanoom.github.io/4urneyRoadmap/assets/pinky-DRiVgFHX.png",
            disabled: false,
          },
        ],
        Developer_Digital_Twin: [
          {
            id: "444",
            name: "Backend Master",
            description:
              "Skilled in APIs, databases, and advanced backend development (currently disabled).",
            tag: ["API", "APT", "Database", "Manchester United"],
            img: "https://i.ytimg.com/vi/_mPDAQm58i8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLC6FUnQqoRI2VllYnROF6rX-nmR7w",
            disabled: true,
          },
          {
            id: "555",
            name: "Testing",
            description:
              "Focused on comprehensive testing processes (currently disabled).",
            tag: [
              "long texttttt",
              "long texttttt",
              "long texttttt",
              "long texttttt",
              "long texttttt",
              "long texttttt",
              "long texttttt",
              "long texttttt",
              "long texttttt",
            ],
            img: "",
            disabled: true,
          },
        ],
      },
      //bot
      componentsMode: `list`,
      botMode: `create`,
      botItem: null,
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
    clickBot(item) {
      this.componentsMode = `createBot`;
      this.botItem = item;
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

.v-chip__content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
