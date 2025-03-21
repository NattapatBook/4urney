<template>
  <v-dialog v-model="dialog" width="500">
    <v-card class="rounded-xl">
      <!-- Dialog Title -->
      <v-card-text
        class="mt-2 pb-0"
        :style="{ fontWeight: `bold`, fontSize: `1.2rem` }"
      >
        <span>Edit Customer Profile</span>
      </v-card-text>

      <!-- Dialog Content : field -->
      <v-card-text
        class="py-0"
        :style="{
          display: `flex`,
          justifyContent: `center`,
          flexDirection: `column`,
        }"
      >
        <div
          v-for="(key, idx) in keys"
          :key="`editCustomerProfile_${idx}`"
          class="pt-4 px-4"
        >
          <div>
            <div
              :style="{
                display: `flex`,
                justifyContent: `center`,
                flexDirection: `column`,
              }"
            >
              <v-text-field
                v-if="key !== `birthday`"
                :label="formatLabel(key)"
                density="compact"
                variant="outlined"
                :style="{ borderRadius: '8px', maxWidth: `500px` }"
                v-model="userInformationForm[key]"
              />
              <v-menu
                v-else-if="key === `birthday`"
                v-model="menuDate"
                :close-on-content-click="false"
                transition="scale-transition"
                max-width="290"
                offset-y
              >
                <template v-slot:activator="{ props }">
                  <v-text-field
                    v-model="userInformationForm[key]"
                    :label="formatLabel(key)"
                    density="compact"
                    variant="outlined"
                    readonly
                    append-inner-icon="mdi-calendar"
                    v-bind="props"
                  ></v-text-field>
                </template>

                <v-date-picker
                  v-model="date"
                  @update:model-value="updateDate(key, date)"
                ></v-date-picker>
              </v-menu>
            </div>
          </div>
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
            backgroundColor: `#5EB491`,
          }"
        >
          Apply
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "editCustomerProfileDialog",
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    dashboardDataProp: {
      type: Object,
      default: () => ({
        dissatisfaction: 0,
        intentSummary: [],
        priority: "",
        satisfaction: 0,
        totalMessage: 0,
        totalSession: 0,
        urgent: 0,
        id: "-1",
        userInformation: {
          birthday: "",
          citizenId: "",
          email: "",
          gender: "",
          name: "",
          phoneNumber: "",
        },
      }),
    },
  },
  watch: {
    modelValue: {
      handler(newVal) {
        if (newVal === true) {
          this.userInformationForm = JSON.parse(
            JSON.stringify(this.dashboardDataProp.userInformation)
          );
        }
      },
      immediate: true,
    },
  },
  data() {
    return {
      menuDate: false,
      date: null,
      userInformationForm: {
        id: "",
        birthday: "",
        citizenId: "",
        email: "",
        gender: "",
        name: "",
        phoneNumber: "",
      },
      keys: [`name`, `citizenId`, `gender`, `birthday`, `phoneNumber`, `email`],
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
      this.clearField();
      this.dialog = false;
    },
    clearField() {
      this.userInformationForm = {
        id: "",
        birthday: "",
        citizenId: "",
        email: "",
        gender: "",
        name: "",
        phoneNumber: "",
      };
    },
    updateDate(key, date) {
      const day = String(date.getDate()).padStart(2, "0");
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const year = date.getFullYear();

      this.userInformationForm[key] = `${day}/${month}/${year}`;
      this.menuDate = false;
    },
    clickApply() {
      this.userInformationForm.id = this.dashboardDataProp.id;
      this.$emit(
        "callbackConfirmEditCustomerProfileDialog",
        this.userInformationForm
      );
      this.closeDialog();
    },
    formatLabel(str) {
      return str
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
    },
  },
};
</script>

<style scoped></style>
