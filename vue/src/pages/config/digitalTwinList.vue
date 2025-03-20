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
                    Digital Twin Portfolio
                  </p>
                  <span :style="{ fontSize: '0.8rem', color: 'grey' }">
                    "Explore digital twins or create and optimize your own to
                    reflect and enhance real-world assets."
                  </span>
                </v-card-title>
                <v-card-text :class="windowWidth > 900 ? `` : `pa-3`">
                  <div
                    :style="{
                      textAlign: `-webkit-center`,
                    }"
                  >
                    <div
                      :style="{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        flexDirection: 'row',
                        alignContent: 'center',
                        maxWidth: `420px`,
                      }"
                    >
                      <v-text-field
                        class="mr-3"
                        v-model="filterTerm"
                        density="compact"
                        label="Filter by bot name"
                        hide-details
                        variant="outlined"
                        rounded="xl"
                        clearable
                      ></v-text-field>
                      <v-tooltip text="Tooltip" location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            class="mr-2"
                            @click="clickBot(null)"
                            v-bind="props"
                            icon
                            color="primary"
                          >
                            <v-icon>mdi-plus</v-icon>
                          </v-btn>
                        </template>
                        <span>Create chatbot</span>
                      </v-tooltip>
                      <v-menu
                        v-model="menuFilter"
                        offset-y
                        :close-on-content-click="false"
                        transition="scale-transition"
                        location="bottom"
                      >
                        <template v-slot:activator="{ props }">
                          <v-tooltip text="Tooltip" location="bottom">
                            <template
                              v-slot:activator="{ props: tooltipProps }"
                            >
                              <v-btn
                                v-bind="{ ...props, ...tooltipProps }"
                                icon
                                color="primary"
                              >
                                <v-icon>mdi-filter</v-icon>
                              </v-btn>
                            </template>
                            Filter
                          </v-tooltip>
                        </template>
                        <v-card
                          elevation="0"
                          :style="{
                            height: `100%`,
                            width: `100%`,
                            borderRadius: `8px`,
                            border: `solid 1px lightgrey`,
                          }"
                        >
                          <v-card-title
                            :style="{
                              display: `flex`,
                              alignItems: `center`,
                            }"
                          >
                            <span :style="{ fontWeight: `bold` }"
                              >Chatbot Filter</span
                            >
                            <v-spacer />
                            <v-btn
                              @click="menuFilter = false"
                              variant="text"
                              icon="mdi-close"
                            ></v-btn>
                          </v-card-title>
                          <div
                            :style="{
                              overflowY: `auto`,
                              overflowX: `hidden`,
                            }"
                          >
                            <!-- filter Status -->
                            <v-card-text class="pt-2 pb-4">
                              <v-autocomplete
                                v-model="isActiveFilter"
                                label="Is Active Filter"
                                variant="outlined"
                                hide-details
                                rounded="lg"
                                item-title="title"
                                item-value="val"
                                density="comfortable"
                                :color="`#ff5d97`"
                                :items="isActiveFilterItem"
                                :style="{
                                  textTransform: `capitalize`,
                                }"
                                @update:model-value="
                                  changeStatusFilter(isActiveFilter, `isActive`)
                                "
                              >
                              </v-autocomplete>
                            </v-card-text>
                            <!-- filter isPublish -->
                            <v-card-text class="pt-2">
                              <v-autocomplete
                                v-model="isPublishFilter"
                                label="Is Publish Filter"
                                variant="outlined"
                                hide-details
                                rounded="lg"
                                item-title="title"
                                item-value="val"
                                density="comfortable"
                                :color="`#ff5d97`"
                                :items="isPublishFilterItem"
                                :style="{
                                  textTransform: `capitalize`,
                                }"
                                @update:model-value="
                                  changeStatusFilter(
                                    isPublishFilter,
                                    `isPublish`
                                  )
                                "
                              >
                              </v-autocomplete>
                            </v-card-text>
                          </div>
                        </v-card>
                      </v-menu>
                    </div>
                  </div>
                </v-card-text>
                <v-card-text
                  class="pa-4 pt-0"
                  :style="
                    isLoading || isError || menu.DigitalTwin.length < 1
                      ? {
                          height: `calc(100% - 220px)`,
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: `center`,
                        }
                      : {
                          overflowY: `auto`,
                          overflowX: `hidden`,
                          maxHeight: `calc(100% - 170px)`,
                          width: `100%`,
                        }
                  "
                >
                  <div v-if="isLoading">
                    <Loading
                      :message="`Loading Chatbot List, please wait...`"
                    />
                  </div>
                  <div
                    v-else-if="
                      !isLoading && (isError || menu.DigitalTwin.length < 1)
                    "
                  >
                    <DataError
                      :message="
                        menu.DigitalTwin.length < 1 ? `No Data` : errMsg
                      "
                    />
                  </div>
                  <!--menu-->
                  <div
                    v-else-if="!isLoading && !isError"
                    :style="{ display: `flex`, flexDirection: `column` }"
                    v-for="(key, idx) in Object.keys(menu)"
                    :key="`main_menu_${key}_${idx}`"
                  >
                    <v-container class="py-0">
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
                      <v-row
                        v-if="filteredMenu[key].length < 1"
                        :style="{
                          minHeight: `calc(100dvh - 305px)`,
                          display: `flex`,
                          alignItems: `center`,
                          overflow: `hidden`,
                        }"
                      >
                        <v-col cols="12">
                          <DataError :message="`No Data Avaliable`" />
                        </v-col>
                      </v-row>
                      <v-row v-else>
                        <v-col
                          class="mb-5"
                          :cols="
                            windowWidth > 1500 ? 4 : windowWidth > 960 ? 6 : 12
                          "
                          v-for="item in filteredMenu[key]"
                        >
                          <v-card
                            :elevation="!item.isPublish ? `0` : `3`"
                            class="rounded-lg"
                            :style="{
                              height: `100%`,
                              backgroundColor: !item.isPublish
                                ? `lightgrey`
                                : ``,
                              //filter: !item.isActive ? `grayscale(1)` : ``,
                              //cursor: `pointer`,
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
                              <div>
                                <div
                                  :style="{
                                    display: `flex`,
                                    justifyContent: `space-between`,
                                    alignItems: `center`,
                                  }"
                                >
                                  <div>
                                    <v-tooltip text="Tooltip" location="bottom">
                                      <template v-slot:activator="{ props }">
                                        <div
                                          v-bind="props"
                                          :style="{ cursor: `pointer` }"
                                        >
                                          <v-chip
                                            :color="
                                              item.isPublish
                                                ? '#5EB491'
                                                : '#D6584D'
                                            "
                                          >
                                            <span>
                                              {{
                                                item.isPublish
                                                  ? `Publish`
                                                  : `Unpublish`
                                              }}
                                            </span>
                                          </v-chip>
                                          <v-chip
                                            class="ml-1"
                                            :color="
                                              item.isActive
                                                ? '#5EB491'
                                                : '#D6584D'
                                            "
                                            v-bind="props"
                                          >
                                            <v-icon>{{
                                              item.isActive
                                                ? `mdi-robot`
                                                : `mdi-robot-off`
                                            }}</v-icon>
                                          </v-chip>
                                        </div>
                                      </template>
                                      <p>
                                        <span>Is Publish : </span>
                                        <span
                                          :style="{
                                            fontWeight: `bold`,
                                            color: item.isPublish
                                              ? '#5EB491'
                                              : '#D6584D',
                                          }"
                                        >
                                          {{
                                            item.isPublish
                                              ? `Publish`
                                              : `Unpublish`
                                          }}
                                        </span>
                                      </p>
                                      <p>
                                        <span>Is Active : </span>
                                        <span
                                          :style="{
                                            fontWeight: `bold`,
                                            color: item.isActive
                                              ? '#5EB491'
                                              : '#D6584D',
                                          }"
                                        >
                                          {{
                                            item.isActive
                                              ? `Active`
                                              : `Inactive`
                                          }}
                                        </span>
                                      </p>
                                    </v-tooltip>
                                  </div>
                                  <!-- <v-btn
                                    @click="clickBot(item)"
                                    :icon="`mdi-cog`"
                                  /> -->
                                  <v-menu
                                    transition="fab-transition"
                                    class="rounded-xl"
                                  >
                                    <template v-slot:activator="{ props }">
                                      <v-btn
                                        class="no-ripple"
                                        icon="mdi-dots-vertical"
                                        variant="text"
                                        v-bind="props"
                                      ></v-btn>
                                    </template>

                                    <v-list class="pa-0 rounded-lg">
                                      <!-- Config Action -->
                                      <v-list-item
                                        class="pa-0"
                                        @click="clickBot(item)"
                                      >
                                        <v-card
                                          class="pa-4 d-flex align-center"
                                          elevation="0"
                                        >
                                          <v-icon>mdi-cog</v-icon>
                                          <span class="ms-2"
                                            >Configuration</span
                                          >
                                        </v-card>
                                      </v-list-item>

                                      <!-- Delete Action -->
                                      <v-list-item
                                        class="pa-0"
                                        @click="clickDeleteBot(item)"
                                      >
                                        <v-card
                                          class="pa-4 d-flex align-center"
                                          elevation="0"
                                        >
                                          <v-icon>mdi-delete</v-icon>
                                          <span class="ms-2">Remove</span>
                                        </v-card>
                                      </v-list-item>
                                    </v-list>
                                  </v-menu>
                                </div>
                              </div>
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
                              <div v-if="item.description">
                                <span>{{
                                  truncateText(item.description, 76)
                                }}</span>
                              </div>
                              <div>
                                <span
                                  >Industry :
                                  {{ truncateText(item.industry, 30) }}</span
                                ><br />
                                <span
                                  >Mastery :
                                  {{ truncateText(item.mastery, 30) }}</span
                                >
                              </div>
                              <div
                                v-if="item.tag"
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
                              <div>
                                <div
                                  :style="{
                                    height: `48px`,
                                  }"
                                ></div>
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
                @backToMain="clickBackToMain"
                @callbackNewSaveDraft="firstTimeSaveDraft"
                @catchEditErr="getErrOnEdit"
                :item="botItem"
                :session="botSession"
              />
            </v-col>
          </v-row>
        </div>
      </v-col>
      <!--snackbar-->
      <v-snackbar
        v-model="snackbarAlert"
        timeout="5000"
        :color="snackbarSuccess ? '#5EB491' : '#D6584D'"
        location="top"
        location-strategy="connected"
      >
        <span>
          <v-icon v-if="snackbarSuccess"
            >mdi-checkbox-marked-circle-outline</v-icon
          >
          <v-icon v-else>mdi-alert-circle</v-icon>
          {{ snackbarMsg }}
        </span>

        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="snackbarAlert = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-row>
  </div>
