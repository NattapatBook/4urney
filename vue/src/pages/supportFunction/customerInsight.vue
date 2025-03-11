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
                    Customer Insight
                  </p>
                  <span :style="{ fontSize: '0.8rem', color: 'grey' }">
                    "Better understand your customers by capturing chatbot
                    data."
                  </span>
                </v-card-title>
                <v-card-text class="px-4 pb-0">
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
                        v-model="filter"
                        density="compact"
                        label="Filter"
                        hide-details
                        variant="outlined"
                        rounded="xl"
                        clearable
                        :disabled="isLoading || isError"
                      ></v-text-field>
                      <v-tooltip text="Tooltip" location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            class="mr-2"
                            v-bind="props"
                            :disabled="isLoading || isError"
                            icon
                            color="primary"
                            @click="onUpload"
                          >
                            <v-icon>mdi-download</v-icon>
                          </v-btn>
                        </template>
                        <span>Download</span>
                      </v-tooltip>
                      <v-tooltip text="Tooltip" location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            v-bind="props"
                            :disabled="isLoading || isError"
                            icon
                            color="primary"
                            @click="getList"
                          >
                            <v-icon>mdi-refresh</v-icon>
                          </v-btn>
                        </template>
                        <span>Refresh</span>
                      </v-tooltip>
                    </div>
                  </div>
                  <v-container>
                    <v-row>
                      <v-col
                        class="px-0"
                        :style="{
                          width: windowWidth > 660 ? `25%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <v-btn
                            block
                            :style="{ textTransform: `capitalize` }"
                            variant="text"
                            @click="this.setSort(`field_name`)"
                            >Field Name
                            <v-icon v-if="sortKey === `field_name`">
                              &nbsp;{{
                                sortOrder ? `mdi-arrow-up` : `mdi-arrow-down`
                              }}
                            </v-icon>
                          </v-btn>
                        </div>
                      </v-col>
                      <v-col
                        class="px-0"
                        :style="{
                          width: windowWidth > 660 ? `25%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <v-btn
                            block
                            :style="{ textTransform: `capitalize` }"
                            variant="text"
                            @click="this.setSort(`result`)"
                            >Result
                            <v-icon v-if="sortKey === `result`">
                              &nbsp;{{
                                sortOrder ? `mdi-arrow-up` : `mdi-arrow-down`
                              }}
                            </v-icon></v-btn
                          >
                        </div>
                      </v-col>
                      <v-col
                        class="px-0"
                        v-if="windowWidth > 660"
                        :style="{
                          width: windowWidth > 660 ? `25%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <v-btn
                            block
                            :style="{ textTransform: `capitalize` }"
                            variant="text"
                            @click="this.setSort(`username`)"
                            >Username
                            <v-icon v-if="sortKey === `uploaded_at`">
                              &nbsp;{{
                                sortOrder ? `mdi-arrow-up` : `mdi-arrow-down`
                              }}
                            </v-icon></v-btn
                          >
                        </div>
                      </v-col>
                      <v-col
                        class="px-0"
                        v-if="windowWidth > 660"
                        :style="{
                          width: windowWidth > 660 ? `25%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <v-btn
                            block
                            :style="{ textTransform: `capitalize` }"
                            variant="text"
                            @click="this.setSort(`message`)"
                            >Message
                            <v-icon v-if="sortKey === `message`">
                              &nbsp;{{
                                sortOrder ? `mdi-arrow-up` : `mdi-arrow-down`
                              }}
                            </v-icon></v-btn
                          >
                        </div>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-text
                  class="pa-4 pt-0"
                  :style="
                    isLoading ||
                    isError ||
                    sort(filteredData, sortKey, sortOrder).length < 1
                      ? {
                          height: `calc(100% - 200px)`,
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: `center`,
                        }
                      : {
                          overflowY: `auto`,
                          overflowX: `hidden`,
                          maxHeight: `calc(100% - 200px)`,
                          width: `100%`,
                        }
                  "
                >
                  <div v-if="isLoading">
                    <Loading
                      :message="`Loading Customer Insight, please wait...`"
                    />
                  </div>
                  <div
                    v-else-if="
                      !isLoading &&
                      (isError ||
                        sort(filteredData, sortKey, sortOrder).length < 1)
                    "
                  >
                    <DataError
                      :message="
                        sort(filteredData, sortKey, sortOrder).length < 1
                          ? `No Data Avaliable`
                          : errMsg
                      "
                    />
                  </div>
                  <v-card
                    v-else-if="
                      !isLoading &&
                      !isError &&
                      sort(filteredData, sortKey, sortOrder).length > 0
                    "
                    class="mb-2 rounded-xl py-2"
                    elevation="0"
                    :style="{ border: `solid 1px lightgrey` }"
                    v-for="(item, idx) in sort(
                      filteredData,
                      sortKey,
                      sortOrder
                    )"
                    :key="`customerInsight_list_${idx}`"
                  >
                    <v-container class="py-0 px-3">
                      <v-row>
                        <v-col
                          class="px-0"
                          :style="{
                            width: windowWidth > 660 ? `25%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div :style="{ textAlign: `center` }">
                            <v-tooltip text="Tooltip" location="bottom">
                              <template v-slot:activator="{ props }">
                                <v-chip
                                  :color="`#1867c0`"
                                  v-bind="props"
                                  :size="
                                    windowWidth > 660 ? `default` : `small`
                                  "
                                  dark
                                  small
                                >
                                  <div
                                    :style="{
                                      whiteSpace: `nowrap`,
                                      overflow: `hidden`,
                                      textOverflow: `ellipsis`,
                                      maxWidth: `140px`,
                                      cursor: `pointer`,
                                    }"
                                  >
                                    {{ item.field_name }}
                                  </div>
                                </v-chip>
                              </template>
                              <p :style="{ fontWeight: `bold` }">Field Name</p>
                              <span> {{ item.field_name }}</span>
                            </v-tooltip>
                          </div>
                        </v-col>
                        <v-col
                          class="px-0"
                          :style="{
                            width: windowWidth > 660 ? `25%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div :style="{ textAlign: `center` }">
                            <v-tooltip text="Tooltip" location="bottom">
                              <template v-slot:activator="{ props }">
                                <div
                                  v-bind="props"
                                  :style="{
                                    textAlign: `center`,
                                    whiteSpace: `nowrap`,
                                    overflow: `hidden`,
                                    textOverflow: `ellipsis`,
                                    maxWidth: `90%`,
                                    cursor: `pointer`,
                                  }"
                                >
                                  <span :style="{ fontWeight: `bold` }">{{
                                    item.result
                                  }}</span>
                                </div>
                              </template>
                              <p :style="{ fontWeight: `bold` }">Result</p>
                              <span> {{ item.result }}</span>
                            </v-tooltip>
                          </div>
                        </v-col>
                        <v-col
                          class="px-0"
                          v-if="windowWidth > 660"
                          :style="{
                            width: windowWidth > 660 ? `25%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div :style="{ textAlign: `center` }">
                            <v-tooltip text="Tooltip" location="bottom">
                              <template v-slot:activator="{ props }">
                                <div
                                  v-bind="props"
                                  :style="{
                                    textAlign: `center`,
                                    whiteSpace: `nowrap`,
                                    overflow: `hidden`,
                                    textOverflow: `ellipsis`,
                                    maxWidth: `90%`,
                                    cursor: `pointer`,
                                  }"
                                >
                                  <span :style="{ fontWeight: `bold` }">{{
                                    item.username
                                  }}</span>
                                </div>
                              </template>
                              <p>Username</p>
                              <span> {{ item.username }}</span>
                            </v-tooltip>
                          </div>
                        </v-col>
                        <v-col
                          v-if="windowWidth > 660"
                          class="px-0"
                          :style="{
                            width: windowWidth > 660 ? `25%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <v-tooltip text="Tooltip" location="bottom">
                            <template v-slot:activator="{ props }">
                              <div
                                v-bind="props"
                                :style="{
                                  textAlign: `center`,
                                  whiteSpace: `nowrap`,
                                  overflow: `hidden`,
                                  textOverflow: `ellipsis`,
                                  maxWidth: `90%`,
                                  cursor: `pointer`,
                                }"
                              >
                                <span :style="{ fontWeight: `bold` }">{{
                                  item.message
                                }}</span>
                              </div>
                            </template>
                            <p>Message</p>
                            <span> {{ item.message }}</span>
                          </v-tooltip>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card>
                </v-card-text>
              </v-card>
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
import DataError from "@/components/tools/dataError.vue";
import Loading from "@/components/tools/loading.vue";
import axios from "axios";

export default {
  name: "knowledgeManagement",
  components: {
    DataError,
    Loading,
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      filter: "",
      customerInsightData: [],
      //loading
      isLoading: true,
      isError: false,
      errMsg: `Untitled`,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: `untitled`,
      //sort
      sortKey: null,
      sortOrder: null,
    };
  },
  computed: {
    filteredData() {
      if (!this.filter || this.filter.trim().length < 1) {
        return this.customerInsightData;
      } else {
        return this.searchInObjects(this.customerInsightData, this.filter);
      }
    },
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
    this.getList();
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
    onUpload() {
      this.uploadDialog = true;
    },
    getList() {
      this.isLoading = true;
      this.customerInsightData = [
        {
          field_name: `name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1name1`,
          result: `นันทกร1นันทกร1นันทกร1นันทกร1นันทกร1นันทกร1นันทกร1นันทกร1นันทกร1`,
          username: `บาสหมี9บาสหมี9บาสหมี9บาสหมี9บาสหมี9บาสหมี9บาสหมี9บาสหมี9บาสหมี9`,
          message: `5สวัสดีครับ ผมนันทกร เบอร์โทร 088778899088778899088778899088778899088778899088778899088778899088778899088778899088778899088778899`,
        },
        {
          field_name: `name2`,
          result: `6นันทกร`,
          username: `2บาสหมี`,
          message: `4สวัสดีครับ ผมนันทกร เบอร์โทร 088778899`,
        },
        {
          field_name: `name3`,
          result: `นันทกร5`,
          username: `บาสหมี3`,
          message: `1สวัสดีครับ ผมนันทกร เบอร์โทร 088778899`,
        },
      ];
      this.isLoading = false;
      //   axios
      //     .get(`api/chat_center/list_upload_file/`)
      //     .then((res) => {
      //       this.files = res.data;
      //       this.checkAndAddDescription();
      //       return this.$nextTick();
      //     })
      //     .then(() => {
      //       this.isLoading = false;
      //     })
      //     .catch((err) => {
      //       this.errMsg = err;
      //       this.isError = true;
      //       this.isLoading = false;
      //       this.snackbarAction({
      //         snackbarMsg: err,
      //         snackbarSuccess: false,
      //         snackbarAlert: true,
      //       });
      //     });
    },

    snackbarAction(item) {
      this.snackbarMsg = item.snackbarMsg;
      this.snackbarSuccess = item.snackbarSuccess;
      this.snackbarAlert = item.snackbarAlert;
    },
    timeSince(dateString, short = false) {
      const date = new Date(dateString);
      const now = new Date();
      const differenceInSeconds = Math.floor(Math.abs((now - date) / 1000));

      let interval = differenceInSeconds / 31536000; // seconds in a year
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` yr.` : ` years ago`}`;
      }

      interval = differenceInSeconds / 2592000; // seconds in a month
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` mo.` : ` months ago`}`;
      }

      interval = differenceInSeconds / 86400; // seconds in a day
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` d.` : ` days ago`}`;
      }

      interval = differenceInSeconds / 3600; // seconds in an hour
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` h.` : ` hours ago`}`;
      }

      interval = differenceInSeconds / 60; // seconds in a minute
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` m.` : ` minute ago`}`;
      }

      return short ? `now` : "just now";
    },
    sort(items, sortKey, order) {
      if (!this.sortKey || this.order === null) return [...items];
      const sortedItems = [...items].sort((a, b) => {
        let valueA = a[sortKey];
        let valueB = b[sortKey];

        if (valueA < valueB) return order ? -1 : 1;
        if (valueA > valueB) return order ? 1 : -1;
        return 0;
      });
      return sortedItems;
    },
    setSort(key) {
      if (this.sortKey !== key) {
        this.sortKey = key;
        this.sortOrder = true;
      } else {
        if (this.sortOrder === null) {
          this.sortOrder = true;
        } else if (this.sortOrder === true) {
          this.sortOrder = false;
        } else if (this.sortOrder === false) {
          this.sortOrder = null;
          this.sortKey = null;
        }
      }
    },
    searchInObjects(dataArray, searchString) {
      const results = [];
      for (const obj of dataArray) {
        for (const key in obj) {
          if (obj.hasOwnProperty(key)) {
            const value = obj[key];
            if (typeof value === "string" && value.includes(searchString)) {
              results.push(obj);
              break;
            }
          }
        }
      }
      return results;
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
</style>
