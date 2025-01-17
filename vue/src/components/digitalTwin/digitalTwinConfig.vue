<template>
  <v-card class="rounded-xl" :style="{ height: `calc(100dvh - 110px)` }">
    <v-card-title>
      <p class="gradient-text" :style="{ fontWeight: 'bold' }">
        {{
          botMode === `edit`
            ? `Customize Your Chatbot Settings`
            : `Build Your Personalized Chatbot!`
        }}
      </p>
      <span :style="{ fontSize: '0.8rem', color: 'grey' }">
        {{
          botMode === `edit`
            ? `${item.name}: Adjust settings.`
            : `Set up your chatbot.`
        }}
      </span>
    </v-card-title>

    <v-card-text
      class="py-0 px-1"
      :style="{
        overflowY: `hidden`,
        overflowX: `hidden`,
        height: `calc(100% - 148px)`,
        width: `100%`,
      }"
    >
      <v-container :style="{ height: `100%` }" class="px-3">
        <v-row :style="{ height: `100%` }">
          <v-col
            :cols="windowWidth < 470 ? 4 : 3"
            :style="{
              height: `100%`,
              borderRight: `solid 1px lightgrey`,
              overflowY: `auto`,
            }"
          >
            <v-row
              v-for="item in subMode"
              :key="`subMode_digitalTwinConfig_${item.id}`"
            >
              <v-col class="pa-1 pr-2">
                <v-card
                  @click="selectedSubMode = item.id"
                  class="hover-card rounded-lg pa-4"
                  :elevation="selectedSubMode === item.id ? 0 : 4"
                  :disabled="item.disabled"
                  :style="{
                    minHeight: `10dvh`,
                    display: `flex`,
                    flexDirection: `column`,
                    alignItems: `center`,
                    justifyContent: `center`,
                    cursor: item.disabled ? `` : `pointer`,
                  }"
                >
                  <div
                    class="pa-4"
                    :style="{
                      display: `flex`,
                      flexDirection: `column`,
                      alignItems: `center`,
                      justifyContent: `center`,
                    }"
                  >
                    <span :style="{ fontSize: `1.5rem` }">
                      {{ item.icon }}
                    </span>
                    <span :style="{ fontSize: `1rem`, fontWeight: `500` }">
                      {{ item.name }}
                    </span>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
          <v-col :cols="windowWidth < 470 ? 8 : 9" :style="{ height: `100%` }">
            <div
              :style="{
                height: `100%`,
                display: selectedSubMode === 1 ? `` : `none`,
              }"
            >
              <div
                :style="{
                  display: `flex`,
                  flexDirection: `column`,
                }"
              >
                <span :style="{ fontWeight: `bold` }"
                  >Define Chatbot Identity 👤</span
                >
                <span :style="{ color: `grey`, fontSize: `0.7rem` }">
                  "How should I behave? What do you want me to be?"</span
                >
              </div>
              <div :style="{ height: `100%`, overflowY: `auto` }">
                <v-form ref="form">
                  <div
                    v-for="(item, idx) in defineChatBotItem"
                    :key="item.id"
                    class="pt-4 px-4"
                  >
                    <div class="mb-2">
                      <p>{{ item.description }}</p>
                    </div>
                    <!-- Text input field -->
                    <div v-if="item.type === 'text'">
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-text-field
                          :label="menuNamed(item.key)"
                          density="compact"
                          variant="outlined"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          v-model="formData[item.key]"
                          :rules="[requiredRule(item)]"
                        />
                      </div>
                    </div>

                    <!-- Autocomplete field -->
                    <div v-if="item.type === 'autocomplete'">
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-autocomplete
                          v-model="formData[item.key]"
                          :items="item.item"
                          :label="menuNamed(item.key)"
                          item-value="name"
                          item-text="name"
                          variant="outlined"
                          density="compact"
                          :style="{ borderRadius: '8px', maxWidth: `500px` }"
                          :rules="[requiredRule(item)]"
                        />
                      </div>
                    </div>

                    <!-- Boolean (Checkbox) field -->
                    <div v-if="item.type === 'boolean'">
                      <div
                        :style="{
                          display: `flex`,
                          justifyContent: `center`,
                        }"
                      >
                        <v-switch
                          v-model="formData[item.key]"
                          :label="formData[item.key] ? `Yes` : `No`"
                          inset
                          :color="`#5EB491`"
                        />
                      </div>
                    </div>
                    <v-divider
                      class="my-2"
                      v-if="idx < defineChatBotItem.length - 1"
                      :style="{ maxWidth: '500px', margin: 'auto' }"
                    />
                  </div>
                </v-form>
              </div>
            </div>
            <div
              :style="{
                height: `100%`,
                display: selectedSubMode === 2 ? `` : `none`,
              }"
            >
              <div
                :style="{
                  display: `flex`,
                  flexDirection: `column`,
                }"
              >
                <span :style="{ fontWeight: `bold` }"
                  >Define Skills, Tasks 🤖</span
                >
                <span :style="{ color: `grey`, fontSize: `0.7rem` }">
                  "What skills should I have? How can I assist you best?"</span
                >
              </div>
              <div :style="{ height: `100%`, overflowY: `auto` }"></div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
    <v-card-text
      :style="{
        display: `flex`,
        alignItems: `center`,
        justifyContent: `flex-end`,
      }"
    >
      <v-btn
        :style="{ width: `120px` }"
        class="mr-2"
        @click="clickBackToMain()"
        :text="`back`"
      />
      <v-btn
        :disabled="!isFormValid"
        :style="{ width: `120px`, color: `white`, backgroundColor: `#5EB491` }"
        @click="submitForm()"
        :text="`Apply`"
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "digitalTwinConfig",
  props: {
    item: {
      type: Object,
      default: null,
    },
  },
  watch: {
    "item.id": {
      handler(newVal) {
        if (newVal) {
          console.log(newVal, "Load this on API");
          this.botMode = `edit`;
        } else {
          console.log("Setup Components for create");
          this.botMode = `create`;
        }
      },
      immediate: true,
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      botMode: `create`,
      botItem: null,
      selectedSubMode: 1,
      subMode: [
        {
          id: 1,
          name: `Define Chatbot Identity`,
          icon: `👤`,
          disabled: false,
        },
        {
          id: 2,
          name: `Define Skills, Tasks`,
          icon: `🤖`,
          disabled: false,
        },
        {
          id: 3,
          name: `Setup Guard Rails`,
          icon: `🛡️`,
          disabled: true,
        },
      ],
      defineChatBotItem: [
        {
          id: 1,
          key: "bot_name",
          description: "What would you like to name me?",
          type: "text",
        },
        {
          id: 2,
          key: "routing",
          description:
            "How would you like me to respond? (e.g., mastery, friendly, formal)",
          type: "text",
        },
        {
          id: 3,
          key: "prompt",
          description: "What do you want me to say to the user?",
          type: "text",
        },
        {
          id: 4,
          key: "industry",
          description:
            "In which industry do you need me to work? (e.g., Technology, Customer Support)",
          type: "text",
        },
        {
          id: 5,
          key: "retrieve_image",
          description: "Should I be able to retrieve images? (Yes/No)",
          type: "boolean",
        },
        {
          id: 6,
          key: "knowledge_base",
          description: "Where should I pull my information from?",
          type: "autocomplete",
          item: ["Tech Support", "Customer Service", "IT Solutions"],
        },
        {
          id: 7,
          key: "line_integration_uuid",
          description: "Do you want me connected to LINE? (Yes/No)",
          type: "autocomplete",
          item: ["LINE Integration 1", "LINE Integration 2"],
        },
      ],
      formData: {
        bot_name: "",
        routing: "",
        prompt: "",
        industry: "",
        retrieve_image: false,
        knowledge_base: "",
        line_integration_uuid: "",
      },
    };
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
    this.getDefineChatbotItem();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  computed: {
    isFormValid() {
      return this.defineChatBotItem.every((item) => {
        if (item.type === "boolean") return true;
        return this.formData[item.key]?.length > 0;
      });
    },
  },
  methods: {
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    clickBackToMain() {
      this.$emit(`backToMain`);
    },
    getDefineChatbotItem() {
      this.defineChatBotItem[5].item = [`test_1`, `test_2`, `test_3`]; // knowledge_base
      this.defineChatBotItem[6].item = [
        `No`,
        `Test_Line_1`,
        `Test_Line_2`,
        `Test_Line_3`,
      ]; // line_integration_uuid
    },
    requiredRule(item) {
      return item.type !== "boolean"
        ? (v) => !!v || `${item.key} is required.`
        : true;
    },
    submitForm() {
      if (this.isFormValid) {
        if (
          !this.formData.line_integration_uuid ||
          this.formData.line_integration_uuid === `No`
        ) {
          this.formData.line_integration_uuid = null;
        }
        console.log("Form submitted successfully:", this.formData);
        this.clearForm();
      } else {
        console.error("Form is invalid. Please fill all required fields.");
      }
    },
    clearForm() {
      this.formData = {
        bot_name: "",
        routing: "",
        prompt: "",
        industry: "",
        retrieve_image: false,
        knowledge_base: "",
        line_integration_uuid: "",
      };
    },
    menuNamed(string) {
      let name = string.replaceAll(`_`, ` `);
      return name;
    },
  },
};
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
</style>