</template>

<script>
import DigitalTwinConfig from "@/components/digitalTwin/digitalTwinConfigReDesign.vue";
import DataError from "@/components/tools/dataError.vue";
import Loading from "@/components/tools/loading.vue";
import axios from "axios";
export default {
  name: "configurationMenu",
  components: { DigitalTwinConfig, Loading, DataError },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      menu: {
        DigitalTwin: [],
      },
      filterTerm: ``,
      //bot
      componentsMode: `list`,
      botMode: `create`,
      botItem: null,
      botSession: null,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: `untitled`,
      //filter
      menuFilter: false,
      isActiveFilter: null,
      isActiveFilterItem: [
        { title: "All", val: null },
        { title: "Active", val: true },
        { title: "Inactive", val: false },
      ],
      isPublishFilter: null,
      isPublishFilterItem: [
        { title: "All", val: null },
        { title: "Publish", val: true },
        { title: "Unpublish", val: false },
      ],
      //loading
      isLoading: false,
      isError: false,
      errorMsg: `untitled`,
    };
  },
  computed: {
    filteredMenu() {
      const filtered = {};

      for (const key in this.menu) {
        let items = this.menu[key];
        const filterTerm = this.filterTerm ? this.filterTerm.trim() : "";
        if (filterTerm) {
          items = items.filter((item) =>
            item.name.toLowerCase().includes(filterTerm.toLowerCase())
          );
        }

        if (this.isActiveFilter !== null) {
          items = items.filter((item) => item.isActive === this.isActiveFilter);
        }

        if (this.isPublishFilter !== null) {
          items = items.filter(
            (item) => item.isPublish === this.isPublishFilter
          );
        }

        filtered[key] = items;
      }

      return filtered;
    },
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
    this.getListUser();
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
    async getListUser() {
      this.isLoading = false;
      this.isLoading = true;
      this.isError = false;
      axios
        .get(`api/chat_center/list_bot_ai_management/`)
        .then((res) => {
          this.menu.DigitalTwin = res.data;
          this.isLoading = false;
          this.isError = false;
        })
        .catch((err) => {
          this.errorMsg = err;
          this.isLoading = false;
          this.isError = true;
        });
    },
    firstTimeSaveDraft(item) {
      this.botItem = JSON.parse(JSON.stringify(item.botItem));
      this.botSession = JSON.parse(JSON.stringify(item.botSession));
    },
    // createBotAction(item) {
    //   if (item.case) {
    //     this.componentsMode = `list`;
    //     this.getListUser();
    //     this.snackbarSuccess = true;
    //     this.snackbarMsg = item.msg;
    //     this.snackbarAlert = true;
    //   } else {
    //     this.snackbarSuccess = false;
    //     this.snackbarMsg = item.msg;
    //     this.snackbarAlert = true;
    //   }
    // },
    clickDeleteBot(item) {
      axios
        .post(`api/chat_center/remove_bot/`, {
          id: item.id,
        })
        .then(() => {
          // this.menu.DigitalTwin = res.data;
          this.getListUser();
        })
        .catch((err) => {
          this.$emit(`catchEditErr`, err);
        });
    },
    changeStatusFilter(item, mode) {
      if (mode === `isActive`) {
        this.isActiveFilter = item;
      } else {
        this.isPublishFilter = item;
      }
    },
    clickBackToMain() {
      this.componentsMode = `list`;
      this.getListUser();
    },
    getErrOnEdit(msg) {
      this.snackbarMsg = msg;
      this.snackbarSuccess = false;
      this.snackbarAlert = true;
      this.clickBackToMain();
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
