<template>
  <div :style="{ width: '100%', height: `100%` }">
    <div
      v-if="
        !selectedUserProp ||
        selectedUserProp.id === `-1` ||
        !selectedChatProp ||
        selectedChatProp.id === `-1`
      "
      :style="{
        height: `100%`,
        display: `flex`,
        justifyContent: `center`,
      }"
    >
      <DataError
        :iconSize="`3rem`"
        :iconColor="`#5EB491`"
        :message="`No Chat Selected`"
        :sub-message="`Please select a chatbot and session from the list.`"
        :icon="`mdi-message-alert`"
      />
    </div>
    <div
      v-else
      :style="{
        height: `100%`,
      }"
    >
      <!--user information & tools bar-->
      <v-card-text
        class="px-1"
        :style="{
          display: `flex`,
          justifyContent: `space-between`,
          height: `80px`,
          alignItems: `center`,
        }"
      >
        <v-container class="px-2 mx-0" :style="{ maxWidth: `100%` }">
          <v-row>
            <!--user information-->
            <v-col :style="{ display: `flex` }" cols="10" class="pa-2">
              <div :style="{ display: `flex`, alignItems: `center` }">
                <!--user-->
                <div>
                  <v-avatar>
                    <v-img
                      v-if="selectedUser.img"
                      :src="selectedUser.img"
                      aspect-ratio="1"
                    ></v-img>
                    <v-img
                      v-else
                      :src="`https://ui-avatars.com/api/?name=${checkTextTooLong(
                        selectedUser.name,
                        15
                      )}`"
                      aspect-ratio="1"
                    ></v-img>
                  </v-avatar>
                </div>
                <div
                  class="ml-2"
                  :style="{
                    display: `flex`,
                    flexDirection: `row`,
                    maxWidth: `calc(70%)`,
                    alignItems: `center`,
                  }"
                >
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      fontWeight: `500`,
                      fontSize: `1.15rem`,
                    }"
                    >{{ selectedUser.name }}</span
                  >
                  <v-progress-circular
                    v-if="isLoading"
                    class="ml-3"
                    :width="3"
                    :size="20"
                    color="rgb(254,56,147)"
                    indeterminate
                  ></v-progress-circular>
                </div>
              </div>
            </v-col>
            <!--v-btn-->
            <v-col v-if="!hideTopMenu" cols="2" class="pa-2">
              <div
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `flex-end`,
                }"
              >
                <v-menu transition="fab-transition" class="rounded-xl">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      class="no-ripple"
                      icon="mdi-dots-vertical"
                      variant="text"
                      v-bind="props"
                    ></v-btn>
                  </template>
                  <v-list class="pa-0 rounded-lg">
                    <v-list-item class="pa-0" @click="clickFullScreen()">
                      <v-card
                        class="pa-4"
                        elevation="0"
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                        }"
                      >
                        <v-icon>{{
                          fullscreen ? `mdi-fullscreen-exit` : `mdi-fullscreen`
                        }}</v-icon>
                        <span
                          >&nbsp;{{
                            fullscreen ? ` Exit Full Screen` : ` Full Screen`
                          }}</span
                        >
                      </v-card>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-divider class="mx-3" />
      <!--chat panel-->
      <div :style="{ height: `calc(100% - 80px - 56px)` }">
        <div
          v-if="isErrorListChat"
          :style="{ display: `flex`, justifyContent: `center`, height: `100%` }"
        >
          <DataError :message="errMsg" />
        </div>
        <ChatInternalChatbot
          v-else
          class="py-4"
          :chat-log-prop="chatLogs"
          :selected-user-props="selectedUser"
          :key="`chatPanel_chatbot_update_${isUpdate}`"
        />
      </div>
      <!-- text field -->
      <v-card-text
        class="pt-0"
        :class="!selectedUser.isActive ? `pb-0 mt-4` : ``"
        :style="
          !selectedUser.isActive
            ? {
                display: `flex`,
                justifyContent: `center`,
              }
            : {}
        "
      >
        <div v-if="!selectedUser.isActive">
          <span :style="{ color: `grey` }">
            The chatbot is here but currently inactive.
          </span>
        </div>
        <v-text-field
          v-else
          v-model="msgBox"
          :disabled="isErrorListChat || isLoading"
          :append-inner-icon="`mdi-send-variant`"
          :placeholder="`Write something...`"
          hint="Hmm, How did you found this!"
          density="compact"
          hide-details
          variant="outlined"
          :style="{ borderRadius: `8px` }"
          @keyup.up="clickFullScreen()"
          @keyup.enter="msgBox.trim().length > 0 ? clickSendMsg() : ``"
          @click:appendInner="msgBox.trim().length > 0 ? clickSendMsg() : ``"
        ></v-text-field>
      </v-card-text>
    </div>
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
        <v-btn color="white" text v-bind="attrs" @click="snackbarAlert = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
import ChatInternalChatbot from "./subInternalChatbot/chatInternalChatbot.vue";
import axios from "axios";
export default {
  name: "Component_ChatPanelBot",
  components: {
    DataError,
    ChatInternalChatbot,
    // Chat,
  },
  props: {
    selectedUserProp: {
      type: Object,
      default: null,
      deep: true,
    },
    selectedChatProp: {
      type: Object,
      default: null,
      deep: true,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
    fullscreen: {
      type: Boolean,
      default: false,
    },
    hideTopMenu: {
      type: Boolean,
      default: false,
    },
    mode: {
      type: String,
      default: `internalChatbot`,
    },
  },
  watch: {
    selectedChatProp(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.selectedUser = JSON.parse(JSON.stringify(this.selectedUserProp));
        this.selectedChat = JSON.parse(JSON.stringify(this.selectedChatProp));
      }
      if (
        this.selectedUser &&
        this.selectedUser.id !== `-1` &&
        this.selectedChat &&
        this.selectedChatProp.id !== `-1`
      ) {
        this.getListMessage(this.selectedUser.id, this.selectedChat.id);
      }
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      selectedUser: {
        id: `-1`,
        img: ``,
        name: `untitled`,
        industry: `untitled`,
        mastery: `untitled`,
        isActive: true,
      },
      selectedChat: {
        id: `-1`,
        name: `untitled`,
        lastConversationTime: new Date(),
      },
      msgBox: ``,
      chatLogs: [],
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      isUpdate: false,
      isLoading: false,
      isErrorListChat: false,
      errMsg: `untitled`,
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
    //tools
    timeSince(dateString, short = false) {
      // Convert the input date string to a Date object
      const date = new Date(dateString);
      // Get the current time
      const now = new Date();

      // Convert both dates to milliseconds since epoch
      const utcDate = date.getTime();
      const utcNow = now.getTime();

      // Calculate the time difference in seconds
      const differenceInSeconds = Math.floor(
        Math.abs((utcNow - utcDate) / 1000)
      );

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
    //Tools
    checkTextTooLong(text, cutVal) {
      if (text.length > cutVal) {
        return `${text.slice(0, cutVal)}...`;
      } else {
        return text;
      }
    },
    clickSendMsg() {
      this.isLoading = true;
      if (this.mode === `internalChatbot`) {
        axios
          .post(`api/chat_center/send_message_internal_chat/`, {
            id: this.selectedUser.id,
            sessionId: this.selectedChat.id,
            msg: this.msgBox,
          })
          .then((res) => {
            this.msgBox = ``;
            this.chatLogs = res.data;
            this.isLoading = false;
            this.isUpdate = !this.isUpdate;
          })
          .catch((err) => {
            this.isLoading = false;
            this.errMsg = err;
            this.snackbarCallback(err, false, true);
            this.isUpdate = !this.isUpdate;
          });
      } else if (this.mode === `ChatWithData`) {
        console.log(`chat with data -> answer`);
      }
    },
    clickFullScreen() {
      this.$emit(`fullscreen`);
    },
    getListMessage(userId, sessionId) {
      if (this.mode === `internalChatbot`) {
        axios
          .post(`api/chat_center/get_internal_chat/`, {
            id: userId,
            sessionId: sessionId,
          })
          .then((res) => {
            this.chatLogs = res.data;
            this.isUpdate = !this.isUpdate;
          })
          .catch((err) => {
            this.isErrorListChat = true;
            this.errMsg = err;
            this.snackbarCallback(err, false, true);
          });
      } else if (this.mode === `ChatWithData`) {
        const mockupData =
          this.selectedChat.id === `-999`
            ? [
                {
                  by: `user`,
                  msg: `ขอข้อมูลยอดขายแบ่งตามประเภทของสินค้าของแต่ละเดือนในปี 2024 ครับ`,
                },
                {
                  by: `bot`,
                  msg: `จากการสืบค้นและวิเคราะห์ข้อมูลจากฐานข้อมูล พบว่า ยอดขายมีแนวโน้มเพิ่มขึ้นในช่วงปลายปี โดยเฉพาะในเดือนตุลาคมและพฤศจิกายน ซึ่งเป็นช่วงที่มียอดขายสูงสุด

