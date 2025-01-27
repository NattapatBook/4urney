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
                  overflowY: `auto`,
                }"
              >
                <ChatDashboard
                  :selected-user-prop="selectedUser"
                  :is-change="isSelectedDataChange"
                  :dashboard-data-prop="dashboardData"
                />
              </v-card>
            </v-col>
          </v-row>
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

export default {
  name: "listen",
  components: {
    ListUser,
    ListUserCompact,
    ChatPanel,
    ChatDashboard,
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
        .get(`api/chat_center/list_user_test/`)
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
      axios
        .get(`api/chat_center/list_dashboard_test/${id}`)
        .then((res) => {
          // console.log(res.data);
          this.dashboardData = res.data;
        })
        .catch((err) => {
          console.error(err);
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
