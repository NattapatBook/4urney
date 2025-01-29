<template>
  <v-dialog v-model="dialog" width="500">
    <v-card class="rounded-xl">
      <!-- Dialog Title -->
      <v-card-text
        class="mt-2 pb-0"
        :style="{ fontWeight: `bold`, fontSize: `1.2rem` }"
      >
        <span>
          {{
            mode === `process`
              ? `Confirm to process this knowledge?`
              : mode === `edit`
              ? `Edit file description.`
              : mode === `remove`
              ? `Remove this file?`
              : `Untitled`
          }}</span
        >
      </v-card-text>
      <!-- Dialog Content -->
      <v-card-text>
        <div>
          <span>
            {{
              mode === `process`
                ? `Are you sure you want to process this knowledge? This action will proceed with the necessary steps and cannot be undone.`
                : mode === `edit`
                ? `Modify the file description below. Ensure the details are accurate before saving your changes.`
                : mode === `remove`
                ? `Are you sure you want to remove this file? This action is irreversible, and the file will be permanently deleted.`
                : `Untitled`
            }}</span
          >
        </div>
      </v-card-text>
      <!-- Dialog Content : Files -->
      <v-card-text
        class="pt-0"
        :class="mode === `edit` ? `pb-0` : ``"
        :style="{
          display: `flex`,
          justifyContent: `center`,
        }"
      >
        <div>
          <v-icon
            class="mr-2"
            :style="{
              color:
                mode === `process`
                  ? `#5EB491`
                  : mode === `edit`
                  ? `#1867c0`
                  : mode === `remove`
                  ? `#D6584D`
                  : `grey`,
            }"
          >
            {{
              mode === `process`
                ? `mdi-file-check`
                : mode === `edit`
                ? `mdi-file-edit`
                : mode === `remove`
                ? `mdi-file-remove`
                : `Untitled`
            }}
          </v-icon>
          <v-chip>{{ item.file_name }}</v-chip>
        </div>
      </v-card-text>
      <!-- Dialog Content : Edit Text-Field -->
      <v-card-text
        class="mb-3"
        v-if="mode === `edit`"
        :style="{ height: `156px` }"
      >
        <div>
          <v-textarea
            v-model="description"
            rounded
            :label="`File Description`"
            :placeholder="`Enter a new description for this file...`"
            no-resize
            density="compact"
            variant="outlined"
            :style="{ borderRadius: '8px', maxWidth: `500px` }"
          />
        </div>
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
        <v-btn @click="closeDialog" variant="text"> Cancel </v-btn>
        <v-btn
          @click="clickApply"
          class="ml-2"
          text
          :style="{
            width: `110px`,
            color: `white`,
            backgroundColor:
              mode === `process`
                ? `#5EB491`
                : mode === `edit`
                ? `#1867c0`
                : mode === `remove`
                ? `#D6584D`
                : `grey`,
          }"
        >
          {{ mode === `remove` ? `Remove` : `Apply` }}
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "knowledgeBaseActionDialog",
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    mode: {
      type: String,
      default: `untitled`,
    },
    item: {
      type: Object,
      default: () => ({
        id: -1,
        file: "untitled",
        uploaded_at: null,
        collection_name: null,
        embedded_date: null,
        status: null,
        user: "untitled",
        file_url: "untitled",
        file_name: "untitled",
        description: `No Description`,
      }),
    },
  },
  watch: {
    mode: {
      handler(newVal) {
        if (newVal === `edit`) {
          this.description = this.item.description;
        }
      },
      immediate: true,
    },
  },
  data() {
    return {
      description: ``,
    };
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
  methods: {
    closeDialog() {
      this.dialog = false;
    },
    clickApply() {
      this.$emit("callbackAction", {
        mode: this.mode,
        item: this.item,
        description: this.description,
      });
    },
  },
};
</script>

<style scoped></style>
