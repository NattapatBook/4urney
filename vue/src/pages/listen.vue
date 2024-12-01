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
                  :selected-user-prop="selectedUser"
                  :is-change="isSelectedDataChange"
                  :fullscreen="fullscreen"
                  @fullscreen="fullscreen = !fullscreen"
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

export default {
  name: "listen",
  components: { ListUser, ListUserCompact, ChatPanel, ChatDashboard },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      hideListuserPanel: false,
      userItems: [
        {
          agent: "Agent1",
          id: "888",
          img: "",
          isUrgent: false,
          lastestMsg: "T1_test_line_lastest_message",
          messageType: "Closed Messages",
          name: "T1_test_line",
          priority: "medium",
          provider: "line",
          replyToken: null,
          tag: "",
          timestamp: "2023-04-03 17:00:04+07:00",
        },
        {
          agent: "Agent2",
          id: "999",
          img: "",
          isUrgent: false,
          lastestMsg: "T2_test_messenger_lastest_message",
          messageType: "Closed Messages",
          name: "T2_test_messenger",
          priority: "medium",
          provider: "messenger",
          replyToken: null,
          tag: "",
          timestamp: "2023-04-03 17:00:04+07:00",
        },
        {
          agent: "Agent3",
          id: "111",
          img: "",
          isUrgent: false,
          lastestMsg: "T3_test_instagram_lastest_message",
          messageType: "Closed Messages",
          name: "T3_test_instagram",
          priority: "low",
          provider: "instagram",
          replyToken: null,
          tag: "",
          timestamp: "2023-04-03 17:00:04+07:00",
        },
        {
          agent: "Agent4",
          id: "222",
          img: "",
          isUrgent: false,
          lastestMsg: "T4_test_tiktok_lastest_message",
          messageType: "Closed Messages",
          name: "T4_test_tiktok",
          priority: "low",
          provider: "tiktok",
          replyToken: null,
          tag: "",
          timestamp: "2023-04-03 17:00:04+07:00",
        },
        {
          agent: "Agent4",
          id: "8989123897",
          img: "",
          isUrgent: false,
          lastestMsg: "T4_test_tiktok_lastest_message",
          messageType: "Closed Messages",
          name: "T5_test_line",
          priority: "low",
          provider: "tiktok",
          replyToken: null,
          tag: "",
          timestamp: "2024-07-18 13:22:40.086815+07:00",
        },
        {
          agent: "Me",
          id: "982349299",
          img: "",
          isUrgent: false,
          lastestMsg: "Hi",
          messageType: "Closed Messages",
          name: "BAS",
          priority: "high",
          provider: "line",
          replyToken: null,
          tag: "VIP",
          timestamp: "2023-04-03 17:00:04+07:00",
        },
        {
          agent: "Me",
          id: "982349232",
          img: "",
          isUrgent: false,
          lastestMsg: "Hello",
          messageType: "Opened Messages",
          name: "Bamnardo",
          priority: "high",
          provider: "line",
          replyToken: null,
          tag: "VVIP",
          timestamp: "2024-04-03 17:00:04+07:00",
        },
        {
          agent: "Me",
          id: "242378958",
          img: "",
          isUrgent: false,
          lastestMsg: "Yoo !",
          messageType: "Closed Messages",
          name: "JobJoob",
          priority: "high",
          provider: "line",
          replyToken: null,
          tag: "VIP",
          timestamp: "2024-04-03 17:00:04+07:00",
        },
      ],
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
        dissatisfaction: 3,
        intentSummary: [
          "ลูกค้าต้องการทราบสูตรปุ๋ยที่เหมาะสำหรับเร่งรากสัปปะรด",
          "ลูกค้าสนใจเกี่ยวกับบอท เช่น เพศของบอท, บอททำงานที่ไหน",
          "บอทเป็นส่วนหนึ่งของบริษัท Chia Tai Group Co.,Ltd. และมีหน้าที่ให้ข้อมูลเกี่ยวกับปุ๋ยและโดรน",
          "ลูกค้ามีความสนใจที่จะสอบถามเกี่ยวกับปุ๋ยหรือโดรนจากบริษัท Chia Tai Group Co.,Ltd.",
        ],
        priority: "medium",
        satisfaction: 75,
        totalMessage: 189278342,
        totalSession: 2123,
        urgent: 30,
        id: "U32afe3db274f527b57262faf86bb1359",
        userInformation: {
          birthday: "5/5/1985",
          citizenId: "2 2000 00000 00 2",
          email: "pasith@4plus.co.th",
          gender: "Male",
          name: "Pasith Thanapatpaisarn",
          phoneNumber: "089-555-0101",
        },
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
        this.scrollTo("chatPanel");
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
