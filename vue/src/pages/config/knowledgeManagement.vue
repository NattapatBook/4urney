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
                            class="mr-2"
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
                            @click="this.setSort(`file_name`)"
                            >File Name
                            <v-icon v-if="sortKey === `file_name`">
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
                            @click="this.setSort(`status`)"
                            >Status
                            <v-icon v-if="sortKey === `status`">
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
                            @click="this.setSort(`uploaded_at`)"
                            >Date
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
                            @click="this.setSort(`user`)"
                            >By
                            <v-icon v-if="sortKey === `user`">
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
                    sort(filteredFiles, sortKey, sortOrder).length < 1
                      ? {
                          height: `calc(100% - 220px)`,
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: `center`,
                        }
                      : {
                          overflowY: `auto`,
                          overflowX: `hidden`,
                          maxHeight: `calc(100% - 220px)`,
                          width: `100%`,
                        }
                  "
                >
                  <div v-if="isLoading">
                    <Loading
                      :message="`Loading Knowledge Base, please wait...`"
                    />
                  </div>
                  <div
                    v-else-if="
                      !isLoading &&
                      (isError ||
                        sort(filteredFiles, sortKey, sortOrder).length < 1)
                    "
                  >
                    <DataError
                      :message="
                        sort(filteredFiles, sortKey, sortOrder).length < 1
                          ? `No Data Avaliable`
                          : errMsg
                      "
                    />
                  </div>
                  <v-card
                    v-else-if="
                      !isLoading &&
                      !isError &&
                      sort(filteredFiles, sortKey, sortOrder).length > 0
                    "
                    class="mb-2 rounded-xl"
                    elevation="0"
                    :style="{ border: `solid 1px lightgrey` }"
                    v-for="item in sort(filteredFiles, sortKey, sortOrder)"
                    :key="`knowledgeManagement_files_list_${item.id}`"
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
                                <v-list-item
                                  class="pa-0"
                                  v-if="item.status === `Pending`"
                                >
                                  <v-card
                                    @click="
                                      knowledgeActionDialog(item, `process`)
                                    "
                                    class="pa-4"
                                    elevation="0"
                                    :style="{
                                      display: `flex`,
                                      alignItems: `center`,
                                    }"
                                  >
                                    <v-icon>mdi-play</v-icon>
                                    <span>&nbsp;Process</span>
                                  </v-card>
                                </v-list-item>
                                <v-list-item class="pa-0">
                                  <v-card
                                    @click="clickDownloadKnowledgeBase(item)"
                                    class="pa-4"
                                    elevation="0"
                                    :style="{
                                      display: `flex`,
                                      alignItems: `center`,
                                    }"
                                  >
                                    <v-icon>mdi-download</v-icon>
                                    <span>&nbsp;Download</span>
                                  </v-card>
                                </v-list-item>
                                <v-list-item class="pa-0">
                                  <v-card
                                    @click="knowledgeActionDialog(item, `edit`)"
                                    class="pa-4"
                                    elevation="0"
                                    :style="{
                                      display: `flex`,
                                      alignItems: `center`,
                                    }"
                                  >
                                    <v-icon>mdi-pencil</v-icon>
                                    <span>&nbsp;Edit Descriptions</span>
                                  </v-card>
                                </v-list-item>
                                <v-list-item class="pa-0">
                                  <v-card
                                    @click="
                                      knowledgeActionDialog(item, `remove`)
                                    "
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
                            <v-tooltip text="Tooltip" location="bottom">
                              <template v-slot:activator="{ props }">
                                <span
                                  :style="{ cursor: `pointer` }"
                                  v-bind="props"
                                  >{{ item.file_name }}</span
                                >
                              </template>
                              <span>Description: {{ item.description }}</span>
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
                            width: windowWidth > 660 ? `25%` : `50%`,
                            alignContent: `center`,
                          }"
                        >
                          <div :style="{ textAlign: `center` }">
                            <span>{{ timeSince(item.uploaded_at) }}</span>
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
                          <div
                            :style="{
                              textAlign: `center`,
                              whiteSpace: `nowrap`,
                              overflow: `hidden`,
                              textOverflow: `ellipsis`,
                            }"
                          >
                            <span>{{ item.user }}</span>
                          </div>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card>
                </v-card-text>
              </v-card>
              <!--dialog-->
              <UploadKnowledgeBase
                v-model="uploadDialog"
                @snackbar="snackbarAction"
                @successUpload="getList"
              />
              <KnowledgeBaseActionDialog
                v-model="actionDialog"
                :mode="actionMode"
                :item="actionItem"
                @callbackAction="callbackAction"
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
import KnowledgeBaseActionDialog from "@/components/knowledgeBase/knowledgeBaseActionDialog.vue";
import DataError from "@/components/tools/dataError.vue";
import Loading from "@/components/tools/loading.vue";
import axios from "axios";

