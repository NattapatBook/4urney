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
      <!--customer profile-->
      <div>
        <v-card-text
          class="px-1 py-0"
          :style="{
            display: `flex`,
            justifyContent: `space-between`,
            alignItems: `center`,
          }"
        >
          <v-container class="px-2 mx-0 pb-0" :style="{ maxWidth: `100%` }">
            <v-row>
              <!--Customer Profile-->
              <v-col
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `space-between`,
                  height: `72px`,
                }"
                cols="12"
              >
                <div>
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      fontWeight: `500`,
                      fontSize: `1.15rem`,
                    }"
                    >Customer Profile</span
                  >
                </div>
                <div>
                  <v-tooltip text="Tooltip" location="bottom">
                    <template v-slot:activator="{ props }">
                      <v-btn
                        v-bind="props"
                        text
                        :icon="`mdi-file-edit-outline`"
                        rounded="pill"
                        :size="
                          windowWidth > 960 && windowWidth < 1400
                            ? `x-small`
                            : `default`
                        "
                      />
                    </template>
                    <span>Edit</span>
                  </v-tooltip>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-text class="px-2 py-0">
          <v-container class="px-2 pt-2 mx-0" :style="{ maxWidth: `100%` }">
            <v-row>
              <!--User Information-->
              <v-col
                v-for="(key, idx) in userInformationKey"
                :key="`listen_user_information_dashboard_${idx}`"
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `flex-start`,
                }"
                cols="4"
              >
                <div
                  :style="{
                    width: `100%`,
                    display: `flex`,
                    flexDirection: `column`,
                    alignItems: `flex-start`,
                  }"
                >
                  <p
                    :style="{
                      textAlign: `start`,
                      fontWeight: `bold`,
                      fontSize: `0.8rem`,
                      width: `100%`,
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                    }"
                  >
                    {{ camelCaseToTitleCase(key) }}
                  </p>
                  <v-tooltip text="Tooltip" location="start">
                    <template v-slot:activator="{ props }">
                      <p
                        v-bind="props"
                        :style="{
                          textAlign: `start`,
                          fontSize: `0.8rem`,
                          width: `100%`,
                          whiteSpace: `nowrap`,
                          overflow: `hidden`,
                          textOverflow: `ellipsis`,
                        }"
                      >
                        {{ dashboardDataProp.userInformation[key] }}
                      </p>
                    </template>
                    <span> {{ dashboardDataProp.userInformation[key] }}</span>
                  </v-tooltip>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </div>
      <v-divider class="mx-3" />
      <!--case detail -->
      <div>
        <v-card-text
          class="px-1 py-0"
          :style="{
            display: `flex`,
            justifyContent: `space-between`,
            alignItems: `center`,
          }"
        >
          <v-container class="px-2 mx-0 pb-0" :style="{ maxWidth: `100%` }">
            <v-row>
              <!--Case Details-->
              <v-col
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `space-between`,
                  height: `72px`,
                }"
                cols="12"
              >
                <div>
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      fontWeight: `500`,
                      fontSize: `1.15rem`,
                    }"
                    >Case Details</span
                  >
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-text class="px-2 py-0">
          <v-container class="px-2 pt-2 mx-0" :style="{ maxWidth: `100%` }">
            <v-row>
              <!--Case Information-->
              <v-col
                v-for="(key, idx) in caseInformationKey"
                :key="`listen_case_information_dashboard_${idx}`"
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `flex-start`,
                }"
                cols="6"
              >
                <div
                  :style="{
                    width: `100%`,
                    display: `flex`,
                    flexDirection: `column`,
                    alignItems: `flex-start`,
                  }"
                >
                  <p
                    :style="{
                      textAlign: `start`,
                      fontWeight: `bold`,
                      fontSize: `0.8rem`,
                      width: `100%`,
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                    }"
                  >
                    {{ camelCaseToTitleCase(key) }}
                  </p>
                  <!--wihtout number-->
                  <p
                    v-if="key === `priority`"
                    :style="{
                      textAlign: `start`,
                      fontSize: `0.8rem`,
                      width: `100%`,
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      textTransform: `capitalize`,
                    }"
                  >
                    {{ dashboardDataProp[key] }}
                  </p>
                  <!--other with number-->
                  <v-tooltip
                    v-else-if="key !== `satisfaction` && key !== `urgent`"
                    text="Tooltip"
                    location="bottom"
                  >
                    <template v-slot:activator="{ props }">
                      <span
                        v-bind="props"
                        :style="{
                          whiteSpace: `nowrap`,
                          overflow: `hidden`,
                          textOverflow: `ellipsis`,
                          cursor: `pointer`,
                        }"
                        >{{ numberKMB(dashboardDataProp[key]) }}</span
                      >
                    </template>
                    {{ dashboardDataProp[key].toLocaleString() }}
                  </v-tooltip>
                  <!-- pie chart (satisfaction && urgent) -->
                  <v-tooltip v-else text="Tooltip" location="bottom">
                    <template v-slot:activator="{ props }">
                      <div
                        v-bind="props"
                        :style="{
                          display: `flex`,
                          flexDirection: `column`,
                          cursor: `pointer`,
                        }"
                      >
                        <div class="text-start my-3">
                          <v-progress-circular
                            :rotate="0"
                            :color="
                              key === `satisfaction`
                                ? dashboardDataProp[key] >= 80
                                  ? `#5EB491`
                                  : dashboardDataProp[key] >= 50
                                  ? `#ffa600`
                                  : dashboardDataProp[key] >= 0
                                  ? `#D6584D`
                                  : `#ff5d97`
                                : key === `urgent`
                                ? dashboardDataProp[key] >= 80
                                  ? `#D6584D`
                                  : dashboardDataProp[key] >= 50
                                  ? `#ffa600`
                                  : dashboardDataProp[key] >= 0
                                  ? `#5EB491`
                                  : `#ff5d97`
                                : `black`
                            "
                            :size="80"
                            :width="10"
                            :model-value="
                              satisfactionResponse(key, dashboardDataProp[key])
                                .percentage
                            "
                          >
                            <template v-slot:default>
                              <span :style="{ fontWeight: `bold` }">
                                {{
                                  satisfactionResponse(
                                    key,
                                    dashboardDataProp[key]
                                  ).percentage
                                }}
                                %
                              </span>
                            </template>
                          </v-progress-circular>
                        </div>
                      </div>
                    </template>
                    {{
                      satisfactionResponse(key, dashboardDataProp[key])
                        .explanation
                    }}
                  </v-tooltip>
                </div>
              </v-col>
              <v-col cols="12" class="pt-0">
                <div
                  class="animated-gradient-border"
                  :style="{ width: `100%` }"
                >
                  <div class="content">
                    <div
                      class="mb-2"
                      :style="{ display: `flex`, alignItems: `center` }"
                    >
                      <span class="pr-2" :style="{ fontWeight: `bold` }"
                        >Summary</span
                      >
                      <v-tooltip text="Tooltip" location="bottom">
                        <template v-slot:activator="{ props }">
                          <div
                            v-bind="props"
                            :style="{
                              border: `solid 2px black`,
                              borderRadius: `4px`,
                              cursor: `pointer`,
                            }"
                          >
                            <span class="px-1" :style="{ fontWeight: `bold` }"
                              >Ai</span
                            >
                          </div>
                        </template>
                        <span>Auto Intent Captured powered by GPT</span>
                      </v-tooltip>
                    </div>
                    <div :style="{ height: `18dvh`, overflowY: `auto` }">
                      <li
                        :style="{ textAlign: `start` }"
                        v-for="(item, idx) in dashboardDataProp.intentSummary"
                        :key="`intents_summary_dash_chat_${idx}`"
                      >
                        {{ item }}
                      </li>
                    </div>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </div>
    </div>
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
export default {
  name: "Component_ChatDashboard",
  components: { DataError },
  props: {
    selectedUserProp: {
      type: Object,
      default: null,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
    dashboardDataProp: {
      type: Object,
      default: {
        dissatisfaction: -1,
        intentSummary: [],
        priority: "untitled",
        satisfaction: -1,
        totalMessage: -1,
        totalSession: -1,
        urgent: -1,
      },
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
      userInformationKey: [
        `name`,
        `citizenId`,
        `gender`,
        `birthday`,
        `phoneNumber`,
        `email`,
      ],
      caseInformationKey: [
        `priority`,
        `dissatisfaction`,
        `totalMessage`,
        `totalSession`,
        `satisfaction`,
        `urgent`,
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
    numberKMB(num) {
      if (num < 1000) {
        return num;
      }
      const si = [
        { v: 1e3, s: "K" },
        { v: 1e6, s: "M" },
        { v: 1e9, s: "B" },
        { v: 1e12, s: "T" },
        { v: 1e15, s: "P" },
        { v: 1e18, s: "E" },
      ];
      let i;
      for (i = si.length - 1; i > 0; i--) {
        if (num >= si[i].v) {
          break;
        }
      }
      return (
        (num / si[i].v).toFixed(2).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, "$1") +
        si[i].s
      );
    },
    satisfactionResponse(mode, point) {
      // let percentage = (point / 10) * 100
      let percentage = point;
      let wording = "";
      let explanation = "";

      if (mode === "satisfaction") {
        if (point > 90) {
          wording = "Very Satisfied";
          explanation =
            "The customer is extremely satisfied with the service and requires immediate acknowledgment to maintain their high level of satisfaction.";
        } else if (point > 80) {
          wording = "Satisfied";
          explanation =
            "The customer is satisfied with the service, but timely follow-up is important to ensure continued satisfaction.";
        } else if (point > 50) {
          wording = "Neutral";
          explanation =
            "The customer feels neutral about the service. Address their concerns in a timely manner to improve their satisfaction.";
        } else if (point > 30) {
          wording = "Dissatisfied";
          explanation =
            "The customer is dissatisfied with the service. Prompt action is needed to address their issues and improve their experience.";
        } else {
          wording = "Very Dissatisfied";
          explanation =
            "The customer is very dissatisfied with the service. Immediate action is required to resolve their concerns and prevent further dissatisfaction.";
        }
      } else if (mode === "urgent") {
        if (point > 90) {
          wording = "Immediate Action Required";
          explanation =
            "The customer needs an immediate response. Address this issue as soon as possible.";
        } else if (point > 80) {
          wording = "High Priority";
          explanation =
            "The customer’s concern is very important and should be addressed quickly.";
        } else if (point > 50) {
          wording = "Moderate Priority";
          explanation =
            "The customer’s concern should be addressed in a timely manner.";
        } else if (point > 30) {
          wording = "Low Priority";
          explanation =
            "The customer’s concern is less urgent but should still be addressed.";
        } else {
          wording = "No Immediate Action Needed";
          explanation =
            "The customer’s concern is not urgent and can be addressed at your convenience.";
        }
      }

      return {
        percentage: percentage,
        wording: wording,
        explanation: explanation,
      };
    },
    camelCaseToTitleCase(input) {
      return input
        .replace(/([a-z])([A-Z])/g, "$1 $2") // Add a space between lowercase and uppercase letters
        .replace(/^./, (char) => char.toUpperCase()); // Capitalize the first letter
    },
  },
};
</script>

<style scoped>
.animated-gradient-border {
  position: relative;
  padding: 8px;
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );
  background-size: 200% 200%;
  animation: move-gradient 5s linear infinite;
  border-radius: 12px;
  display: inline-block;
}

.content {
  background: white;
  border-radius: 10px;
  padding: 16px;
  text-align: center;
}

@keyframes move-gradient {
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
</style>
