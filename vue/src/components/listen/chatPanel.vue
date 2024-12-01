<template>
  <div :style="{ width: '100%', height: `100%` }">
    <div
      v-if="!selectedUserProp || selectedUserProp.id === `-1`"
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
        :sub-message="`Please select a chat from the list to view and respond.`"
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
                    flexDirection: `column`,
                    maxWidth: `calc(70%)`,
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
                </div>
              </div>
            </v-col>
            <!--v-btn-->
            <v-col cols="2" class="pa-2">
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
                    <v-list-item class="pa-0">
                      <v-card
                        class="pa-4"
                        elevation="0"
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                        }"
                      >
                        <v-icon>mdi-account-arrow-right</v-icon>
                        <span>&nbsp; Assign to</span>
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
                        <v-icon>{{
                          selectedUser.messageType === `Closed Messages`
                            ? `mdi-sticker-check-outline`
                            : `mdi-sticker-remove-outline`
                        }}</v-icon>
                        <span
                          >&nbsp;{{
                            selectedUser.messageType === `Closed Messages`
                              ? ` Open Messages`
                              : ` Close Messages`
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
        <Chat
          class="py-4"
          :chat-log-prop="chatLogs"
          :selected-user-props="selectedUser"
        />
      </div>
      <!-- text field -->
      <v-card-text
        class="pt-0"
        :class="
          selectedUser.messageType === `Closed Messages` ? `pb-0 mt-4` : ``
        "
        :style="
          selectedUser.messageType === `Closed Messages`
            ? {
                display: `flex`,
                justifyContent: `center`,
              }
            : {}
        "
      >
        <div v-if="selectedUser.messageType === `Closed Messages`">
          <span :style="{ color: `grey` }"
            >Please open messages to start chat with user</span
          >
        </div>
        <v-text-field
          v-else-if="selectedUser.messageType === `Opened Messages`"
          v-model="msgBox"
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
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
import Chat from "./subChatPanel/chat.vue";
export default {
  name: "Component_ChatPanel",
  components: { DataError, Chat },
  props: {
    selectedUserProp: {
      type: Object,
      default: null,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
    fullscreen: {
      type: Boolean,
      default: false,
    },
    userItems: {
      type: Object,
      default: () => {
        return [];
      },
    },
  },
  watch: {
    isChange(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.selectedUser = JSON.parse(JSON.stringify(this.selectedUserProp));
        console.log(this.selectedUserProp);
        console.log(this.isChange);
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
        tag: `untitled`,
        priority: `untitled`,
        lastestMsg: `untitled`,
        timestamp: new Date(),
        isUrgent: false,
        provider: `untitled`,
      },
      msgBox: ``,
      chatLogs: [
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีค่ะ มีอะไรให้ช่วยแนะนำหรือสอบถามเกี่ยวกับปุ๋ยหรือโดรนจากบริษัทเจียไต๋บ้างคะ?",
          timestamp: "2024-11-28 19:15:07.985070+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ1",
          timestamp: "2024-11-28 19:14:51.724000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีค่ะ ฉันเป็นบอทให้ข้อมูลเกี่ยวกับปุ๋ยและโดรนที่บริษัท Chia Tai Group Co.,Ltd. ค่ะ ฉันพร้อมให้ข้อมูลและตอบคำถามเกี่ยวกับผลิตภัณฑ์ของเราให้กับพนักงานบริษัท เกษตรกร หรือชาวบ้านค่ะ มีคำถามเกี่ยวกับปุ๋ยหรือโดรนไหมคะ?",
          timestamp: "2024-11-28 17:54:28.827758+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ บอททำงานที่",
          timestamp: "2024-11-28 17:54:13.288000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีค่ะ ฉันเป็นบอทของบริษัท Chia Tai Group Co.,Ltd. ค่ะ ฉันไม่ได้อยู่ในสถานที่ใดสถานที่หนึ่ง แต่ฉันสามารถให้ข้อมูลและตอบคำถามเกี่ยวกับผลิตภัณฑ์และบริการของบริษัทได้ค่ะ หากมีคำถามเพิ่มเติมเกี่ยวกับปุ๋ยหรือโดรน สามารถสอบถามได้เลยค่ะ",
          timestamp: "2024-11-28 17:48:55.486605+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ บอททำงานที่ไหน",
          timestamp: "2024-11-28 17:48:40.119000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีค่ะ ฉันเป็นระบบตอบคำถามอัตโนมัติของบริษัท Chia Tai Group Co.,Ltd. ค่ะ ฉันสามารถให้ข้อมูลเกี่ยวกับปุ๋ยและโดรนได้ หากคุณมีคำถามเพิ่มเติมเกี่ยวกับผลิตภัณฑ์หรือบริการของเรา สามารถสอบถามได้เลยค่ะ",
          timestamp: "2024-11-28 17:33:28.731357+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ บอททำงานที่ไหน",
          timestamp: "2024-11-28 17:33:17.770000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ฉันเป็นพนักงานเพศหญิงค่ะ มีอะไรที่ฉันสามารถช่วยคุณได้บ้างเกี่ยวกับผลิตภัณฑ์ปุ๋ยหรือโดรนของบริษัท Chia Tai Group Co.,Ltd. คะ?",
          timestamp: "2024-11-28 17:32:51.312867+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "บอทเป็นเพศอะไร",
          timestamp: "2024-11-28 17:32:40.164000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ฉันเป็นบอทที่ถูกออกแบบมาเพื่อให้ข้อมูล ไม่ได้มีเพศจริงๆ แต่ในบทบาทนี้ ฉันเป็นพนักงานเพศหญิงของบริษัท Chia Tai Group Co.,Ltd. ค่ะ มีคำถามเกี่ยวกับปุ๋ยหรือโดรนที่ฉันสามารถช่วยเหลือได้ไหมคะ?",
          timestamp: "2024-11-22 13:54:46.473844+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "บอทเป็นเพศอะไร",
          timestamp: "2024-11-22 13:54:37.524000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีค่ะ! มีอะไรให้ช่วยหรือสอบถามเกี่ยวกับปุ๋ยหรือโดรนของบริษัท Chia Tai Group Co.,Ltd. ไหมคะ?",
          timestamp: "2024-11-22 13:54:25.807898+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ",
          timestamp: "2024-11-22 13:54:18.079000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ มีอะไรให้ช่วยเหลือได้บ้างครับ?",
          timestamp: "2024-11-22 13:46:26.702936+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับบ",
          timestamp: "2024-11-22 13:46:18.844000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "แนะนำใช้สูตร 21-0-0 ผสม สูตร 15-15-15 ครับ",
          timestamp: "2024-11-22 13:41:19.521928+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "เร่งรากสัปปะรดสูตรไหนคะ",
          timestamp: "2024-11-22 13:41:08.831000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สำหรับเร่งรากสัปปะรด แนะนำใช้สูตร 21-0-0 ผสมสูตร 15-15-15 ค่ะ",
          timestamp: "2024-11-22 12:52:57.813669+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "เร่งรากสัปปะรดสูตรไหนคะ",
          timestamp: "2024-11-22 12:52:16.770000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ปุ๋ยสูตรนี้เหมาะสำหรับบำรุงพืชผัก, ไม้ผล และผักหัว เช่น ผักใบ, พริก, มะเขือเทศ, มะนาว, ขิง, ข่า, หอมแดง, และไม้ผลเช่น ทุเรียน มะม่วง และส้ม",
          timestamp: "2024-11-22 12:31:34.805740+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ปุ๋ยตรากระต่าย สูตร 25-7-7 บลู ช่วยบำรุงพืชอะไรได้บ้าง?",
          timestamp: "2024-11-22 12:31:24.161000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดีครับ/ค่ะ มีอะไรที่สามารถช่วยเหลือได้บ้างครับ/ค่ะ?",
          timestamp: "2024-11-22 12:28:49.709289+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สวัสดี",
          timestamp: "2024-11-22 12:28:01.485000+07:00",
        },
        {
          by: "admin",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "Test",
          timestamp: "2024-11-22 08:42:59.350116+07:00",
        },
        {
          by: "admin",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "เฮลโหล",
          timestamp: "2024-11-22 06:43:17.495958+07:00",
        },
        {
          by: "admin",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "มันวิ่งมามาโชว์บน 4urney แล้วปะ",
          timestamp: "2024-11-22 06:43:04.181053+07:00",
        },
        {
          by: "admin",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "เป็นกำลังใจให้บาสหมีนะครับ ช่วงนี้น่าจะเครียดดด",
          timestamp: "2024-11-13 07:07:34.548574+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "อาการที่ท่านเล่ามานั้นอาจเป็นโรคใบจุดในข้าวโพดครับ ลักษณะอาการของโรคนี้มักเริ่มต้นด้วยจุดเล็กๆ สีเขียวอ่อนบนใบ และมีวงแหวนสีเหลืองล้อมรอบครับ หากไม่ได้รับการดูแลเหมาะสม โรคอาจลามขยายได้จนทำให้ใบข้าวโพดไหม้ทั้งใบและอาจแห้งตายได้นะครับ. บริษัทขอแนะนำให้ลองตรวจสอบให้แน่ใจและหากพบว่าเป็นกรณีดังกล่าว อาจพิจารณาใช้วิธีการปลูกที่ห่างกันเพื่อหลีกเลี่ยงความแออัดของพืชในแปลง และใช้ปุ๋ยตรากระต่ายที่เหมาะสมเพื่อช่วยบำรุงดินและพืชครับ.",
          timestamp: "2024-11-11 14:40:16.704827+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "Whats happening to my corn!?? There are many yellow dot",
          timestamp: "2024-11-11 14:39:23.896000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ข้าวโพดที่มีสีน้ำตาลและมีขนปุยอาจเป็นสัญญาณของโรคสนิมข้าวโพด โรคนี้ทำให้เกิดจุดหรือแผ่นสีน้ำตาลถึงสนิมบนใบของข้าวโพด และบางครั้งจะมีลักษณะเป็นขนปุยก็ได้ โรคสนิมอาจทำให้การสังเคราะห์แสงในข้าวโพดลดลง ส่งผลกระทบต่อผลผลิตและคุณภาพของเมล็ดข้าวโพด",
          timestamp: "2024-11-11 13:56:13.540136+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ข้าวโพดสีมันออกสีน้ำตาล มีขนปุกปุย",
          timestamp: "2024-11-11 13:56:00.714000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ดูเหมือนว่าคุณอาจจะพูดถึงอาการบนพืชที่คุณพบ ถ้าพบว่ามีลักษณะสีน้ำตาลและมีขนปุกปุย อาจเป็นไปได้ว่าพืชของคุณมีอาการเกิดจากโรคพืชที่เกิดจากเชื้อราหรือโรคอื่น ๆ เช่นโรคราน้ำค้าง หรืออาจเป็นโรคอื่นตามที่คำอธิบายลักษณะอาการ กรุณาให้รายละเอียดเพิ่มเติม เช่น พืชชนิดไหนที่พบอาการ เพื่อที่จะได้วินิจฉัยอย่างถูกต้องมากยิ่งขึ้นค่ะ.",
          timestamp: "2024-11-11 13:55:33.292552+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "สีมันออกสีน้ำตาล มีขนปุกปุย",
          timestamp: "2024-11-11 13:55:18.462000+07:00",
        },
        {
          by: "bot",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ปุ๋ยสูตรนี้เหมาะสำหรับบำรุงพืชผัก, ไม้ผล และผักหัว เช่น ผักใบ, พริก, มะเขือเทศ, มะนาว, ขิง, ข่า, หอมแดง, และไม้ผลเช่น ทุเรียน มะม่วง และส้ม",
          timestamp: "2024-11-11 12:50:21.927903+07:00",
        },
        {
          by: "customer",
          id: "U32afe3db274f527b57262faf86bb1359",
          msg: "ปุ๋ยตรากระต่าย สูตร 25-7-7 บลู ช่วยบำรุงพืชอะไรได้บ้าง?",
          timestamp: "2024-11-11 12:50:10.566000+07:00",
        },
      ],
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
      alert(this.msgBox);
      this.msgBox = ``;
    },
    clickFullScreen() {
      this.$emit(`fullscreen`);
    },
  },
};
</script>

<style scoped>
.no-ripple .v-ripple__container {
  pointer-events: none !important;
}
</style>
