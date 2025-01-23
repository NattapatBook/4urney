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
                    Knowledge Base
                  </p>
                  <span :style="{ fontSize: '0.8rem', color: 'grey' }">
                    "Manage the data sources your bot uses to access and respond
                    to user queries."
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
                        label="Filter by name"
                        hide-details
                        variant="outlined"
                        rounded="xl"
                        clearable
                        :disabled="isLoading || isError"
                      ></v-text-field>
                      <v-tooltip text="Tooltip" location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            v-bind="props"
                            :disabled="isLoading || isError"
                            icon
                            color="primary"
                            @click="onUpload"
                          >
                            <v-icon>mdi-upload</v-icon>
                          </v-btn>
                        </template>
                        <span>Upload file</span>
                      </v-tooltip>
                    </div>
                  </div>
                  <v-container>
                    <v-row>
                      <v-col
                        class="px-0"
                        :style="{
                          width: windowWidth > 660 ? `33.33%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <span>File Name</span>
                        </div>
                      </v-col>
                      <v-col
                        class="px-0"
                        :style="{
                          width: windowWidth > 660 ? `33.33%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <span>Status</span>
                        </div>
                      </v-col>
                      <v-col
                        class="px-0"
                        v-if="windowWidth > 660"
                        :style="{
                          width: windowWidth > 660 ? `33.33%` : `50%`,
                          alignContent: `center`,
                        }"
                      >
                        <div :style="{ textAlign: `center` }">
                          <span>Date</span>
                        </div>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-text
                  class="pa-4 pt-0"
                  :style="
                    isLoading || isError || files.length < 1
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
                  <div class="hereeerere" v-if="isLoading">
                    <Loading
                      :message="`Loading Knowledge Base, please wait...`"
                    />
                  </div>
                  <div v-else-if="!isLoading && (isError || files.length < 1)">
                    <DataError
                      :message="files.length < 1 ? `No Data` : errMsg"
                    />
                  </div>
                  <v-card
                    v-else-if="!isLoading && !isError && files.length > 0"
                    class="mb-2 rounded-xl"
                    elevation="0"
                    :style="{ border: `solid 1px lightgrey` }"
                    v-for="item in filteredFiles"
                    :key="`knowledgeManagement_files_list_${item.id}`"
                  >
                    <v-container class="py-0">
                      <v-row>
                        <v-col
                          class="px-0"
                          :style="{
                            width: windowWidth > 660 ? `33.33%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div
                            :style="{
                              textAlign: `start`,
                              whiteSpace: `nowrap`,
                              overflow: `hidden`,
                              textOverflow: `ellipsis`,
                            }"
                          >
                            <v-menu
                              transition="fab-transition"
                              class="rounded-xl"
                            >
                              <template v-slot:activator="{ props }">
                                <v-btn
                                  :size="
                                    windowWidth > 660 ? `default` : `small`
                                  "
                                  class="no-ripple"
                                  icon="mdi-dots-vertical"
                                  variant="text"
                                  v-bind="props"
                                ></v-btn>
                              </template>
                              <v-list class="pa-0 rounded-lg">
                                <v-list-item class="pa-0">
                                  <v-card
                                    class="pa-4"
                                    elevation="0"
                                    :style="{
                                      display: `flex`,
                                      alignItems: `center`,
                                    }"
                                  >
                                    <v-icon>mdi-pencil</v-icon>
                                    <span>&nbsp;Rename</span>
                                  </v-card>
                                </v-list-item>
                                <v-list-item class="pa-0">
                                  <v-card
                                    class="pa-4"
                                    elevation="0"
                                    :style="{
                                      display: `flex`,
                                      alignItems: `center`,
                                    }"
                                  >
                                    <v-icon>mdi-delete</v-icon>
                                    <span>&nbsp;Remove</span>
                                  </v-card>
                                </v-list-item>
                              </v-list>
                            </v-menu>
                            &nbsp;
                            <span>{{ item.fileName }}</span>
                          </div>
                        </v-col>
                        <v-col
                          class="px-0"
                          :style="{
                            width: windowWidth > 660 ? `33.33%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div :style="{ textAlign: `center` }">
                            <v-chip
                              :size="windowWidth > 660 ? `default` : `small`"
                              :color="getStatusColor(item.status)"
                              dark
                              small
                            >
                              {{ item.status }}
                            </v-chip>
                          </div>
                        </v-col>
                        <v-col
                          class="px-0"
                          v-if="windowWidth > 660"
                          :style="{
                            width: windowWidth > 660 ? `33.33%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div :style="{ textAlign: `center` }">
                            <span>{{ item.date }}</span>
                          </div>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card>
                </v-card-text>
              </v-card>
              <UploadKnowledgeBase
                v-model="uploadDialog"
                @snackbar="snackbarAction"
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
import UploadKnowledgeBase from "@/components/knowledgeBase/uploadKnowledgeBase.vue";
import DataError from "@/components/tools/dataError.vue";
import Loading from "@/components/tools/loading.vue";
import axios from "axios";

export default {
  name: "knowledgeManagement",
  components: { DataError, Loading, UploadKnowledgeBase },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      filter: "",
      files: [],
      //loading
      isLoading: true,
      isError: false,
      errMsg: `Untitled`,
      //dialog
      uploadDialog: false,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: `untitled`,
    };
  },
  computed: {
    filteredFiles() {
      if (!this.filter) return this.files;
      return this.files.filter((file) =>
        file.fileName.toLowerCase().includes(this.filter.toLowerCase())
      );
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
    getStatusColor(status) {
      switch (status) {
        case "Pending":
          return "orange";
        case "Processing":
          return "blue";
        case "Completed":
          return "green";
        default:
          return "grey";
      }
    },
    renameFile(item) {
      console.log("Rename file:", item.fileName);
    },
    removeFile(item) {
      console.log("Remove file:", item.fileName);
    },
    onUpload() {
      this.uploadDialog = true;
    },
    getList() {
      this.isLoading = true;
      axios
        .get(`api/chat_center/list_knowledge_base/`)
        .then((res) => {
          // this.files = res.data;
          this.files = this.postMockData(res.data);
          this.isLoading = false;
        })
        .catch((err) => {
          this.errMsg = err;
          this.isError = true;
          this.isLoading = false;
          this.snackbarAction({
            snackbarMsg: err,
            snackbarSuccess: false,
            snackbarAlert: true,
          });
        });
    },
    postMockData(arr) {
      let postData = [];
      arr.forEach((item, idx) => {
        postData.push({
          id: idx,
          fileName: item,
          status: `Pending`,
          date: "2025-01-20",
        });
      });
      return postData;
    },
    snackbarAction(item) {
      this.snackbarMsg = item.snackbarMsg;
      this.snackbarSuccess = item.snackbarSuccess;
      this.snackbarAlert = item.snackbarAlert;
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
