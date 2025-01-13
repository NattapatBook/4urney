<template>
  <v-dialog v-model="internalModel" width="500">
    <v-card class="rounded-xl">
      <!-- Dialog Title -->
      <v-card-text
        class="mt-2 pb-0"
        :style="{ fontWeight: `bold`, fontSize: `1.2rem` }"
      >
        <slot name="title">
          {{
            mode === `newChat`
              ? `Create a New Chat.`
              : mode === `delete`
              ? `Delete Chat`
              : mode === `rename`
              ? `Rename Chat`
              : `Untitled`
          }}
        </slot>
      </v-card-text>

      <!-- Dialog Content -->
      <v-card-text>
        <span v-if="mode === `newChat`">Enter a name for your chat...</span>
        <span v-else-if="mode === `delete`">
          Are you sure you want to delete "<span
            :style="{ fontWeight: `bold` }"
            >{{ this.item.name }}</span
          >"? This chat will be
          <span :style="{ fontWeight: `bold` }">permanently</span> deleted and
          cannot be restored.
        </span>
        <span v-else-if="mode === `rename`">
          Enter a new name for this chat.
        </span>

        <v-text-field
          v-if="mode === 'rename' || mode === 'newChat'"
          v-model="textField"
          clearable
          multiple
          variant="outlined"
          :density="'comfortable'"
          rounded="lg"
          :rules="getValidationRules"
        >
        </v-text-field>
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
        <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
        <v-btn
          @click="clickApply()"
          :disabled="mode !== `delete` && !isFormValid"
          :style="{
            backgroundColor: mode === `delete` ? `#D6584D` : `#5EB491`,
            color: `white`,
          }"
          class="ml-2"
          text
          >{{ mode === `delete` ? `Delete` : `Apply` }}</v-btn
        >
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "chatSessionDialog",
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    mode: {
      type: String,
      required: `untitled`,
    },
    item: {
      type: Object,
      default: () => {
        return {
          id: `-1`,
          name: `untitled`,
          lastConversationTime: new Date(),
        };
      },
    },
  },
  data() {
    return {
      textField: ``,
    };
  },
  emits: ["update:modelValue"],
  watch: {
    modelValue: {
      handler() {
        if (this.mode === `rename`) {
          this.oldName = this.item.name;
          this.textField = this.item.name;
        } else {
          this.textField = ``;
        }
      },
      deep: true,
    },
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
    getValidationRules() {
      return [
        (value) =>
          value.trim() !== "" || "The name is required and cannot be blank.",
        ...(this.mode === "rename"
          ? [
              (value) =>
                value.trim() !== this.oldName.trim() ||
                "The new name cannot be the same as the old name.",
            ]
          : []),
      ];
    },
    isFormValid() {
      const rules = this.getValidationRules;
      return rules.every((rule) => rule(this.textField) === true);
    },
  },
  methods: {
    closeDialog() {
      this.internalModel = false;
    },
    clickApply() {
      this.$emit("apply", {
        mode: this.mode,
        item: this.item,
        name: this.textField,
      });
      this.internalModel = false;
    },
  },
};
</script>
