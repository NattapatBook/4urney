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
        justifyItems: `center`,
      }"
    >
      <v-col cols="12">
        <div :style="{ marginTop: `90px`, width: `100%` }">
          <v-row class="ma-2" :style="{ paddingInline: `10px` }">
            <!-- list panel -->
            <v-col
              v-if="!hideListuserPanel"
              :cols="windowWidth > 1280 ? 3 : windowWidth > 1024 ? 4 : 12"
              class="pa-1"
              :style="{ height: `100%` }"
            >
              <v-card
                :style="{
                  height: `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <ListUser
                  class="shake"
                  @selectUser="selectUser"
                  @minimize="hideListuserPanel = !hideListuserPanel"
                  :selected-user-prop="selectedUser"
                  :user-items="userItems"
                />
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
                class="px-0"
                :style="{
                  height: `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <ListUserCompact
                  class="shake"
                  @selectUser="selectUser"
                  @minimize="hideListuserPanel = !hideListuserPanel"
                  :selected-user-prop="selectedUser"
                  :user-items="userItems"
                />
              </v-card>
            </v-col>
            <!-- chat panel -->
            <v-col
              id="chatPanel"
              :class="fullscreen ? `pa-0` : `pa-1`"
              :style="{
                height: fullscreen ? '100dvh' : '',
                display: 'grid',
                position: fullscreen ? 'fixed' : 'relative',
                top: fullscreen ? '0' : '',
                left: fullscreen ? '0' : '',
                width: fullscreen ? '100dvw' : 'auto',
                zIndex: fullscreen ? '999' : '',
              }"
            >
              <v-card
                :class="fullscreen ? `rounded-0` : ``"
                :style="{
                  height: fullscreen ? '100dvh' : `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? '0px' : '15px',
                  borderRadius: '8px',
                }"
              >
                <ChatPanel
                  ref="chat_panel_ref"
                  :selected-user-prop="selectedUser"
                  :is-change="isSelectedDataChange"
                  :fullscreen="fullscreen"
                  @fullscreen="fullscreen = !fullscreen"
                  @changeMessageType="getListUser"
                />
              </v-card>
            </v-col>
            <!-- dashboard panel -->
            <v-col
              id="dashboard"
              :cols="windowWidth > 1280 ? 4 : windowWidth > 1024 ? 4 : 12"
              class="pa-1"
              :style="{
                height: `100%`,
                display:
                  !selectedUser || selectedUser.id === `-1` ? `none` : ``,
              }"
            >
              <v-card
                :style="{
                  height: windowWidth > 1024 ? `calc(100dvh - 110px)` : `100%`,
                  marginBottom: windowWidth > 1024 ? `0px` : `15px`,
                  borderRadius: `8px`,
                  overflowX: 'hidden',
                  overflowY:
                    isLoadingDashboard || isErrorDashboard ? `hidden` : `auto`,
                }"
              >
                <div
                  v-if="isLoadingDashboard"
                  :style="{
                    height: 'calc(-110px + 100dvh)',
                    marginBottom: '0px',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    overflowY: 'hidden',
                    overflowX: 'hidden',
                  }"
                >
                  <Loading
                    :style="{ fontSize: `1.2rem` }"
                    :message="`Dashboard is Loading...`"
                  />
                </div>

                <div v-else-if="!isLoadingDashboard && isErrorDashboard">
                  <DataError
                    :style="{
                      height: 'calc(-110px + 100dvh)',
                      marginBottom: '0px',
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                      overflowY: 'hidden',
                      overflowX: 'hidden',
                    }"
                    :message="errDashboardMsg"
                  />
                </div>
                <ChatDashboard
                  v-else-if="!isLoadingDashboard && !isErrorDashboard"
                  :selected-user-prop="selectedUser"
                  :is-change="isSelectedDataChange"
                  :dashboard-data-prop="dashboardData"
                  @callbackEditCustomerProfile="editCustomerProfile"
                />
              </v-card>
            </v-col>
          </v-row>
          <!--Dialog-->
          <EditCustomerProfileDialog
            v-model="editCustomerDialog"
            :dashboard-data-prop="dashboardData"
            @callbackConfirmEditCustomerProfileDialog="
              confirmEditCustomerProfileDialog
            "
          />
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
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ChatDashboard from "@/components/listen/chatDashboard.vue";
import ChatPanel from "@/components/listen/chatPanel.vue";
import ListUser from "@/components/listen/listUser.vue";
import ListUserCompact from "@/components/listen/listUserCompact.vue";
import axios from "axios";
import { createPersistentWebSocket } from "@/utils/websocket";
import EditCustomerProfileDialog from "@/components/listen/subChatDashboard/editCustomerProfileDialog.vue";
import Loading from "@/components/tools/loading.vue";
import DataError from "@/components/tools/dataError.vue";

export default {
  name: "listen",
  components: {
    ListUser,
    ListUserCompact,
    ChatPanel,
    ChatDashboard,
    EditCustomerProfileDialog,
    Loading,
    DataError,
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      hideListuserPanel: false,
      userItems: [],
      //selectedUser
      selectedUser: {
        id: `-1`,
        img: ``,
        name: `untitled`,
        tag: `untitled`,
        priority: `untitled`,
        lastestMsg: `untitled`,
        timestamp: new Date(),
        isUrgent: false,
        provider: `untitled`,
      },
      //
      isSelectedDataChange: false,
      fullscreen: false,
      //dashboard
      dashboardData: {
        dissatisfaction: 0,
        intentSummary: [],
        priority: "untitled",
        satisfaction: 0,
        totalMessage: 0,
        totalSession: 0,
        urgent: 0,
        id: "-1",
        userInformation: {
          birthday: "untitled",
          citizenId: "untitled",
          email: "untitled",
          gender: "untitled",
          name: "untitled",
          phoneNumber: "untitled",
        },
      },
      isLoadingDashboard: true,
      isErrorDashboard: false,
      errDashboardMsg: `untitled`,
      //dialog
      editCustomerDialog: false,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      socket: null,
    };
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();

    //getData
    this.openSocket();
    this.getListUser();
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
    scrollTo(id) {
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    },
    selectUser(user, flag) {
      const oldId = this.selectedUser.id;
      this.selectedUser = user ? user : null;
      this.isSelectedDataChange = flag;
      if (user && user.id !== `-1` && oldId !== user.id) {
        this.updateTimestamp(user.id, user.timestamp);
        this.scrollTo("chatPanel");
        this.getListDashboard(user.id);
      }
    },
    //getData
    getListUser() {
      axios
        .get(`api/chat_center/list_user_new/`)
        .then((res) => {
          // console.log(res.data);
          this.userItems = res.data;
          this.saveToLocalStorage(this.userItems);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getListDashboard(id) {
      this.isLoadingDashboard = true;
      this.isErrorDashboard = false;
      //id === user.id
      axios
        .get(`api/chat_center/summarize_dashboard_new/${id}`)
        .then(() => {
          this.getListDashboardSumarized(id);
        })
        .catch((err) => {
          this.errDashboardMsg = err;
          this.isLoadingDashboard = false;
          this.isErrorDashboard = true;
          // console.error(err);
          this.snackbarMsg = err;
          this.snackbarSuccess = false;
          this.snackbarAlert = true;
        });
    },
    getListDashboardSumarized(id) {
      this.isLoadingDashboard = true;
      this.isErrorDashboard = false;
      axios
        .get(`api/chat_center/list_dashboard_new/${id}`)
        .then((res) => {
          // console.log(res.data);
          this.dashboardData = res.data;
          this.isLoadingDashboard = false;
          this.isErrorDashboard = false;
        })
        .catch((err) => {
          this.errDashboardMsg = err;
          this.isLoadingDashboard = false;
          this.isErrorDashboard = true;
          // console.error(err);
          this.errDashboardMsg = err;
          this.snackbarMsg = err;
          this.snackbarSuccess = false;
          this.snackbarAlert = true;
          this.dashboardData = {
            dissatisfaction: 0,
            intentSummary: [],
            priority: "untitled",
            satisfaction: 0,
            totalMessage: 0,
            totalSession: 0,
            urgent: 0,
            id: "-1",
            userInformation: {
              birthday: "untitled",
              citizenId: "untitled",
              email: "untitled",
              gender: "untitled",
              name: "untitled",
              phoneNumber: "untitled",
            },
          };
        });
    },
    openSocket() {
      const { websocket, send, close } = createPersistentWebSocket(
        "chat_center/chat",
        (event) => {
          const data = JSON.parse(event.data);

          if (data.type === "message_update") {
            this.userItems = data.formatted_data;
            this.saveToLocalStorage(this.userItems);
            if (this.selectedUser && this.selectedUser.id !== `-1`) {
              const item = this.findById(this.selectedUser.id);
              if (item.timestamp !== this.selectedUser.timestamp) {
                this.selectUser(item, this.isSelectedDataChange);
                this.$refs.chat_panel_ref.updateLastestChat();
              }
            }
          }
        }
      );
      this.socket = { websocket, send, close };
      console.log("WebSocket connection established");
    },
    findById(id) {
      return this.userItems.find((item) => item.id === id);
    },
    saveToLocalStorage(data) {
      const reducedData = data.map((item) => ({
        id: item.id,
        timestamp: item.timestamp,
      }));

      //reduce to 1000 history
      const latestData = reducedData.slice(-1000);

      localStorage.setItem("chatData", JSON.stringify(latestData));
    },
    updateTimestamp(id, newTimestamp) {
      const storedData = JSON.parse(localStorage.getItem("chatData")) || [];
      const index = storedData.findIndex((item) => item.id === id);
      if (index !== -1) {
        storedData[index].timestamp = newTimestamp;
        localStorage.setItem("chatData", JSON.stringify(storedData));
      } else {
        console.warn(`id not found!`);
      }
    },
    editCustomerProfile() {
      this.editCustomerDialog = true;
    },
    confirmEditCustomerProfileDialog(item) {
      if (item.id && item.id !== `-1`) {
        axios
          .post(`api/chat_center/edit_customer_profile_new/`, item)
          .then((res) => {
            // console.log(res.data);
            this.dashboardData = res.data;
            this.snackbarMsg = `Your customer profile has been successfully edited.`;
            this.snackbarSuccess = true;
            this.snackbarAlert = true;
          })
          .catch((err) => {
            this.snackbarMsg = err;
            this.snackbarSuccess = false;
            this.snackbarAlert = true;
          });
      } else {
        this.snackbarMsg = `Oops, something went wrong. Please try again.`;
        this.snackbarSuccess = false;
        this.snackbarAlert = true;
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
