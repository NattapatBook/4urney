<template>
  <v-dialog v-model="internalModel" width="800">
    <v-card class="rounded-xl">
      <!-- Dialog Title -->
      <v-card-text
        class="mt-2 pb-0"
        :style="{ fontWeight: `bold`, fontSize: `1.2rem` }"
      >
        Add
        <span :style="{ textTransform: `capitalize` }" v-if="selectedChannel"
          >{{ selectedChannel }}&nbsp;</span
        >Channel
      </v-card-text>

      <v-card-text class="pt-1">
        <div>
          <span>{{
            !selectedChannel
              ? `Choose a channel you want to sent messages to`
              : `Fill out the entire form to add your ${selectedChannel} channel link to 4urney.`
          }}</span>
        </div>
      </v-card-text>
      <!-- Dialog Content - select channels -->
      <v-card-text
        v-if="!selectedChannel"
        :style="{
          display: `flex`,
          justifyContent: `center`,
        }"
        class="pt-0"
      >
        <v-container class="pa-0">
          <v-row>
            <v-col
              :cols="windowWidth > 900 ? 3 : 12"
              v-for="(item, idx) in channelsItem"
              :key="`addChannelDialog_${idx}`"
            >
              <v-card
                class="rounded-xl"
                :elevation="item.disabled ? 0 : 4"
                :disabled="item.disabled"
                :style="
                  item.disabled
                    ? {
                        backgroundColor: `rgb(189 189 189)`,
                        filter: `grayscale(1)`,
                      }
                    : {
                        cursor: `pointer`,
                        backgroundColor: `#f9f9f9`,
                      }
                "
                @click="clickSelectChannel(item)"
              >
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `center`,
                    alignItems: `center`,
                    flexDirection: `column`,
                    aspectRatio: windowWidth > 900 ? `1` : ``,
                  }"
                >
                  <div class="mt-4">
                    <v-avatar>
                      <v-img :src="item.icon" />
                    </v-avatar>
                  </div>
                  <p class="mb-4" :style="{ textTransform: `capitalize` }">
                    {{ item.name }}
                  </p>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <!-- Dialog Content - body -->
      <v-card-text
        v-else-if="selectedChannel"
        :style="{
          display: `flex`,
          justifyContent: `center`,
        }"
        class="py-0"
      >
        <v-card
          elevation="0"
          class="rounded-xl pt-4 mb-4 pa-5"
          :style="{
            border: `solid 1px lightgrey`,
            width: `100%`,
            maxWidth: `400px`,
          }"
        >
          <div>
            <div
              :style="{
                display: `flex`,
                justifyContent: `center`,
              }"
            >
              <v-avatar size="80" class="mb-4">
                <v-img :src="channelsItem[selectedChannel].icon" />
              </v-avatar>
            </div>
            <div :style="{ width: `100%` }">
              <div
                v-for="(item, idx) in channelsItem[selectedChannel].fields"
                :key="`addChannelDialog_fields_${idx}`"
                :style="{
                  display: `flex`,
                  justifyContent: `center`,
                }"
                class="my-2"
              >
                <v-text-field
                  v-model="form[item.key]"
                  rounded="lg"
                  v-if="item.type === `text`"
                  :label="menuNamed(item.label)"
                  density="compact"
                  variant="outlined"
                  :rules="[requiredRule(item)]"
                  :style="{ borderRadius: '8px', maxWidth: `500px` }"
                />
              </div>
            </div>
          </div>
        </v-card>
      </v-card-text>

      <!-- Dialog Actions -->
      <v-card-text
        class="pt-0"
        :style="{
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'flex-end',
        }"
      >
        <v-btn v-if="!selectedChannel" variant="text" @click="clickCancel()">
          Cancel
        </v-btn>
        <v-btn
          v-else
          @click="selectedChannel = clickCancelChannel()"
          variant="text"
        >
          Back
        </v-btn>
        <v-btn
          v-if="selectedChannel"
          :disabled="isFormValid || isLoading"
          :loading="isLoading"
          color="primary"
          class="ml-2"
          text
          :style="{ width: `130px` }"
          @click="applyAdd()"
        >
          Apply
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import line_icon from "@/assets/img/provider/line_icon.png";
import messenger_icon from "@/assets/img/provider/messenger_icon.png";
import instagram_icon from "@/assets/img/provider/instagram_icon.png";
import tiktok_icon from "@/assets/img/provider/tiktok_icon.png";
import axios from "axios";
export default {
  name: "addChannelDialog",
  components: {},
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      selectedChannel: null,
      channelsItem: {
        line: {
          name: `line`,
          icon: line_icon,
          fields: [
            {
              label: `Line account name`,
              key: `line_username`,
              type: `text`,
              require: true,
            },
            {
              label: `Channel ID`,
              key: `channel_id`,
              type: `text`,
              require: true,
            },
            {
              label: `Secret ID`,
              key: `secret_id`,
              type: `text`,
              require: true,
            },
          ],
          api: `/api/chat_center/add_line_chatbot/`,
          disabled: false,
        },
        messenger: { name: `messenger`, icon: messenger_icon, disabled: true },
        instagram: { name: `instagram`, icon: instagram_icon, disabled: true },
        tiktok: { name: `tiktok`, icon: tiktok_icon, disabled: true },
      },
      isLoading: false,
      form: {},
    };
  },
  computed: {
    internalModel: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    isFormValid() {
      if (!this.selectedChannel) {
        return true;
      }

      const selectedChannelData = this.channelsItem[this.selectedChannel];

      if (!selectedChannelData || !Array.isArray(selectedChannelData.fields)) {
        console.error("Invalid channel data:", selectedChannelData);
        return true;
      }

      return selectedChannelData.fields.some((item) => {
        if (item.require && item.type !== "boolean") {
          return !this.form[item.key] || this.form[item.key].length < 1;
        }
        return false;
      });
    },
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
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    clickCancel() {
      this.selectedChannel = null;
      this.internalModel = false;
    },
    menuNamed(string) {
      let name = string.replaceAll(`_`, ` `);
      return name;
    },
    clickSelectChannel(item) {
      item.fields.forEach((item) => {
        this.form[item.key] = null;
      });
      this.selectedChannel = item.name;
    },
    clickCancelChannel() {
      this.form = {};
      this.selectedChannel = null;
    },
    requiredRule(item) {
      return item.type !== "boolean"
        ? (v) => !!v || `${item.key} is required.`
        : true;
    },
    applyAdd() {
      this.isLoading = true;
      const api = this.channelsItem[this.selectedChannel].api;
      axios
        .post(api, this.form)
        .then(() => {
          this.isLoading = false;
          this.$emit(`callbackAddedChannel`, {
            msg: `New ${this.selectedChannel} added successfully!`,
            isSuccess: true,
          });
          this.clickCancel();
        })
        .catch((err) => {
          this.isLoading = false;
          this.$emit(`callbackAddedChannel`, {
            msg: err,
            isSuccess: false,
          });
        });
    },
  },
};
</script>

<style scoped></style>