export default {
  name: "knowledgeManagement",
  components: {
    DataError,
    Loading,
    UploadKnowledgeBase,
    KnowledgeBaseActionDialog,
  },
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
      //upload dialog
      uploadDialog: false,
      //action dialog
      actionDialog: false,
      actionMode: `untitled`,
      actionItem: {
        id: -1,
        file: "untitled",
        uploaded_at: null,
        collection_name: null,
        embedded_date: null,
        status: null,
        user: "untitled",
        file_url: "untitled",
        file_name: "untitled",
        description: "untitled",
      },
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
    filteredFiles() {
      if (!this.filter) return this.files;
      return this.files.filter((file) =>
        file.file_name.toLowerCase().includes(this.filter.toLowerCase())
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
      if (typeof status !== "string") {
        return "grey";
      }

      switch (status.toLowerCase()) {
        case "pending":
          return "orange";
        case "processing":
          return "blue";
        case "completed":
          return "green";
        default:
          return "grey";
      }
    },
    // renameFile(item) {
    //   console.log("Rename file:", item.fileName);
    // },
    // removeFile(item) {
    //   console.log("Remove file:", item.fileName);
    // },
    clickDownloadKnowledgeBase(item) {
      axios
        .post(
          `api/chat_center/download_s3_file/`,
          { file: item.file },
          {
            responseType: "blob",
          }
        )
        .then((res) => {
          const blob = res.data;

          const contentType =
            res.headers["content-type"] || "application/octet-stream";

          const contentDisposition = res.headers["content-disposition"];
          let filename = item.file_name || "downloaded_file";

          if (contentDisposition) {
            const filenameMatch = contentDisposition.match(
              /filename[^;=\\r\\n]*=((['"])(.*?)\2|([^;=\\r\\n]*))/i
            );
            if (filenameMatch) {
              filename = filenameMatch[3] ? filenameMatch[3] : filenameMatch[4];

              try {
                if (filename.indexOf("%") > -1) {
                  filename = decodeURIComponent(filename.replace(/\+/g, " "));
                }
              } catch (e) {
                console.warn("Could not decode filename:", filename, e);
              }
            }
          }

          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.style.display = "none";
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();

          setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          }, 100);

          this.snackbarAction({
            snackbarMsg: `Download complete: ${filename}`,
            snackbarSuccess: true,
            snackbarAlert: true,
          });
        })
        .catch((err) => {
          this.snackbarAction({
            snackbarMsg: err,
            snackbarSuccess: false,
            snackbarAlert: true,
          });
        });
    },
    onUpload() {
      this.uploadDialog = true;
    },
    getList() {
      this.isLoading = true;
      axios
        .get(`api/chat_center/list_upload_file/`)
        .then((res) => {
          this.files = res.data;
          this.checkAndAddDescription();
          return this.$nextTick();
        })
        .then(() => {
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
    checkAndAddDescription() {
      this.files = this.files.map((file) => ({
        ...file,
        description: file.description ?? "No Description",
      }));
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
    knowledgeActionDialog(item, mode) {
      this.actionItem = item;
      this.actionMode = mode;
      this.actionDialog = true;
    },
    callbackAction(item) {
      const path =
        item.mode === `process`
          ? `/api/chat_center/embedded_data/`
          : item.mode === `remove`
          ? `/api/chat_center/remove_upload_file/`
          : item.mode === `edit`
          ? `/api/chat_center/edit_upload_file/`
          : ``;
      const body =
        item.mode === `process`
          ? {
              file_url: item.item.file_url,
            }
          : item.mode === `remove`
          ? { id: item.item.id }
          : item.mode === `edit`
          ? { id: item.item.id, description: item.description }
          : {};

      this.isLoading = true;
      axios
        .post(path, body)
        .then((res) => {
          if (item.mode === `remove` || item.mode === `edit`) {
            this.files = res.data;
            this.checkAndAddDescription();
          }
          return this.$nextTick();
        })
        .then(() => {
          if (item.mode === `remove` || item.mode === `edit`) {
            this.snackbarAction({
              snackbarMsg:
                item.mode === "remove"
                  ? "File removed successfully!"
                  : "Description updated successfully!",
              snackbarSuccess: true,
              snackbarAlert: true,
            });
            this.isLoading = false;
          } else if (item.mode === `process`) {
            this.snackbarAction({
              snackbarMsg: `Embedding task has been started.`,
              snackbarSuccess: true,
              snackbarAlert: true,
            });
            this.getList();
          }
        })
        .catch((err) => {
          this.errMsg = err;
          // this.isError = true;
          this.isLoading = false;
          this.snackbarAction({
            snackbarMsg: err,
            snackbarSuccess: false,
            snackbarAlert: true,
          });
        });
    },
    sort(items, sortKey, order) {
      if (!this.sortKey || this.order === null) return [...items];
      const sortedItems = [...items].sort((a, b) => {
        let valueA = a[sortKey];
        let valueB = b[sortKey];

        if (sortKey === "status") {
          const statusOrder = { Pending: 0, Processing: 1, Completed: 2 };
          valueA = statusOrder[valueA] ?? -1;
          valueB = statusOrder[valueB] ?? -1;
        }

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