**ข้อเสนอแนะเชิงปฏิบัติการจากข้อมูลที่ได้ ได้แก่:**

1. การวางแผนการตลาด: ควรให้ความสำคัญกับการทำการตลาดและจัดกิจกรรมส่งเสริมการขายในช่วงปลายปี โดยเฉพาะเดือนตุลาคมและพฤศจิกายน ซึ่งเป็นช่วงเวลายอดขายพุ่งสูง
2. การบริหารจัดการสต็อกสินค้า: ควรเตรียมสต็อกสินค้าให้เพียงพอในช่วงเวลาดังกล่าว เพื่อให้สามารถตอบสนองต่อความต้องการของลูกค้าได้อย่างมีประสิทธิภาพ
3. การวิเคราะห์เชิงลึกเพิ่มเติม: แนะนำให้แย่กวิเคราะห์ยอดขายตามประเภทสินค้า หรือช่องทางการขาย เพื่อให้สามารถวางกลยุทธ์ทางธุรกิจได้อย่างแม่นยำและตรงจุดยิ่งขึ้น`,
                },
                //line chart
                {
                  plotly: true,
                  id: 799,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        x: [
                          "2024-01-01",
                          "2024-02-01",
                          "2024-03-01",
                          "2024-04-01",
                          "2024-05-01",
                          "2024-06-01",
                          "2024-07-01",
                          "2024-08-01",
                          "2024-09-01",
                          "2024-10-01",
                          "2024-11-01",
                          "2024-12-01",
                        ],
                        y: [
                          6029.21, 6866.34, 12368.99, 9323.46, 17482.81,
                          19008.59, 12475.9, 15441.88, 29096.64, 22245.7,
                          37056.72, 31916.72,
                        ],
                        mode: "lines+markers",
                        type: "scatter",
                        name: "Furniture",
                        line: {
                          color: "#428fd7",
                        },
                        marker: {
                          size: 8,
                          color: "#428fd7",
                        },
                      },
                      {
                        x: [
                          "2024-01-01",
                          "2024-02-01",
                          "2024-03-01",
                          "2024-04-01",
                          "2024-05-01",
                          "2024-06-01",
                          "2024-07-01",
                          "2024-08-01",
                          "2024-09-01",
                          "2024-10-01",
                          "2024-11-01",
                          "2024-12-01",
                        ],
                        y: [
                          21287.45, 7407.77, 14930.87, 15072.19, 13762.89,
                          16986.39, 10303.67, 31068.72, 31946.31, 28334.05,
                          31479.02, 31256.13,
                        ],
                        mode: "lines+markers",
                        type: "scatter",
                        name: "Office Supplies",
                        line: {
                          color: "#9ad2ff",
                          dash: "dashdot",
                        },
                        marker: {
                          size: 8,
                          color: "#9ad2ff",
                          symbol: "diamond",
                        },
                      },
                      {
                        x: [
                          "2024-01-01",
                          "2024-02-01",
                          "2024-03-01",
                          "2024-04-01",
                          "2024-05-01",
                          "2024-06-01",
                          "2024-07-01",
                          "2024-08-01",
                          "2024-09-01",
                          "2024-10-01",
                          "2024-11-01",
                          "2024-12-01",
                        ],
                        y: [
                          16942.55, 6027.02, 33428.62, 12383.39, 13909.79,
                          17061.1, 23209.93, 17619.16, 27021.62, 32895.04,
                          49918.77, 22002.19,
                        ],
                        mode: "lines+markers",
                        type: "scatter",
                        name: "Technology",
                        line: {
                          color: "#ff6464",
                        },
                        marker: {
                          size: 8,
                          color: "#ff6464",
                          symbol: "circle",
                        },
                      },
                    ],
                    layout: {
                      title: "ยอดขายรายเดือนตามประเภทสินค้า ปี 2024",
                      xaxis: {
                        title: "เดือน",
                      },
                      yaxis: {
                        title: "ยอดขาย (บาท)",
                      },
                      legend: {
                        orientation: "h",
                        yanchor: "bottom",
                        y: 1.02,
                        xanchor: "right",
                        x: 1,
                      },
                      hovermode: "closest",
                      margin: {
                        l: 50,
                        r: 50,
                        b: 50,
                        t: 80,
                        pad: 4,
                      },
                    },
                  },
                },
              ]
            : [
                //normal msg
                {
                  id: 741,
                  msg: "1. **ตารางการเข้าเวรหมอ** \n\n   | แผนก            | แพทย์                        | วันและเวลา                |\n   |------------------|-------------------------------|---------------------------|\n   | กุมารเวช        | พญ.ณัฐวดี สุขเกษม         | เสาร์ 08:00 - 12:00       |\n   | จิตเวช          | พญ.ดารารัตน์ สุขศรี       | พุธ, เสาร์ 13:00 - 17:00 |\n   | โรคหัวใจ        | นพ.เกียรติศักดิ์ เรืองไกร | พุธ, เสาร์ 09:00 - 14:00 |\n\n---\n\n2. **เวลาทำการของแผนกต่าง ๆ**\n\n   | แผนก                          | เวลาทำการ                             | วันหยุด                        | หมายเหตุ                          |\n   |-------------------------------|---------------------------------------|-------------------------------|-----------------------------------|\n   | อายุรกรรม (Internal Medicine) | จันทร์ - ศุกร์, 08:00 - 17:00      | เสาร์-อาทิตย์                 | ปิดวันหยุดนักขัตฤกษ์            |\n   | ศัลยกรรมกระดูก (Orthopedic Surgery) | อังคาร, พฤหัสบดี, เสาร์ 09:00 - 16:00 | เปิดวันเสาร์เฉพาะ OPD       |                                   |\n   | กุมารเวช (Pediatrics)        | เสาร์ 08:00 - 12:00                 | เปิดเฉพาะวัคซีนเด็ก        |                                   |\n   | โรคหัวใจ (Cardiology)        | จันทร์ - เสาร์ 09:00 - 16:00       | ต้องจองล่วงหน้า             |                                   |\n   | ผิวหนัง (Dermatology)        | ทุกวัน 10:00 - 20:00                | เปิดรับ Walk-in              |                                   |\n\nหากคุณต้องการข้อมูลเพิ่มเติมหรือต้องการรายละเอียดในส่วนใดเพิ่มเติม กรุณาแจ้งได้เลย!",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                },
                //line chart
                {
                  plotly: true,
                  id: 799,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        x: [1, 2, 3, 4, 5],
                        y: [3, 7, 2, 8, 5],
                        mode: "lines+markers",
                        type: "scatter",
                        name: "ชุดข้อมูล A",
                        line: {
                          color: "#17BECF",
                        },
                        marker: {
                          size: 8,
                          color: "#17BECF",
                        },
                      },
                      {
                        x: [1, 2, 3, 4, 5],
                        y: [1, 4, 3, 6, 2],
                        mode: "lines+markers",
                        type: "scatter",
                        name: "ชุดข้อมูล B",
                        line: {
                          color: "#7F7F7F",
                          dash: "dashdot",
                        },
                        marker: {
                          size: 8,
                          color: "#7F7F7F",
                          symbol: "diamond",
                        },
                      },
                    ],
                    layout: {
                      title: "กราฟเส้นแสดงแนวโน้ม 2 ชุดข้อมูล",
                      xaxis: {
                        title: "เวลา (เดือน)",
                      },
                      yaxis: {
                        title: "ค่า (หน่วย)",
                      },
                      legend: {
                        orientation: "h",
                        yanchor: "bottom",
                        y: 1.02,
                        xanchor: "right",
                        x: 1,
                      },
                      hovermode: "closest",
                      margin: {
                        l: 50,
                        r: 50,
                        b: 50,
                        t: 80,
                        pad: 4,
                      },
                    },
                  },
                },
                //bar chart (stack)
                {
                  plotly: true,
                  id: 801,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                        y: [20, 14, 23, 25, 22, 19],
                        name: "สินค้า A",
                        type: "bar",
                        marker: {
                          color: "#264E86",
                        },
                      },
                      {
                        x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                        y: [12, 18, 29, 21, 20, 22],
                        name: "สินค้า B",
                        type: "bar",
                        marker: {
                          color: "#A65628",
                        },
                      },
                    ],
                    layout: {
                      title: "ยอดขายสินค้า A และ B (Stacked Bar)",
                      yaxis: {
                        title: "ยอดขาย (พันบาท)",
                      },
                      barmode: "stack",
                      margin: {
                        l: 50,
                        r: 50,
                        b: 50,
                        t: 80,
                        pad: 4,
                      },
                    },
                  },
                },
                //pie chart
                {
                  plotly: true,
                  id: 802,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        values: [40, 25, 20, 15],
                        labels: ["หมวด A", "หมวด B", "หมวด C", "หมวด D"],
                        type: "pie",
                        hole: 0.4,
                        hoverinfo: "label+percent+value",
                        textinfo: "label+percent",
                        textposition: "inside",
                        marker: {
                          colors: ["#636efa", "#EF553B", "#00cc96", "#ab63fa"],
                        },
                        insidetextorientation: "radial",
                      },
                    ],
                    layout: {
                      title: "สัดส่วนค่าใช้จ่ายตามหมวด",
                      margin: {
                        l: 50,
                        r: 50,
                        b: 50,
                        t: 80,
                        pad: 4,
                      },
                    },
                  },
                },
                //Scatter Plot
                {
                  plotly: true,
                  id: 803,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        x: [10, 20, 30, 40, 50],
                        y: [5, 15, 10, 25, 20],
                        mode: "markers",
                        type: "scatter",
                        marker: {
                          size: [20, 40, 30, 60, 50],
                          color: [10, 20, 30, 40, 50],
                          colorscale: "Viridis",
                          showscale: true,
                        },
                        text: [
                          "จุดที่ 1",
                          "จุดที่ 2",
                          "จุดที่ 3",
                          "จุดที่ 4",
                          "จุดที่ 5",
                        ],
                        hoverinfo: "text+x+y+marker.size+marker.color",
                      },
                    ],
                    layout: {
                      title: "กราฟกระจายแบบ Bubble พร้อมสี",
                      xaxis: {
                        title: "ตัวแปร X",
                      },
                      yaxis: {
                        title: "ตัวแปร Y",
                      },
                      margin: {
                        l: 50,
                        r: 50,
                        b: 50,
                        t: 80,
                        pad: 4,
                      },
                    },
                  },
                },
                //3D Scatter Plot
                {
                  plotly: true,
                  id: 804,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        x: [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
                        y: [1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 1, 1],
                        z: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        mode: "markers",
                        type: "scatter3d",
                        marker: {
                          size: 12,
                          color: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                          colorscale: "Rainbow",
                        },
                      },
                    ],
                    layout: {
                      title: "กราฟกระจาย 3 มิติ",
                      margin: {
                        l: 0,
                        r: 0,
                        b: 0,
                        t: 50,
                      },
                      scene: {
                        xaxis: { title: "แกน X" },
                        yaxis: { title: "แกน Y" },
                        zaxis: { title: "แกน Z" },
                      },
                    },
                  },
                },
                //Surface 3D
                {
                  plotly: true,
                  id: 805,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        z: [
                          [8, 8, 8, 8, 8, 8, 8, 8],
                          [8, 8, 8, 8, 8, 8, 8, 8],
                          [8, 8, 8, 8, 8, 8, 8, 8],
                          [8, 8, 16, 16, 16, 8, 8, 8],
                          [8, 8, 16, 16, 16, 8, 8, 8],
                          [8, 8, 16, 16, 16, 8, 8, 8],
                          [8, 8, 8, 8, 8, 8, 8, 8],
                          [8, 8, 8, 8, 8, 8, 8, 8],
                        ],
                        type: "surface",
                        colorscale: "Greens",
                        contours: {
                          z: {
                            show: true,
                            usecolormap: true,
                            project: { z: true },
                          },
                        },
                      },
                    ],
                    layout: {
                      title: "กราฟพื้นผิว 3 มิติ",
                      scene: {
                        xaxis: { title: "แกน X" },
                        yaxis: { title: "แกน Y" },
                        zaxis: { title: "แกน Z" },
                      },
                      margin: {
                        l: 0,
                        r: 0,
                        b: 0,
                        t: 50,
                      },
                    },
                  },
                },
                //Heatmap Chart
                {
                  plotly: true,
                  id: 805,
                  msg: "",
                  by: "bot",
                  timestamp: "2025-02-25 10:05:11+0000",
                  package: {
                    data: [
                      {
                        z: [
                          [1, null, 30, 50, 1],
                          [20, 1, 60, 80, 30],
                          [30, 60, 1, -10, 20],
                        ],
                        x: ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์"],
                        y: ["เช้า", "บ่าย", "เย็น"],
                        type: "heatmap",
                        colorscale: "Plasma",
                      },
                    ],
                    layout: {
                      title: "Heatmap แสดงค่าความหนาแน่น",
                      xaxis: { ticks: "", position: "top" },
                      yaxis: { ticks: "", orientation: "h", side: "left" },
                      margin: {
                        l: 80,
                        r: 50,
                        b: 50,
                        t: 80,
                        pad: 4,
                      },
                    },
                  },
                },
              ];
        this.chatLogs = mockupData;
        this.isUpdate = !this.isUpdate;
      }
    },
    snackbarCallback(snackbarMsg, snackbarSuccess, snackbarAlert) {
      this.$emit("snackbar", {
        snackbarMsg,
        snackbarSuccess,
        snackbarAlert,
      });
    },
  },
};
</script>

<style scoped>
.no-ripple .v-ripple__container {
  pointer-events: none !important;
}
</style>
